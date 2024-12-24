import re
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Dict, cast

import pandas as pd
from dateutil.relativedelta import relativedelta

from ..base import helpers


def get_df_balances(journal_str: str, conta: str, begin: str, end: str):
    balance_command = [
        "balance",
        conta,
        "-b",
        begin,
        "-e",
        end,
        "--unmarked",
        "--historical",
        "--daily",
        "--transpose",
        "--output-format=csv",
    ]

    balance = helpers.hledger_file(journal_str, balance_command)
    df_balance = cast(
        pd.DataFrame,
        pd.read_csv(StringIO(balance), header=None, skiprows=1),
    )

    if df_balance.shape[1] != 3:
        return

    df_balance = cast(
        pd.DataFrame,
        df_balance.set_axis(["data", "valor", "total"], axis=1).drop("total", axis=1),
    )

    df_balance["valor"] = (
        df_balance["valor"].str.replace("\\$|,", "", regex=True).astype(float)
    )
    df_balance = cast(pd.DataFrame, df_balance.set_index("data"))
    df_balance = df_balance[df_balance["valor"] != 0]
    return df_balance


def get_df_saldos(saldos: Dict[str, str]):
    df_saldos = pd.DataFrame(
        saldos.values(),
        index=list(saldos.keys()),
        columns=["valor"],
    )
    df_saldos.index.name = "data"
    df_saldos["valor"] = pd.to_numeric(df_saldos["valor"], errors="coerce")
    df_saldos = df_saldos.dropna(subset=["valor"])

    return df_saldos


def get_df_erro(df_saldos: pd.DataFrame, df_balance: pd.DataFrame):
    df_conciliacao = df_balance.join(
        df_saldos,
        how="inner",
        lsuffix="_calculado",
        rsuffix="_informado",
    )
    df_conciliacao.index.name = "data"
    df_conciliacao["diferenca"] = (
        df_conciliacao["valor_calculado"] - df_conciliacao["valor_informado"]
    )
    df_conciliacao["saldo_anterior"] = df_conciliacao["valor_informado"].shift(1)

    df_erro: pd.DataFrame = df_conciliacao[df_conciliacao["diferenca"] != 0]
    return df_erro


def get_error_msg(conta: str, journal_str: str, df_erro: pd.DataFrame):
    if df_erro.empty:
        print("Verificada conta " + conta)
    else:
        serie_erro: pd.Series = df_erro.reset_index().iloc[0]

        data_erro: str = serie_erro["data"]
        saldo_anterior = serie_erro["saldo_anterior"]
        command = [
            "register",
            conta,
            "--unmarked",
            "--historical",
            "--period",
            data_erro,
        ]
        txns_erro = helpers.hledger_file(journal_str, command)
        erro = f"""
Erro na conta {conta}
------------------------------------
{serie_erro.to_string()}

Saldo Anterior: {saldo_anterior}
{txns_erro}
"""
        return erro


def concilia_conta(conta: str, saldos: Dict[str, str], journal_str: str):
    if len(saldos) == 0:
        return

    df_saldos = get_df_saldos(saldos)

    last_saldo: str = df_saldos.iloc[-1].name  # pyright: ignore
    end_date = datetime.strptime(last_saldo, "%Y-%m-%d") + relativedelta(days=1)
    end = end_date.strftime("%Y-%m-%d")
    begin: str = df_saldos.iloc[0].name  # pyright: ignore
    df_balances = get_df_balances(journal_str, conta, begin, end)
    if df_balances is None:
        return

    df_erro = get_df_erro(df_saldos, df_balances)
    erro_msg = get_error_msg(conta, journal_str, df_erro)
    return erro_msg


def get_imovel_principal(imovel: str):
    regex = re.search(".*:\\w*", imovel)
    if not regex:
        return imovel
    return regex[0]


def get_erros_imoveis(journal_file: str, imoveis_file: str):
    imoveis_txns = helpers.hledger_file(
        journal_file, ["tags", "imovel", "--values"]
    ).split("\n")
    imoveis_txns_principal = [get_imovel_principal(imovel) for imovel in imoveis_txns]

    imoveis_cadastrados = Path(imoveis_file).read_text().split("\n")

    imoveis_errados = set(imoveis_txns_principal).difference(imoveis_cadastrados)
    imoveis_errados.discard("")

    msg = ""
    if len(imoveis_errados) > 0:
        msg = helpers.underline("Imoveis não cadastrados presentes em transacoes")
        msg += "\n" + "\n".join(imoveis_errados)

    return msg


def get_erros_contas(journal_file: str):
    accts_txns = helpers.hledger_file(journal_file, ["accounts", "--used"]).split("\n")
    accts_declared = helpers.hledger_file(
        journal_file, ["accounts", "--declared"]
    ).split("\n")
    accts_no_root = [acct for acct in accts_declared if re.match(".*:.*", acct)]
    accts_errados = set(accts_txns).difference(accts_no_root)
    accts_errados.discard("")

    msg = ""
    if len(accts_errados) > 0:
        msg = helpers.underline("Contas nao cadastradas") + "\n"
        msg += "\n".join(accts_errados)

    return msg


def conferencias(journal_file: str, conciliacao_file: str, nome_imoveis_file: str):
    saldos_all = helpers.ini_parser()
    saldos_all.read(conciliacao_file)
    args = [(conta, dict(saldos), journal_file) for conta, saldos in saldos_all.items()]
    with ProcessPoolExecutor() as p:
        erros_conciliacao = p.map(concilia_conta, *zip(*args))
        for erro in erros_conciliacao:
            print(erro or "")
        print("Verificado conciliacao\n")

        erros_imoveis_fut = p.submit(get_erros_imoveis, journal_file, nome_imoveis_file)
        erros_contas_fut = p.submit(get_erros_contas, journal_file)

        erros_imoveis = erros_imoveis_fut.result()
        if erros_imoveis == "":
            print("Verificado nome dos imoveis\n")
        else:
            print(erros_imoveis + "\n")

    erros_contas = erros_contas_fut.result()
    if erros_contas == "":
        print("Verificado nome das contas\n")
    else:
        print(erros_contas + "\n")
