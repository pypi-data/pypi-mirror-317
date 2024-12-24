import configparser
import os
import re
import shlex
import subprocess
import tempfile
from datetime import date
from pathlib import Path
from typing import List, Optional

import holidays
import numpy as np
import questionary
from dateutil.relativedelta import relativedelta

from .webdav import WebDav


def val_int_range(min: int, max: int):
    def validate(x: str):
        try:
            n = int(x)
        except ValueError:
            return "Precisa ser numero"

        cond = min <= n <= max
        if cond is False:
            return f"Entre {min} e {max}"
        return True

    return validate


def get_date(
    default_year: Optional[int] = None, default_month: Optional[int] = None
) -> date:
    default_date = date.today() - relativedelta(months=1)
    year = default_year or default_date.year
    month = default_month or default_date.month
    ano = questionary.text(
        "Digite o ano",
        default=str(year),
        validate=val_int_range(2010, 2030),
    ).ask()
    mes = questionary.text(
        "Digite o mes",
        default=str(month),
        validate=val_int_range(1, 12),
    ).ask()
    data = date(year=int(ano), month=int(mes), day=1)
    return data


def hledger_stdin(journal_str: str, args: List[str]) -> str:
    proc = subprocess.run(
        ["hledger", "-f-", *args],
        capture_output=True,
        input=journal_str.encode(),
    )
    if proc.returncode != 0:
        raise RuntimeError("Erro:\n" + proc.stderr.decode("utf8"))

    return proc.stdout.decode("utf8")


def hledger_file(filename: str, args: List[str]) -> str:
    command = ["hledger", "-f", filename, *args]
    proc = subprocess.run(command, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError("Erro:\n" + proc.stderr.decode("utf8"))

    return proc.stdout.decode("utf8")


def join_journal_last(txns_dir_path: str, year: int) -> str:
    year_previous = year - 1
    inicio_path = Path(txns_dir_path).joinpath(f"{year}.journal")
    previous_path = Path(txns_dir_path).joinpath(f"{year_previous}.journal")
    journal = f"include {inicio_path}\n"
    if previous_path.exists() is True:
        journal += f"include {previous_path}\n"
    return journal


def underline(text: str) -> str:
    under = "-" * len(text)
    result = "\n" + text + "\n" + under
    return result


def is_valid_file(file: Path) -> bool:
    if re.search("^\\.?.*[~|#]", file.name) is None and file.is_dir() is False:
        return True
    else:
        return False


def get_journal_year(txns_dir: str, year: Optional[int] = None) -> str:
    year = year or date.today().year
    journal = Path(txns_dir).joinpath(f"{year}.journal")
    journal_str = str(journal)
    return journal_str


def intro(locador: str):
    hoje = date.today()
    dia_ano = hoje.strftime("%j")
    porcento_ano = f"{int(dia_ano) / 365 * 100:.2f}%"
    user = os.environ["HL_USER"]
    dia = hoje.strftime(f"%A, %d de %B de %Y. %jo. dia do ano")
    result = f"{dia} ({porcento_ano})\nUsuario: {user}\tLocador:{locador}\n"
    return result


def open_editor(file_path: str, *args: str):
    editor = os.environ.get("EDITOR", "emacs -nw")
    subprocess.run([*shlex.split(editor), *args, file_path], check=True)


def print_pdf(text: str, dav: WebDav, output_path: str):
    output_parent = Path(output_path).resolve().parent
    output_stem = Path(output_path).stem
    output = output_parent.joinpath(output_stem + ".pdf")

    ens_proc = subprocess.run(
        ["enscript", "--no-header", "--landscape", "-p", "-"],
        check=True,
        input=text.encode("latin-1"),
        capture_output=True,
    )

    with tempfile.NamedTemporaryFile("wb", suffix=".pdf") as f:
        name = f.name
        subprocess.run(
            ["ps2pdf", "-", name],
            check=True,
            input=ens_proc.stdout,
            capture_output=True,
        )
        dav.upload_file(name, str(output))


def ini_parser() -> configparser.ConfigParser:
    parser = configparser.ConfigParser(delimiters="=", interpolation=None, strict=False)
    parser.optionxform = lambda optionstr: optionstr
    return parser


def sanitize_filename(filename: str):
    sanitized = re.sub(r"<|>|:|\"|/|\\|\||\?|\*", "-", filename)
    return sanitized


def get_txns_curr(txns_dir: str, ano: str):
    txns_curr_path = Path(txns_dir).joinpath(f"{ano}.journal")
    txns_curr = str(txns_curr_path)
    return txns_curr


def bday_off(base_date: date = date.today(), days: int = 0) -> date:
    feriados = holidays.country_holidays(
        country="BR",
        years=[base_date.year, base_date.year - 1],
    )
    roll = "forward" if days > 0 else "backward"
    date_off_np = np.busday_offset(
        base_date,
        offsets=days,
        roll=roll,
        holidays=list(feriados),
    )
    date_off = date_off_np.astype(date)
    return date_off
