import pytest

from app.calculation import add , sub, mul, div, BankAccount, InsufficientFund
## Creating a Fixture for our Bank account class 

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize(
    "num1, num2, result", 
    [ (3,3,6), 
    (4,2,6),
    (4,5,9),
    (1,3,4)  ]
)
def test_add(num1, num2,result ):
    assert add(num1, num2) == result


def test_sub():
    assert sub(9,5) == 4

def test_mul():
    assert mul(1,2) == 2

def test_div():
    assert div(4,2) == 2



def test_bank_set_init_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_withdraw_amount(bank_account):
    bank_account.withdraw(50)
    assert bank_account.balance ==  0

def test_bank_deposit_amount(bank_account):
    bank_account.deposit(10)
    assert bank_account.balance == 60

def test_bank_interest_amount(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 2) == 55.00
    
@pytest.mark.parametrize(
    "deposited, withdraw, result", 
    [ (500,300,200), 
    (400,200,200),
    (400,400,0),
    (1000,300,700)  ]
)
def test_bank_transaction(zero_bank_account, deposited, withdraw,result):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == result


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFund):
        bank_account.withdraw(200)


