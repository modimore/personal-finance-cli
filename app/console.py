from argparse import ArgumentParser
from .router import ActionRouter
from .actions import *

def action_missing_action(args):
    print(args)
    print("No such action:", args.cli_action)

main_parser = ArgumentParser()
main_subparsers = main_parser.add_subparsers(dest="cli_action")

accounts_parser = main_subparsers.add_parser("accounts")
accounts_subparsers = accounts_parser.add_subparsers(dest="accounts_action")
accounts_add_parser = accounts_subparsers.add_parser("add")
accounts_add_parser.add_argument("account_name")
account_parser = main_subparsers.add_parser("account")
account_parser.add_argument("account_name")
import_parser = main_subparsers.add_parser("import")
import_parser.add_argument("account_name")
import_parser.add_argument("csv_filename", default="transactions.csv")
import_parser.add_argument("csv_format", default="chase")
transactions_parser = main_subparsers.add_parser("transactions")
transactions_parser.add_argument("-n", "--num", type=int, default=20)
transactions_parser.add_argument("--start", default=None)
transactions_parser.add_argument("--end", default=None)
transactions_subparsers = transactions_parser.add_subparsers(dest="transactions_action")
transactions_summary_parser = transactions_subparsers.add_parser("summary")

router = ActionRouter("cli_action", action_missing_action)
router.register("account", action_account)
accounts_router = router.register_subrouter("accounts", "accounts_action", action_accounts)
accounts_router.register("add", action_accounts_add)
router.register("import", action_import)
transactions_router = router.register_subrouter("transactions", "transactions_action", action_transactions)
transactions_router.register("summary", action_transaction_summary)
