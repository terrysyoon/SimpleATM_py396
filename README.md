# Simple ATM Controller

Date: Aug 1st, 2023

Author: Terry

yoonsb@hanyang.ac.kr

This wiki is to archive the project, “Implement a simple ATM controller”

## Given Requirements

At least the following flow should be implemented:

Insert Card => PIN number => Select Account => See Balance/Deposit/Withdraw

For simplification, there are only 1 dollar bills in this world, no cents. Thus account balance can be represented in integer.

Your code doesn't need to integrate with a real bank system, but keep in mind that we may want to integrate it with a real bank system in the future. It doesn't have to integrate with a real cash bin in the ATM, but keep in mind that we'd want to integrate with that in the future. And even if we integrate it with them, we'd like to test our code. Implementing bank integration and ATM hardware like cash bin and card reader is not a scope of this task, but testing the controller part (not including the bank system, cash bin, etc) is within the scope.

A bank API wouldn't give the ATM the PIN number, but it can tell you if the PIN number is correct or not.

Based on your work, another engineer should be able to implement the user interface. You don't need to implement any REST API, RPC, network communication etc, but just functions/classes/methods, etc.

You can simplify some complex real-world problems if you think it's not worth illustrating in the project.

## Verified to run on this system

Operating System: macOS Ventura 13.4.1 (Apple Silicon)

Python: Version 3.9.6

No special packages or pre-install dependencies are required.

## How to run

### Clone

Clone this git repository as it is from CLI or a git client of your choice. Please be sure that you are on the master branch.

### Run

Since this repository only contains a single Python file, just locate your terminal to the repository directory and run the following shell script.

```bash
python3 bank.py
```

![Screenshot 2023-08-01 at 10.44.37 PM.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/Screenshot_2023-08-01_at_10.44.37_PM.png)

Upon successful firing up, you should see the welcoming script above.

# Test Scenarios

```python
testServer = Server('bearBank')
testCard = testServer.issueCard(123456789, cardAuthKey, 1234) #CardNo, CardKey, PIN
testAccount = testServer.openAccount(123456789, 0, 1234)
testServer.addCardToAccount(123456789, 123456789) #CardNo, AccountNo
testATM = ATM(testServer)
testATM.loop()
#The bottom of the source code
```

Currently the bank, ‘bearBank’, has one bank account open and one ATM card issued, which the number of both are ‘123456789’ and the pincode is ‘1234’. 

A bank account may have multiple ATM cards associated with it and the card may also be linked to multiple accounts.

![bank.drawio.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/bank.drawio.png)

## Inserting an ATM card and checking PIN

![Screenshot 2023-08-02 at 12.17.11 AM.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/Screenshot_2023-08-02_at_12.17.11_AM.png)

A real ATM, it would wait for a user to insert their card.

For this mockup, the testing card described above is automatically loaded. Please enter the pin code ‘1234’ and proceed to selecting bank accounts.

***Error Case***

![Screenshot 2023-08-02 at 12.50.36 AM.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/Screenshot_2023-08-02_at_12.50.36_AM.png)

When you enter the wrong passcode, it asks you to give another try.

## Select an account

![Screenshot 2023-08-02 at 12.20.02 AM.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/Screenshot_2023-08-02_at_12.20.02_AM.png)

Once you successfully pass the pin code verification, the ATM contacts with the bank server to inquire the accounts linked to this ATM card.

Type the index on the left side of the column to select the account displayed as a listing. (It must be 0 in this case.)

***Error Case***

![Screenshot 2023-08-02 at 12.51.34 AM.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/Screenshot_2023-08-02_at_12.51.34_AM.png)

When you input an index that does not fall on the given list, it asks you again.

When no account is linked to the ATM card, a situation which can be demonstrated by commenting out a single line from the source code,

```python
testServer = Server('bearBank')
testCard = testServer.issueCard(123456789, cardAuthKey, 1234) #CardNo, CardKey, PIN
testAccount = testServer.openAccount(123456789, 0, 1234)
#testServer.addCardToAccount(123456789, 123456789) #CardNo, AccountNo
testATM = ATM(testServer)
testATM.loop()
```

![Screenshot 2023-08-02 at 12.55.02 AM.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/Screenshot_2023-08-02_at_12.55.02_AM.png)

It aborts the transaction and returns the ATM card.

## Make transaction

Once you select your account, this transaction selection menu pops up.

### Withdraw

![Screenshot 2023-08-02 at 12.40.30 AM.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/Screenshot_2023-08-02_at_12.40.30_AM.png)

Choose withdraw action from the main transaction loop.

After you type the correct pin for your account, the machine shows your current balance.

Once the transaction is confirmed, the machine displays the updated balance and dispenses the requested amount of cash.

***Error Case***

![Screenshot 2023-08-02 at 12.46.44 AM.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/Screenshot_2023-08-02_at_12.46.44_AM.png)

- When you enter the wrong passcode, it asks you to give another try.
- The machine rejects the transaction when your balance shorts on your requested transaction value.

***Exit***

![Screenshot 2023-08-02 at 12.49.11 AM.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/Screenshot_2023-08-02_at_12.49.11_AM.png)

Typing ‘exit’ instead of a pin will bring you to the main transaction loop again.

### Deposit

![Screenshot 2023-08-02 at 12.31.34 AM.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/Screenshot_2023-08-02_at_12.31.34_AM.png)

Choose deposit action from the main transaction loop.

