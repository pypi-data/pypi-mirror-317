import csv
import re
from concurrent.futures import ProcessPoolExecutor
from datetime import date
from io import StringIO
from pathlib import Path
from typing import Dict

from dateutil.relativedelta import relativedelta

from hlpj.base.webdav import WebDav

from ..base import helpers
from ..base.config import JournalConfig, JournalPaths


def get_report_commands(data_base: date, journal: str) -> Dict[str, str]:
    inicio_str = (data_base - relativedelta(months=2)).strftime("%Y-%m-%d")
    final_str = (data_base + relativedelta(months=1)).strftime("%Y-%m-%d")

    base_report_command = [
        "--monthly",
        "--tree",
        "--no-elide",
        "--begin",
        inicio_str,
        "--end",
        final_str,
        "not:desc:#closing#",
    ]

    lucro_report = [
        "--auto",
        "--unmarked",
        "is",
        "--forecast=from 2021-01-01",
        *base_report_command,
    ]

    var_bp_report = ["bs", "--change", "--unmarked", *base_report_command]

    reserva_report = [
        "bse",
        "^Ativo:Disponibilidade:|^Passivo:Passivo Circulante:|^Patrimonio Liquido:Dividendos",
        "--historical",
        "--auto",
        "--unmarked",
        "--forecast=from 2021-01-01",
        *base_report_command,
    ]
    locatarios_pago_report = [
        "--real",
        "--unmarked",
        "bal",
        "^Receita:",
        "--pivot",
        "payee",
        *base_report_command,
    ]
    locatarios_atrasado_report = [
        "--real",
        "--pending",
        "bal",
        "^Receita",
        "--pivot",
        "payee",
        "--historical",
        *base_report_command,
    ]

    reports_cmd = {
        "Locatarios - Pagos": locatarios_pago_report,
        "Locatarios - Atrasado": locatarios_atrasado_report,
        "Lucro Operacional": lucro_report,
        "Variacao do Balanco Patrimonial": var_bp_report,
        "Reservas de Capital": reserva_report,
    }

    with ProcessPoolExecutor() as p:
        reports_fut = {
            nome: p.submit(helpers.hledger_stdin, journal, report_cmd)
            for nome, report_cmd in reports_cmd.items()
        }
        reports = {
            nome: report_fut.result() for nome, report_fut in reports_fut.items()
        }

    return reports


def fix_valor(valor_str: str):
    valor_fixed_str = re.sub(r"\$|,", "", valor_str)
    valor = abs(float(valor_fixed_str))
    return valor


def get_imp_txn(receita_mes: Dict[str, str]):
    rec_locacao = fix_valor(receita_mes.get("Receita:Locacao", "0"))
    rec_financeira = fix_valor(receita_mes.get("Receita:Financeira", "0"))
    rec_venda = fix_valor(receita_mes.get("Receita:Venda de Imovel", "0"))
    base_rec = (rec_locacao * 0.32) + rec_financeira + (rec_venda * 0.08)
    base_adic = max(base_rec - 20000, 0)

    imp = [
        rec_locacao * 0.1133,
        rec_financeira * 0.2153,
        rec_venda * 0.0773,
        base_adic * 0.1,
    ]
    imp_total = round(sum(imp), 2)

    txn = f"""
{receita_mes['account']}-15 Impostos presumidos mensais
    Despesa:Imposto:Competencia                  {imp_total}
    Passivo:Passivo Circulante:Imposto a Pagar    {-imp_total}
"""
    return txn


def get_imp_txns(journal_all: str):
    flags = [
        "bal",
        "^Receita:",
        "not:desc:#closing#",
        "--unmarked",
        "--month",
        "--transpose",
        "--no-total",
        "--output-format=csv",
    ]
    txns_str = helpers.hledger_stdin(journal_all, flags)

    txns_csv = csv.DictReader(StringIO(txns_str))
    txns = "\n"
    for rec_mes in txns_csv:
        txns += get_imp_txn(rec_mes)

    return txns


def get_report_str(reports: Dict[str, str], data_base: date):
    date_str = data_base.strftime("%Y-%m")
    result = f"Data-base: {date_str}\n\n"
    for name, report in reports.items():
        result += helpers.underline(name) + "\n"
        result += report + "\n\n"
    return result


def get_controle(journal_paths: JournalPaths, config: JournalConfig):
    # Get info
    data_base = helpers.get_date()
    journal = Path(journal_paths.journal_all).read_text()
    controle = Path(journal_paths.controle_file).read_text()

    dav = WebDav(config.dav_options)

    # Get journal
    txns_imp = get_imp_txns(journal)
    journal_joined = journal + controle + txns_imp
    controle_file = Path(config.relatorios_dir).joinpath(
        f"controle-{data_base.year}-{data_base.month}.journal"
    )
    dav.upload_txt(journal_joined, str(controle_file))

    # Generate reports
    reports = get_report_commands(data_base, journal_joined)
    reports_str = get_report_str(reports, data_base)
    print(reports_str)
    reports_filename = (
        f"controle-{config.apelido}-{data_base.year}-{data_base.month}.pdf"
    )
    output_path = Path(config.relatorios_dir).joinpath(reports_filename)
    helpers.print_pdf(reports_str, dav, str(output_path))
    print("Salvo arquivo " + str(output_path))
