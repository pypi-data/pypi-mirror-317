import re
import shlex
from datetime import datetime
from pathlib import Path

import questionary
from dateutil.relativedelta import relativedelta

from hlpj.base.webdav import WebDav

from ..base import helpers
from ..base.config import JournalConfig, JournalPaths


def get_report(
    journal_paths: JournalPaths, args: str, data_inicial: str, data_final: str
) -> str:
    year_inicial = datetime.strptime(data_inicial, "%Y-%m").year
    year_final = datetime.strptime(data_final, "%Y-%m").year
    if year_final - year_inicial == 0:
        file_str = str(Path(journal_paths.txns_dir).joinpath(f"{year_inicial}.journal"))
    else:
        file_str = str(Path(journal_paths.journal_all))

    args_command = shlex.split(args)
    args_command.extend(["-b", data_inicial, "-e", data_final])

    report = helpers.hledger_file(file_str, args_command)
    return report


def val_date(data_str: str) -> bool:
    reg = re.search("(\\d{4})-(\\d{2})", data_str)
    if reg is None or len(reg.groups()) != 2:
        return False

    try:
        datetime(year=int(reg.groups()[0]), month=int(reg.groups()[1]), day=1)
    except ValueError or TypeError:
        return False

    return True


def choose_relatorio(journal_paths: JournalPaths, journal_config: JournalConfig):
    default_inicio = datetime.today() - relativedelta(months=1)
    data_inicial: str = questionary.text(
        "Data inicial (YYYY-MM)            ",
        default=default_inicio.strftime("%Y-%m"),
        validate=val_date,
    ).ask()

    default_final = datetime.strptime(data_inicial, "%Y-%m") + relativedelta(months=1)
    data_final: str = questionary.text(
        "Data final (YYYY-MM) - Não inclusa",
        default=default_final.strftime("%Y-%m"),
        validate=val_date,
    ).ask()

    relatorios = helpers.ini_parser()
    relatorios.read(journal_paths.relatorios_file)

    options = list(relatorios["relatorios"].keys())
    option = questionary.select(
        "Escolha o relatorio",
        choices=options,
        use_shortcuts=True,
    ).ask()
    args = relatorios["relatorios"][option]
    report = get_report(journal_paths, args, data_inicial, data_final)
    if len(report) == 0:
        input("Relatorio vazio ")
        return

    report_file = str(
        Path(journal_config.relatorios_dir).joinpath(f"{option}_{data_inicial}.pdf")
    )

    titulo = f"{option} -> Periodo: {data_inicial} a {data_final} (Não Incluso)"
    result = helpers.underline(titulo) + "\n\n"
    result += report
    print(result)
    dav = WebDav(journal_config.dav_options)
    helpers.print_pdf(result, dav, report_file)
    input("Relatorio salvo ")
