import os
from pathlib import Path

import questionary

from ..base import helpers
from ..base.config import JournalConfig, JournalPaths
from .TxnAsk import CancelAddError, TxnAsk


def add_txns(journal_paths: JournalPaths, journal_config: JournalConfig):
    ano = journal_config.ano
    nome_imoveis_file = journal_config.nome_imoveis_file
    completo = journal_paths.journal_all
    txns_dir = journal_paths.txns_dir

    while True:
        os.system("clear")
        print(helpers.underline("Adicionar transacao"))
        print('"q" para sair\n')

        try:
            txn = TxnAsk(
                ano,
                nome_imoveis_file,
                completo,
                txns_dir,
            )
            txn_hledger = txn.ask_questions()
        except CancelAddError:
            print("Cancelado")
            return

        print("\n" + txn_hledger + "\n")
        confirm = questionary.confirm(
            "Acrescenta transacao", auto_enter=True, default=False
        ).ask()
        if confirm:
            journal_path = Path(journal_paths.txns_dir).joinpath(
                f"{journal_config.ano}.journal"
            )
            with open(journal_path, "a") as f:
                f.write("\n" + txn_hledger + "\n")
        else:
            print("Cancelado...")
