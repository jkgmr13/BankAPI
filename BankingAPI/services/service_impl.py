from Entities.accounts import Account
from Entities.clients import Client
from Exceptions.account_error import AccountOwnershipError
from Exceptions.resource_error import ResourceNotFoundError
from daos.account_dao import AccountDao
from daos.client_dao import ClientDao
from services.service_methods import AccountService


class AccountServiceImpl(AccountService):

    def __init__(self, client_dao: ClientDao, account_dao: AccountDao):
        self.client_dao = client_dao
        self.account_dao = account_dao

    def add_client(self, client: Client) -> Client:
        client = self.client_dao.create_client(client)
        return client

    def add_account(self, account: Account) -> Account:
        if self.client_dao.get_client_by_id(account.client_id):
            account = self.account_dao.create_account(account)
            return account
        else:
            raise ResourceNotFoundError(f"Couldn't find a client with id: {account.client_id}")

    def get_client(self, client_id: int) -> Client:
        client = self.client_dao.get_client_by_id(client_id)
        if client is None:
            raise ResourceNotFoundError(f'could not find client with id: {client_id}')
        else:
            return client

    def get_account(self, account_id: int) -> Account:
        account = self.account_dao.get_account_by_id(account_id)
        if account is None:
            raise ResourceNotFoundError(f'could not find account with id: {account_id}')
        else:
            return account

    def get_all_accounts(self) -> list[Account]:
        accounts = self.account_dao.get_all_accounts()
        if len(accounts) == 0:
            raise ResourceNotFoundError("There are no accounts in Ba Sing Se")
        else:
            return accounts

    def get_all_accounts_by_client(self, client_id: int) -> list[Account]:
        if self.get_client(client_id):
            accounts = self.account_dao.get_all_accounts()
            my_accounts = [account for account in accounts if account.client_id == client_id]
            return my_accounts
        else:
            raise ResourceNotFoundError(f'Could not find client with id: {client_id}')

    def get_all_accounts_lower_balance_bound(self, client_id: int, lower_bound: float) -> list[Account]:
        accounts = self.get_all_accounts_by_client(client_id)
        my_accounts = [account for account in accounts if account.account_balance > lower_bound]
        return my_accounts

    def get_all_accounts_upper_balance_bound(self, client_id: int, upper_bound: float) -> list[Account]:
        accounts = self.get_all_accounts_by_client(client_id)
        my_accounts = [account for account in accounts if account.account_balance < upper_bound]
        return my_accounts

    def get_all_accounts_bounded(self, client_id: int, lower_bound: float, upper_bound: float) -> list[Account]:
        accounts = self.get_all_accounts_by_client(client_id)
        my_accounts = [account for account in accounts if lower_bound <= account.account_balance <= upper_bound]
        return my_accounts

    def get_all_clients(self) -> list[Client]:
        clients = self.client_dao.get_all_clients()
        if len(clients) == 0:
            raise ResourceNotFoundError("There are no clients in Ba Sing Se")
        return clients

    def update_client(self, client: Client) -> Client:
        client = self.client_dao.update_client(client)
        if client is None:
            raise ResourceNotFoundError(f'No such client exists')
        else:
            return client

    def update_account(self, account: Account) -> Account:
        client = self.client_dao.get_client_by_id(account.client_id)
        exist = self.account_dao.get_account_by_id(account.account_id)
        if exist is None:
            raise ResourceNotFoundError(f'No such account exists with id: {account.account_id}')
        if client is None:
            raise ResourceNotFoundError(f'No such client exists with id: {account.client_id}')
        account = self.account_dao.update_account(account)
        return account

    def delete_account(self, account_id: int):
        if self.account_dao.delete_account_by_id(account_id):
            return True
        else:
            raise ResourceNotFoundError(f'Could not find account with id: {account_id}')

    def delete_client(self, client_id: int) -> bool:
        client = self.get_client(client_id)
        if client is None:
            raise ResourceNotFoundError(f'no client with id {client_id} exists')
        accounts = self.get_all_accounts_by_client(client.client_id)
        for account in accounts:
            self.delete_account(account.account_id)
        return self.client_dao.delete_client_by_id(client_id)

    def withdraw(self, client_id: int, account_id: int, amount: float) -> bool:
        if self.client_dao.get_client_by_id(client_id) is None:
            raise ResourceNotFoundError(f'Could not find client with id: {client_id}')
        account = self.get_account(account_id)
        if account.client_id == client_id:
            if amount <= account.account_balance:
                account.account_balance -= amount
                account = self.update_account(account)
                return True
            else:
                raise ValueError("Insufficient Funds")
        else:
            raise AccountOwnershipError('You do not have authorization to withdraw from this account')

    def deposit(self, client_id: int, account_id: int, amount: float) -> bool:
        if self.get_client(client_id) is None:
            raise ResourceNotFoundError(f'Could not find client with id {client_id}')
        if self.get_account(account_id) is None:
            raise ResourceNotFoundError(f'Could not find account with id: {account_id}')
        account = self.get_account(account_id)
        account.account_balance += amount
        account = self.update_account(account)
        return True

    def transfer(self, client_id: int, initial_account_id: int, target_account_id: int, amount: float) -> list[Account]:
        if self.get_client(client_id) is None:
            raise ResourceNotFoundError(f'Could not find client with id: {client_id}')
        if self.get_account(initial_account_id) is None:
            raise ResourceNotFoundError(f'Could not find account with id: {initial_account_id}')
        if self.get_account(target_account_id) is None:
            raise ResourceNotFoundError(f'Could not find account with id: {target_account_id}')

        initial_account = self.get_account(initial_account_id)
        target_account = self.get_account(target_account_id)

        if initial_account.client_id == client_id:
            if initial_account.account_balance >= amount:
                initial_account.account_balance -= amount
                target_account.account_balance += amount
                self.update_account(initial_account)
                self.update_account(target_account)
                return True
            else:
                raise ValueError('Insufficient Funds')
        else:
            raise AccountOwnershipError('You do not have authorization to transfer from this account')
