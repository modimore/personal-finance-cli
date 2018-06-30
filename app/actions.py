from datetime import datetime
from .schema import t_accounts, t_transactions
from .sql import q_account_for_name, q_accounts, q_transactions,\
    q_transactions_in_range, q_transaction_summary, q_transaction_summary_in_range,\
    i_accounts
from .transaction_import import import_bss, import_chase

DATEFORMAT_H = "%m/%d/%Y"
DATEFORMAT_DB = "%Y-%m-%d %H:%M:%S"

def currency_string(amount):
    return "${:.2f}".format(amount).replace("$-", "-$")

def action_accounts(args):
    accounts = q_accounts.execute()
    for account in accounts:
        print("[{0}] {1:>25}: {2:>12}".format(account.id, account.name, currency_string(account.balance)))

def action_accounts_add(args):
    i_accounts.execute([(args.account_name,)])

def action_account(args):
    q_account_for_name.set_param("name", args.account_name)
    accounts = q_account_for_name.execute()
    if len(accounts) < 1:
        print("No account by that name found.")
    else:
        account = accounts[0]
        print("[{0}] {1}: {2}".format(account.id, account.name, currency_string(account.balance)))

def action_transactions(args):
    if args.start is not None:
        args.start = datetime.strptime(args.start, DATEFORMAT_H)
        args.end = datetime.strptime(args.end, DATEFORMAT_H) if args.end is not None else datetime.now()
        q_transactions_in_range.set_param("start", args.start)
        q_transactions_in_range.set_param("end", args.end)
        transactions = q_transactions_in_range.execute()
    else:
        transactions = q_transactions.execute(args.num)
    
    for transaction in transactions:
        print("{0} {1:<25} {2:>12} {3:<15} {4}".format(
            transaction.time.split()[0], transaction.account_name, currency_string(transaction.amount), transaction.category_name if transaction.category_name is not None else "", transaction.description
        ))

def action_transaction_summary(args):
    if args.start is not None:
        args.start = datetime.strptime(args.start, DATEFORMAT_H)
        args.end = datetime.strptime(args.end, DATEFORMAT_H) if args.end is not None else datetime.now()
        q_transaction_summary_in_range.set_param("start", args.start)
        q_transaction_summary_in_range.set_param("end", args.end)
        agg = q_transaction_summary_in_range.execute()[0]
        print("{0}-{1}: {2}".format(
            args.start.date().strftime(DATEFORMAT_H), args.end.date().strftime(DATEFORMAT_H), currency_string(agg.total)))
    else:
        agg = q_transaction_summary.execute()[0]
        print("{}".format(currency_string(agg.total)))

def action_import(args):
    q_account_for_name.set_param("name", args.account_name)
    account = q_account_for_name.execute()[0]
    args.csv_format = args.csv_format.lower()
    if args.csv_format == "chase":
        import_chase(account.id, args.csv_filename)
    elif args.csv_format in ["bss", "boiling springs"]:
        import_bss(account.id, args.csv_filename)

