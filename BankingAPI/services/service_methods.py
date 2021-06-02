
# abstract interface for service methods
from abc import abstractmethod, ABC

from Entities.accounts import Account
from Entities.clients import Client


class AccountService(ABC):

    # CRUD operations
    @abstractmethod
    def add_client(self, client: Client) -> Client:
        pass

    @abstractmethod
    def add_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def get_client(self, client_id: int) -> Client:
        pass

    @abstractmethod
    def get_account(self, account_id: int) -> Account:
        pass

    @abstractmethod
    def get_all_accounts(self) -> list[Account]:
        pass

    @abstractmethod
    def get_all_clients(self) -> list[Client]:
        pass

    @abstractmethod
    def get_all_accounts_by_client(self, client_id: int) -> list[Account]:
        pass

    @abstractmethod
    def get_all_accounts_lower_balance_bound(self,client_id: int, lower_bound: float):
        pass

    @abstractmethod
    def get_all_accounts_upper_balance_bound(self, client_id: int, upper_bound: float):
        pass

    @abstractmethod
    def get_all_accounts_bounded(self, client_id: int, lower_bound: float, upper_bound: float):
        pass

    @abstractmethod
    def update_client(self, client: Client) -> Client:
        pass

    @abstractmethod
    def update_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def delete_client(self, client_id: int) -> bool:
        pass

    @abstractmethod
    def delete_account(self, account_id: int):
        pass

    # Non-CRUD service methods
    @abstractmethod
    def withdraw(self, client_id: int, account_id: int, amount: float) -> bool:
        pass

    @abstractmethod
    def deposit(self, client_id: int, account_id: int, amount: float) -> bool:
        pass

    @abstractmethod
    def transfer(self, client_id: int, initial_account_id: int, target_account_id: int, amount: float) -> bool:
        pass
