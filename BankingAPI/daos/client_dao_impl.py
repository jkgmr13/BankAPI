from Entities.clients import Client
from daos.client_dao import ClientDao


class ClientDaoLocal(ClientDao):

    id_maker = 0
    client_table = {}

    def create_client(self, client: Client) -> Client:
        ClientDaoLocal.id_maker += 1
        client.client_id = ClientDaoLocal.id_maker
        ClientDaoLocal.client_table[client.client_id] = client
        return client

    def get_client_by_id(self, client_id: int) -> Client:
        try:
            return ClientDaoLocal.client_table[client_id]
        except KeyError:
            return None

    def get_all_clients(self) -> list[Client]:
        client_list = list(ClientDaoLocal.client_table.values())
        return client_list

    def delete_client_by_id(self, client_id: int) -> bool:
        try:
            del ClientDaoLocal.client_table[client_id]
            return True
        except KeyError:
            return False

    def update_client(self, client: Client) -> Client:
        if self.get_client_by_id(client.client_id) is not None:
            ClientDaoLocal.client_table[client.client_id] = client
            return client
        else:
            return None
