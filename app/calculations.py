def add(n1:int, n2:int):
    return( n1 + n2)

def divide(n1:int, n2:int):
    return(n1 / n2)


def subtract(n1:int, n2:int):
    if n1 > n2:
        return(n1 - n2)
    else:
        return(n2 - n1)
    
def multiply(n1:int, n2:int):
    return(n1 * n2)


class InsufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance
        
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Insufficient Funds ")
        self.balance -= amount
    
    def collect_interest(self):
        self.balance *= 1.1