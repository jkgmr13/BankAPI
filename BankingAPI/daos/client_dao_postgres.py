from Entities.clients import Client
from Exceptions.resource_error import ResourceNotFoundError
from daos.client_dao import ClientDao
from util.postgres_con import connection


class ClientDaoPostgres(ClientDao):
    def create_client(self, client: Client) -> Client:
        sql = """insert into client (client_first_name, client_last_name) values (%s, %s) returning client_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (client.first_name, client.last_name))
        connection.commit()
        client_id = cursor.fetchone()[0]
        client.client_id = client_id
        return client

    def get_client_by_id(self, client_id) -> Client:
        sql = """select * from client where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError(f'There is no client with id: {client_id}')
        else:
            client = Client(*record)
            return client

    def get_all_clients(self) -> list[Client]:
        sql = """select * from client"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        clients = [Client(*record) for record in records]
        return clients

    def delete_client_by_id(self, client_id) -> bool:
        sql = """delete from client where client_id = %s"""
        sql_check = """select * from client where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql_check, [client_id])
        record = cursor.fetchone()
        cursor.execute(sql, [client_id])
        connection.commit()
        if record is None:
            return False
        else:
            return True

    def update_client(self, client: Client) -> Client:
        sql = """update client set client_first_name=%s, client_last_name=%s where client_id=%s"""
        sql_check = """select * from client where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql_check, [client.client_id])
        record = cursor.fetchone()
        cursor.execute(sql, (client.first_name, client.last_name, client.client_id))
        connection.commit()
        if record is None:
            return None
        else:
            return client

