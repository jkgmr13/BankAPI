from Entities.accounts import Account
from Entities.clients import Client
from Exceptions.account_error import AccountOwnershipError
from daos.account_dao import AccountDao
from daos.account_dao_impl import AccountDaoLocal
from daos.account_dao_postgres import AccountDaoPostgres
from daos.client_dao import ClientDao
from daos.client_dao_impl import ClientDaoLocal
from daos.client_dao_postgres import ClientDaoPostgres
from services.service_impl import AccountServiceImpl
from services.service_methods import AccountService

from unittest.mock import MagicMock


mock_account_dao: AccountDao = AccountDaoPostgres()
mock_client_dao: ClientDao = ClientDaoPostgres()
account_service: AccountService = AccountServiceImpl(mock_client_dao, mock_account_dao)

accounts = [Account(0, 1, "checking", 0), Account(1, 1, "saving", 100), Account(2, 2, "cd", 1000)]
test_client = Client(1, "joe", "kell")

mock_account_dao.get_all_accounts = MagicMock(return_value=accounts)

mock_account_dao.get_account_by_id = MagicMock(return_value=accounts[1])

mock_client_dao.get_client_by_id = MagicMock(return_value=test_client)


def test_get_all_accounts_by_client():
    result = account_service.get_all_accounts_by_client(1)
    assert len(result) == 2


def test_withdraw_valid():
    account_service.withdraw(1, 2, 100)
    assert accounts[1].account_balance == 0.0


def test_withdraw_invalid2():
    try:
        account_service.withdraw(1, 1, 10000)
        assert False
    except ValueError:
        assert True

