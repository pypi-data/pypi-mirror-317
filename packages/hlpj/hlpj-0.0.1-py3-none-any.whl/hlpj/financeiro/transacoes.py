import subprocess
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional

import questionary
from prompt_toolkit.shortcuts import CompleteStyle

from ..base import helpers
from ..base.config import JournalConfig, JournalPaths
from .conciliacao import conferencias


def corrigir_txns(file_path: str):
    subprocess.run(["hledger", "-f", file_path, "stats"])
    linha = input("Para corrigir, digite a linha ou enter para sair: ")
    if linha != "":
        helpers.open_editor(file_path, f"+{linha}")
    return


def load_hledger_ui(
    file_path: str,
    params: list,
    conciliacao_file: Optional[str] = None,
    nome_imoveis_file: Optional[str] = None,
):
    command = subprocess.run(
        [
            "hledger-ui",
            "-f",
            file_path,
            "--future",
            "--watch",
            *params,
        ]
    )

    if command.returncode != 0:
        corrigir_txns(file_path)
        return

    if conciliacao_file and nome_imoveis_file:
        conferencias(file_path, conciliacao_file, nome_imoveis_file)


def ui_ano_corrente(journal_paths: JournalPaths, journal_config: JournalConfig):
    load_hledger_ui(
        journal_config.journal_year,
        ["--tree", "--future"],
        journal_paths.conciliacao_file,
        journal_config.nome_imoveis_file,
    )


def ui_ano_especifico(journal_paths: JournalPaths, journal_config: JournalConfig):
    choices = [
        questionary.Choice(title=file.stem, value=file)
        for file in Path(journal_paths.txns_dir).iterdir()
        if helpers.is_valid_file(file)
    ]
    journal_all_path = Path(journal_paths.journal_all)
    choices.append(
        questionary.Choice(title=journal_all_path.stem, value=journal_all_path)
    )
    escolhido: Path = questionary.select(
        "Opção", choices=choices, use_shortcuts=True
    ).ask()
    load_hledger_ui(
        str(escolhido),
        ["--tree", "--future"],
        journal_paths.conciliacao_file,
        journal_config.nome_imoveis_file,
    )


def ask_options(choices: List[str]) -> str:
    choosen = questionary.autocomplete(
        "Comece a digitar ou <TAB>",
        choices=choices,
        ignore_case=True,
        match_middle=True,
        style=questionary.Style([("answer", "fg:#f71b07")]),
        complete_style=CompleteStyle.MULTI_COLUMN,
    ).ask()
    return choosen


def val_month(month: str):
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        return "Formato de data errado"


def update_desp_imovel(journal_paths: JournalPaths, journal_config: JournalConfig):
    journal_config
    this_month = date.today().strftime("%Y-%m")
    month = questionary.text("Digite o mes (YYYY-MM)", default=str(this_month)).ask()

    journal = helpers.get_journal_year(journal_paths.txns_dir, int(journal_config.ano))

    imoveis = helpers.hledger_file(journal, ["tags", "imovel", "--values"]).split("\n")
    imovel = ask_options(imoveis)
    ui_comm = [
        "Despesa:Imovel:",
        "-p",
        month,
        "--pending",
        f"tag:imovel={imovel}",
        "tag:tipo=despesa_recorrente",
        "--change",
        "--tree",
        "--future",
        "--register=Despesa:Imovel",
    ]
    load_hledger_ui(journal, ui_comm)


def ui_filter(journal_paths: JournalPaths, journal_config: JournalConfig):
    # Ask
    option = questionary.select(
        "Escolha filtro",
        choices=["imovel", "pessoa", "descricao", "hospede", "tipo"],
        use_shortcuts=True,
    ).ask()
    journal = helpers.get_journal_year(journal_paths.txns_dir, int(journal_config.ano))

    # Open
    if option == "imovel":
        possible = helpers.hledger_file(journal, ["tags", "imovel", "--values"]).split(
            "\n"
        )
        choosen = ask_options(possible)
        load_hledger_ui(
            journal,
            [f"tag:imovel={choosen}", "--tree"],
            journal_paths.conciliacao_file,
            journal_config.nome_imoveis_file,
        )

    elif option == "pessoa":
        possible = helpers.hledger_file(journal, ["payee"]).split("\n")
        choosen = ask_options(possible)

        load_hledger_ui(
            journal,
            [f"payee:{choosen}", "--tree"],
            journal_paths.conciliacao_file,
            journal_config.nome_imoveis_file,
        )

    elif option == "descricao":
        possible = helpers.hledger_file(journal, ["notes"]).split("\n")
        choosen = ask_options(possible)
        load_hledger_ui(
            journal,
            [f"note:{choosen}", "--tree"],
            journal_paths.conciliacao_file,
            journal_config.nome_imoveis_file,
        )
    elif option == "hospede":
        hospedes = helpers.hledger_file(journal, ["tags", "hospede", "--values"]).split(
            "\n"
        )
        hospede = ask_options(hospedes)
        load_hledger_ui(
            journal,
            [f"tag:hospede={hospede}"],
            journal_paths.conciliacao_file,
            journal_config.nome_imoveis_file,
        )
    elif option == "tipo":
        tipos = helpers.hledger_file(journal, ["tags", "tipo", "--values"]).split("\n")
        tipo = ask_options(tipos)
        load_hledger_ui(
            journal,
            [f"tag:tipo={tipo}", "--tree"],
            journal_paths.conciliacao_file,
            journal_config.nome_imoveis_file,
        )


def show_plano_contas(journal_paths: JournalPaths, journal_config: JournalConfig):
    current_file = Path(journal_paths.txns_dir).joinpath(
        journal_config.ano + ".journal"
    )
    accounts = helpers.hledger_file(
        str(current_file), ["accounts", "--declared", "--tree"]
    )
    print(accounts)
