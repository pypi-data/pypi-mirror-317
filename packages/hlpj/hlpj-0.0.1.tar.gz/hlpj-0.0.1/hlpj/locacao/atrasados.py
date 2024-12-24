import csv
import sys
from collections import deque
from datetime import date
from io import StringIO
from pathlib import Path
from typing import Dict, cast

import holidays
import numpy as np
import pandas as pd

from ..base import config, helpers
from ..base.config import JournalConfig, JournalPaths
from ..base.email_send import Email
from ..base.webdav import WebDav


def filter_agenda(origem: str, agenda_df: pd.DataFrame) -> pd.DataFrame:
    pendente_df = agenda_df[agenda_df.Concluido != "x"]
    pendente_df = pendente_df[pendente_df.Data < np.datetime64(date.today())]
    pendente_df = pendente_df.drop("Concluido", axis=1).fillna("")
    pendente_df["Obs"] = pendente_df.Obs.str.slice(0, 20)
    pendente_df.insert(0, "Origem", origem)
    return pendente_df


def get_pendente(agenda_file: str):
    if not agenda_file or agenda_file == "":
        result = dict(status="", body="")
        return result
    try:
        dtype = {
            "Data": np.datetime64,
            "Parcela": str,
            "Tipo": str,
            "Concluido": str,
            "Obs": str,
        }
        agendas_df: Dict[str, pd.DataFrame] = pd.read_excel(
            agenda_file, sheet_name=None, header=0, dtype=dtype
        )

        pendentes = [
            filter_agenda(origem, agenda_df) for origem, agenda_df in agendas_df.items()
        ]
        pendentes_df = cast(pd.DataFrame, pd.concat(pendentes).sort_values(by="Data"))
        pendentes_df["Data"] = pendentes_df.Data.dt.strftime("%Y-%m-%d")

        pendentes_str = ""
        for item in pendentes_df.iterrows():
            new_item = item[1].to_string() or ""
            pendentes_str += new_item + "\n\n"

        status = "ALERTA DE PENDENCIAS" if not pendentes_df.empty else "SEM PENDENCIAS"
        result = dict(status=status, body=pendentes_str)
        return result
    except BaseException as e:
        status = "ERRO AO GERAR PENDENCIA"
        body = "Erro para gerar pendencias da agenda\n" + "\n".join(e.args)
        return dict(status=status, body=body)


def get_last_date(journal_file: str):
    unmarked_cmd = ["reg", "--unmarked", "--output-format=csv"]
    unmarked_str = helpers.hledger_file(journal_file, unmarked_cmd)
    unmarked_csv = csv.reader(StringIO(unmarked_str))
    dd = deque(unmarked_csv, 1)
    last_unmarked_date = dd.pop()[1]

    today = date.today()
    feriados = holidays.country_holidays(
        country="BR",
        years=[today.year - 1, today.year],
        state="SP",
    )
    feriados_np = np.array(list(feriados.keys()), dtype="datetime64")
    last_date: np.datetime64 = np.busday_offset(
        np.datetime64(last_unmarked_date), -1, roll="backward", holidays=feriados_np
    )
    last_date_str: str = last_date.astype(str)
    return last_date_str


def get_atrasados(journal_paths: JournalPaths):
    today = date.today()
    journal_file = Path(journal_paths.txns_dir).joinpath(f"{today.year}.journal")
    last_date_str = get_last_date(str(journal_file))
    atrasados_command = ["print", "tag:tipo=locacao", "--pending", "-e", last_date_str]
    txns = helpers.hledger_file(str(journal_file), atrasados_command)

    titulo = helpers.underline(f"Atrasados até: {last_date_str} (não incluso)")
    result = f"""
{titulo}

{txns}
"""

    return result


def send_atrasados(journal_paths: JournalPaths, journal_config: JournalConfig, to: str):
    from_ = journal_config.email_login
    pass_file = journal_config.email_pass_file
    with open(pass_file, "r") as f:
        password = next(f).rstrip("\n")

    if not password:
        raise ValueError("password nao encontrado")

    pendente = get_pendente(journal_config.agenda_file)
    subject = f"{pendente['status']} e Atrasados {journal_config.apelido}"
    email = Email(
        journal_config.email_host,
        int(journal_config.email_port),
        from_,
        password,
        subject,
        to,
    )
    email.text_body("Veja arquivo anexo\n\nPendencias:\n" + pendente["body"])

    today_str = date.today().strftime("%Y-%m-%d")
    relatorio_file = str(
        Path(journal_config.relatorios_dir).joinpath(
            f"atrasados locacao em {today_str}.pdf"
        )
    )
    relatorio = get_atrasados(journal_paths)
    dav = WebDav(journal_config.dav_options)
    helpers.print_pdf(relatorio, dav, relatorio_file)
    email.attach(relatorio_file)

    print(relatorio + "\n\n")
    print("Status: " + pendente["status"])
    print(pendente["body"])
    print("Enviando email")
    result = email.send()
    print(result)


if __name__ == "__main__":
    print(__name__)
    base_dir = sys.argv[1]
    to = sys.argv[2]

    journal_paths = config.get_journal_paths(base_dir)
    journal_config = config.get_config(base_dir)

    if to == "stdout":
        pendente = get_pendente(journal_config.agenda_file)
        print(pendente["body"])
        sys.exit()

    send_atrasados(journal_paths, journal_config, to)
