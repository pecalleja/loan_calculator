from abc import ABC, abstractmethod
from math import ceil, floor, log


class Calculation(ABC):
    _i: float

    @abstractmethod
    def calculate(self):
        raise NotImplementedError

    @property
    def i(self):
        return self._i

    @i.setter
    def i(self, value):
        self._i = value / (12 * 100)


class MonthlyCalculation(Calculation):
    def __init__(self, p, n):
        self.p = p
        self.n = n

    def calculate(self):
        mid = (1 + self.i) ** self.n
        result = self.p * (self.i * mid) / (mid - 1)
        print(f"Your monthly payment = {ceil(result)}!")


class PeriodsCalculation(Calculation):
    def __init__(self, p, a):
        self.p = p
        self.a = a

    def calculate(self):
        x = self.a / (self.a - self.i * self.p)
        base = 1 + self.i
        result = ceil(log(x, base))
        years = result // 12
        months = result - (years * 12)
        months_text, year_text = self.years_month_text(months, years)

        print(f"It will take {year_text}{months_text} to repay this loan!")

    def years_month_text(self, months, years):
        if years > 1:
            year_text = f"{years} years"
        elif years == 1:
            year_text = "1 month"
        else:
            year_text = ""
        if year_text and months:
            year_text += " and "
        if months > 1:
            months_text = f"{months} months"
        elif months == 1:
            months_text = "1 month"
        else:
            months_text = ""
        return months_text, year_text


class PrincipalCalculation(Calculation):
    def __init__(self, a, n):
        self.a = a
        self.n = n

    def calculate(self):
        mid = (1 + self.i) ** self.n
        result = self.a / ((self.i * mid) / (mid - 1))
        print(f"Your loan principal = {floor(result)}!")


print("What do you want to calculate?")
print('type "n" for number of monthly payments')
print('type "a" for annuity monthly payment amount')
print('type "p" for loan principal:')
option = input()

if option == "n":
    print("Enter the loan principal:")
    principal = int(input())
    print("Enter the monthly payment:")
    monthly = int(input())
    formula = PeriodsCalculation(principal, monthly)

elif option == "a":
    print("Enter the loan principal:")
    principal = int(input())
    print("Enter the number of periods:")
    periods = int(input())
    formula = MonthlyCalculation(principal, periods)

elif option == "p":
    print("Enter the annuity payment:")
    annuity = float(input())
    print("Enter the number of periods:")
    periods = int(input())
    formula = PrincipalCalculation(annuity, periods)

else:
    raise ValueError("Invalid option")

print("Enter the loan interest:")
interest = float(input())
formula.i = interest
formula.calculate()
