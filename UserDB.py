'''Ozon решил придумать новую систему хранения информации пользователей, в данной базе каждому пользователю будет сопоставлен его номер - id (целое неотрицательное число). Так как Ozon — крупная компания, то постоянно регистрируются новые пользователи, для выделения id нового пользователя берется минимальное неотрицательное число, которого еще нет в множестве (боле формально берется Mex набора чисел), например, mex([4, 33, 0, 1, 1, 5]) = 2, а mex([1, 2, 3]) = 0.

К сожалению, любая база должна быть защищена от злоумышленников, для этого иногда базу перестраивают — выбирается какое-то число x и для каждого пользователя его id заменяется на idLx (операци побитового сложения по модулю 2), надо реализовать такую структуру, возвращающую Mex множества и выполняющую операцию шифрования для заданого x.

Формат входных данных
Считайте, что данные подаются в любом удобном вам виде, вам требуется просто реализовать

структуру, выполняющая два вида запросов:

1) Зарегистрировать нового пользователя.

2) Зашифровать все текущие данные с помощью нового ключа x.


Для примера разберем следующий случай :

Пусть изначально у нас есть 2 пользователя с id = 1 и 3, пусть сначала мы решили зашифровать нашу базу с помощью числа 1, затем создать нового пользователя, тогда его номер будет 1, так как база будет состоять из номеров 0 и 2, допустим теперь текущую базу требуется зашифровать еще раз с помощью снова ключа 1, тогда текущая база состоит из чисел 0, 1, 2 и она станет 0, 1, 3, теперь при регистрации нового пользователя нам нужно будет выдать ему номер 2.



Формат выходных данных

Для каждого нового пользователя вывести его id.


Замечание

От вас требуется придумать наиболее оптимальное решение для задачи с точки зрения асимптотики.

'''

import datetime
LOGGER = True


class UserDB(object):
    def __init__(self, userList=None):
        
        if userList is not None:
            self.userList = userList
            print("Initial user list: {0}".format(self.userList))
        else:
            self.userList = []
            
        self._enumerator = Enumerator(self.userList)
        self._buildUserDBIndex()


    def addUser(self):
        userID = self._getNextUserId()
        #print("Adding userID {0}".format(userID))
        self.userList.append(userID)
        
        #print("Current user DB(after add user) {0}: {1}".format(userID, self.userList))

    def cipherUserDB(self, cipherKey):
        print("Cipher by key: {0}".format(cipherKey))
        newUserList = []
        #Cipher - O(n)
        # TODO Check how to make this faster...
        for userID in self.userList:
            newUserID = userID ^ cipherKey
            newUserList.append(newUserID)
        self.userList = newUserList
        self._buildUserDBIndex()
        #print("Current free user DB(after cipherUserDB): {0}".format(self.freeUserIDList))
        #print("Current user DB(after cipherUserDB): {0}".format(self.userList))

    def _calculateFreeUserIDList(self):
        """
        #TODO Check if it is necessary to recreate list every time. Or maybe we can do it faster.
        freeUserIDList = []
        counter = 0
        for userID in self.userList:
            while counter < userID:
                freeUserIDList.append(counter)
                counter += 1
            counter += 1
        self.freeUserIDList = freeUserIDList
        print("Current free user DB: {0}".format(self.freeUserIDList))
        """


    def _buildUserDBIndex(self):
        # Initial sort = O(log(n))
        # TODO Check if it is necessary to sort list here
        self.userList.sort()
        self._enumerator.changeList(self.userList)
        
        

    def _getNextUserId(self):
        # Get first element of array - O(1)
        return self._enumerator.getNextUserId()

