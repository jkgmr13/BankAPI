from abc import ABC, abstractmethod

from Entities.clients import Client


class ClientDao(ABC):

    # Basic CRUD methods
    @abstractmethod
    def create_client(self, client: Client) -> Client:
        pass

    @abstractmethod
    def get_client_by_id(self, client_id) -> Client:
        pass

    @abstractmethod
    def get_all_clients(self) -> list[Client]:
        pass

    @abstractmethod
    def delete_client_by_id(self, client_id) -> bool:
        pass

    @abstractmethod
    def update_client(self, client: Client) -> Client:
        pass
