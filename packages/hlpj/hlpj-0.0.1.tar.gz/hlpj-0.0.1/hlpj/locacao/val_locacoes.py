import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, ValidationError, parse_obj_as, root_validator, validator

from ..base import helpers
from ..base.config import JournalConfig, JournalPaths
from ..financeiro.conciliacao import get_imovel_principal

FILE = "/home/eduardo/temp/pulsar/locacoes.ini"


def get_model(imoveis_list: List[str], accts_list: List[str]):
    re_conta = re.compile("^Receita|^Despesa")

    class Cp(BaseModel):
        class Config:
            extra = "allow"

        locatario: str
        status: str
        grupo: str
        dia_vencimento: str
        inicio_contrato: str
        final_contrato: str
        imovel: str
        endereco: str
        cnpj: str
        email: str
        contato: str
        reajuste: str
        garantia: str
        observacao: str
        alerta: str
        desp_atual: str
        conta_banco: str

        @root_validator(allow_reuse=True)
        def tem_virgula(cls, values: Dict[str, str]):
            props: Dict[str, str] = cls.schema()["properties"].keys()
            com_virgula = {
                key
                for key, value in values.items()
                if key in props and re.search(",", value)
            }
            if len(com_virgula) > 0:
                raise (ValueError(f"Proibido virgula nos campos {com_virgula}"))
            return values

        @root_validator(allow_reuse=True)
        def valor_contas(cls, values: Dict[str, str]):
            error_msg = 'Seguir formato valor, categoria, competencia para contas de "Receita" e "Despesa"'
            props: Dict[str, str] = cls.schema()["properties"].keys()
            contas_list = {
                key: value
                for key, value in values.items()
                if re.sub(r"^\d+", "", key) not in props
            }
            for value in contas_list.values():
                splitted = value.split(",", 2)
                if len(splitted) != 3:
                    raise ValueError(error_msg)
                try:
                    float(splitted[0])
                    int(splitted[2])
                except ValueError:
                    raise ValueError(error_msg)

            return values

        @validator("dia_vencimento", allow_reuse=True)
        def dia_valido(cls, v):
            if v[0] == "0":
                raise ValueError("Não pode zero a esquerda")
            try:
                dia_vencimento = int(v)
            except (SyntaxError, ValueError):
                raise ValueError(f"Erro")
            if not 1 <= dia_vencimento <= 31:
                raise ValueError(f"Deve estar entre 1 e 31")

            return v

        @validator("inicio_contrato", "final_contrato", allow_reuse=True)
        def data_valida(cls, v):
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Data invalida")
            return v

        @validator("reajuste", allow_reuse=True)
        def reajuste_valido(cls, v):
            if v == "":
                return v
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Data invalida")
            return v

        @validator("imovel", allow_reuse=True)
        def imovel_cadastrado(cls, v):
            if get_imovel_principal(v) not in imoveis_list:
                raise ValueError(f"Imovel não cadastrado")
            return v

        @root_validator(allow_reuse=True)
        def contas_cadastradas(cls, values: Dict[str, str]):
            contas = {conta for conta in values.keys() if re_conta.search(conta)}
            falta_contas = contas.difference(set(accts_list))
            if len(falta_contas) > 0:
                raise ValueError(f"As contas a seguir estão incorretas {falta_contas}")
            return values

    return Cp


def get_error(error):
    nome = error["loc"][1]
    campo = error["loc"][2]
    msg = error["msg"]

    result = f"Contrato: {nome}, Campo:{campo}\n"
    result += f"{msg}\n"
    return result


def is_posting(row: str, props: List[str]):
    match = re.search(r"^\w+", row)
    if not match:
        return False
    result = match.group()
    if result in props:
        return False
    return True


def val_locacoes(journal_paths: JournalPaths, journal_config: JournalConfig):
    imoveis_str = Path(journal_config.nome_imoveis_file).read_text()
    imoveis_list = imoveis_str.split("\n")

    journal_path = Path(journal_paths.txns_dir).joinpath(
        f"{journal_config.ano}.journal"
    )
    accts_str = helpers.hledger_file(str(journal_path), ["accounts", "--declared"])
    accts_list = accts_str.split("\n")
    Cp = get_model(imoveis_list, accts_list)
    props = Cp.schema()["properties"].keys()

    locacao_str = ""
    with open(journal_paths.locacoes_file, "r") as locacao_file:
        for uid, row in enumerate(locacao_file):
            if is_posting(row, props):
                locacao_str += str(uid) + row
            else:
                locacao_str += row
            uid += 1

    locacoes_ini = helpers.ini_parser()
    locacoes_ini.read_string(locacao_str)
    contratos = {
        nome: dict(contrato)
        for nome, contrato in locacoes_ini.items()
        if len(contrato.keys()) > 0
    }

    try:
        parse_obj_as(Dict[str, Cp], contratos)
    except ValidationError as e:
        error_list = [get_error(error) for error in e.errors()]
        error_str = "\n".join(error_list)
        raise ValueError(error_str)


if __name__ == "__main__":
    from ..base import config

    base_dir = "/home/eduardo/temp/pulsar"

    val_locacoes(config.get_journal_paths(base_dir), config.get_config(base_dir))
