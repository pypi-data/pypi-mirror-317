from pathlib import Path
from typing import Callable, List, NamedTuple, TypedDict

from ..base import helpers
from . import ask


class TxnAdd(NamedTuple):
    name: str
    question: Callable[[], str]


class TxnAnswer(TypedDict):
    name: str
    answer: str


class TxnBase:
    def __init__(self, ano: str, nome_imoveis_file: str, completo: str):
        self.ano = ano
        self.completo = completo

        self.payees = helpers.hledger_file(self.completo, ["payees"]).split("\n")
        self.imoveis = Path(nome_imoveis_file).read_text().split("\n")

        self.base_answers: List[TxnAnswer] = list()
        self.base_questions_len = len(self.base_questions)

    def get_txn_item(self, name: str):
        value_gen = (
            item["answer"] for item in self.base_answers if item["name"] == name
        )
        value = next(value_gen, "")
        return value

    @property
    def description(self):
        payee = self.get_txn_item("payee")
        note = self.get_txn_item("note")

        if payee == "":
            description = note
        else:
            description = f"{payee} | {note}"

        return description

    @property
    def txn_dict(self):
        result = {txn["name"]: txn["answer"] for txn in self.base_answers}
        return result

    @property
    def base_questions(self):
        data = self.get_txn_item("date")
        payee = self.get_txn_item("payee")
        note = self.get_txn_item("note")
        imovel = self.get_txn_item("imovel")

        ask_date = ask.ask_date(data)
        ask_payee = ask.ask_payee(data, self.ano, self.payees, payee)
        ask_note = ask.ask_note(payee, self.completo, note)
        ask_imovel = ask.ask_imovel(self.imoveis, imovel)

        ask_questions = [
            TxnAdd("date", ask_date),
            TxnAdd("payee", ask_payee),
            TxnAdd("note", ask_note),
            TxnAdd("imovel", ask_imovel),
        ]
        return ask_questions
