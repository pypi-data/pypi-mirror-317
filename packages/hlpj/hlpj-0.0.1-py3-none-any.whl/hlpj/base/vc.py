import os
import subprocess
from pathlib import Path

import questionary


def repo_init(dir_str: str):
    subprocess.run(["git", "init"], check=True, cwd=dir_str)
    Path(dir_str).joinpath(".gitignore").write_text("*.log\n*~\n")


def commit_change(dir_str: str):
    if Path(dir_str).joinpath(".git").exists() is False:
        questionary.print(
            "\nNão existe repositorio iniciado.\n", style="bold italic fg:red"
        )
        return

    status_proc = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, check=True, cwd=dir_str
    )

    if status_proc.stdout.decode() == "":
        return

    user = os.environ["HL_USER"]
    add_proc = subprocess.run(["git", "add", "-A"], cwd=dir_str)
    if add_proc.returncode != 0:
        print('Erro "add to git": ' + add_proc.stderr.decode())
        return

    commit_proc = subprocess.run(
        [
            "git",
            "commit",
            "-m",
            f"Automatic commit by {user}",
        ],
        capture_output=True,
        cwd=dir_str,
    )
    if commit_proc.returncode != 0:
        print('Erro "commit git": ' + commit_proc.stderr.decode())
        return

    print(f"Edição realizado por {user} salva no histórico.")
