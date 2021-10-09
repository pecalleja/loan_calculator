from math import ceil
# loan_principal = 'Loan principal: 1000'
# final_output = 'The loan has been repaid!'
# first_month = 'Month 1: repaid 250'
# second_month = 'Month 2: repaid 250'
# third_month = 'Month 3: repaid 500'
#
# # write your code here
# print("Loan principal: 1000")
# print("Month 1: repaid 250")
# print("Month 2: repaid 250")
# print("Month 3: repaid 500")
# print("The loan has been repaid!")
print("Enter the loan principal:")
principal = int(input())
print('What do you want to calculate?')
print('type "m" - for number of monthly payments,')
print('type "p" - for the monthly payment:')
option = input()
months = 0
payments = 0
if option == "p":
    print("Enter the number of months:")
    months = int(input())
    result = ceil(principal/months)
    last = principal - (result * (months - 1))
    print(f"Your monthly payment = {result} and the last payment = {last}.")
elif option == "m":
    print("Enter the monthly payment:")
    payments = int(input())
    result = ceil(principal/payments)
    print(f"It will take {result} month{'s' if result>1 else ''} to repay the loan")
else:
    raise ValueError("Invalid option")

