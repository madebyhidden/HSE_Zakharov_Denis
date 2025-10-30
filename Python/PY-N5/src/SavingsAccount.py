# -*- coding: cp1251 -*-
import datetime
import Account


class SavingsAccount(Account.Account):
    account_type = "Savings Account"
    def __init__(self, account_holder, balance=0.0):
        super().__init__(account_holder, balance)
        self.account_number: str = f'SAVACC-{super().account_counter()}'


    def up_savings_balance(self, amount, chacc):
        try:
            if amount < 0:
                self.operations_history.append( [f"Не смогли перевести {amount} на сберсчёт. Баланс на момент: {self.__balance}",
                     datetime.datetime.strftime(datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S"),
                     "status.Code.Failed"])
                raise ValueError()
            else:
                chacc.withdraw(amount, transaction=True)
                super().deposit(amount)
        except ValueError:
            print("Деньги не минусем!")




    def withdraw(self, amount: float):
        if self.get_balance() - amount <= self.get_balance() * 0.5:
            super().withdraw(amount)
