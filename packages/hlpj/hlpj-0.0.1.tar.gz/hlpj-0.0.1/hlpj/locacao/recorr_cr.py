import re
from calendar import monthrange
from configparser import SectionProxy
from datetime import date
from pathlib import Path
from typing import Dict, List

import questionary
from dateutil.relativedelta import relativedelta

from hlpj.base.webdav import WebDav

from ..base import helpers, recorr
from ..base.config import JournalConfig, JournalPaths
from .val_locacoes import val_locacoes

TIPO = "locacao"


def get_groups_locacao(locacao_file: str) -> List[str]:
    locacao = helpers.ini_parser()
    locacao.read(locacao_file)

    groups = sorted(
        set(
            [
                locacao[contrato].get("grupo", "0")
                for contrato in locacao
                if contrato != "DEFAULT"
            ]
        ),
        key=lambda group: int(group),
    )
    return groups


def get_real_key(key: str, contrato: Dict[str, str]) -> str:
    result = next(
        (
            key_with_uuid
            for key_with_uuid in contrato.keys()
            if re.search(f"^\\d+{key}$", key_with_uuid)
        ),
        None,
    )

    if result is None:
        raise ValueError(f"Erro no item: key")
    return result


def get_date(year: int, month: int, day: int):
    month_tup = monthrange(year, month)
    real_day = day if day < month_tup[1] else month_tup[1]
    result = date(year, month, real_day)
    return result


def get_locacao(contrato_section: SectionProxy, base_date: date, tipo: str):
    contrato = dict(contrato_section)
    payee = contrato.pop(get_real_key("locatario", contrato))
    conta_banco = contrato.pop(get_real_key("conta_banco", contrato))
    contrato.pop(get_real_key("status", contrato))
    dia_vencimento_key = get_real_key("dia_vencimento", contrato)
    due = get_date(base_date.year, base_date.month, int(contrato[dia_vencimento_key]))
    postings = []

    for key, value in contrato.copy().items():
        key_stripped = re.sub("^\\d+", "", key)
        if key_stripped.startswith("Receita:") or key_stripped.startswith("Despesa:"):
            values_str = contrato.pop(key)
            values = values_str.split(",")
            values = [value.strip() for value in values]
            competencia = due + relativedelta(months=int(values[2]))
            competencia_str = competencia.strftime("%Y-%m")
            posting = {
                "acct": key_stripped,
                "amt": values[0],
                "categoria": values[1],
                "competencia": competencia_str,
            }
            postings.append(posting)

    due_str = due.strftime("%Y/%m/%d")
    inicio_contrato_key = get_real_key("inicio_contrato", contrato)
    txn = f"{due_str} ! {payee} | Contrato de locacao de {contrato[inicio_contrato_key]}\n"
    txn += f"    ; tipo:{tipo}\n"
    for key, value in contrato.items():
        key_stripped = re.sub("^\\d+", "", key)
        txn += f"    ; {key_stripped}:{value}\n"

    receita_posting = next(
        (posting for posting in postings if posting["acct"] == "Receita:Locacao"), None
    )
    txn += f"    ; vencimento_original: {due}\n"
    if receita_posting:
        txn += f"    ; aluguel_original: {receita_posting['amt']}\n"

    for posting in postings:
        amt = round(float(posting["amt"]) * -1, 2)
        txn += f"    {posting['acct']}    {amt}  ; "
        txn += (
            f"categoria:{posting['categoria']}, competencia:{posting['competencia']}\n"
        )

    txn += f"    {conta_banco}"
    return txn


def is_valid_locacao(contrato_section: SectionProxy, grupo: str) -> bool:
    contrato = dict(contrato_section)
    status_key = get_real_key("status", contrato)

    if contrato[status_key] != "ativo":
        return False

    try:
        grupo_key = get_real_key("grupo", contrato)
        return contrato[grupo_key] == grupo
    except ValueError:
        return grupo == "0"


def get_locacoes(journal_path: str, base_date: date, tipo: str, grupo: str = "0"):
    # Add UID in key
    locacao_str = ""
    uid = 0
    with open(journal_path, "r") as locacao_file:
        for row in locacao_file:
            if re.match("^\\w", row):
                locacao_str += str(uid) + row
            else:
                locacao_str += row
            uid += 1

    recorrentes = helpers.ini_parser()
    recorrentes.read_string(locacao_str)

    txns_list = [
        get_locacao(recorrentes[locatario], base_date, tipo)
        for locatario in recorrentes.sections()
        if is_valid_locacao(recorrentes[locatario], grupo)
    ]
    txns_str = "\n\n".join(txns_list)
    journal_result = "D $1,000.00\n\n"
    journal_result += helpers.hledger_stdin(txns_str, ["print"])
    return journal_result


