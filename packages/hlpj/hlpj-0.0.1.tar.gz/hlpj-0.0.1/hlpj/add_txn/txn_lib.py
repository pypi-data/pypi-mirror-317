import csv
from collections import Counter
from io import StringIO
from pathlib import Path
from typing import Any, List, Set

from ..base import helpers


def get_present(completo: str, field: str, query: List[str]):
    comm_present = ["print", *query, "--output-format=csv"]
    txns_present = helpers.hledger_file(completo, comm_present)
    txns_present_csv = csv.DictReader(StringIO(txns_present))

    field_list = [txn[field] for txn in txns_present_csv]
    fields_counter = Counter(field_list).most_common()
    fields_list = [field[0] for field in fields_counter]
    return fields_list


def get_note(desc: str):
    desc_splitted = desc.split("|", 2)
    if len(desc_splitted) == 1:
        return desc_splitted[0]
    else:
        return desc_splitted[1].strip()


def sort_notes(completo: str, payee: str):
    if payee == "":
        return [""]

    desc_present = get_present(completo, "description", [f"payee:{payee}"])
    notes_present = [get_note(desc) for desc in desc_present]

    desc_all = helpers.hledger_file(completo, ["notes", "not:desc:#closing#"]).split(
        "\n"
    )
    notes_all = [get_note(desc) for desc in desc_all]

    notes_not_present = [note for note in notes_all if note not in notes_present]
    notes_sorted = [*notes_present, *notes_not_present]
    return notes_sorted


def sort_accts(completo: str, payee: str, note: str, used: Set[str]):
    comm = []
    if payee != "":
        comm.append(f"payee:{payee}")
    if note != "":
        comm.append(f"note:{note}")

    accts_present = get_present(completo, "account", comm)
    accts_present = [acct for acct in accts_present if acct not in used]

    accts_all = helpers.hledger_file(completo, ["accounts", "--declared"]).split("\n")
    accts_not_present = [acct for acct in accts_all if acct not in accts_present]

    accts_sorted = [*accts_present, *accts_not_present]
    return accts_sorted


def is_float(n: Any):
    try:
        float(n)
        return True
    except ValueError:
        return False


def get_accts_declared(txns_dir: str, ano: str):
    journal_path = Path(txns_dir).joinpath(f"{ano}.journal")
    accts_declared = helpers.hledger_file(
        str(journal_path), ["accounts", "--declared"]
    ).split("\n")
    accts_declared = [
        acct
        for acct in accts_declared
        if acct == "Duvida"
        or acct.count(":") >= 2
        or (acct.startswith("Receita") and acct.count(":") == 1)
    ]
    result = [*accts_declared, "Duvida"]
    return result
