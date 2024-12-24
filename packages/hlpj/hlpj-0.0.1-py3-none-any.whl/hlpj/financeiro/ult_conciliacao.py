import sys
from datetime import date, datetime

from ..base import helpers


def diff_dias(data_str: str, data_limite: date) -> int:
    data = datetime.strptime(data_str, "%Y-%m-%d").date()
    dias_delta = data_limite - data
    dias = abs(dias_delta.days)
    return dias


def ultima_conta(conciliacao_file: str):
    saldos = helpers.ini_parser()
    saldos.read(conciliacao_file)

    saldos_ultimos = {
        conta: max(section.keys())
        for conta, section in saldos.items()
        if len(section) > 0 and "encerrado" not in list(section.values())[-1]
    }

    data_limite = helpers.bday_off(date.today(), -1)
    atrasados = [
        f"{conta} Saldo em conciliacao atrasado em {diff_dias(data,data_limite)} dias"
        for conta, data in saldos_ultimos.items()
        if datetime.strptime(data, "%Y-%m-%d").date() < data_limite
    ]

    if len(atrasados) > 0:
        error = "\n".join(atrasados)
        print(error, file=sys.stderr)
        sys.exit(1)
    else:
        print("Saldos em conciliacao atualizados")


if __name__ == "__main__":
    conciliacao_file = sys.argv[1]
    ultima_conta(conciliacao_file)