def get_alertas(txns: str, data_base: date) -> str:
    month = data_base.strftime("%Y-%m")
    txns_command = ["print", "not:tag:alerta=^$", f"--forecast={month}"]
    txns_alerta = helpers.hledger_stdin(txns, txns_command)
    return txns_alerta


def get_resumo(journal_combined: str, journal_generated: str, data_base: date):
    journal = journal_combined + "\n\n\n" + journal_generated

    payees_list = (
        helpers.hledger_stdin(journal_generated, ["payee"]).rstrip("\n").split("\n")
    )
    payees_re = "|".join(payees_list)

    inicio = data_base - relativedelta(months=2)
    final = data_base + relativedelta(months=1)
    period = f"from {inicio.strftime('%Y-%m-%d')} to {final.strftime('%Y-%m-%d')}"
    resumo_command = [
        "balance",
        "^Receita:|^Despesa:",
        f"payee:{payees_re}",
        "--invert",
        "--monthly",
        "--tree",
        "--no-elide",
        "-p",
        period,
        "--pivot",
        "payee",
    ]

    resumo = helpers.hledger_stdin(journal, resumo_command)
    return resumo


def salva_recorrentes_receber(
    journal_paths: JournalPaths, journal_config: JournalConfig
) -> None:
    try:
        val_locacoes(journal_paths, journal_config)
    except ValueError as e:
        print(e.args[0])
        input("Aperte enter para continuar")
        return

    default_date = date.today() + relativedelta(months=1)
    data_base = helpers.get_date(
        default_year=default_date.year, default_month=default_date.month
    )

    dav = WebDav(journal_config.dav_options)

    # Get txns
    grupos = get_groups_locacao(journal_paths.locacoes_file)
    grupo: str = questionary.select("Escolha o grupo", grupos, use_shortcuts=True).ask()
    txns = get_locacoes(journal_paths.locacoes_file, data_base, "locacao", grupo)
    report = recorr.get_print_report("Transacoes geradas", txns)
    alertas = get_alertas(txns, data_base)
    report += recorr.get_print_report("Transacoes com alerta", alertas)

    # Resumo
    journal_combined = helpers.join_journal_last(
        journal_paths.txns_dir, int(journal_config.ano)
    )
    resumo = get_resumo(journal_combined, txns, data_base)
    report += recorr.get_print_report("Resumo", resumo)
    # Adiciona
    confirma = questionary.confirm("Confirma as transacoes", default=False).ask()

    if confirma is True:
        mes = data_base.strftime("%Y-%m")
        relatorio_file_name = f"{TIPO}_grupo {grupo}_{mes}.txt"
        relatorio_path = Path(journal_config.relatorios_dir).joinpath(
            relatorio_file_name
        )
        dav.upload_txt(report, str(relatorio_path))

        journal_path = Path(journal_paths.txns_dir).joinpath(
            f"{journal_config.ano}.journal"
        )
        desc_txns = f"{TIPO} de {mes} grupo {grupo}"
        recorr.save_txns(str(journal_path), txns, desc_txns)
    else:
        input("Cancelado... Enter para continuar")


def get_imovel_grupo(journal_paths: JournalPaths, journal_config: JournalConfig):
    grupos = sorted(get_groups_locacao(journal_paths.locacoes_file))
    recorrentes = helpers.ini_parser()
    recorrentes.read(journal_paths.locacoes_file)

    relatorio = ""
    for grupo in grupos:
        relatorio += helpers.underline("Grupo: " + grupo) + "\n"
        contratos = [
            nome
            for nome, items in recorrentes.items()
            if items.get("grupo", "0") == grupo and nome != "DEFAULT"
        ]
        relatorio += "\n".join(contratos) + "\n\n"

    print(relatorio)
    relatorio_path = Path(journal_config.relatorios_dir).joinpath(
        "imovel por grupo.pdf"
    )
    dav = WebDav(journal_config.dav_options)
    helpers.print_pdf(relatorio, dav, str(relatorio_path))
    print("Relatorio Salvo com sucesso")
