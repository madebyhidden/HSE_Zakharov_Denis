# -*- coding: cp1251 -*-
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import re


class Account:
    __account_counter = 1000

    def __init__(self, account_holder, balance=0.0):
        if not self._validate_holder_name(account_holder):
            raise ValueError("Имя владельца должно быть в формате 'Имя Фамилия' с заглавных букв")

        if balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")

        self.holder: str = account_holder
        self.__balance: float = balance
        self.account_number: str = f'ACC-{self.__account_counter}'
        self.operations_history = []
        Account.__account_counter += 1

    def _validate_holder_name(self, name):
        """Проверяет формат имени: 'Имя Фамилия' с заглавных букв"""

        # Паттерн: два слова, каждое начинается с заглавной буквы (кириллица или латиница)
        pattern = r'^[А-ЯЁA-Z][а-яёa-z]+\s[А-ЯЁA-Z][а-яёa-z]+$'
        return bool(re.match(pattern, name))

    def deposit(self, amount, transaction=False):
        try:
            if amount < 0:
                self.operations_history.append(
                    [f"Не смогли добавить {amount} на баланс. Баланс на момент: {self.__balance}",
                     datetime.datetime.strftime(datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S"),
                     "status.Code.Failed"])
                raise ValueError()
            else:
                self.__balance += amount
                if not transaction:
                    print("Деньги на счете, бегом скупать весь Вайлдберис")
                else:
                    print("")
                self.operations_history.append([f"Добавили {amount} на баланс. Баланс на момент: {self.__balance}",
                                                datetime.datetime.strftime(datetime.datetime.now(),
                                                                           format="%Y-%m-%d %H:%M:%S"),
                                                "status.Code.Success"])
        except ValueError:
            print("Деньги не минусем!")

    def withdraw(self, amount, transaction=False, chacc_back=False):
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
                        elif chacc_back:
                            print("Накопил денег и радуешься? Деньги снова на рассчётном счету")
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
        """
        Создаёт DataFrame из истории операций и строит график изменения баланса
        """

        if not self.operations_history:
            print("История операций пуста")
            return

        data = []
        for operation in self.operations_history:
            description = operation[0]
            date_str = operation[1]
            status = operation[2]

            balance_match = re.search(r'Баланс на момент:\s*([\d.]+)', description)
            if balance_match:
                balance = float(balance_match.group(1))

                data.append({
                    'datetime': pd.to_datetime(date_str),
                    'balance': balance,
                    'status': status,
                    'description': description
                })

        df = pd.DataFrame(data)

        df = df.sort_values('datetime')

        plt.figure(figsize=(10, 6))
        plt.plot(df['datetime'], df['balance'], marker='o', linestyle='-', linewidth=2, markersize=6)
        plt.title('Изменение баланса счёта во времени')
        plt.xlabel('Дата и время операции')
        plt.ylabel('Баланс после операции')
        plt.xticks(rotation=45, ha="right")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def analyze_transactions(self, n):
        """
        Выводит последние n крупных операций
        """

        if not self.operations_history:
            print("История операций пуста")
            return

        df = pd.DataFrame(self.operations_history)

        df_recent = df.sort_values('datetime', ascending=False).head(n)

        df_large = df_recent.nlargest(n, 'amount')

        print(f"Последние {n} крупных операций:")
        for idx, row in df_large.iterrows():
            print(f"Тип: {row['type']}, Сумма: {row['amount']}, "
                  f"Дата: {row['datetime']}, Баланс после: {row['balance_after']}, "
                  f"Статус: {row['status']}")

        return df_large
