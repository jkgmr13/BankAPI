
# exception used for when a withdraw or transfer without proper access to the account.

class AccountOwnershipError(Exception):
    pass
