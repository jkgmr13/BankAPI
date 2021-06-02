from Entities.accounts import Account
from daos.account_dao import AccountDao


class AccountDaoLocal(AccountDao):
    id_maker = 0
    account_table = {}

    def create_account(self, account: Account) -> Account:
        AccountDaoLocal.id_maker += 1
        account.account_id = AccountDaoLocal.id_maker
        AccountDaoLocal.account_table[AccountDaoLocal.id_maker] = account
        return AccountDaoLocal.account_table[AccountDaoLocal.id_maker]

    def get_account_by_id(self, account_id: int) -> Account:
        try:
            account = AccountDaoLocal.account_table[account_id]
            return account
        except KeyError:
            return None

    def get_all_accounts(self) -> list[Account]:
        accounts = [account for account in AccountDaoLocal.account_table.values()]
        return accounts

    def update_account(self, account: Account) -> Account:
        AccountDaoLocal.account_table[account.account_id] = account
        return account

    def delete_account_by_id(self, account_id: int) -> bool:
        try:
            del AccountDaoLocal.account_table[account_id]
            return True
        except KeyError:
            return False
