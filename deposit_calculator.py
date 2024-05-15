from datetime import datetime
from dateutil.relativedelta import relativedelta


class DepositCalculator(object):
    def __init__(self, raw_deposit_dict: dict):
        '''
        todo
        '''
        self.raw_deposit_dict = raw_deposit_dict
        self.is_valid, self.validation_msg = self._validate_data()
        if self.is_valid:
            self.date = self.raw_deposit_dict["date"]
            self.periods = self.raw_deposit_dict["periods"]
            self.amount = self.raw_deposit_dict["amount"]
            self.rate = self.raw_deposit_dict["rate"]

    def _validate_data(self) -> tuple[bool, str]:
        '''
        todo
        '''
        if "date" in self.raw_deposit_dict:
            date = self.raw_deposit_dict["date"]
            try:
                date = datetime.strptime(date, "%d.%m.%Y")
            except (ValueError, TypeError):
                return False, "date must be in format [dd.mm.YYYY]"
        else:
            return False, "request must have date:[dd.mm.YYYY] in data"
        
        if "periods" in self.raw_deposit_dict:
            periods = self.raw_deposit_dict["periods"]
            try:
                if isinstance(periods, int) and (1 <= periods <= 60):
                    pass 
                else:
                    return False, "periods must be in format [1 <= int <= 60]"
            except (ValueError, TypeError):
                return False, "periods must be in format [1 <= int <= 60]"
        else:
            return False, "request must have periods: [1 <= int <= 60] in data"
        
        if "amount" in self.raw_deposit_dict:
            amount = self.raw_deposit_dict["amount"]
            try:
                if isinstance(amount, int) and (10000 <= amount <= 3000000):
                    pass
                else:
                    return False, "amount must be in format [10000 <= int <= 3000000]"
            except (ValueError, TypeError):
                return False, "amount must be in format [10000 <= int <= 3000000]"
        else:
            return False, "request must have amount:[10000 <= int <= 3000000] in data"

        if "rate" in self.raw_deposit_dict:
            rate = self.raw_deposit_dict["rate"]
            try:
                if isinstance(float(rate), float) and (1.0 <= float(rate) <= 8.0):
                    pass 
                else:
                    return False, "rate must be in format [1.0 <= float <= 8.0]"
            except (ValueError, TypeError):
                return False, "rate must be in format [1.0 <= float <= 8.0]"
        else:
            return False, "request must have rate:[1.0 <= float <= 8.0] in data"
    
        return True, "correct data format"

    def calculate_deposit(self) -> tuple[dict, str]:
        '''
        todo
        '''
        deposit_dict = {}
        if self.is_valid:
            amount = self.amount 
            month_rate = self.rate / 12 / 100
            request_date = datetime.strptime(self.date, "%d.%m.%Y")
            date = request_date
            for i in range(self.periods):
                amount = amount*(1 + month_rate)
                date_str = date.strftime("%d.%m.%Y")
                deposit_dict[date_str] = round(amount, 2)
                date = request_date + relativedelta(months=1+i)
            return deposit_dict, self.validation_msg
        else:
            return deposit_dict, self.validation_msg


if __name__ == "__main__":
    data = {
        "date": "31.01.2021",
        "periods": 20,
        "amount": 10000,
        "rate": 6
    }
    deposit_calculator = DepositCalculator(data)
    deposit_dict, validation_msg = deposit_calculator.calculate_deposit()
    for key in deposit_dict:
        print(f"{key}: {deposit_dict[key]}")
