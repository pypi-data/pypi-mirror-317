import os
import sys
import traceback
from typing import Callable, List

from questionary import Choice, Separator, select

from .add_txn import add_txn
from .airbnb import airbnb_import, airbnb_transf, desp_apto
from .base import editar, vc
from .base.config import JournalConfig, JournalPaths
from .base.helpers import intro, underline
from .contab import contab
from .financeiro import add_conciliacao, recorr_cp, relatorios, transacoes
from .gestao import controle, info
from .locacao import eventos, fatura, recorr_cr


def sair(journal_path, config_path):
    journal_path
    config_path
    raise SystemExit


choices = [
    Separator(underline("Transacoes")),
    Choice("Ano corrente", transacoes.ui_ano_corrente),
    Choice("Ano especifico", transacoes.ui_ano_especifico),
    Choice("Adicionar transacao", add_txn.add_txns),
    Choice("Filtro", transacoes.ui_filter),
    Choice("Atualizar Despesa Imovel", transacoes.update_desp_imovel),
    Choice("Plano de Contas", transacoes.show_plano_contas),
    Choice("Editar conciliacao", editar.editar_conciliacao),
    Choice("Adicionar conciliacao", add_conciliacao.add_conciliacao),
    Choice("Relatorios - Mensal", relatorios.choose_relatorio),
    Separator(underline("Pagar Recorrente")),
    Choice("Editar recorrente", editar.editar_recorrente_pagar),
    Choice("Gerar", recorr_cp.salva_recorrentes_pagar),
    Separator(underline("Locacao")),
    Choice("Editar recorrente", editar.editar_recorrente_receber),
    Choice("Gera recorrente", recorr_cr.salva_recorrentes_receber),
    Choice("Gerar Faturas", fatura.gera_faturas),
    Choice("Gerar Faturas Atrasadas", fatura.gera_atrasados),
    Choice("Eventos", eventos.show_events),
    Choice("Imovel por grupo", recorr_cr.get_imovel_grupo),
    Separator(underline("Airbnb")),
    Choice("Importar reservas", airbnb_import.import_reservas),
    Choice("Consulta transferencias confirmadas", airbnb_transf.transferido_airbnb_mes),
    Choice("Compensação de Despesas - aptos", desp_apto.desp_apto),
    Separator(underline("Contabilidade")),
    Choice("Exportar", contab.get_contab),
    Choice("Editar Codigos", contab.editar_codigos),
    Choice("Controle", controle.get_controle),
    Choice("Editar info", editar.editar_info),
    Choice("Info", info.get_info, shortcut_key="l"),
    Separator(" \n "),
    Choice("sair", sair, shortcut_key="q"),
]

choices_aux = [
    Choice("Editar conciliacao", editar.editar_conciliacao),
    Choice("Relatorios - Mensal", relatorios.choose_relatorio),
    Choice("Editar recorrente pagar", editar.editar_recorrente_pagar),
    Choice("Editar recorrente receber", editar.editar_recorrente_receber),
    Choice("Atualizar Despesa Imovel", transacoes.update_desp_imovel),
    Choice("Imovel por grupo", recorr_cr.get_imovel_grupo),
    Choice("Gerar Faturas", fatura.gera_faturas),
    Choice("Importar reservas", airbnb_import.import_reservas),
    Choice("sair", sair, shortcut_key="q"),
]


def load_app(journal_paths: JournalPaths, journal_config: JournalConfig, tipo: str):
    while True:
        os.system("clear")
        print(intro(journal_config.locador))

        if tipo == "regular":
            menu(choices, journal_paths, journal_config)  # choices outer scope
        elif tipo == "aux":
            menu(choices_aux, journal_paths, journal_config)  # choices outer scope
        vc.commit_change(journal_paths.base_dir)
        input("Digite tecla para continuar")


def menu(
    choices: List[Choice],
    journal_paths: JournalPaths,
    config_info: JournalConfig,
) -> None:
    choice: Callable = select(
        "Escolha opção", choices=choices, use_shortcuts=True, use_jk_keys=False
    ).ask()
    try:
        choice(journal_paths, config_info)
    except SystemExit:
        sys.exit()
    except:
        print(traceback.format_exc())
        input("Opção inválida. Aperte enter para continuar")
