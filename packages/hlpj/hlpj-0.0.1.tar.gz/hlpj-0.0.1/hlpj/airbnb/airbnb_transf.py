from io import StringIO

import pandas as pd

from ..base import helpers
from ..base.config import JournalConfig, JournalPaths


def transferido_airbnb_mes(journal_paths: JournalPaths, journal_config: JournalConfig):
    journal_config
    txns_dir = journal_paths.txns_dir

    data_base = helpers.get_date()

    journal = helpers.join_journal_last(txns_dir, data_base.year)
    report_command = [
        "reg",
        "-p",
        f"{data_base.year}-{data_base.month}",
        "payee:Airbnb",
        "--daily",
        "--unmarked",
        "--pivot",
        "hospede",
        "Receita|Despesa",
        "--output-format=csv",
    ]
    csv_str = helpers.hledger_stdin(journal, report_command)
    df = pd.DataFrame(pd.read_csv(StringIO(csv_str)))
    df = df.rename({"account": "note"}, axis=1)
    df = df.set_index(["date"])[["note", "amount"]]
    df["amount"] = (
        df["amount"]
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )
    sums = df.groupby(level=0).sum()
    df["total"] = sums["amount"]
    df = df.set_index(["total", "note"], append=True)
    print(df.to_string() + "\n\n")
