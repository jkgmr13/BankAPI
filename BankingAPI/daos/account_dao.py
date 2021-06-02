from abc import abstractmethod, ABC

from Entities.accounts import Account


class AccountDao(ABC):

    @abstractmethod
    def create_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def get_account_by_id(self, account_id: int) -> Account:
        pass

    @abstractmethod
    def get_all_accounts(self) -> list[Account]:
        pass

    @abstractmethod
    def update_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def delete_account_by_id(self, account_id: int) -> bool:
        pass
