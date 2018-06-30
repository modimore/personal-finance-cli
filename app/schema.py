from breezeblocks import Table

t_accounts = Table("Accounts", [
    "id", "name", "balance"
])

t_categories = Table("Categories", [
    "id", "name"
])

t_second_parties = Table("SecondParties", [
    "id", "default_category_id", "name"
])

t_second_party_aliases = Table("SecondPartyAliases", [
    "second_party_id", "alias"
])

t_transactions = Table("Transactions", [
    "id",
    "account_id",
    "category_id",
    "other_party_id",
    "amount",
    "description",
    "time"
])
