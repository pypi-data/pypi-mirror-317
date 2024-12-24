import os
from datetime import datetime

from . import helpers


def save_txns(journal_path: str, txns: str, desc: str):
    agora = datetime.today().strftime("%Y-%m-%d %H:%M")
    user = os.environ["HL_USER"]
    header = f"\n\n; Lancamentos recorrentes, {desc}, gerados em {agora} por {user}\n\n"
    with open(journal_path, "a") as journal_file:
        journal_file.write(header + txns + "\n\n")


def get_print_report(title: str, text: str):
    os.system("clear")
    report = helpers.underline(title) + "\n" + text + "\n\n\n"
    print(report)
    input("Enter para continuar. ")
    return report
