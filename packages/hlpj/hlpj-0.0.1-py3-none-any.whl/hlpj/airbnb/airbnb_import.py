import csv
import os
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Dict, List, NamedTuple, Set, Tuple

import questionary
from dateutil.relativedelta import relativedelta

from hlpj.base.webdav import WebDav

from ..base import helpers
from ..base.config import JournalConfig, JournalPaths

RESERVAS_FILE_NAME = "reservations.csv"


class ReservaFile(NamedTuple):
    codigo: str
    status: str
    hospede: str
    telefone: str
    adultos: str
    criancas: str
    bebes: str
    inicio: str
    termino: str
    noites: str
    reservado: str
    anuncio: str
    ganhos: str


def get_reservas(
    dav: WebDav,
    reservas_path: str,
    existentes: List[str],
    fields: Tuple[str, ...],
) -> List[ReservaFile]:
    reservas_txt = dav.get_txt_content(reservas_path)
    reservas_io = StringIO(reservas_txt)

    reservas_csv = csv.DictReader(reservas_io, fields)
    next(reservas_csv)
    try:
        reservas_list = [ReservaFile(**reserva) for reserva in reservas_csv]
    except TypeError:
        raise TypeError("Erro no arquivo reservations.csv")

    reservas_novas = [
        reserva for reserva in reservas_list if reserva.codigo not in existentes
    ]
    return reservas_novas


def reserva2txn(reserva: ReservaFile, conta_caixa: str, aptos: Dict[str, str]) -> str:
    inicio_date = datetime.strptime(reserva.inicio, "%d/%m/%Y")
    pgmto_date = inicio_date + relativedelta(days=2)
    inicio = inicio_date.strftime("%Y-%m-%d")
    pgmto = pgmto_date.strftime("%Y-%m-%d")
    termino = datetime.strptime(reserva.termino, "%d/%m/%Y").strftime("%Y-%m-%d")
    valor = reserva.ganhos.replace("R$", "").replace(".", "").replace(",", ".")

    apto = aptos.get(reserva.anuncio, "faltando")
    txn = f"""{pgmto} ! Airbnb | Recebimento de aluguel de temporada
    ; tipo:airbnb_reserva
    ; imovel:{apto}
    ; cod_reserva:{reserva.codigo}
    ; hospede:{reserva.hospede}
    ; pessoas:{reserva.adultos} adultos - {reserva.criancas} criancas - {reserva.bebes} bebes
    ; inicio:{inicio}
    ; termino:{termino}
    ; noites:{reserva.noites}
    ; reservado:{reserva.reservado}
    ; valor_total:{valor}
    {conta_caixa}    {valor}
    Receita:Locacao"""
    return txn


def get_acct_cash(journal: str, cash_prefix: str) -> str:
    accts_str = helpers.hledger_stdin(journal, ["accounts", cash_prefix])
    accts = accts_str.split("\n")
    acct_cash: str = questionary.select(
        "Escolha conta: ",
        choices=accts,
        use_shortcuts=True,
    ).ask()
    return acct_cash


def get_aptos(airbnb_file: str) -> Dict[str, str]:
    airbnb_config = helpers.ini_parser()
    airbnb_config.read(airbnb_file)
    aptos = dict(airbnb_config["aptos"])
    return aptos


def save_txns(journal_path: str, txns: str, agora: str, user: str):
    header = f"\n\n; Reservas gerados em {agora} por {user}\n\n"
    with open(journal_path, "a") as journal_file:
        journal_file.write(header + txns + "\n\n")


def get_missing_aptos(reservas: List[ReservaFile], aptos: Dict[str, str]) -> Set[str]:
    anuncios_reserva = {reserva.anuncio for reserva in reservas}
    anuncios_aptos = set(aptos.keys())
    missing_aptos = anuncios_reserva.difference(anuncios_aptos)
    return missing_aptos


def fix_missing_aptos(missing_aptos: Set[str], airbnb_file: str):
    missing_output_list = [missing_apto + " = " for missing_apto in missing_aptos]
    missing_aptos_str = "\n".join(missing_output_list)

    print(helpers.underline("Cadastrar apartamentos abaixo"))
    print(missing_aptos_str)
    confirm_edit = questionary.confirm(
        "Editar lista de apartamentos", default=True, auto_enter=True
    ).ask()
    if confirm_edit:
        helpers.open_editor(airbnb_file)


def import_reservas(journal_paths: JournalPaths, journal_config: JournalConfig):
    # Get dates
    today = datetime.today()

    # Get data
    journal = helpers.join_journal_last(journal_paths.txns_dir, int(journal_config.ano))
    cash_prefix = journal_config.cash_prefix
    acct_cash = get_acct_cash(journal, cash_prefix)
    aptos = get_aptos(journal_paths.airbnb_file)
    cod_existentes = helpers.hledger_stdin(
        journal,
        ["tags", "cod_reserva", "--values"],
    ).split("\n")

    # Get reservas
    fields = ReservaFile._fields
    reservas_file = str(Path(journal_config.files_dir).joinpath(RESERVAS_FILE_NAME))
    dav = WebDav(journal_config.dav_options)
    reservas = get_reservas(dav, reservas_file, cod_existentes, fields)

    # Test missing aptos
    missing_aptos = get_missing_aptos(reservas, aptos)
    if len(missing_aptos) > 0:
        fix_missing_aptos(missing_aptos, journal_paths.airbnb_file)
        return

    # Get txns
    txns = [reserva2txn(reserva, acct_cash, aptos) for reserva in reservas]
    txns_str = "\n\n".join(txns)

    # Add txns
    txns_hledger = helpers.hledger_stdin(txns_str, ["print"])
    print(txns_str)
    confirm_add = questionary.confirm(
        "Adiciona reservas acima", default=False, auto_enter=True
    ).ask()
    if confirm_add:
        save_txns(
            journal_config.journal_year, txns_hledger, str(today), os.environ["HL_USER"]
        )
        today_str = today.strftime("%Y-%m-%d")
        imported_path = Path(journal_config.files_dir).joinpath(
            f"reservations_imported_{today_str}.csv"
        )
        dav.client.move(
            remote_path_from=reservas_file,
            remote_path_to=str(imported_path),
            overwrite=True,
        )

        print("Reservas adicionadas")
        Path(journal_paths.base_dir).joinpath("airbnb_last_imported").write_text(
            today.strftime("%Y-%m-%d")
        )
    else:
        print("Cancelado")
