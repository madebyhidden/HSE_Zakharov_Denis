import Account
import pandas as pd


class CheckingAccount(Account.Account):
    """Класс расчётного счёта (текущий счёт).
    
    Наследуется от Account и используется для основных банковских операций:
    пополнение, снятие средств, переводы на сберегательный счёт.
    """

    account_type = "Checking Account"

    def __init__(self, account_holder, balance=0.0):
        """Инициализирует новый расчётный счёт.
        
        Args:
            account_holder (str): Имя владельца счёта в формате 'Имя Фамилия'
            balance (float, optional): Начальный баланс счёта. По умолчанию 0.0.
        
        Note:
            Номер счёта генерируется автоматически с префиксом 'CHACC-'.
        """
        super().__init__(account_holder, balance)
        # Генерируем уникальный номер счёта с префиксом для расчётного счёта
        self.account_number: str = f'CHACC-{super().account_counter()}'

    def clean_history(self, df: pd.DataFrame) -> pd.DataFrame:
        """Очистка + проверка данных на корректность

        Args:
            df (pd.DataFrame): DataFrame с историей операций.

        Returns:
            pd.DataFrame: Очищенный DataFrame с корректными данными.
        """
        # Извлекаем номер счёта из объекта (последняя часть после дефиса)
        account_num = self.account_number.split('-')[-1]
        # Фильтруем по номеру счёта (извлекаем числовую часть из account_number в файле)
        df["account_num"] = df["account_number"].str.split('-').str[-1]
        df = df[df["account_num"] == account_num]

        df = df[df["account_type"].str.lower() == "checking"]
        df = df[df["status"] == "success"]
        df = df[df["operation"].isin(["deposit", "withdraw"])]
        df = df[df["amount"] > 0]
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df[df["date"].notna()]
        return df

    def load_from_file(self, path: str) -> None:
        """Загрузка истории счёта из файла

        P.S. Я понимаю, что тут по идее надо использовать deposit() и withdraw(), но в моей реализации используется
        автогенерация времени, поэтому нужно использовать ухитрения. А также используется прямое обращение к атрибуту род класса
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
            amount = float(row["amount"])
            dt = row["date"]

            if operation_type == "deposit":
                self._Account__balance += amount
            elif operation_type == "withdraw":
                if self._Account__balance >= amount:
                    self._Account__balance -= amount
                else:
                    continue
            else:
                continue

            formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S")

            if operation_type == "deposit":
                description = f"Добавили {amount} на баланс. Баланс на момент: {self._Account__balance}"
            else:
                description = f"Забрали {amount} с баланса. Баланс на момент: {self._Account__balance}"

            self.operations_history.append([
                description,
                formatted_date,
                "status.Code.Success"
            ])
