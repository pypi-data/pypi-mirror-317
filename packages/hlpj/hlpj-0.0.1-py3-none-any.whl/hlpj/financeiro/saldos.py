import sys
from configparser import SectionProxy
from pathlib import Path

from ..base.helpers import ini_parser


def get_max(items: SectionProxy):
    last_date = max(items.keys())
    last_amount_str = items.get(last_date, "")
    try:
        last_amount = float(last_amount_str)
        return (last_date, last_amount)
    except ValueError:
        return (last_date, last_amount_str)


def get_saldos(conciliacao_file: str):
    conciliacao_ini = ini_parser()
    conciliacao_ini.read(conciliacao_file)

    saldos = [
        (section.split(":")[-1], *get_max(items))
        for section, items in conciliacao_ini.items()
        if section != "DEFAULT"
    ]
    saldos = sorted(saldos, key=lambda conta: conta[0], reverse=True)
    return saldos


if __name__ == "__main__":
    base_dir = sys.argv[1]
    empresa = Path(base_dir).name
    conciliacao_file = str(Path(base_dir).joinpath("conciliacao.ini"))

    print(f"Saldos Bancarios na empresa {empresa}")
    saldos = get_saldos(conciliacao_file)
    for saldo in saldos:
        print("\n----------\n")
        print(f"- Conta: {saldo[0]}")
        print(f"- Data: {saldo[1]}")

        valor = saldo[2]
        if type(valor) == float:
            print(f"- Saldo: {valor:,.2f}")
        else:
            print(f"- Saldo: {valor}")

    total = sum([item[2] for item in saldos if type(item[2]) is float])
    print(f"\n\nTOTAL: {total:,.2f}")
