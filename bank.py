from enum import Enum
import time

cardAuthKey = 1234567890

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
            #self.balance -= amount
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
    
    def openCashBin(self):
        pass


class Card:
    def __init__(self, cardnumber, pinCode): #when issuing a new ATM card, create a new instance of this class.
        self.cardnumber = cardnumber
        self.pinCode = pinCode
        self.unsuccessfulAttempts = 0
        self.unlocked = False
        #self.accountNumberSet = set()
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

class enumTransactionState(Enum):
    IDLE = 0
    WITHDRAW = 1
    DEPOSIT = 2

class Account:
 
    def __init__(self, accountNumber, balance, pinCode): #let's just ignore the holder's name, SSN, etc for now.
        self.accountNumber = accountNumber
        self.pinCode = pinCode
        self.balance = balance
        self.cardNumberSet = set() # A single account may have multiple cards associated with it.
        self.transactionState = enumTransactionState.IDLE

    def getAccountNumber(self):
        return self.accountNumber
    
    def getBalance(self):
        if self.transactionState != enumTransactionState.IDLE:
            return False
        return self.balance
    
    def setBalance(self, balance):
        if self.transactionState != enumTransactionState.IDLE: #if the account is in the middle of a transaction, reject the transaction.
            return False
        self.balance = balance
        return self.balance
    
    def getPinCode(self):
        return self.pinCode

    def withdraw(self, amount):
        if self.transactionState != enumTransactionState.IDLE:
            return False
        self.transactionState = enumTransactionState.WITHDRAW
        if self.balance < amount:
            self.transactionState = enumTransactionState.IDLE
            return False
        self.balance -= amount
        self.transactionState = enumTransactionState.IDLE
        return True
    
    def deposit(self, amount):
        if self.transactionState != enumTransactionState.IDLE:
            return False
        self.transactionState = enumTransactionState.DEPOSIT
        self.balance += amount
        self.transactionState = enumTransactionState.IDLE
        return True

class ServerCardData:
    def __init__(self, cardNumber, cardAuthKey):
        self.cardNumber = cardNumber
        self.cardAuthKey = cardAuthKey
        self.accountNumberSet = set()

class Server: # a single bank server, multiple ATMs are connected to it. stands for a single bank.

    # class cardAuthKey:
    #     def __init__(self, cardNumber, cardAuthKey):
    #         self.cardNumber = cardNumber
    #         self.cardAuthKey = cardAuthKey

    def __init__(self, bankName):
        self.bankName = bankName
        self.accountSet = set()
        self.cardDataSet = set()

    def getBankName(self):
        return self.bankName
        

    def issueCard(self, cardNumber, cardAuthKey, pinCode): #issue a new card to a customer.
        if any(cardNumber == c.cardNumber for c in self.cardDataSet): #colliding card number
            return False
        self.cardDataSet.add(ServerCardData(cardNumber, cardAuthKey))
        return Card(cardNumber, pinCode)
    
    def authCard(self, cardNumber, cardAuthKey): #verify the card is authentic.
        for i in self.cardDataSet:
            if i.cardNumber == cardNumber and i.cardAuthKey == cardAuthKey:
                return True
        return False
    
    def getAccountList(self, cardNumber, cardKey): #returns a list of account numbers associated with the card.
        if(self.authCard(cardNumber, cardKey)):
            for i in self.cardDataSet:
                if i.cardNumber == cardNumber:
                    return i.accountNumberSet
    
    def verifyNewAccountNumber(self, newAccountNumber):
        for i in self.accountSet:
            if i.getAccountNumber() == newAccountNumber:
                return False
        return True

    def openAccount(self, accountNumber, balance, pinCode):
        if self.verifyNewAccountNumber(accountNumber):
            newAccount = Account(accountNumber, balance, pinCode)
            self.accountSet.add(newAccount)
            return newAccount
        return False
    
    def addCardToAccount(self, accountNumber, cardNumber):
        for i in self.accountSet:
            if i.getAccountNumber() == accountNumber:
                i.cardNumberSet.add(cardNumber)
        for i in self.cardDataSet:
            if i.cardNumber == cardNumber:
                i.accountNumberSet.add(accountNumber)

    def getBalance(self, cardNo, cardAuthKey, accountNo, pinCode):
        if not self.authCard(cardNo, cardAuthKey):
            #print('Card not authenticated.')
            return False
        for i in self.accountSet:
            if i.getAccountNumber() == accountNo and i.getPinCode() == pinCode:
                #print('Success')
                return i.getBalance()
        #print('Account not found or pincode mismatches.')
        return False
    
    def withdraw(self, cardNo, cardAuthKey, accountNo, pinCode, amount):
        if not self.authCard(cardNo, cardAuthKey):
            return False
        for i in self.accountSet:
            if i.getAccountNumber() == accountNo and i.getPinCode() == pinCode:
                if i.withdraw(amount): #if the transaction is successful
                    return i.getBalance()
                else:
                    return False
        return False

    def deposit(self, cardNo, cardAuthKey, accountNo,amount):
        if not self.authCard(cardNo, cardAuthKey):
            return False
        for i in self.accountSet:
            if i.getAccountNumber() == accountNo:
                return i.deposit(amount)
        return False

