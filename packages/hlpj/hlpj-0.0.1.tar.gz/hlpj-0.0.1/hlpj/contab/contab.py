import configparser
import csv
from concurrent.futures import ProcessPoolExecutor
from datetime import date, datetime
from io import StringIO
from pathlib import Path
from tempfile import NamedTemporaryFile
from time import perf_counter
from typing import Dict

import pandas as pd
import questionary
from dateutil.relativedelta import relativedelta
from openpyxl import Workbook

from hlpj.base.webdav import WebDav

from ..base import helpers
from ..base.config import JournalConfig, JournalPaths
from .hl_contab import hl2contab
from .imp import get_csll, get_irpj, get_mensal

DATE_FORMAT = "%Y-%m-%d"
MESES_ANTERIOR = 1


class ValContab:
    def __init__(self, codigos_file: str, journal_file: str, data_base: date) -> None:
        self.codigos_file = codigos_file
        self.journal_file = journal_file
        self.month = f"{data_base.year}-{data_base.month}"
        self.sorted_codes = self._sort_codes()

        self.ok = (
            self.codes_dup_error() and self.codes_empty() and self.codes_missing_error()
        )

    def _fix_error(self, msg: str):
        print(msg)
        confirma = questionary.confirm("Deseja editar codigos").ask()
        if confirma:
            helpers.open_editor(self.codigos_file)

    def _sort_codes(self) -> Dict[str, str]:
        codigos_parser = configparser.ConfigParser(delimiters=["="])
        codigos_parser.read(Path(self.codigos_file))
        codigos_dict: Dict[str, str] = dict(codigos_parser["codigos"])
        sorted_codigos = dict(sorted(codigos_dict.items()))
        codigos_parser["codigos"].clear()
        for conta, codigo in sorted_codigos.items():
            codigos_parser["codigos"][conta] = codigo

        with open(self.codigos_file, "w") as codigos_file:
            codigos_parser.write(codigos_file)

        return sorted_codigos

    def codes_dup_error(self):
        codigos_parser = configparser.ConfigParser(delimiters=["="])
        try:
            codigos_parser.read(Path(self.codigos_file))
            return True
        except configparser.DuplicateOptionError as e:
            self._fix_error(f"Conta {e.option} duplicada")
            return False

    def codes_empty(self):
        empty_accts = [acct for acct, code in self.sorted_codes.items() if code == ""]
        if len(empty_accts) == 0:
            return True
        else:
            result = helpers.underline("As seguintes contas não tem codigo") + "\n"
            result += "\n".join(empty_accts)
            self._fix_error(result)
            return False

    def codes_missing_error(self):
        journal_accts_commands = [
            "accounts",
            "--used",
            "--unmarked",
            "-p",
            self.month,
            "not:desc:#closing#",
        ]
        journal_accts_str = helpers.hledger_file(
            self.journal_file, journal_accts_commands
        )

        journal_accts_list = journal_accts_str.split("\n")
        journal_accts = [acct for acct in journal_accts_list if acct != ""]
        missing = [
            f"{acct} = "
            for acct in journal_accts
            if acct.lower() not in self.sorted_codes.keys()
        ]

        if len(missing) == 0:
            return True
        else:
            result = (
                helpers.underline("Copie os codigos que faltam das seguintes contas")
                + "\n"
            )
            result += "\n".join(missing)
            self._fix_error(result)
            return False


