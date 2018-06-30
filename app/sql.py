from breezeblocks.sql import Value
from breezeblocks.sql.aggregates import Sum_
from breezeblocks.sql.join import LeftJoin as Join
from .database import db
from .schema import *

jn_transactions_account_category = Join(Join(t_transactions, t_accounts,
    on=[t_transactions.columns["account_id"] == t_accounts.columns["id"]]),
    t_categories, on=[t_transactions.columns["category_id"] == t_categories.columns["id"]])
jn_second_party_to_aliases = Join(t_second_parties, t_second_party_aliases,
    on=[t_second_parties.columns["id"] == t_second_party_aliases.columns["second_party_id"]])

q_accounts = db.query(t_accounts).get()
q_account_for_id = db.query(t_accounts)\
    .where(t_accounts.columns["id"] == Value(None, param_name="id"))\
    .get()
q_account_for_name = db.query(t_accounts)\
    .where(t_accounts.columns["name"] == Value(None, param_name="name"))\
    .get()

q_second_parties = db.query(t_second_parties).get()
q_second_party_aliases = db.query(jn_second_party_to_aliases.left, jn_second_party_to_aliases.right)\
    .get()

q_transactions = db.query(
        jn_transactions_account_category.tables[t_transactions.get_name()],
        jn_transactions_account_category.tables[t_accounts.get_name()]["name"].as_("account_name"),
        jn_transactions_account_category.tables[t_categories.get_name()]["name"].as_("category_name")
    ).order_by(t_transactions.columns["time"], ascending=False).get()
q_transactions_in_range = db.query(
        jn_transactions_account_category.tables[t_transactions.get_name()],
        jn_transactions_account_category.tables[t_accounts.get_name()]["name"].as_("account_name"),
        jn_transactions_account_category.tables[t_categories.get_name()]["name"].as_("category_name"))\
    .where(jn_transactions_account_category.tables[t_transactions.get_name()]["time"] >= Value(None, param_name="start"))\
    .where(jn_transactions_account_category.tables[t_transactions.get_name()]["time"] <= Value(None, param_name="end"))\
    .order_by(t_transactions.columns["time"], ascending=False).get()

q_transaction_summary = db.query(Sum_(t_transactions.columns["amount"]).as_("total")).get()
q_transaction_summary_in_range = db.query(Sum_(t_transactions.columns["amount"]).as_("total"))\
    .where(t_transactions.columns["time"] >= Value(None, param_name="start"))\
    .where(t_transactions.columns["time"] <= Value(None, param_name="end"))\
    .get()

i_accounts = db.insert(t_accounts)\
    .add_columns(t_accounts.columns["name"]).get()
