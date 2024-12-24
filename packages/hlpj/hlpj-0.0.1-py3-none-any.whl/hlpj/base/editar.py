from ..locacao.val_locacoes import val_locacoes
from .config import JournalConfig, JournalPaths
from .helpers import open_editor


def editar_recorrente_pagar(
    journal_paths: JournalPaths, config_paths: JournalConfig
) -> None:
    config_paths
    open_editor(journal_paths.recorr_pgmto_file)


def editar_recorrente_receber(
    journal_paths: JournalPaths, config_paths: JournalConfig
) -> None:
    config_paths
    open_editor(journal_paths.locacoes_file)

    try:
        val_locacoes(journal_paths, config_paths)
    except ValueError as e:
        print(e.args[0])
        input("Aperte enter para continuar")


def editar_conciliacao(journal_paths: JournalPaths, config: JournalConfig):
    config
    open_editor(journal_paths.conciliacao_file)


def editar_info(journal_paths: JournalPaths, config: JournalConfig):
    config
    open_editor(journal_paths.info_file)
