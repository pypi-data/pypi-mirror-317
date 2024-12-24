import csv
import os
from io import StringIO
from pathlib import Path
from typing import List, cast

import pandas as pd
import questionary
from pandas.core.frame import DataFrame
from prompt_toolkit.shortcuts import CompleteStyle

from ..base import helpers
from ..base.config import JournalConfig, JournalPaths
from ..financeiro.transacoes import load_hledger_ui

DESPESAS_COMPENSAR = r"Despesa:Imovel:(Condominio|IPTU|Concessionaria)"


def get_desp_add(journal_path: str, apto: str, month: str):
    desp_command = [
        "bal",
        DESPESAS_COMPENSAR,
        f"tag:imovel={apto}",
        "-p",
        month,
        "--change",
        "--unmarked",
        "--invert",
        "--no-total",
        "--output-format=csv",
    ]
    desp_str = helpers.hledger_file(journal_path, desp_command)
    desp_dict_list = csv.DictReader(StringIO(desp_str))

    desp_titulo = f"Apto: {apto}. Copie despesas a compensar abaixo:"
    desp_copy = helpers.underline(desp_titulo) + "\n"
    for desp_dict in desp_dict_list:
        acct = desp_dict["account"]
        valor = desp_dict["balance"].replace(",", "")
        desp_row = f"{acct:<35}{valor}"
        desp_copy += desp_row + "\n"

    return desp_copy


def edit_apto(journal_path: str, apto: str, month: str):
    ui_command = [
        f"tag:imovel={apto}",
        "--tree",
        "--forecast",
        "--unmarked",
        "--register",
        "Receita",
        "-p",
        month,
        "Receita",
    ]
    load_hledger_ui(journal_path, ui_command)


def get_lucro_desp(journal_path: str, month_year: str):
    lucro_command = [
        "bal",
        "^Receita:",
        "tag:imovel=apto",
        "tag:tipo=airbnb",
        "-p",
        month_year,
        "--change",
        "--unmarked",
        "--empty",
        "--pivot",
        "imovel",
        "--invert",
        "--no-total",
        "--output-format=csv",
    ]
    desp_command = [
        "bal",
        DESPESAS_COMPENSAR,
        "tag:imovel=apto",
        "-p",
        month_year,
        "--change",
        "--unmarked",
        "--pivot",
        "imovel",
        "--invert",
        "--no-total",
        "--output-format=csv",
    ]

    lucro_csv = helpers.hledger_file(journal_path, lucro_command)
    desp_csv = helpers.hledger_file(journal_path, desp_command)
    lucro_pd = cast(pd.DataFrame, pd.read_csv(StringIO(lucro_csv), index_col="account"))

    desp_pd = cast(pd.DataFrame, pd.read_csv(StringIO(desp_csv), index_col="account"))
    result = lucro_pd.join(desp_pd, how="left", lsuffix="_lucro", rsuffix="_despesa")
    result.index.name = "Apartamento"
    result = result.rename(
        columns={"balance_lucro": "Lucro", "balance_despesa": "Despesa"}
    )
    result["Despesa"] = result["Despesa"].fillna(0)
    return result


def ask_apto(aptos_balance: DataFrame):
    aptos: List[str] = [apto[0] for apto in aptos_balance.reset_index().values]
    apto: str = questionary.autocomplete(
        'Digite apto ou "q" para sair',
        aptos,
        ignore_case=True,
        match_middle=True,
        style=questionary.Style([("answer", "fg:#f71b07")]),
        complete_style=CompleteStyle.MULTI_COLUMN,
        validate=lambda answer: answer in [*aptos, "q"],
    ).ask()
    return apto


def desp_apto(journal_paths: JournalPaths, journal_config: JournalConfig):
    journal_config
    txns_dir = journal_paths.txns_dir
    data_base = helpers.get_date()
    month_year = f"{data_base.year}-{data_base.month}"

    journal = str(Path(txns_dir).joinpath(f"{journal_config.ano}.journal"))

    apto = "inicio"
    while True:
        os.system("clear")

        print(helpers.underline("Resumo"))
        df_lucro_desp: pd.DataFrame = get_lucro_desp(journal, month_year)  # type: ignore
        print(df_lucro_desp)

        apto = ask_apto(df_lucro_desp)
        if apto == "q":
            return
        print(get_desp_add(journal, apto, month_year))

        input("\nEnter para editar. ")
        edit_apto(journal, apto, month_year)
