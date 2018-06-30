import csv
from datetime import datetime
from breezeblocks.sql import Value
from fuzzywuzzy import process as fuzz_process
from .database import db
from .schema import t_accounts, t_transactions
from .sql import q_account_for_name, q_second_parties, q_second_party_aliases

match_ratio_min = 50

i_transactions = db.insert(t_transactions)\
    .add_columns("account_id", "category_id", "other_party_id", "amount", "description", "time")\
    .get()

def build_transaction_chase(csv_row, account_id, second_parties):
    best_second_party_name = fuzz_process.extractOne(csv_row["Description"], second_parties.keys())
    if best_second_party_name[1] > match_ratio_min:
        best_second_party = second_parties[best_second_party_name[0]]
        second_party_id, category_id = best_second_party.id, best_second_party.default_category_id
    else:
        second_party_id, category_id = None, None
    return (
        account_id,
        category_id,
        second_party_id,
        float(csv_row["Amount"]),
        csv_row["Description"],
        datetime.strptime(csv_row["Posting Date"], "%m/%d/%Y")
    )

def build_transaction_bss(csv_row, account_id, second_parties):
    amount = csv_row["Amount"].replace("(", "-").replace(")", "").replace(",", "").replace("$", "")
    best_second_party_name = fuzz_process.extractOne(csv_row["Description"], second_parties.keys())
    if best_second_party_name[1] > match_ratio_min:
        best_second_party = second_parties[best_second_party_name[0]]
        second_party_id, category_id = best_second_party.id, best_second_party.default_category_id
    else:
        second_party_id, category_id = None, None
    return (
        account_id,
        category_id,
        second_party_id,
        float(amount),
        csv_row["Description"],
        datetime.strptime(csv_row["Date"], "%m/%d/%Y")
    )

def import_transactions(account_id, csvfilename, build_transaction):
    second_parties = { r.alias : r for r in q_second_party_aliases.execute() }
    transactions = []
    with open(csvfilename, "r") as csvfile:
        for row in csv.DictReader(csvfile):
            transactions.append(build_transaction(row, account_id, second_parties))
    
    i_transactions.execute(transactions)

def import_chase(account_id, csvfilename):
    import_transactions(account_id, csvfilename, build_transaction_chase)

def import_bss(account_id, csvfilename):
    import_transactions(account_id, csvfilename, build_transaction_bss)
