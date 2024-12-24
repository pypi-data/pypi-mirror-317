import json
import locale
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from io import StringIO
from itertools import groupby
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, List, NamedTuple, Set

import pdfkit
import questionary
from dateutil.relativedelta import relativedelta
from jinja2 import Environment, FileSystemLoader
from jinja2.environment import Template
from tabulate import tabulate

from ..base import helpers
from ..base.config import JournalConfig, JournalPaths
from ..base.hledger_types import HledgerTxn, HledgerTxns, Tposting
from ..base.webdav import WebDav

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
TEMPLATE_PATH = Path(__file__).parent.parent.joinpath("templates")
TCOMMENT_KEYS = {"cnpj", "email", "contato", "endereco"}
PCOMMENT_KEYS = {"categoria", "competencia"}


class FaturaInfo(NamedTuple):
    locatario: str
    imovel: str
    grupo: str
    total: float
    html: str


class PostingData(NamedTuple):
    data: str
    descricao: str
    valor: float
    categoria: str
    competencia: str


class TxnData(NamedTuple):
    now: datetime
    grupo: str
    locatario: str
    descricao: str
    data: datetime
    locador: str
    cnpj: str
    email: str
    contato: str
    endereco: str
    postings: List[PostingData]
    imovel: str


def get_tags_dict(
    pairs: List[List[str]], required_keys: Set[str], data: datetime, descricao: str
) -> Dict[str, str]:
    tags_dict = {pair[0]: pair[1] for pair in pairs}
    found_keys = set(tags_dict.keys())
    missing_keys = required_keys.difference(found_keys)
    assert (
        len(missing_keys) == 0
    ), f"Faltou as categorias {missing_keys} na transacao {data}  {descricao}"
    return tags_dict


def get_posting(posting: Tposting, data: datetime, descricao: str) -> PostingData:
    valor_float_str = posting["pamount"][0]["aquantity"]["floatingPoint"]
    valor_float = float(valor_float_str) * -1
    data_str = data.strftime("%d/%m/%Y")
    ptags = get_tags_dict(posting["ptags"], PCOMMENT_KEYS, data, descricao)
    categoria = ptags["categoria"].strip()
    competencia = ptags["competencia"].strip()
    return PostingData(data_str, descricao, valor_float, categoria, competencia)


def get_txn_data(txn: HledgerTxn, locador: str) -> TxnData:
    now = datetime.today()
    group = next((item[1] for item in txn["ttags"] if item[0] == "grupo"), "0")
    tdescription = txn["tdescription"].split("|", 1)
    locatario = tdescription[0].strip() if len(tdescription) > 1 else ""
    descricao = tdescription[1].strip() if len(tdescription) > 1 else tdescription[0]
    data = datetime.strptime(txn["tdate"], "%Y-%m-%d")
    ttags = get_tags_dict(txn["ttags"], TCOMMENT_KEYS, data, f"Locatario: {locatario}")
    cnpj = ttags["cnpj"].strip()
    email = ttags["email"].strip()
    contato = ttags["contato"].strip()
    endereco = ttags["endereco"].strip()
    imovel = ttags["imovel"].strip()

    postings = [
        get_posting(posting, data, f"Locatario: {locatario}, Imovel: {imovel}")
        for posting in txn["tpostings"]
        if posting["paccount"].startswith("Receita")
        or posting["paccount"].startswith("Despesa")
    ]

    return TxnData(
        now,
        group,
        locatario,
        descricao,
        data,
        locador,
        cnpj,
        email,
        contato,
        endereco,
        postings,
        imovel,
    )


def get_txns(journal: str, data_final_str, locador: str) -> List[TxnData]:
    command = [
        "print",
        "tag:tipo=locacao",
        "Receita|Despesa",
        "-e",
        data_final_str,
        "--pending",
        "--output-format=json",
    ]
    txns_json = helpers.hledger_stdin(journal, command)
    txns_hledger: HledgerTxns = json.load(StringIO(txns_json))
    txns = [get_txn_data(txn, locador) for txn in txns_hledger]
    return txns


def get_sum(postings: List[PostingData]) -> float:
    valores = [posting.valor for posting in postings]
    result = sum(valores)
    return result


def get_vencimento(txns: List[TxnData]):
    now = txns[0].now
    datas = [txn.data for txn in txns]
    last_date = max(datas)
    result = last_date if last_date > now else now + relativedelta(days=1)
    return result


def get_fatura_info(
    template: Template,
    txns: List[TxnData],
    today: str,
    pix: str,
    conta1: str,
    conta2: str,
):
    postings = [postings_txn for txn in txns for postings_txn in txn.postings]
    logo = TEMPLATE_PATH.joinpath("logo.png")
    vencimento = get_vencimento(txns)
    locatario = txns[0].locatario
    imovel = txns[0].imovel
    grupo = txns[0].grupo
    total = get_sum(postings)
    context = dict(
        locador=txns[0].locador,
        locatario=locatario,
        logo=str(logo),
        today=today,
        endereco=txns[0].endereco,
        email=txns[0].email,
        cnpj=txns[0].cnpj,
        contato=txns[0].contato,
        pix=pix,
        conta1=conta1,
        conta2=conta2,
        vencimento=vencimento,
        total=total,
        postings=postings,
    )
    html = template.render(**context)
    fatura_info = FaturaInfo(locatario, imovel, grupo, total, html)
    return fatura_info