class Contab:
    def __init__(
        self,
        journal_paths: JournalPaths,
        journal_config: JournalConfig,
        data_base: date,
    ) -> None:
        self.journal_paths = journal_paths
        self.journal_config = journal_config
        self.data_base = data_base
        self.journal_file = f"{journal_paths.txns_dir}/{journal_config.ano}.journal"

        final = data_base + relativedelta(months=1)
        anterior = data_base - relativedelta(months=1)
        trim_inicio = data_base - relativedelta(months=3)
        self.inicio_str = data_base.strftime("%Y-%m-%d")
        self.final_str = final.strftime("%Y-%m-%d")
        self.anterior_str = anterior.strftime("%Y-%m-%d")
        self.trim_inicio = trim_inicio.strftime("%Y-%m-%d")

        self.txns = self._get_txns()
        self.ativo_accts = self._get_ativo_accts()

        apelido = self.journal_config.apelido
        mes = data_base.strftime("%m-%Y")
        relatorios_path = Path(journal_config.relatorios_dir)
        self.report_file = relatorios_path.joinpath(f"resumo_{apelido}_{mes}.pdf")
        self.contab_file = relatorios_path.joinpath(f"{apelido}_{mes}_Lcto.xlsx")
        self.txns_sheet_file = relatorios_path.joinpath(f"txns_{apelido}_mes.xlsx")

    def _get_txns(self):
        directives = """; Defaults
D $1,000.00
commodity $1,000.00

account Ativo              ; type:A
account Passivo            ; type:L
account Receita            ; type:R
account Despesa            ; type:X
account Patrimonio Liquido ;type:E

"""
        comm = [
            "print",
            "not:desc:#closing",
            "--real",
            "--unmarked",
        ]
        txns = helpers.hledger_file(self.journal_paths.journal_all, comm)
        result = directives + txns
        return result

    def _get_ativo_accts(self):
        ativo_cmds = [
            "account",
            "--used",
            "^Ativo:Disponibilidade",
            "--begin",
            self.inicio_str,
            "--end",
            self.final_str,
        ]
        accts_str = helpers.hledger_stdin(self.txns, ativo_cmds)
        accts = accts_str.split("\n")
        return accts

    @property
    def reports_cmd(self):
        base_cmd = [
            "--begin",
            self.anterior_str,
            "--end",
            self.final_str,
            "--monthly",
            "--tree",
            "--no-elide",
        ]

        cmds_specific = [
            ["bs", "--historical"],
            ["bse", "--change"],
            ["is"],
            ["bal", "^Receita:", "--invert", "--pivot", "payee"],
        ]
        cmds = [[*cmd, *base_cmd] for cmd in cmds_specific]
        return cmds

    @property
    def txns_reg_cmd(self):
        cmds = {
            ativo_acct: [
                "register",
                "not:desc:#closing#",
                ativo_acct,
                "--unmarked",
                "--real",
                "--forecast",
                "--related",
                "--invert",
                "--historical",
                "--begin",
                self.inicio_str,
                "--end",
                self.final_str,
                "--output-format=csv",
            ]
            for ativo_acct in self.ativo_accts
            if ativo_acct != ""
        }
        return cmds

    @staticmethod
    def get_workbook(txns_reg: Dict[str, str]):
        wb = Workbook(write_only=True)
        for ativo_acct, txn_reg in txns_reg.items():
            ws_name = ativo_acct.replace(":", ".")[-30:]
            ws = wb.create_sheet(title=ws_name)
            reg_csv = csv.reader(StringIO(txn_reg))
            next(reg_csv)
            ws.append(["data", "descricao", "outra conta", "valor", "saldo"])
            for reg in reg_csv:
                row = [
                    datetime.strptime(reg[1], "%Y-%m-%d").date(),
                    reg[3],
                    reg[4],
                    float(reg[5].replace("$", "").replace(",", "")),
                    float(reg[6].replace("$", "").replace(",", "")),
                ]
                ws.append(row)
        return wb

    def save_reports(self):
        val_contab = ValContab(
            self.journal_paths.codigos_file,
            self.journal_file,
            self.data_base,
        )
        if not val_contab.ok:
            return

        dav = WebDav(self.journal_config.dav_options)
        with ProcessPoolExecutor() as p:
            contab_data_fut = p.submit(
                hl2contab,
                journal_path=self.journal_file,
                accts=val_contab.sorted_codes,
                inicio_str=self.inicio_str,
                final_str=self.final_str,
            )

            reports_fut = [
                p.submit(helpers.hledger_stdin, self.txns, report_cmd)
                for report_cmd in self.reports_cmd
            ]

            impostos_fut = [p.submit(get_mensal, self.txns, self.data_base)]
            if self.data_base.month % 3 == 0:
                impostos_fut.append(p.submit(get_irpj, self.txns, self.data_base))
                impostos_fut.append(p.submit(get_csll, self.txns, self.data_base))

            txns_reg_fut = {
                acct: p.submit(helpers.hledger_stdin, self.txns, txn_reg)
                for acct, txn_reg in self.txns_reg_cmd.items()
            }

        reports = [report_fut.result() for report_fut in reports_fut]
        impostos = [imposto_fut.result() for imposto_fut in impostos_fut]
        if self.data_base.month % 3 != 0:
            impostos.append("Não há impostos trimestrais esse mes\n\n")

        reports_str = "\n".join(reports) + "\n"
        impostos_str = "\n\n".join(impostos)
        report = reports_str + impostos_str

        txns_reg = {
            acct: txn_reg_fut.result() for acct, txn_reg_fut in txns_reg_fut.items()
        }
        wb = self.get_workbook(txns_reg)

        contab_data = contab_data_fut.result()
        with NamedTemporaryFile("wb+", suffix=".xlsx") as f:
            df = pd.read_csv(StringIO(contab_data))
            df.to_excel(f.name, index=False)
            f.seek(0)
            dav.upload_file(f.name, str(self.contab_file))

        helpers.print_pdf(report, dav, str(self.report_file))
        with NamedTemporaryFile("wb+", suffix=".xlsx") as f:
            wb.save(f.name)
            f.seek(0)
            dav.upload_file(f.name, str(self.txns_sheet_file))

        files_saved = [
            str(self.contab_file),
            str(self.report_file),
            str(self.txns_sheet_file),
        ]
        files_saved_str = "\n".join(files_saved)
        print(report)
        print(f"Arquivos salvos:\n{files_saved_str}")


def get_contab(journal_paths: JournalPaths, journal_config: JournalConfig):
    month_ago = date.today() - relativedelta(months=1)
    data_base = helpers.get_date(month_ago.year, month_ago.month)

    start = perf_counter()
    cont = Contab(journal_paths, journal_config, data_base)
    cont.save_reports()
    duration = round(perf_counter() - start, 2)
    print(f"Em {duration} segundos")


def editar_codigos(journal_paths: JournalPaths, config: JournalConfig):
    config
    helpers.open_editor(journal_paths.codigos_file)
