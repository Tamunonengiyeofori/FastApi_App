from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds
import pytest

@pytest.mark.parametrize(
    "n1 , n2 , result" , [(3, 2, 5), (4, 6, 10), (10, 15, 25)] )
def test_add(n1, n2, result):
    print("testing calculations")
    # sum = add(5, 3)
    assert add(n1, n2) == result
    
@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture()
def bank_account():
    bank_account = BankAccount(100)
    return bank_account

def test_subtract():
    assert subtract(9 , 5) == 4
    
def test_multiply():
    assert multiply(2 , 3) == 6
    
def test_divide():
     assert divide(5, 2) == 2.5
     
def test_bank_set_initial_amount(bank_account):
    # bank_account = BankAccount(50)
    assert bank_account.balance == 100

def test_bank_default_amount(zero_bank_account):
    # bank_account = BankAccount()
    assert zero_bank_account.balance == 0
    
def test_withdraw(bank_account):
    # bank_account = BankAccount(100)
    bank_account.withdraw(30)
    assert bank_account.balance == 70
    
def test_deposit(bank_account):
    # bank_account = BankAccount(50)
    bank_account.deposit(30)
    assert bank_account.balance == 130
    
def test_calaculate_interest(bank_account):
    # bank_account = BankAccount()
    balance_before_int = bank_account.balance
    bank_account.collect_interest()
    # interest = bank_account.balance - balance_before_int
    assert bank_account.balance == (balance_before_int * 1.1 )

@pytest.mark.parametrize(
    "deposited , withdrawn , expected" , [(200, 120, 80), (54, 6, 48), (12000, 1500, 10500)] )    
def test_bank_transaction(zero_bank_account, deposited, withdrawn, expected): 
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    assert zero_bank_account.balance == expected
    

def test_insuffifient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)