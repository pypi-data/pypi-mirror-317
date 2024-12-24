import argparse

from .base import config
from .gestao.info import get_info
from .menu import load_app


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-dir", "-b", type=str, help="base directory", required=False)
    ap.add_argument(
        "--new-company",
        "-n",
        action="store_true",
        help="New company in directory base-dir",
    )
    ap.add_argument(
        "--aux",
        "-a",
        action="store_true",
        help="Aux version",
    )
    ap.add_argument(
        "--info",
        "-i",
        action="store_true",
        help="get info",
    )
    args = ap.parse_args()

    if args.new_company:
        config.new_company()
        return

    journal_paths = config.get_journal_paths(args.base_dir)
    journal_config = config.get_config(args.base_dir)

    if args.info:
        get_info(journal_paths, journal_config)
        return

    tipo = "aux" if args.aux else "regular"
    load_app(journal_paths, journal_config, tipo)


if __name__ == "__main__":
    main()
