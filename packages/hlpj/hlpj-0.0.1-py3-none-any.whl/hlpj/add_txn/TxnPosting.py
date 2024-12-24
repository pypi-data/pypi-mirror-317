from decimal import Decimal
from typing import List, TypedDict

from . import ask
from .txn_lib import get_accts_declared, is_float
from .TxnBase import TxnBase


class AnswerPosting(TypedDict):
    acct: str
    valor: str


class TxnPosting(TxnBase):
    def __init__(self, ano: str, nome_imoveis_file: str, completo: str, txns_dir: str):
        super().__init__(ano, nome_imoveis_file, completo)

        self.accts_declared = get_accts_declared(txns_dir, self.ano)
        self.posting_answers: List[AnswerPosting] = list()

    def posting_answers_len(self):
        return len(self.posting_answers)

    def get_soma(self):
        soma = sum(
            Decimal(posting["valor"])
            for posting in self.posting_answers
            if is_float(posting["valor"])
        )
        return soma

    def get_accts_used(self):
        return set(answer["acct"] for answer in self.posting_answers)

    @property
    def posting_question(self):
        payee = self.get_txn_item("payee")
        note = self.get_txn_item("note")
        posting_answers_len = self.posting_answers_len()
        soma = self.get_soma()

        ask_acct = ask.ask_acct(
            payee,
            note,
            posting_answers_len,
            soma,
            self.accts_declared,
            self.completo,
            self.get_accts_used(),
        )
        ask_valor = ask.ask_valor(soma, posting_answers_len)

        questions = {"acct": ask_acct, "valor": ask_valor}
        return questions
