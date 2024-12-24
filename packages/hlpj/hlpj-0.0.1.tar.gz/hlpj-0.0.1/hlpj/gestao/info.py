import configparser
from datetime import datetime
from pathlib import Path
from time import time
from typing import NamedTuple

from dateutil.relativedelta import relativedelta
from tabulate import tabulate

from hlpj.base.webdav import WebDav

from ..base import helpers
from ..base.config import JournalConfig, JournalPaths
from ..financeiro.conciliacao import conferencias


class Saldos(NamedTuple):
    conta: str
    data: str
    valor: float


def get_atrasados(txns_dir: str, year: str):
    today = datetime.today()
    last_date = (
        today - relativedelta(days=3)
        if today.weekday() <= 1
        else today - relativedelta(days=1)
    )
    last_date_str = last_date.strftime("%Y-%m-%d")
    journal_str = helpers.join_journal_last(txns_dir, int(year))
    command = [
        "balance",
        "^Ativo|^Passivo",
        "tag:tipo=locacao",
        "-e",
        last_date_str,
        "--pending",
        "--pivot=payee",
        "historical",
    ]
    result = helpers.hledger_stdin(journal_str, command)
    return result


def get_last_saldo(saldos: configparser.SectionProxy, conta: str):
    last_date = max(saldos)
    last_saldo = Saldos(conta, last_date, float(saldos[last_date]))
    return last_saldo


def get_info(journal_paths: JournalPaths, journal_config: JournalConfig):
    start = time()
    result = helpers.intro(journal_config.locador) + "\n"

    stats = helpers.hledger_file(journal_paths.journal_all, ["stats"])
    result += stats + "\n\n"

    info = Path(journal_paths.info_file).read_text()
    result += helpers.underline("Informacoes gerais") + "\n"
    result += info + "\n\n\n"

    result += helpers.underline("Atrasados") + "\n"
    result += get_atrasados(journal_paths.txns_dir, journal_config.ano)

    result += (
        str(
            conferencias(
                journal_paths.journal_all,
                journal_paths.conciliacao_file,
                journal_config.nome_imoveis_file,
            )
        )
        + "\n\n"
    )

    saldos = configparser.ConfigParser(delimiters=["="])
    saldos.read(journal_paths.conciliacao_file)
    last_saldos = [
        get_last_saldo(saldo, conta)
        for conta, saldo in saldos.items()
        if conta != "DEFAULT"
    ]
    last_saldos_table = tabulate(
        last_saldos,
        headers=["Conta", "Data", "Saldo"],
        numalign="right",
        floatfmt=",.2f",
        tablefmt="simple",
    )
    result += helpers.underline("Saldos") + "\n"
    result += last_saldos_table + "\n\n\n"

    total = sum([last_saldo.valor for last_saldo in last_saldos])

    result += f"Total: {total:,.2f}" + "\n\n"

    info_path = Path(journal_config.relatorios_dir).joinpath("hlpj_info.pdf")
    dav = WebDav(journal_config.dav_options)
    helpers.print_pdf(result, dav, str(info_path))
    print("Arquivo salvo")
    print(result)
    print(f"\n Resultado em {time() - start}")
