import sys
from typing import Literal

from blessed import Terminal

from ..base import helpers
from .TxnBase import TxnAnswer
from .TxnPosting import AnswerPosting, TxnPosting


class CancelAddError(Exception):
    pass


class TxnAsk(TxnPosting):
    def __init__(self, ano: str, nome_imoveis_file: str, completo: str, txns_dir: str):
        super().__init__(ano, nome_imoveis_file, completo, txns_dir)

        self.base_step = 0
        self.term = Terminal()
        self.next_posting: Literal["acct", "valor"] = "acct"
        self.encerrado = False

    def go_up(self):
        sys.stdout.write(self.term.move_up * 2)
        sys.stdout.write(self.term.move_left)
        sys.stdout.write(self.term.clear_eol)

    def change_next_posting(self):
        if self.next_posting == "acct":
            self.next_posting = "valor"
        else:
            self.next_posting = "acct"

    def ask_base(self):
        answerTup = self.base_questions[self.base_step]
        name = answerTup.name
        answer = answerTup.question()

        if answer == "q":
            raise CancelAddError()
        elif answer == "p":
            self.go_up()
            self.base_step = max(0, self.base_step - 1)
            self.base_answers.pop()
        else:
            self.base_answers.append(TxnAnswer(name=name, answer=answer))
            self.base_step += 1

    def add_posting(self, answer: str):
        if self.next_posting == "acct":
            answer_posting = AnswerPosting(acct=answer, valor="")
            self.posting_answers.append(answer_posting)
        if self.next_posting == "valor":
            self.posting_answers[-1]["valor"] = answer

    def ask_posting(self):
        answer = self.posting_question[self.next_posting]()
        if answer == "q":
            raise CancelAddError()

        if answer == "":
            self.encerrado = True
            return

        if answer != "p":
            self.add_posting(answer)
            self.change_next_posting()
            return

        p_answers_len = self.posting_answers_len()
        self.go_up()
        if p_answers_len == 0:
            self.base_step -= 1
            return

        if self.next_posting == "acct":
            self.posting_answers[-1]["valor"] = "0"
        if self.next_posting == "valor":
            self.posting_answers.pop()
        self.change_next_posting()

    def get_hl_txn(self):
        txn_str = f"\n{self.txn_dict['date']} {self.description}\n"
        if self.txn_dict["imovel"] != "":
            txn_str += f"  ; imovel:{self.txn_dict['imovel']}\n"

        for posting in self.posting_answers:
            txn_str += f"  {posting['acct']}    {posting['valor']}\n"

        txn_hledger = helpers.hledger_stdin(txn_str, ["print"])
        return txn_hledger

    def ask_questions(self):
        while not self.encerrado:
            if self.base_step < self.base_questions_len:
                self.ask_base()
            else:
                self.ask_posting()

        hl_txn = self.get_hl_txn()
        return hl_txn
