import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from dateutil.relativedelta import relativedelta
from tabulate import tabulate

from ..base import helpers
from ..base.config import JournalConfig, JournalPaths, get_config, get_journal_paths
from ..base.webdav import WebDav


def get_events(locacoes_path: str):
    recorrentes = helpers.ini_parser()
    recorrentes.read(locacoes_path)

    final_contratos = [
        (recorrentes[contrato].get("final_contrato", ""), contrato, "Final do Contrato")
        for contrato in recorrentes
        if recorrentes[contrato].get("final_contrato", "") != ""
    ]
    reajustes = [
        (recorrentes[contrato].get("reajuste", ""), contrato, "Reajuste")
        for contrato in recorrentes
        if recorrentes[contrato].get("reajuste", "") != ""
    ]
    hoje_rows = (datetime.today().strftime("%Y-%m-%d"), "----------", "HOJE")
    eventos: List[Tuple[str, str, str]] = [*final_contratos, *reajustes, hoje_rows]
    eventos_sorted = sorted(eventos, key=lambda item: item[0])
    return eventos_sorted


def show_events(journal_paths: JournalPaths, journal_config: JournalConfig):
    events_table = get_events(journal_paths.locacoes_file)
    table_result = tabulate(
        events_table, headers=["Data", "Contrato", "Evento"], tablefmt="simple"
    )

    result = helpers.underline("Eventos") + "\n" + table_result
    print(result)
    events_path = Path(journal_config.relatorios_dir).joinpath("eventos_locacao.pdf")
    dav = WebDav(journal_config.dav_options)
    helpers.print_pdf(result, dav, str(events_path))
    input("Salvo relatorio. Pressione enter para continuar. ")


if __name__ == "__main__":
    base_dir = sys.argv[1]
    nome = Path(base_dir).name
    journal_paths = get_journal_paths(base_dir)
    config_paths = get_config(base_dir)

    events = get_events(journal_paths.locacoes_file)
    last_date = datetime.today() + relativedelta(months=4)
    events_close = [
        event
        for event in events
        if datetime.strptime(event[0], "%Y-%m-%d") <= last_date
    ]

    print(f"Eventos da empresa {nome}\n")
    for event in events_close:
        print("-" * 10)
        print(f"- Data: {event[0]}")
        print(f"- Contrato: {event[1]}")
        print(f"- Evento: {event[2]}")
