from decimal import Decimal
from typing import List, Set, Union

from prompt_toolkit.shortcuts import CompleteStyle
from questionary import Style, autocomplete, text

from . import validation
from .txn_lib import sort_accts, sort_notes


def ask_date(default: str):
    def ask():
        date: str = text(
            "Data (YYYY-MM-DD)",
            validate=validation.val_date,
            default=default,
        ).ask()
        return date

    return ask


def ask_payee(data: str, ano: str, payees: List[str], default: str):
    def ask():
        validate = validation.val_payee(data, ano)
        payee: str = autocomplete(
            message='Recebido de/Pago a ou <TAB> ("!" para nao confirmada)',
            choices=payees,
            validate=validate,
            default=default,
            ignore_case=True,
            match_middle=True,
            style=Style([("answer", "fg:#f71b07")]),
            complete_style=CompleteStyle.COLUMN,
        ).ask()
        return payee

    return ask


def ask_note(payee: str, completo: str, default: str):
    def ask():
        notes = sort_notes(completo, payee)
        note: str = autocomplete(
            message="Descricao ou <TAB>",
            choices=notes,
            default=default,
            validate=validation.val_note,
            ignore_case=True,
            match_middle=True,
            style=Style([("answer", "fg:#f71b07")]),
            complete_style=CompleteStyle.COLUMN,
        ).ask()
        return note

    return ask


def ask_imovel(imoveis: List[str], default: str = ""):
    def ask():
        validate = validation.val_imovel(imoveis)
        imovel: str = autocomplete(
            message="Imovel ou <TAB>",
            choices=imoveis,
            validate=validate,
            default=default,
            ignore_case=True,
            match_middle=True,
            style=Style([("answer", "fg:#f71b07")]),
            complete_style=CompleteStyle.COLUMN,
        ).ask()
        return imovel

    return ask


def ask_acct(
    payee: str,
    note: str,
    posting_answers_len: int,
    soma: Union[Decimal, int],
    accts_declared: List[str],
    completo: str,
    accts_used: Set[str],
):
    def ask():
        validate = validation.val_acct(posting_answers_len, soma, accts_declared)
        accts = sort_accts(completo, payee, note, accts_used)
        acct: str = autocomplete(
            message="Conta (Enter para encerrar)",
            choices=accts,
            validate=validate,
            ignore_case=True,
            match_middle=True,
            style=Style([("answer", "fg:#f71b07")]),
            complete_style=CompleteStyle.COLUMN,
        ).ask()
        return acct

    return ask


def ask_valor(soma: Union[Decimal, int], posting_answer_len: int):
    def ask():
        if posting_answer_len > 1 and soma != 0:
            valor_default = str(soma * -1)
        else:
            valor_default = ""

        valor: str = text(
            "Valor",
            validate=validation.val_valor,
            default=valor_default,
        ).ask()
        return valor

    return ask
