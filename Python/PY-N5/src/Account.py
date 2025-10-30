# -*- coding: cp1251 -*-
import datetime
import matplotlib.pyplot as plt


class Account:
    __account_counter = 1000
    holder = str()
    account_number = int()

    def __init__(self, account_holder, balance=0.0):
        self.account_holder: str = account_holder
        self.__balance: float = balance
        self.account_number: str = f'ACC-{self.__account_counter}'
        self.operations_history = []
        Account.__account_counter += 1

    def deposit(self, amount):
        try:
            if amount < 0:
                self.operations_history.append(
                    [f"Не смогли добавить {amount} на баланс. Баланс на момент: {self.__balance}",
                     datetime.datetime.strftime(datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S"),
                     "status.Code.Failed"])
                raise ValueError()
            else:
                self.__balance += amount
                print("Деньги на счете, бегом скупать весь Вайлдберис")
                self.operations_history.append([f"Добавили {amount} на баланс. Баланс на момент: {self.__balance}",
                                                datetime.datetime.strftime(datetime.datetime.now(),
                                                                           format="%Y-%m-%d %H:%M:%S"),
                                                "status.Code.Success"])
        except ValueError:
            print("Деньги не минусем!")

    def withdraw(self, amount, transaction=False):
        try:
            if amount < 0:
                self.operations_history.append(
                    [f"Не смогли снять {amount} с баланса. Баланс на момент: {self.__balance}",
                     datetime.datetime.strftime(datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S"),
                     "status.Code.Failed"])
                raise ValueError()
            else:
                try:
                    if self.__balance < amount:
                        raise ValueError()
                    else:
                        self.__balance -= amount
                        self.operations_history.append(
                            [f"Забрали {amount} с баланса. Баланс на момент: {self.__balance}",
                             datetime.datetime.strftime(datetime.datetime.now(),
                                                        format="%Y-%m-%d %H:%M:%S"),
                             "status.Code.Success"])
                        if not transaction:
                            print("Темки через наличку крутим? Ладно, держи!")
                        else:
                            print("Переведено на сберсчет. Кап кап денежки. Кап кап")
                except ValueError:
                    self.operations_history.append(
                        [f"Не смогли снять {amount} с баланса. Баланс на момент: {self.__balance}",
                         datetime.datetime.strftime(datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S"),
                         "status.Code.Failed"])
                    print("Нужно больше золота! (Остаток меньше желаемой суммы)")
        except ValueError:
            print("Деньги не минусем!")

    def get_balance(self):
        return self.__balance

    def get_history(self):
        return self.operations_history


    def account_counter(self):
        return Account.__account_counter


    def plot_history(self):
        y = [int(key[0].split(".")[1].split(":")[1].replace(" ", '')) for key in self.operations_history]
        x = [key[1] for key in self.operations_history]
        plt.plot(x, y)
        plt.xticks(rotation=45, ha="right")
        plt.show()
