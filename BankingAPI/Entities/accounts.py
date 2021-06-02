
class Account:

    def __init__(self, account_id: int, client_id: int, account_type: str, account_balance: float):
        self.client_id = client_id
        self.account_type = account_type
        self.account_balance = account_balance
        self.account_id = account_id

    def as_json_dict(self):
        return {
            "accountId": self.account_id,
            "clientId": self.client_id,
            "account_type": self.account_type,
            "account_balance": self.account_balance
        }