class ATM: # a single ATM machine
    def __init__(self, server):
        self.cardReader = CardReader() #a physical card reader
        self.cashBin = cashBin(10000, 100000) #initial balance of $10K, max capacity of $100K
        self.server = server #reference to its bank server
        #self.card = None #reference to the card inserted
        self.accountNo = None #reference to the account selected
    
    #def insertCard(self, cardObj): # to be integrated with a physical card reader
        #self.card = cardObj
    
    def inquireAccountList(self): #Error checks are honestly abundant, as the control flow of the caller prevents any errors from happening.
        if not self.cardReader.hasCard:
            return False
        if not self.cardReader.card.isUnlocked():
            return False
        return self.server.getAccountList(self.cardReader.card.getCardNumber(), self.cardReader.card.getCardKey())

    def withdrawMenu(self):
        print('== Withdraw ==')
        print('Account Number: ' + str(self.accountNo) + '\n')

        pinCode = None
        while True:
            pinCode = input('Please enter your account PIN code. Type "exit" to cancel the transaction: ')
            if pinCode == 'exit':
                return
            balance = self.server.getBalance(self.cardReader.card.getCardNumber(), self.cardReader.card.getCardKey(), self.accountNo, int(pinCode))
            if balance >= 0:
                print('Balance: ' + str(balance) + '\n')
                break
            else:
                print('PIN code incorrect. Please try again.\n')

        amount = input('Please enter the amount you wish to withdraw. Type "exit" to cancel the transaction: ')
        if amount == 'exit':
            return
        amount = int(amount)
        if self.cashBin.withdrawCheck(amount):
            balance = self.server.withdraw(self.cardReader.card.getCardNumber(), self.cardReader.card.getCardKey(), self.accountNo, int(pinCode), amount)
            if balance:
                print('Balance: ' + str(balance) + '\n')
                self.cashBin.withdrawCommit(amount)
                print('Please collect your cash.\n')
                return
            else:
                print('Error processing withdraw. Insufficient balance.\n')
                return
        else:
            print('Insufficient cash in the ATM. Please try again.\n')
            return

    
    def depositMenu(self):
        print('== Deposit ==')
        print('Account Number: ' + str(self.accountNo) + '\n')

        print('Please insert your cash into the cash bin.')
        amount = self.cashBin.readDepositAmount()
        if self.cashBin.depositCheck(amount):
            if self.server.deposit(self.cardReader.card.getCardNumber(), self.cardReader.card.getCardKey(), self.accountNo, amount):
                self.cashBin.depositCommit(amount)
                return
            else:
                print('Error processing deposit. Please try again.\n')
                self.cashBin.openCashBin()
                return
        else:
            print('Error processing cash. This might be because the cash reserve is full.\n')
            self.cashBin.openCashBin()
            return

    def checkBalanceMenu(self):
        print('== Check Balance ==')
        print('Account Number: ' + str(self.accountNo) + '\n')
        while True:
            pinCode = input('Please enter your account PIN code. Type "exit" to cancel the transaction: ')
            if pinCode == 'exit':
                return
            balance = self.server.getBalance(self.cardReader.card.getCardNumber(), self.cardReader.card.getCardKey(), self.accountNo, int(pinCode))
            if balance >= 0:
                print('Balance: ' + str(balance) + '\n')
                return
            else:
                print('PIN code incorrect. Please try again.\n')
            
    def returnToMainMenu(self):
        print('Thank you for using ' + self.server.getBankName() + ' ATM.')
        self.cardReader.ejectCard()
        print('Please collect your card.\n')

    def mainMenu(self):
        print('Welcome to ' + self.server.getBankName() + ' ATM')
        print('Please insert your card to begin.')
        #Test Code~
        print('-- Since this is a test program, a mockup card will be inserted after 3 seconds. --\n')
        time.sleep(3)
        self.cardReader.insertCard(testCard)
        #~Test Code
        while not self.cardReader.hasCard:
            pass
        while True:
            print('Please enter your ATM card PIN code. Type "exit" to cancel the transaction.')
            print('-- Since this is a test program, the PIN code is 1234. --\n')
            print('PIN: ', end='')
            pinCode = input()
            if pinCode == 'exit':
                self.returnToMainMenu()
                return
            if self.cardReader.unlockCard(pinCode):
                print('Pincode verified!\n')
                break
            else:
                print('Pincode incorrect. Please try again.\n')

        print('Please select an account to proceed.')
        accountNumberList = list(self.inquireAccountList())
        #print(accountNumberList)

        if(len(accountNumberList) == 0):
            print('No account associated with this card.')
            print('Please contact your bank for more information.')
            self.returnToMainMenu()
            return
        
        for i in range(len(accountNumberList)):
            print(str(i) + ': ' + str(accountNumberList[i]))
        
        while True:
            print('Please enter the number of the account you wish to access. Type "exit" to cancel the transaction.')
            index = int(input())
            if index >= len(accountNumberList) or index < 0:
                print('Invalid input. Please try again.')
                continue
            self.accountNo = accountNumberList[index]
            break

        while True:
            print('Please select an action.')
            print('1. Withdraw')
            print('2. Deposit')
            print('3. Check Balance')
            print('4. Exit')
            print('Action: ', end='')
            action = input()
            if action == '1':
                self.withdrawMenu()
            elif action == '2':
                self.depositMenu()
            elif action == '3':
                self.checkBalanceMenu()
            elif action == '4':
                self.returnToMainMenu()
                return
            else:
                print('Invalid input. Please try again.')
                continue

    def loop(self):
        while True:
            self.mainMenu()

testServer = Server('bearBank')
testCard = testServer.issueCard(123456789, cardAuthKey, 1234) #CardNo, CardKey, PIN
testAccount = testServer.openAccount(123456789, 0, 1234)
testServer.addCardToAccount(123456789, 123456789) #CardNo, AccountNo
testATM = ATM(testServer)
testATM.loop()