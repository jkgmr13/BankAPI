from Entities.clients import Client
from daos.client_dao import ClientDao
from daos.client_dao_impl import ClientDaoLocal
from daos.client_dao_postgres import ClientDaoPostgres

client_dao: ClientDao = ClientDaoPostgres()

test_client = Client(0, "Joseph", "Keller")


def test_create_client():
    client = client_dao.create_client(test_client)
    assert client.client_id != 0


def test_get_client_by_id():
    client = client_dao.get_client_by_id(test_client.client_id)
    assert client.last_name == test_client.last_name


def test_get_clients():
    client_list = client_dao.get_all_clients()
    assert len(client_list) >= 1


def test_update_client():
    test_client.first_name = "Joe"
    client = client_dao.update_client(test_client)
    assert client.first_name == test_client.first_name


def test_delete_client():
    assert client_dao.delete_client_by_id(test_client.client_id)


def test_delete_client_invalid():
    assert not client_dao.delete_client_by_id(test_client.client_id)