It does not show the balance of the account before or after the transaction as deposits do not require pin code.

***Error Case***

![Screenshot 2023-08-02 at 12.34.00 AM.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/Screenshot_2023-08-02_at_12.34.00_AM.png)

When the cash bin report that it cannot hold the inserted amount of cash, the ATM aborts the transaction and opens the cash door to return them to the user.

### Check Balance

![Screenshot 2023-08-02 at 12.23.43 AM.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/Screenshot_2023-08-02_at_12.23.43_AM.png)

Type the pin code for the account to view its balance.

***Error Case***

![Screenshot 2023-08-02 at 12.27.15 AM.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/Screenshot_2023-08-02_at_12.27.15_AM.png)

The machine will ask for the code again if the user fails to provide the correct account pin.

***Exit***

![Screenshot 2023-08-02 at 12.29.05 AM.png](Simple%20ATM%20Controller%20b777e8add63b4eca8e67e202e0f74bf1/Screenshot_2023-08-02_at_12.29.05_AM.png)

Typing ‘exit’ instead of a pin will bring you to the main transaction loop again.

## Designs

Directed that the project must be future ready for integrating with real banking equipments and systems, I tried to make the source code more modular and mimic how transactions are verified in the real word. 

### General Information

In the real word, the pin code for a chip enabled ATM card is recorded in the secure element of the card, and the card provides data required to establish a transaction only when it successfully verifies the code entered from a card reader.

This explains the intention of my design regarding the class ***Card*** and ***CardReader***.

The authentication key in an ATM card is accessible when the card is unlocked with the correct pin code, and this code is sent to the bank system to verify if the ATM card is legitimate.

Speaking of the real world banking equipment, I constructed the class ***cashBin***, which acts as an abstract version of a physical one and hopefully the real one will work right away as I expect it would have pretty much the same interface with the model I developed.

The class ***Server*** and ***Account*** are introduced to symbolize a main banking infrastructure for a bank and a checking account respectively.

### By individual class

**CardReader**

```python
class CardReader:
    def __init__(self):
        self.hasCard = False
        self.card = None
    def insertCard(self, card):
        self.hasCard = True;
        self.card = card
    def ejectCard(self):
        self.card.lockCard()
        self.hasCard = False;
        self.card = None
    def unlockCard(self, pinCode):
        if self.hasCard:
            return self.card.verifyPin(pinCode)
        print('No card inserted.')
        return False
```

Models a physical card reader in an ATM.

- hasCard: If the reader has its card slot filled.
- card: Reference to the card object it has inserted.

**Card**

```python
class Card:
    def __init__(self, cardnumber, pinCode): #when issuing a new ATM card, create a new instance of this class.
        self.cardnumber = cardnumber
        self.pinCode = pinCode
        self.unsuccessfulAttempts = 0
        self.unlocked = False
        self.cardKey = cardAuthKey #this is to verify the card is authentic. This is a private key that is only known to the bank.
    
    def getCardNumber(self):
        if(self.unlocked):
            return self.cardnumber
        return ''
    
    def getCardKey(self):
        if(self.unlocked):
            return self.cardKey
        return ''
    
    def verifyPin(self, pinCode):
        self.unlocked = False
        #print('enterd: ' + str(pinCode) + ' expected: ' + str(self.pinCode))
        if int(self.pinCode) == int(pinCode):
            self.unsuccessfulAttempts = 0
            self.unlocked = True
            #print('unlocked')
            return True
        else:
            self.unsuccessfulAttempts += 1
            return False
        
    def isUnlocked(self):
        return self.unlocked
    
    def lockCard(self): #when you finished your transaction, lock the card upon ejecting.
        self.unlocked = False
```

Models a single ATM card.

- cardnumber: The cardnumber that is printed on the ATM card.
- pinCode: The pin code the card holder must enter to authorize a transaction.
- unsucessfulAttempts: How many attempts in a row failed to verify the pin code, although it does not have any functionality as of now.
- unlocked: If the pincode has been verified once after the card is inserted into an ATM machine. The secure element is expected to return credentials only when this flag is set.
- cardKey: The authentication code that is sent to the bank to proceed a transaction.

**cashBin**

```python
class cashBin:
    def __init__(self, balance, maxCapacity):
        self.balance = balance
        self.maxCapacity = maxCapacity #max capacity of the dispenser. in $1 notes.

    def getBalance(self):
        return self.balance
    
    def setBalance(self, balance): #when a banker fills the dispenser up.
        self.balance = balance
        return self.balance
    
    def withdrawCheck(self, amount):
        if(self.getBalance() < amount): #dispenser shorts on cash, reject the transaction
            return False
        else:
            return True

    def withdrawCommit(self, amount):
        self.balance -= amount
        print('CashBin> Dispensing $' + str(amount) + '...')
        return self.balance

    def depositCheck(self, amount):
        if(self.getBalance() + amount > self.maxCapacity): #dispenser overflows, reject the transaction
            return False
        else:
            #self.balance += amount
            return True
        
    def depositCommit(self, amount):
        self.balance += amount
        return self.balance
    
    def readDepositAmount(self): #read the amount of cash deposited. To be integrated with the hardware team.
        amount = input('CashBin> Please enter the amount of cash deposited: ')
        return int(amount)
    
    def openCashBin(self): #when deposit is aborted, return the money.
        pass
```

Models a physical cash window and storage.

- balance: The amount of cash in the storage currently.
- maxCapacity: The amount of cash the storage may hold at maximum.