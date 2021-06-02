from Entities.accounts import Account
from Entities.clients import Client
from daos.account_dao import AccountDao
from daos.account_dao_impl import AccountDaoLocal
from daos.account_dao_postgres import AccountDaoPostgres
from daos.client_dao import ClientDao
from daos.client_dao_postgres import ClientDaoPostgres

account_dao: AccountDao = AccountDaoPostgres()
client_dao: ClientDao = ClientDaoPostgres()
test_client = Client(0, "Joe", "keller")
test_client = client_dao.create_client(test_client)
test_account = Account(0, test_client.client_id, 'Savings', 150.00)


def test_create_account():
    account = account_dao.create_account(test_account)
    assert account.account_id != 0


def test_get_account_by_id():
    account = account_dao.get_account_by_id(test_account.account_id)
    assert account.account_balance == test_account.account_balance


def test_get_account_by_id_invalid():
    account = account_dao.get_account_by_id(9999)
    assert account is None


def test_get_accounts():
    account_list = account_dao.get_all_accounts()
    print(account_list)
    assert len(account_list) >= 1


def test_update_account():
    test_account.first_name = "Joe"
    account = account_dao.update_account(test_account)
    assert account.first_name == test_account.first_name


def test_delete_account():
    result = account_dao.delete_account_by_id(test_account.account_id)
    assert result


def test_delete_account_invalid():
    assert not account_dao.delete_account_by_id(9999)