class Enumerator(object):
    """
        TODO: Add docstring
        This class works with sorted list of user IDs
    """
    def __init__(self, integerList=None):
        self._freeIntegersList = []
        self._nextInteger = 0
        if integerList is not None:
            self.integerList = integerList
        else:
            self.integerList = []
        self.buildSequence()

    def getNextUserId(self):
        """
        TODO: Add docstring
        """
        nextUserID = self._nextInteger
        self._calculateNextUserID()
        #self.integerList.append(nextUserID)
        return nextUserID

    def changeList(self, newList):
        self.integerList = newList
        self.buildSequence()

    def buildSequence(self):
        """
        TODO: Add docstring
        """
        # TODO Check if it is necessary to recreate list every time. Or maybe we can do it faster.
        # TODO: This is another point to investigate asymptotic complexity
        self._maxIntegerFromList = self.integerList[-1]
        self._freeIntegersList = []

        if len(self.integerList) != 0:
            firstUsedInteger = self.integerList[0]
            counter = 0
            
            if firstUsedInteger != 0:
                self._freeIntegersList.append([0, firstUsedInteger - 1])
                counter = firstUsedInteger  # Start next loop directly from first used element

            for userID in self.integerList:
                
                if userID == counter:
                    counter += 1
                else:
                    self._freeIntegersList.append([counter, userID - 1])
                    counter = userID + 1

        self._calculateNextUserID()
        print("Built seqience of free integers: {0}".format(self._freeIntegersList))
    def _calculateNextUserID(self):
        """
        TODO: Add docstring
        """
         # Get first element of array - O(1)
        if len(self.integerList) == 0:
            self._nextInteger = 0
        else:
            if len(self._freeIntegersList) == 0:
                self._maxIntegerFromList += 1
                self._nextInteger = self._maxIntegerFromList
            else:
                if isinstance(self._freeIntegersList[0], list):
                    self._nextInteger = self._freeIntegersList[0][0]
                    if self._freeIntegersList[0][0] == self._freeIntegersList[0][1]:
                        self._freeIntegersList = self._freeIntegersList[1:]
                    else:
                        self._freeIntegersList[0][0] += 1
                else:
                    self._nextInteger = self._freeIntegersList[0]
                    self._freeIntegersList = self._freeIntegersList[1:]
        #print("Next free integer: {0}".format(self._nextInteger))


        


def workWithUserDB():
    print("Task started at: {0}\n".format(datetime.datetime.now()))
    userList = [100002, 324453, 14151544, 11116564, 54546547]
    userdb = UserDB(userList)
    #userdb.cipherUserDB(2)
    for _ in range(10000):
        userdb.addUser()
    userdb.cipherUserDB(32145)
    print("Length of database: {0}".format(len(userdb.userList)))
    for _ in range(10000):
        userdb.addUser()
    userdb.cipherUserDB(154872)
    print("Length of database: {0}".format(len(userdb.userList)))

    for _ in range(1000000):
        userdb.addUser()
    userdb.cipherUserDB(154872)
    print("Length of database: {0}".format(len(userdb.userList)))

    for _ in range(1000000):
        userdb.addUser()
    userdb.cipherUserDB(4548723)
    print("Length of database: {0}".format(len(userdb.userList)))

    for _ in range(150000000):
        userdb.addUser()
    userdb.cipherUserDB(13235478)
    print("Length of database: {0}".format(len(userdb.userList)))

    print("Task completed at: {0}\n".format(datetime.datetime.now()))
    
    """
    for _ in range(10):
        userdb.addUser()
    print("Current user DB(before cipherUserDB): {0}".format(userdb.userList))
    print("Cipher started at: {0}\n".format(datetime.datetime.now()))
    userdb.cipherUserDB(100)
    print("Cipher completed at: {0}\n".format(datetime.datetime.now()))
    print(userdb.maxUserID)
    print("Current user DB(after cipherUserDB): {0}".format(userdb.userList))
"""

# Идеи:
# - Использовать промежутки значений вместо самих значений "пропусков"(чтобы не загромождать базу)
#   - Это можно сделать только для первого промежутка
#       - Реализовать запись промежутка для первого значения
#       - Реализовать получение номера и смещение текущего счетчика
#       - Вынести все это в отдельный класс ""
# # - Изучить глубже функцию побитового сложения - ее свойства и примерение в зависимости от отношения чисел в операции
    # Построить график побитового сравнения

if __name__ == '__main__':
    workWithUserDB()
