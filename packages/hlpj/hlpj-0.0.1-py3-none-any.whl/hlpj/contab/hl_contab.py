import csv
import json
from datetime import datetime
from io import StringIO
from typing import Dict, List, Literal, Tuple, TypedDict, Union

from ..base import helpers
from ..base.hledger_types import HledgerTxn, Tposting


class ValorConta(TypedDict):
    conta: str
    valor: float
    tipo: Union[Literal["debito"], Literal["credito"]]


class Contab(TypedDict):
    valor: float
    debito: str
    credito: str


def posting2valor_conta(posting: Tposting, accts: Dict[str, str]) -> ValorConta:
    acct_name = posting["paccount"].lower()
    acct_code = accts[acct_name]
    valor_str = posting["pamount"][0]["aquantity"]["floatingPoint"]
    valor = float(valor_str)
    tipo = "debito" if valor >= 0 else "credito"
    valor_abs = abs(valor)
    result = ValorConta(conta=acct_code, valor=valor_abs, tipo=tipo)
    return result


def valores_conta2contab(valores_conta: List[ValorConta]) -> List[Contab]:
    # Prepara dados
    valores_conta.sort(
        key=lambda valor_conta: valor_conta["valor"],
        reverse=True,
    )
    debitos = [
        valor_conta for valor_conta in valores_conta if valor_conta["tipo"] == "debito"
    ]
    creditos = [
        valor_conta for valor_conta in valores_conta if valor_conta["tipo"] == "credito"
    ]

    # Testa
    debitos_sum = sum([debito["valor"] for debito in debitos])
    creditos_sum = sum([credito["valor"] for credito in creditos])
    assert round(debitos_sum, 2) == round(
        creditos_sum, 2
    ), f"Soma de debitos e creditos diferente:\n{valores_conta}"

    # Loop
    id = 0
    ic = 0
    ld = len(debitos)
    lc = len(creditos)
    result: List[Contab] = []

    while id < ld and ic < lc:
        valor_debito = debitos[id]["valor"]
        valor_credito = creditos[ic]["valor"]
        conta_debito = debitos[id]["conta"]
        conta_credito = creditos[ic]["conta"]

        if valor_debito > valor_credito:
            contab = Contab(
                valor=valor_credito,
                debito=conta_debito,
                credito=conta_credito,
            )
            result.append(contab)
            debitos[id]["valor"] = valor_debito - valor_credito
            ic += 1
        elif valor_debito < valor_credito:
            contab = Contab(
                valor=valor_debito,
                debito=conta_debito,
                credito=conta_credito,
            )
            result.append(contab)
            creditos[ic]["valor"] = valor_credito - valor_debito
            id += 1
        else:
            contab = Contab(
                valor=valor_debito,
                debito=conta_debito,
                credito=conta_credito,
            )
            result.append(contab)
            ic += 1
            id += 1

    result_sum = sum([item["valor"] for item in result])
    assert round(result_sum, 2) == round(
        debitos_sum, 2
    ), "soma debitos diferente de resultado"
    assert round(result_sum, 2) == round(
        creditos_sum, 2
    ), "soma debitos diferente de resultado"
    return result


def desc2complemento(description: str) -> str:
    if description.find("|") > -1:
        desc_split = description.split("|", 1)
        pessoa = desc_split[0].strip()[:25]
        complemento = desc_split[1].strip()[:150] + f" De/Para:{pessoa}"
    else:
        complemento = description[:180]

    complemento = complemento.ljust(200, " ")
    return complemento


def get_float_string_comma(value: float):
    value_str_prec = f"{value:.2f}"
    value_str = value_str_prec.replace(".", ",")
    return value_str


def txn2contab(txn: HledgerTxn, accts: Dict[str, str]) -> List[Tuple[str, ...]]:
    data_str = datetime.strptime(txn["tdate"], "%Y-%m-%d").strftime("%d/%m/%Y")
    complemento = desc2complemento(txn["tdescription"])

    valores_conta = [
        posting2valor_conta(posting, accts) for posting in txn["tpostings"]
    ]
    valores_contab = valores_conta2contab(valores_conta)

    result = [
        (
            "EXTRATO BANCARIO",
            data_str,
            get_float_string_comma(valor_contab["valor"]),
            valor_contab["debito"],
            valor_contab["credito"],
            complemento,
        )
        for valor_contab in valores_contab
    ]
    return result


def hl2contab(
    journal_path: str, accts: Dict[str, str], inicio_str: str, final_str: str
) -> str:
    hl = helpers.hledger_file(
        journal_path,
        [
            "print",
            "not:desc:#closing#",
            "--unmarked",
            "--real",
            "-b",
            inicio_str,
            "-e",
            final_str,
            "--output-format=json",
        ],
    )
    txns = json.load(StringIO(hl))
    contab_list_list = [txn2contab(txn, accts) for txn in txns]
    contab_list = [txn for txn_list in contab_list_list for txn in txn_list]
    header = ["tipo", "data", "valor", "debito", "credito", "historico"]
    contab_io = StringIO()
    contab_csv = csv.writer(contab_io)
    contab_csv.writerow(header)
    contab_csv.writerows(contab_list)
    contab_io.seek(0)
    contab = contab_io.read()

    return contab
