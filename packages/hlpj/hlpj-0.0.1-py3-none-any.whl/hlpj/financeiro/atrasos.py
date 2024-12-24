import csv
import re
import sys
from io import StringIO
from pathlib import Path

from ..base.config import get_config, get_journal_paths
from ..base.helpers import hledger_file
from .saldos import get_saldos


def get_journal_last_date(journal_file: str) -> str:
    comm = ["reg", "^Ativo:Disponibilidade", "--unmarked"]
    journal = hledger_file(journal_file, comm)
    dates = re.findall(r"^\d{4}-\d{2}-\d{2}", journal, re.MULTILINE)
    if len(dates) > 0:
        return dates[-1]
    else:
        raise ValueError("Data de transacao nao encontrada")


def get_conciliacao_last_date(conciliacao_file: str):
    saldos = get_saldos(conciliacao_file)
    conciliacao_date = min([saldo[1] for saldo in saldos])
    return conciliacao_date


def get_atrasados(journal_file: str, last_date: str):
    comm = [
        "bal",
        "^Receita:",
        "--pending",
        "--end",
        last_date,
        "--pivot",
        "payee",
        "--output-format=csv",
    ]
    atrasados_txn = hledger_file(journal_file, comm)
    atrasados_csv = csv.reader(StringIO(atrasados_txn))
    for atrasado in atrasados_csv:
        print(f"{atrasado[0]}: {atrasado[1]}")


if __name__ == "__main__":
    base_dir = sys.argv[1]
    nome = Path(base_dir).name
    journal_paths = get_journal_paths(base_dir)
    config_paths = get_config(base_dir)
    journal_file = str(
        Path(journal_paths.base_dir)
        .joinpath("transacoes")
        .joinpath(f"{config_paths.ano}.journal")
    )

    conciliacao_file = str(journal_paths.conciliacao_file)

    conciliacao_last = get_conciliacao_last_date(conciliacao_file)
    journal_last = get_journal_last_date(journal_file)
    print(f"Empresa: {config_paths.apelido}. Ultima data: {journal_last}\n")
    get_atrasados(str(journal_file), journal_last)
