import datetime
import pandas as pd

import Account


class SavingsAccount(Account.Account):
    """Класс сберегательного счёта.
    
    Наследуется от Account и добавляет функциональность для накоплений:
    - Ограничение на снятие средств (не более 50% от баланса)
    - Начисление процентов на остаток
    """

    account_type = "Savings Account"
    __savingsBalance = 0.0

    def __init__(self, account_holder, balance=0.0):
        """Инициализирует новый сберегательный счёт.
        
        Args:
            account_holder (str): Имя владельца счёта в формате 'Имя Фамилия'
            balance (float, optional): Начальный баланс счёта. По умолчанию 0.0.
        
        Note:
            Номер счёта генерируется автоматически с префиксом 'SAVACC-'.
            Начальный savingsBalance устанавливается в 0.0.
        """
        super().__init__(account_holder, balance)
        # Генерируем уникальный номер счёта с префиксом для сберегательного счёта
        self.account_number: str = f'SAVACC-{super().account_counter()}'

    def up_savings_balance(self, amount, chacc):
        """Переводит средства с расчётного счёта на сберегательный.
        
        Снимает указанную сумму с расчётного счёта и добавляет её
        на сберегательный счёт. Также обновляет внутренний счётчик
        максимальной суммы, которая была на счету (savingsBalance).
        
        Args:
            amount (float): Сумма для перевода на сберегательный счёт.
            chacc (CheckingAccount): Объект расчётного счёта, с которого переводятся средства.
        
        Note:
            Если сумма отрицательная или недостаточно средств на расчётном счёте,
            операция записывается как неудачная.
        """
        try:
            if amount < 0:
                # Отрицательная сумма - записываем как неудачную операцию
                self.operations_history.append(
                    [f"Не смогли перевести {amount} на сберсчёт. Баланс на момент: {self.get_balance()}",
                     datetime.datetime.strftime(datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S"),
                     "status.Code.Failed"])
                raise ValueError()
            else:

                if chacc.get_balance() >= amount:
                    # Определяем, открывается ли счёт впервые или пополняется существующий
                    if self.__savingsBalance > amount:
                        print(f"Добавлено на счет {amount}")
                    else:
                        print(f"Открыт счет на сумму {amount}")
                    # Выполняем перевод: снимаем с расчётного и добавляем на сберегательный
                    chacc.withdraw(amount, transaction=True)
                    super().deposit(amount, transaction=True)
                    # Обновляем счётчик максимальной суммы
                    self.__savingsBalance += amount
                else:
                    print("Нет денег на расчетном счету")

        except ValueError:
            print("Деньги не минусуем!")

    def withdraw(self, amount: float, chacc):
        """Снимает средства со сберегательного счёта с ограничением.
        
        Args:
            amount (float): Сумма для снятия со сберегательного счёта.
            chacc (CheckingAccount): Объект расчётного счёта, на который переводятся средства.
        
        Note:
            Если попытка снять более 50% от баланса, операция блокируется
            и записывается как неудачная.
        """
        try:
            # Проверяем ограничение: после снятия должно остаться не менее 50% от МАКСИМАЛЬНОГО баланса.
            # Если положили 1000, а потом еще 500, то половину считаем от суммы, то есть нельзя снять ниже 750
            if self.get_balance() - amount >= self.__savingsBalance * 0.5:

                super().withdraw(amount, transaction=True, chacc_back=True)
                chacc.deposit(amount)
            else:
                raise ValueError()
        except ValueError:

            print("Я запрещаю Вам снимать больше 50%")
            self.operations_history.append(
                [f"Не смогли снять {amount} со сберсчёта. Баланс на момент: {self.get_balance()}",
                 datetime.datetime.strftime(datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S"),
                 "status.Code.Failed"])

    def apply_interest(self, rate):
        """Начисляет проценты на текущий баланс сберегательного счёта.
        
        Args:
            rate (float): Процентная ставка для начисления (например, 5.0 для 5%).
        
        Note:
            Если процентная ставка отрицательная или нулевая, операция блокируется
            и записывается как неудачная.
        """
        try:
            if rate > 0:
                interest_amount = self.get_balance() * (rate / 100)

                super().deposit(interest_amount, transaction=True)

                self.operations_history.append(
                    [f":Добавили {rate}% на счет. Баланс на момент: {self.get_balance()}",
                     datetime.datetime.strftime(datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S"),
                     "status.Code.Success"])
                print(f"Что же натекло под камушек? {rate}% уже на счету. Баланс на момент: {self.get_balance()}")
            else:
                raise ValueError()

        except ValueError:
            # Отрицательная или нулевая ставка - блокируем операцию
            print("Пу-пу-пу... Не уменьшай себе сбережения! Только плюс, только вайб")
            self.operations_history.append(
                [f"Не смогли добавить {rate}% на счет. Баланс на момент: {self.get_balance()}",
                 datetime.datetime.strftime(datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S"),
                 "status.Code.Failed"])

    def get_savingsBalance(self):
        """Возвращает накопленную сумму на сберегательном счёте.
        
        Returns:
            float: Сумма, накопленная на сберегательном счёте (savingsBalance).

        """
        return self.__savingsBalance

    def clean_history(self, df: pd.DataFrame) -> pd.DataFrame:
        """Очистка + проверка данных на корректность

        Args:
            df (pd.DataFrame): DataFrame с историей операций.

        Returns:
            pd.DataFrame: Очищенный DataFrame с корректными данными.
        """

        account_num = self.account_number.split('-')[-1]
        # Фильтруем по номеру счёта (извлекаем числовую часть из account_number в файле)
        df["account_num"] = df["account_number"].str.split('-').str[-1]
        df = df[df["account_num"] == account_num]

        df = df[df["account_type"].str.lower() == "savings"]
        df = df[df["status"] == "success"]
        df = df[df["operation"].isin(["deposit", "withdraw", "interest"])]
        # Для deposit и withdraw проверяем amount > 0
        mask = (df["operation"].isin(["deposit", "withdraw"]) & (df["amount"] > 0)) | (df["operation"] == "interest")
        df = df[mask]
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df[df["date"].notna()]
        return df

    def load_from_file(self, path: str) -> None:
        """Загрузка истории счёта из файла

        P.S. Я понимаю, что тут по идее надо использовать deposit() и withdraw(), но в моей реализации используется
        автогенерация времени, поэтому нужно использовать ухитрения. А также используется прямое обращение к атрибуту род. класса
        (плохая практика)

        """
        if path.endswith(".csv"):
            df = pd.read_csv(path)
        elif path.endswith(".json"):
            df = pd.read_json(path)
        else:
            raise ValueError("Формат не поддерживается, используйте csv или json")

        df_clean = self.clean_history(df)

        for _, row in df_clean.iterrows():
            operation_type = row["operation"]
            dt = row["date"]

            if operation_type == "deposit":
                amount = float(row["amount"])
                self._Account__balance += amount
                self.__savingsBalance += amount
            elif operation_type == "withdraw":
                amount = float(row["amount"])
                if self._Account__balance >= amount:
                    self._Account__balance -= amount
                else:
                    continue
            elif operation_type == "interest":
                balance_after = float(row["balance_after"])
                interest_amount = balance_after - self._Account__balance
                if interest_amount > 0:
                    self._Account__balance = balance_after
                    rate = (interest_amount / (self._Account__balance - interest_amount)) * 100
                else:
                    continue
            else:
                continue

            formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S")

            if operation_type == "deposit":
                description = f"Добавили {amount} на баланс. Баланс на момент: {self._Account__balance}"
            elif operation_type == "withdraw":
                description = f"Забрали {amount} с баланса. Баланс на момент: {self._Account__balance}"
            else:
                description = f"Добавили {rate:.2f}% на счет. Баланс на момент: {self._Account__balance}"

            self.operations_history.append([
                description,
                formatted_date,
                "status.Code.Success"
            ])
