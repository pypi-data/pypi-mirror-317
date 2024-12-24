import os
from pathlib import Path
from sys import argv

from ..base import config
from .add_txn import add_txns


def main():
    base_dir = str(Path(argv[2]).expanduser().parent.parent)
    journal_path = config.get_journal_paths(base_dir)
    journal_config = config.get_config(base_dir)

    try:
        add_txns(journal_path, journal_config)
    except ValueError:
        pass
    finally:
        os.system("clear")


if __name__ == "__main__":
    main()
