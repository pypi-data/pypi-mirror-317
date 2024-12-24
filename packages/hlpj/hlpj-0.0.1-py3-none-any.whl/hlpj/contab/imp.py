import re
from datetime import date
from io import StringIO
from typing import Union, cast

import pandas as pd
from dateutil.relativedelta import relativedelta
from tabulate import tabulate

from ..base import helpers


def to_float(ser: pd.Series):
    ser_float: pd.Series = ser.str.replace(r"\$|,", "", regex=True).astype(float) * -1
    return ser_float


def castdf(df):
    return cast(pd.DataFrame, df)


def df2table(df: Union[pd.DataFrame, pd.Series]):
    if type(df) is pd.Series:
        df.name = "Valor"
        df = df.to_frame()

    table = tabulate(
        df,  # pyright: ignore
        headers="keys",
        floatfmt=",.2f",
        numalign="right",
        tablefmt="github",  # pyright: ignore
    )
    return table


def adjust_index(df: pd.DataFrame):
    new_index = [re.sub(".+:", "", i) for i in df.index.to_list()]

    dfa = df.copy().set_axis(new_index, axis=0)
    dfa.index.name = "Receita"
    return dfa


def get_tables(
    name: str, df_receita: pd.DataFrame, df_imp: Union[pd.DataFrame, pd.Series]
):
    result = helpers.underline(name) + "\n\n"
    result += df2table(df_receita) + "\n\n\n"
    result += df2table(df_imp) + "\n\n"
    return result


def get_receitas(txns_str: str, begin: date, end: date):
    begin_str = begin.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")

    flags = [
        "bal",
        "^Receita:",
        "not:desc:#closing#",
        "--unmarked",
        "--begin",
        begin_str,
        "--end",
        end_str,
        "--no-total",
        "--row-total",
        "-M",
        "--output-format=csv",
    ]
    receitas_str = helpers.hledger_stdin(txns_str, flags)
    df = castdf(pd.read_csv(StringIO(receitas_str), index_col="account"))
    df = castdf(pd.read_csv(StringIO(receitas_str), index_col="account"))
    df = castdf(df.apply(to_float, axis=1)).abs()

    return df


def get_irrf(txns_str: str, begin: date, end: date):
    begin_str = begin.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")

    flags = [
        "bal",
        "^Despesa:Imposto:Geral:IRRF",
        "not:desc:#closing#",
        "--unmarked",
        "--begin",
        begin_str,
        "--end",
        end_str,
        "--no-total",
        "--row-total",
        "-M",
        "--output-format=csv",
    ]

    irrf_str = helpers.hledger_stdin(txns_str, flags)
    df = (
        castdf(pd.read_csv(StringIO(irrf_str), index_col="account"))
        .apply(to_float, axis=1)
        .abs()
    )
    total: float = df.total.sum()
    return total


def get_mensal(txns_str: str, data_base: date):
    begin = date(data_base.year, data_base.month, 1)
    end = begin + relativedelta(months=1)

    df_receita = get_receitas(txns_str, begin, end)
    df_receita.loc["Receita:Locacao", "Base (%)"] = 100
    df_receita.loc["Receita:Venda de Imovel", "Base (%)"] = 100
    df_receita = df_receita.fillna(0)
    df_receita["Base de Calculo"] = df_receita.total * df_receita["Base (%)"] / 100
    df_receita.loc["total"] = df_receita.sum()
    df_receita.loc["total", "Base (%)"] = None
    df_receita = adjust_index(df_receita)

    base_total: float = df_receita.loc["total", "Base de Calculo"]  # pyright: ignore
    pis = base_total * 0.0065
    cofins = base_total * 0.03

    imp_mensal = {
        "Base de Calculo": base_total,
        "PIS (0.65%)": pis,
        "COFINS (3.00%)": cofins,
    }
    serie_mensal = pd.Series(imp_mensal)
    result = get_tables("Impostos Mensais", df_receita, serie_mensal)
    return result


def get_irpj(txns_str: str, data_base: date):
    begin = date(data_base.year, data_base.month, 1)
    end = begin + relativedelta(months=1)
    begin_tri = end - relativedelta(months=3)

    df_receita = get_receitas(txns_str, begin_tri, end)
    df_receita.loc["Receita:Locacao", "Base (%)"] = 32
    df_receita.loc["Receita:Financeira", "Base (%)"] = 100
    df_receita.loc["Receita:Venda de Imovel", "Base (%)"] = 8
    df_receita = df_receita.fillna(0)
    df_receita["Base de Calculo"] = df_receita.total * df_receita["Base (%)"] / 100
    df_receita.loc["total"] = df_receita.sum()
    df_receita.loc["total", "Base (%)"] = None
    df_receita = adjust_index(df_receita)

    base_total: float = df_receita.loc["total", "Base de Calculo"]  # pyright: ignore
    base_adicional = max(base_total - 60000, 0)
    irpj = base_total * 0.15
    ir_adic = base_adicional * 0.1
    irpj_total = irpj + ir_adic
    irrf = get_irrf(txns_str, begin_tri, end)

    imp_irpj = {
        "Base de Calculo": base_total,
        "Base Adicional": base_adicional,
        "IRPJ (15%)": irpj,
        "Adic IRPJ (10%)": ir_adic,
        "IRRF": -irrf,
        "IRPJ Total": irpj_total - irrf,
    }
    df_irpj = pd.Series(imp_irpj)
    result = get_tables("IRPJ", df_receita, df_irpj)
    return result


def get_csll(txns_str: str, data_base: date):
    begin = date(data_base.year, data_base.month, 1)
    end = begin + relativedelta(months=1)
    begin_tri = end - relativedelta(months=3)

    df_receita = get_receitas(txns_str, begin_tri, end)
    df_receita.loc["Receita:Locacao", "Base (%)"] = 32
    df_receita.loc["Receita:Financeira", "Base (%)"] = 100
    df_receita.loc["Receita:Venda de Imovel", "Base (%)"] = 12
    df_receita = df_receita.fillna(0)
    df_receita["Base de Calculo"] = df_receita.total * df_receita["Base (%)"] / 100
    df_receita.loc["total"] = df_receita.sum()
    df_receita.loc["total", "Base (%)"] = None
    df_receita = adjust_index(df_receita)

    base_total: float = df_receita.loc["total", "Base de Calculo"]  # pyright: ignore

    imp_csll = {"Base de Calculo": base_total, "CSLL (9%)": base_total * 0.09}
    df_csll = pd.Series(imp_csll)
    result = get_tables("CSLL", df_receita, df_csll)
    return result
