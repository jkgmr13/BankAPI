from flask import Flask, request, jsonify
import logging

from Entities.accounts import Account
from Entities.clients import Client
from Exceptions.account_error import AccountOwnershipError
from Exceptions.resource_error import ResourceNotFoundError
from daos.account_dao import AccountDao
from daos.account_dao_impl import AccountDaoLocal
from daos.account_dao_postgres import AccountDaoPostgres
from daos.client_dao import ClientDao
from daos.client_dao_impl import ClientDaoLocal
from daos.client_dao_postgres import ClientDaoPostgres
from services.service_impl import AccountServiceImpl
from services.service_methods import AccountService

client_dao: ClientDao = ClientDaoPostgres()
account_dao: AccountDao = AccountDaoPostgres()


service: AccountService = AccountServiceImpl(client_dao, account_dao)


app: Flask = Flask(__name__)
logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s')

@app.post('/clients')
def create_client():
    body = request.json
    client = Client(body["clientId"], body["firstName"], body["lastName"])
    client = service.add_client(client)
    return f'created new client with id {client.client_id}', 201


@app.get('/clients/<client_id>')
def get_client(client_id: str):
    try:
        client = service.get_client(int(client_id))
        return client.as_json_dict(), 200
    except ResourceNotFoundError as e:
        return str(e), 404


@app.get('/clients')
def get_all_clients():
    try:
        clients = service.get_all_clients()
        json_clients = [c.as_json_dict() for c in clients]
        return jsonify(json_clients), 200
    except ResourceNotFoundError as e:
        return str(e), 404


@app.put('/clients/<client_id>')
def update_client(client_id: str):
    try:
        body = request.json
        client = Client(int(client_id), body["firstName"], body["lastName"])
        client.client_id = int(client_id)
        service.update_client(client)
        return 'updated successfully', 200

    except ResourceNotFoundError as e:
        return str(e), 404


@app.delete('/clients/<client_id>')
def delete_client(client_id: str):
    try:
        service.delete_client(int(client_id))
        return 'Deleted Successfully', 205
    except ResourceNotFoundError as e:
        return str(e), 404


@app.post('/clients/<client_id>/accounts')
def create_account(client_id: str):
    body = request.json
    try:
        account = service.add_account(Account(body["accountId"], int(client_id),
                                              body["accountType"], body["accountBalance"]))
        return f'Account create with id: {account.account_id}', 201
    except ResourceNotFoundError as e:
        return str(e), 404


@app.get('/clients/<client_id>/accounts')
def get_clients_accounts(client_id: str):
    try:
        account_list = service.get_all_accounts_by_client(int(client_id))
        upper_amount = request.args.get("amountLessThan")
        lower_amount = request.args.get("amountGreaterThan")
        if lower_amount is None and upper_amount is None:
            json_accounts = [account.as_json_dict() for account in account_list]
            return jsonify(json_accounts), 200
        if lower_amount is not None and upper_amount is not None:
            accounts = service.get_all_accounts_bounded(int(client_id), float(lower_amount), float(upper_amount))
        elif lower_amount is not None:
            accounts = service.get_all_accounts_lower_balance_bound(int(client_id), float(lower_amount))
        elif upper_amount is not None:
            accounts = service.get_all_accounts_upper_balance_bound(int(client_id), float(upper_amount))
        json_accounts = [account.as_json_dict() for account in accounts]
        return jsonify(json_accounts), 200
    except ResourceNotFoundError as e:
        return str(e), 404


@app.get('/clients/<client_id>/accounts/<account_id>')
def get_clients_account_by_id(client_id: str, account_id: str):
    try:
        accounts = service.get_all_accounts_by_client(int(client_id))
        account = None
        for a in accounts:
            if a.account_id == int(account_id):
                account = a
        if account is None:
            return f'No account with id: {int(account_id)}', 404
        return account.as_json_dict(), 200
    except ResourceNotFoundError as e:
        return str(e), 404


@app.put('/clients/<client_id>/accounts/<account_id>')
def update_account(client_id: str, account_id: str):
    try:
        body = request.json
        account = Account(*body.values())
        account.account_id = int(account_id)
        account.client_id = int(client_id)
        service.update_account(account)
        return 'Account updated successfully', 200
    except ResourceNotFoundError as e:
        return str(e), 404
    except AccountOwnershipError as e:
        return str(e), 403


@app.delete('/clients/<client_id>/accounts/<account_id>')
def delete_account(client_id: str, account_id: str):
    try:
        service.delete_account(int(account_id))
        return 'Account deleted successfully', 205
    except ResourceNotFoundError as e:
        return str(e), 404


@app.patch('/clients/<client_id>/accounts/<account_id>')
def edit_balance(client_id: str, account_id: str):
    body = request.json
    if body.get("withdraw") is not None:
        try:
            service.withdraw(int(client_id), int(account_id), body.get("withdraw"))
            return 'Amount withdrawn successfully', 200
        except AccountOwnershipError as e:
            return str(e), 403
        except ResourceNotFoundError as e:
            return str(e), 404
        except ValueError as e:
            return str(e), 422
    if body.get("deposit") is not None:
        try:
            service.deposit(int(client_id), int(account_id), body.get("deposit"))
            return 'Amount deposited successfully', 200
        except ResourceNotFoundError as e:
            return str(e), 404


@app.patch('/clients/<client_id>/accounts/<initial_account_id>/transfer/<target_account_id>')
def transfer_balance(client_id: str, initial_account_id: str, target_account_id: str):
    try:
        body = request.json
        service.transfer(int(client_id), int(initial_account_id), int(target_account_id), body["amount"])
        return 'accounts updated successfully', 200
    except AccountOwnershipError as e:
        return str(e), 403
    except ResourceNotFoundError as e:
        return str(e), 404
    except ValueError as e:
        return str(e), 422


if __name__ == '__main__':
    app.run()
