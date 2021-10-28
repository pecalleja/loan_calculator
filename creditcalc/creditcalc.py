from abc import ABC, abstractmethod
from math import ceil, floor, log
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--type")
parser.add_argument("--principal")
parser.add_argument("--payment")
parser.add_argument("--periods")
parser.add_argument("--interest")

args = parser.parse_args()


class IncorrectParameter(SystemExit):
    def __init__(self, *args, **kwargs):
        print("Incorrect parameters")
        exit()


if args.type not in ["annuity", "diff"]:
    raise IncorrectParameter

if args.type == "diff" and args.payment is not None:
    raise IncorrectParameter

if args.interest is None:
    raise IncorrectParameter

for argument in ["principal", "payment", "periods", "interest"]:
    argument_value = getattr(args, argument)
    if argument_value and float(argument_value) < 0:
        raise IncorrectParameter


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
        result = ceil(self.p * (self.i * mid) / (mid - 1))
        print(f"Your annuity payment = {result}!")
        over_payment = result * self.n - self.p
        return over_payment


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
        over_payment = result * self.a - self.p
        return over_payment

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
        result = floor(self.a / ((self.i * mid) / (mid - 1)))
        print(f"Your loan principal = {result}!")
        over_payment = int(self.a * self.n - result)
        return over_payment


class DifferentiatePaymentCalculation(Calculation):
    def __init__(self, p, n):
        self.p = p
        self.n = n

    def calculate(self):
        total = 0
        for n in range(1, self.n + 1):
            mid = self.p * (n - 1) / self.n
            month_diff = (self.p / self.n) + self.i * (self.p - mid)
            result = ceil(month_diff)
            total += result
            print(f"Month {n}: payment is {result}")
        print()
        over_payment = total - self.p
        return over_payment


if args.type == "diff" and args.principal and args.periods and args.interest:
    principal = int(args.principal)
    periods = int(args.periods)
    formula = DifferentiatePaymentCalculation(principal, periods)
elif args.type == "annuity" and args.principal and args.periods and args.interest and not args.payment:
    principal = int(args.principal)
    periods = int(args.periods)
    formula = MonthlyCalculation(principal, periods)
elif args.type == "annuity" and args.payment and args.periods and args.interest and not args.principal:
    annuity = float(args.payment)
    periods = int(args.periods)
    formula = PrincipalCalculation(annuity, periods)
elif args.type == "annuity" and args.principal and args.payment and args.interest and not args.periods:
    principal = int(args.principal)
    monthly = int(args.payment)
    formula = PeriodsCalculation(principal, monthly)
else:
    raise IncorrectParameter


interest = float(args.interest)
formula.i = interest
overpayment = formula.calculate()
print(f"Overpayment = {overpayment}")
