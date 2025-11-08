import datetime
import re

import matplotlib.pyplot as plt
import pandas as pd


class Account:
    """Базовый класс для банковского счёта.
    
    Предоставляет базовую функциональность для работы со счётом:
    пополнение, снятие средств, ведение истории операций.
    """

    __account_counter = 1000

    def __init__(self, account_holder, balance=0.0):
        """Инициализирует новый банковский счёт.
        
        Args:
            account_holder (str): Имя владельца счёта в формате 'Имя Фамилия'
            balance (float, optional): Начальный баланс счёта. По умолчанию 0.0.
        
        Raises:
            ValueError: Если имя владельца не соответствует формату или
                       если начальный баланс отрицательный.
        """
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
        """Проверяет формат имени владельца счёта.
        
        Args:
            name (str): Имя для проверки.
        
        Returns:
            bool: True если имя соответствует формату, False иначе.
        """
        # Паттерн: два слова, каждое начинается с заглавной буквы (кириллица или латиница)
        pattern = r'^[А-ЯЁA-Z][а-яёa-z]+\s[А-ЯЁA-Z][а-яёa-z]+$'
        return bool(re.match(pattern, name))

    def deposit(self, amount, transaction=False):
        """Пополняет счёт на указанную сумму.

        Args:
            amount (float): Сумма для пополнения счёта.
            transaction (bool, optional): Флаг внутренней транзакции (без вывода сообщений).
                                        По умолчанию False.
        
        Note:
            Операция всегда записывается в историю, даже если она неудачна.
            Формат записи: [описание, дата/время, статус]
        """
        try:
            if amount < 0:
                # Отрицательная сумма - записываем как неудачную операцию
                self.operations_history.append(
                    [f"Не смогли добавить {amount} на баланс. Баланс на момент: {self.__balance}",
                     datetime.datetime.strftime(datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S"),
                     "status.Code.Failed"])
                raise ValueError()
            else:

                self.__balance += amount
                # Используется проверка для внутренних операций, чтобы не путать пользователя в консоли
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
        """Снимает указанную сумму со счёта.

        Args:
            amount (float): Сумма для снятия со счёта.
            transaction (bool, optional): Флаг внутренней транзакции. По умолчанию False.
            chacc_back (bool, optional): Флаг возврата средств на расчётный счёт.
                                        По умолчанию False.
        
        Note:
            Операция записывается в историю в любом случае (успешная или неудачная).
            Если средств недостаточно или сумма отрицательная, операция помечается как Failed.
        """
        try:
            if amount < 0:
                # Отрицательная сумма - записываем как неудачную операцию
                self.operations_history.append(
                    [f"Не смогли снять {amount} с баланса. Баланс на момент: {self.__balance}",
                     datetime.datetime.strftime(datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S"),
                     "status.Code.Failed"])
                raise ValueError()
            else:
                try:
                    # Проверяем достаточность средств на счёте
                    if self.__balance < amount:
                        raise ValueError()
                    else:

                        self.__balance -= amount
                        self.operations_history.append(
                            [f"Забрали {amount} с баланса. Баланс на момент: {self.__balance}",
                             datetime.datetime.strftime(datetime.datetime.now(),
                                                        format="%Y-%m-%d %H:%M:%S"),
                             "status.Code.Success"])
                        # Используется проверка для внутренних операций, чтобы не путать пользователя в консоли
                        if not transaction:
                            print("Темки через наличку крутим? Ладно, держи!")
                        elif chacc_back:
                            print("Накопил денег и радуешься? Деньги снова на рассчётном счету")
                        else:
                            print("Переведено на сберсчет. Кап кап денежки. Кап кап")
                except ValueError:
                    # Недостаточно средств - записываем как неудачную операцию
                    self.operations_history.append(
                        [f"Не смогли снять {amount} с баланса. Баланс на момент: {self.__balance}",
                         datetime.datetime.strftime(datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S"),
                         "status.Code.Failed"])
                    print("Нужно больше золота! (Остаток меньше желаемой суммы)")
        except ValueError:
            print("Деньги не минусем!")

    def get_balance(self):
        """Возвращает текущий баланс счёта.
        
        Returns:
            float: Текущий баланс счёта.
        """
        return self.__balance

    def get_history(self):
        """Возвращает историю всех операций по счёту.
        
        Returns:
            list: Список операций, где каждая операция представлена списком:
                  [описание, дата/время, статус]
        """
        return self.operations_history

    def account_counter(self):
        """Возвращает текущее значение счётчика номеров счетов.
        
        Returns:
            int: Текущее значение счётчика (используется для генерации уникальных номеров).
        """
        return Account.__account_counter

    def plot_history(self):
        """Создаёт график изменения баланса счёта во времени."""
        if not self.operations_history:
            print("История операций пуста")
            return

        # Извлекаем данные из истории операций
        data = []
        for operation in self.operations_history:
            description = operation[0]
            date_str = operation[1]
            status = operation[2]

            # Извлекаем баланс из текстового описания с помощью регулярного выражения
            # Ищем паттерн "Баланс на момент: число"
            balance_match = re.search(r'Баланс на момент:\s*([\d.]+)', description)
            if balance_match:
                balance = float(balance_match.group(1))

                data.append({
                    'datetime': pd.to_datetime(date_str),
                    'balance': balance,
                    'status': status,
                    'description': description
                })

        # Создаём DataFrame и сортируем по дате
        df = pd.DataFrame(data)
        df = df.sort_values('datetime')

        # Строим график
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
        """Выводит последние n крупных операций."""
        if not self.operations_history:
            print("История операций пуста")
            return

        data = []
        for operation in self.operations_history:
            description = operation[0]
            date_str = operation[1]
            status = operation[2]

            # Определяем тип операции
            if "Добавили" in description:
                op_type = "deposit"
                amount_match = re.search(r'Добавили\s+([\d.]+)', description)
            elif "Забрали" in description:
                op_type = "withdraw"
                amount_match = re.search(r'Забрали\s+([\d.]+)', description)
            else:
                op_type = "other"
                amount_match = None

            # Извлекаем сумму
            amount = 0.0
            if amount_match:
                amount = float(amount_match.group(1))

            # Извлекаем баланс
            balance_match = re.search(r'Баланс на момент:\s*([\d.]+)', description)
            balance_after = 0.0
            if balance_match:
                balance_after = float(balance_match.group(1))

            data.append({
                'type': op_type,
                'amount': amount,
                'datetime': pd.to_datetime(date_str),
                'balance_after': balance_after,
                'status': status
            })

        df = pd.DataFrame(data)
        df = df[df['status'] == 'status.Code.Success']
        df = df[df['amount'] > 0]

        if len(df) == 0:
            print("Нет успешных операций")
            return

        df = df.sort_values('datetime', ascending=False)
        df = df.head(n)
        df = df.sort_values('amount', ascending=False)

        print(f"Последние {n} крупных операций:")
        for idx, row in df.iterrows():
            if row['type'] == 'deposit':
                type_ru = "Пополнение"
            elif row['type'] == 'withdraw':
                type_ru = "Снятие"
            else:
                type_ru = "Другое"
            print(f"Тип: {type_ru}, Сумма: {row['amount']:.2f}, "
                  f"Дата: {row['datetime']}, Баланс после: {row['balance_after']:.2f}")

        return df
