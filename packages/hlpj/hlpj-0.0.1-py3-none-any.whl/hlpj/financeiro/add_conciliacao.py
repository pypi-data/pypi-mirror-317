from configparser import ConfigParser
from datetime import datetime

import questionary
from tabulate import tabulate

from hlpj.base.config import JournalConfig, JournalPaths

from ..add_txn.validation import val_date
from ..base import helpers


def val_valor(v_str: str):
    try:
        float(v_str)
    except ValueError:
        return "Digite numero valido"

    if not "." in v_str:
        return True

    decimal = v_str.split(".")[1]
    if len(decimal) > 2:
        return "Maximo duas casas decimais"
    return True


def ultimas(conciliacao: ConfigParser):
    conta_data = [
        (section, max(conciliacao[section].keys()))
        for section in conciliacao.sections()
    ]

    conta_data = sorted(conta_data, key=lambda item: item[1])

    table = tabulate(conta_data, headers=["Conta", "Ultima Conciliacao"])
    return table


def add_conciliacao(journal_paths: JournalPaths, journal_config: JournalConfig):
    conciliacao = helpers.ini_parser()
    conciliacao.read(journal_paths.conciliacao_file)

    print(ultimas(conciliacao) + "\n\n")
    contas = [conta for conta in conciliacao.sections() if conta != "DEFAULT"]

    conta: str = questionary.select("Escolha a conta", contas).ask()

    conta_saldos = conciliacao[conta]
    ult_data_str = max(conta_saldos)
    ult_data = datetime.strptime(ult_data_str, "%Y-%m-%d").date()
    prox_data = helpers.bday_off(ult_data, 1)
    prox_data_str = prox_data.strftime("%Y-%m-%d")

    data_saldo = questionary.text(
        "Data do saldo", default=prox_data_str, validate=val_date
    ).ask()
    valor_saldo: str = questionary.text("Saldo na data", validate=val_valor).ask()
    conciliacao.set(conta, data_saldo, valor_saldo)
    with open(journal_paths.conciliacao_file, "w") as f:
        conciliacao.write(f)