def html2pdf(dav: WebDav, html: str, output_path: str):
    pdfkit_options = dict(encoding="utf-8", quiet="", allow=str(TEMPLATE_PATH))
    with NamedTemporaryFile(suffix=".html") as html_file, NamedTemporaryFile(
        suffix=".pdf"
    ) as pdf_file:
        html_file.write(html.encode())
        html_file.seek(0)
        pdfkit.from_file(
            input=html_file.name,
            output_path=pdf_file.name,
            options=pdfkit_options,
        )
        dav.upload_file(pdf_file.name, output_path)
        filename = Path(output_path).name
        print("Salvo arquivo: " + filename)


def get_jinja_template():
    env = Environment(loader=FileSystemLoader(TEMPLATE_PATH), trim_blocks=True)
    env.filters["format_date"] = lambda x: x.strftime("%d/%m/%Y")
    env.filters["format_num"] = lambda x: locale.currency(x, symbol=True, grouping=True)
    template = env.get_template("fatura.jinja2")
    return template


def get_faturas(
    config: JournalConfig,
    txns: List[TxnData],
):
    template = get_jinja_template()
    txns_sorted = sorted(txns, key=lambda txn: (txn.locatario, txn.imovel))

    grouped = groupby(txns_sorted, key=lambda txn: (txn.locatario, txn.imovel))

    today = datetime.now().strftime("%d/%m/%Y")
    faturas = [
        get_fatura_info(
            template,
            list(grouped_txns[1]),
            today,
            config.pix,
            config.conta1,
            config.conta2,
        )
        for grouped_txns in grouped
    ]
    return faturas


def get_grupo(txns: List[TxnData]) -> str:
    grupos = sorted(set([txn.grupo for txn in txns]))
    grupo: str = questionary.select("Escolha o grupo", grupos, use_shortcuts=True).ask()
    return grupo


def save_faturas(
    dav: WebDav,
    config: JournalConfig,
    mes_base: str,
    grupo: str,
    faturas_info: List[FaturaInfo],
):
    dir_leaf = helpers.sanitize_filename(
        f"faturas - mes {mes_base} - grupo {grupo} - {config.apelido}"
    )
    faturas_dir = Path(config.relatorios_dir).joinpath(dir_leaf)

    dav.remove_if_exist(str(faturas_dir))
    dav.client.mkdir(str(faturas_dir))

    with ProcessPoolExecutor() as p:
        for fatura_info in faturas_info:
            filename = helpers.sanitize_filename(
                f"{fatura_info.locatario}_{fatura_info.imovel}  - grupo {fatura_info.grupo}"
            )
            output_path = faturas_dir.joinpath(f"{filename}.pdf")
            dav = WebDav(config.dav_options)
            p.submit(html2pdf, dav, fatura_info.html, str(output_path))


def get_resumo(faturas_info: List[FaturaInfo]):
    headers = ["Locatario", "Imovel", "Total"]
    rows = [
        [
            fatura_info.locatario,
            fatura_info.imovel,
            fatura_info.total,
        ]
        for fatura_info in faturas_info
    ]
    resumo = tabulate(
        rows,
        headers=headers,
        floatfmt=",.2f",
        tablefmt="simple",
    )
    return resumo


def gera_faturas(journal_paths: JournalPaths, config: JournalConfig) -> None:
    # Get data e grupo
    data_base = helpers.get_date()
    mes_base = data_base.strftime("%Y_%m")
    data_final = data_base + relativedelta(months=1)
    data_final_str = data_final.strftime("%Y-%m-%d")

    dav = WebDav(config.dav_options)

    # Get journal
    journal = helpers.join_journal_last(journal_paths.txns_dir, int(config.ano))
    txns = get_txns(journal, data_final_str, config.locador)

    # Filter group
    grupo = get_grupo(txns)
    txns_grupo = [txn for txn in txns if txn.grupo == grupo]

    # Faturas
    print("Obtendo dados...")
    print("template path" + str(TEMPLATE_PATH))
    faturas_info = get_faturas(config, txns_grupo)
    print("Salvando pdfs")

    save_faturas(dav, config, mes_base, grupo, faturas_info)

    # Resumo
    print("Salvando resumo")
    resumo = get_resumo(faturas_info)
    print(helpers.underline("Resumo") + "\n" + resumo)
    today = datetime.today().strftime("%Y%m%d")
    resumo_path = Path(config.relatorios_dir).joinpath(
        f"faturas - mes {mes_base} - grupo {grupo} - gerado {today}.txt"
    )
    dav.upload_txt(resumo, str(resumo_path))
    print("Planilha e Faturas salvas.")


def gera_atrasados(journal_paths: JournalPaths, config: JournalConfig) -> None:
    ontem = datetime.today() - relativedelta(days=1)
    ontem_str = ontem.strftime("%Y-%m-%d")

    dav = WebDav(config.dav_options)

    # Get journal
    journal = helpers.join_journal_last(journal_paths.txns_dir, ontem.year)
    txns = get_txns(journal, ontem_str, config.locador)

    # Faturas
    mes_base = "atrasados"
    grupo = "todos"
    print("Obtendo dados...")

    faturas_info = get_faturas(config, txns)
    print("Salvando pdfs")
    save_faturas(dav, config, mes_base, grupo, faturas_info)

    # Resumo
    print("Salvando resumo")
    resumo = get_resumo(faturas_info)
    print(helpers.underline("Resumo") + "\n" + resumo)
    resumo_path = Path(config.relatorios_dir).joinpath(
        f"faturas - mes {mes_base} - grupo {grupo}.txt"
    )
    dav.upload_txt(resumo, str(resumo_path))
    print("\nPlanilha e Faturas salvas.")
