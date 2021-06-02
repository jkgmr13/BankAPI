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


account_dao: AccountDao = AccountDaoPostgres()
client_dao: ClientDao = ClientDaoPostgres()
account_service: AccountService = AccountServiceImpl(client_dao, account_dao)

test_client13 = Client(0, 'Joe', 'kell')
test_client13 = account_service.add_client(test_client13)
test_client14 = Client(0, 'Joseph', 'Keller')
test_client14 = account_service.add_client(test_client14)
test_account13 = Account(0, test_client13.client_id, 'checking', 100.0)
test_account14 = Account(0, test_client14.client_id, 'savings', 100.0)
test_account13 = account_service.add_account(test_account13)
test_account14 = account_service.add_account(test_account14)
test_account15 = Account(0, test_client13.client_id, 'cd', 500)
test_account15 = account_service.add_account(test_account15)


def test_get_all_accounts_by_client():
    accounts = account_service.get_all_accounts_by_client(test_client13.client_id)
    assert len(accounts) >= 2


def test_withdraw_valid():
    account_service.withdraw(test_client13.client_id, test_account13.account_id, 50.0)
    assert account_service.get_account(test_account13.account_id).account_balance == 50.0


def test_withdraw_invalid():
    try:
        account_service.withdraw(test_client13.client_id, test_account13.account_id, 100.01)
        assert False
    except ValueError:
        assert True


def test_withdraw_invalid2():
    try:
        account_service.withdraw(test_client13.client_id, test_account14.account_id, 100)
        assert False
    except AccountOwnershipError:
        assert True


def test_deposit():
    account_service.deposit(test_client13.client_id, test_account13.account_id, 50)
    assert test_account13.account_balance == 100.0


def test_transfer_valid():
    account_service.transfer(test_client13.client_id, test_account13.account_id, test_account14.account_id, 50)
    assert account_service.get_account(test_account13.account_id).account_balance == 50.0 and account_service.get_account(test_account14.account_id).account_balance == 150.0


def test_transfer_invalid():
    try:
        account_service.transfer(test_client13.client_id, test_account13.account_id, test_account14.account_id, 10000)
        assert False
    except ValueError:
        assert True


def test_transfer_invalid2():
    try:
        account_service.transfer(test_client13.client_id, test_account14.account_id, test_account13.account_id, 10)
        assert False
    except AccountOwnershipError:
        assert True


def test_delete_client():
    test_accounts = account_service.get_all_accounts_by_client(test_client13.client_id)
    account_service.delete_client(test_client13.client_id)
    accounts = account_service.get_all_accounts()
    assert test_accounts not in accounts



