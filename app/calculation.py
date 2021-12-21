
def add(x1, x2= 2):
    return x1+ x2 


def sub(x1, x2=2):
    return x1 -x2 

def mul(x1, x2=2):
    return x1 * x2 

def div (x1, x2=2):
    return x1 / x2 


class InsufficientFund(Exception):
    def __init__(self, message) -> None:
        self.message = message


class BankAccount():
    def __init__(self, starting_balance=0) -> None:
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount 

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFund ("ERROR: Insufficient Funds")
        self.balance -= amount
    
    def collect_interest(self):
        self.balance *= 1.1 
