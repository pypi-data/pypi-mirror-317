import shutil
import sys
from configparser import ConfigParser
from pathlib import Path
from typing import NamedTuple

import questionary

from . import helpers

CASH_PREFIX = "Ativo:Disponibilidade:Caixa e Bancos:"
CONTA_AIRBNB = "Receita:Receita:Locacao"


class JournalPaths(NamedTuple):
    base_dir: str
    txns_dir: str
    recorr_pgmto_file: str
    recorr_receb_file: str
    controle_file: str
    codigos_file: str
    journal_all: str
    conciliacao_file: str
    info_file: str
    airbnb_file: str
    locacoes_file: str
    relatorios_file: str


class JournalConfig(NamedTuple):
    apelido: str
    locador: str
    cash_prefix: str
    conta_airbnb: str
    ano: str
    files_dir: str
    relatorios_dir: str
    nome_imoveis_file: str
    pix: str
    conta1: str
    conta2: str
    journal_year: str
    email_host: str
    email_login: str
    email_port: str
    email_name: str
    email_pass_file: str
    agenda_file: str
    dav_options: dict


def get_journal_paths(dir_str: str) -> JournalPaths:
    base_dir = str(Path(dir_str))
    txns_dir = f"{base_dir}/transacoes"
    paths = JournalPaths(
        base_dir=base_dir,
        txns_dir=txns_dir,
        recorr_pgmto_file=f"{base_dir}/recorr_pgmto.journal",
        recorr_receb_file=f"{base_dir}/recorr_receb.journal",
        controle_file=f"{base_dir}/controle.journal",
        codigos_file=f"{base_dir}/codigos.ini",
        journal_all=f"{base_dir}/completo.journal",
        conciliacao_file=f"{base_dir}/conciliacao.ini",
        info_file=f"{base_dir}/info.txt",
        airbnb_file=f"{base_dir}/airbnb.ini",
        locacoes_file=f"{base_dir}/locacoes.ini",
        relatorios_file=f"{base_dir}/relatorios.ini",
    )
    return paths


def get_config(dir_str: str) -> JournalConfig:
    config_path = Path(dir_str).joinpath("config.ini")
    config = helpers.ini_parser()
    config.read(config_path)

    empresa = dict(config["empresa"])
    paths = dict(config["paths"])
    pagamento = dict(config["pagamento"])
    email = dict(config["email"])

    year = config["empresa"]["ano"]
    journal_year = str(Path(dir_str).joinpath("transacoes", year + ".journal"))

    dav_options = dict(
        webdav_hostname=config["webdav"]["url"],
        webdav_login=config["webdav"]["username"],
        webdav_password=config["webdav"]["password"],
    )

    configTuple = JournalConfig(
        **empresa,
        **paths,
        **pagamento,
        **email,
        journal_year=journal_year,
        dav_options=dav_options,
    )
    return configTuple


def new_company():
    # Get base_dir
    dir_input = questionary.text("Pasta de dados: ").ask()
    apelido = questionary.text("Apelido empresa").ask()
    base_dir = Path(dir_input).expanduser().resolve().joinpath(apelido)
    if Path(base_dir).exists() is True:
        sys.exit("Erro: Pasta já existe. Cancelando...")

    # Copy files
    new_company_dir = Path(__file__).parent.joinpath("new_company")
    shutil.copytree(new_company_dir, base_dir)

    # Add dirs to config.ini
    config_path = base_dir.joinpath("config.ini")
    files_dir = questionary.text("Pasta de arquivos").ask()
    config = ConfigParser(delimiters="=")
    config.read(config_path)
    files_path = Path(files_dir).expanduser().resolve()
    relatorios_path = files_path.parent.joinpath("relatorios")
    config["paths"]["files_dir"] = str(files_path)
    config["paths"]["relatorios_dir"] = str(relatorios_path)
    config["empresa"]["apelido"] = apelido
    with open(config_path, "w") as config_file:
        config.write(config_file)
