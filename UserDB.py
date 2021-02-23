class UserDB(object):
    def __init__(self, userList=None):
        if userList is not None:
            # Initial sort = O(log(n))
            #TODO Check if it is necessary to sort list here
            userList.sort()
            self.userList = userList
            self._calculateFreeUserIDList()
        else:
            self.userList = []
            self.freeUserIDList = []

    def addUser(self):
        userID = self._getNextUserId()
        self.userList.append(userID)
        print("Current user DB(after add user) ")
        print(self.freeUserIDList)

    def cipherUserDB(self, cipherKey):
        newUserList = []
        #Cipher - O(n)
        #TODO Check how to make this faster...
        for userID in self.userList:
            newUserID = userID ^ cipherKey
            newUserList.append(newUserID)
        self.userList = newUserList
        #TODO Check if it is necessary to sort list here
        self.userList.sort()
        self._calculateFreeUserIDList()

    def _calculateFreeUserIDList(self):
        #TODO Check if it is necessary to recreate list every time. Or maybe we can do it faster.
        freeUserIDList = []
        counter = 0
        for userID in self.userList:
            while counter < userID:
                freeUserIDList.append(counter)
                counter += 1
            counter += 1
        self.freeUserIDList = freeUserIDList
        print("Free numbers ")
        print(freeUserIDList)

    def _getNextUserId(self):
        # Get first element of array - O(1)
        if len(self.freeUserIDList):
            #TODO: Add logic for evaluating max(self.userList)+1
            #TODO: This is another point to investigate asymptotic complexity
            raise NotImplementedError
        else:
            nextUserId = self.freeUserIDList[0]
            self.freeUserIDList = self.freeUserIDList[1:]
        return nextUserId


def workWithUserDB():
    userList = [2, 3, 4, 6, 7]
    userdb = UserDB(userList)
    userdb.cipherUserDB(2)

    print("Current user DB ")
    print(userdb.userList)

    userdb.addUser()
    print("Current user DB after adding user ")
    print(userdb.userList)


if __name__ == '__main__':
    workWithUserDB()
