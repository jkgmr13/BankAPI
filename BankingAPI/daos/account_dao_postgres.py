from Entities.accounts import Account
from daos.account_dao import AccountDao
from util.postgres_con import connection


class AccountDaoPostgres(AccountDao):
    def create_account(self, account: Account) -> Account:
        sql = """insert into account (account_type, account_balance, c_id) values (%s, %s, %s) returning account_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (account.account_type, account.account_balance, account.client_id))
        connection.commit()
        account_id = cursor.fetchone()[0]
        account.account_id = account_id
        return account

    def get_account_by_id(self, account_id: int) -> Account:
        sql = """select * from account where account_id=%s"""
        cursor = connection.cursor()
        cursor.execute(sql, [account_id])
        record = cursor.fetchone()
        if record is None:
            return None
        else:
            return Account(*record)

    def get_all_accounts(self) -> list[Account]:
        sql = """select * from account"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        accounts = [Account(*record) for record in records]
        return accounts

    def update_account(self, account: Account) -> Account:
        sql = """update account set c_id=%s, account_type=%s, account_balance=%s where account_id=%s"""
        sql_check = """select * from account where account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql_check, [account.account_id])
        record = cursor.fetchone
        cursor.execute(sql, (account.client_id, account.account_type, account.account_balance, account.account_id))
        connection.commit()
        if record is None:
            return None
        else:
            return account

    def delete_account_by_id(self, account_id: int) -> bool:
        sql = """delete from account where account_id = %s"""
        sql_check = """select * from account where account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql_check, [account_id])
        record = cursor.fetchone()
        cursor.execute(sql, [account_id])
        connection.commit()
        if record is None:
            return False
        else:
            return True
