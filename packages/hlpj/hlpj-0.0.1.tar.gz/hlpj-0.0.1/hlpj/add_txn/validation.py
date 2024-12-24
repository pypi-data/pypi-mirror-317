from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import List, Union

from .txn_lib import is_float


def val_date(data_str: str):
    if data_str == "q":
        return True
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
    except ValueError:
        return "Data no formato correto"
    return True


def val_payee(data: str, ano: str):
    def val(payee: str):
        if payee in ["p", "q", ""]:
            return True
        date_year = datetime.strptime(data, "%Y-%m-%d").year
        if not payee.startswith("!") and date_year < int(ano):
            return "Transacao confirmada nao pode ser anterior a " + ano
        return True

    return val


def val_note(note: str):
    if len(note) == 0:
        return "Digite a descrição"
    return True


def val_imovel(imoveis: List[str]):
    def val(imovel: str):
        if imovel in ["", None, "p", "q"]:
            return True
        if imovel not in imoveis:
            return "Imovel invalido"
        return True

    return val


def val_acct(
    posting_answers_len: int, soma: Union[Decimal, int], accts_declared: List[str]
):
    def val(acct: str):
        if acct in ["p", "q"]:
            return True
        if acct == "" and posting_answers_len == 0:
            return "Insira uma postagem ou q para cancelar"
        if acct == "" and soma != 0:
            return f"Erro. Soma={soma}. Insira mais uma postagem ou q para cancelar"
        if acct != "" and acct not in accts_declared:
            return "Conta nao permitida"
        return True

    return val


def val_valor(valor: str):
    if valor in ["p", "q"]:
        return True
    if valor in ["", None]:
        return "Nao pode ser vazio"
    if not is_float(valor):
        return "Somente numero"

    try:
        valor_dec = Decimal(valor)
        exponent = int(valor_dec.as_tuple().exponent)
        if exponent > 2:
            return "So pode duas casas decimais"
    except (InvalidOperation, ValueError):
        return "Informe numero valido"
    return True
