from datetime import date
from pathlib import Path

import questionary
from dateutil.relativedelta import relativedelta

from hlpj.base.webdav import WebDav

from ..base import helpers, recorr
from ..base.config import JournalConfig, JournalPaths

TIPO = "despesa_recorrente"


def get_resumo(journal_combined: str, journal_generated: str, data_base: date):
    journal = journal_combined + "\n\n\n" + journal_generated
    inicio = data_base - relativedelta(months=2)
    final = data_base + relativedelta(months=1)
    period = f"from {inicio.strftime('%Y-%m-%d')} to {final.strftime('%Y-%m-%d')}"
    resumo_command = [
        "balance",
        "^Receita:|^Despesa:",
        f"tag:tipo={TIPO}",
        "--invert",
        "--monthly",
        "--tree",
        "--no-elide",
        "--empty",
        "-p",
        period,
    ]

    resumo = helpers.hledger_stdin(journal, resumo_command)
    return resumo


def gera_txns(recorr_path: str, data_base: date):
    month = data_base.strftime("%Y-%m")
    txns_command = ["print", f"tag:tipo={TIPO}", f"--forecast={month}"]
    txns = helpers.hledger_file(recorr_path, txns_command)
    return txns


def salva_recorrentes_pagar(
    journal_paths: JournalPaths, config_paths: JournalConfig
) -> None:
    default_date = date.today() + relativedelta(months=1)
    data_base = helpers.get_date(
        default_year=default_date.year, default_month=default_date.month
    )

    # Gera txns
    txns = gera_txns(journal_paths.recorr_pgmto_file, data_base)
    report = recorr.get_print_report("Transacoes geradas", txns)

    # Resumo
    journal_combined = helpers.join_journal_last(
        journal_paths.txns_dir, int(config_paths.ano)
    )
    resumo = get_resumo(journal_combined, txns, data_base)
    report += recorr.get_print_report("Resumo", resumo)

    # Adiciona
    confirma = questionary.confirm("Confirma as transacoes", default=False).ask()

    if confirma is True:
        mes = data_base.today().strftime("%Y-%m")
        relatorio_file_name = f"recorrentes_{TIPO}_{mes}.txt"
        relatorio_path = Path(config_paths.relatorios_dir).joinpath(relatorio_file_name)
        dav = WebDav(config_paths.dav_options)
        dav.upload_txt(report, str(relatorio_path))
        journal_path = helpers.get_txns_curr(journal_paths.txns_dir, config_paths.ano)
        desc_txns = f"{TIPO} de {data_base}"
        recorr.save_txns(str(journal_path), txns, desc_txns)
    else:
        input("Cancelado... Enter para continuar")
