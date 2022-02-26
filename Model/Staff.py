from datetime import date


class Staff:
    staffId : int
    fullName : str
    gender : str
    idCard : int
    idIssuedDate : date
    idIssuedPlace : str
    birthDay : date
    address : str
    phone : str
    deptId : str
    status : str
    createDate : date
    createUser : str
    updateDate : date
    updateUser : str
    deleteDate : date
    deleteUser : str
    def setStaffId(self, staffId):
        self.staffId = staffId
    def getStaffId(self):
        return self.staffId
    def setFullName(self, fullName):
        self.fullName = fullName
    def getFullName(self):
        return self.fullName
    def setGender(self, gender):
        self.gender = gender
    def getGender(self):
        return self.gender
    def setIdCard(self, idCard):
        self.idCard = idCard
    def getIdCard(self):
        return self.idCard             
    def setIdIssuedDate(self, idIssuedDate):
        self.idIssuedDate = idIssuedDate
    def getIdIssuedDate(self):
        return self.idIssuedDate  
    def setIdIssuedPlace(self, idIssuedPlace):
        self.idIssuedPlace = idIssuedPlace
    def getIdIssuedPlace(self):
        return self.idIssuedPlace  
    def setBirthDay(self, birthDay):
        self.birthDay = birthDay
    def getBirthDay(self):
        return self.birthDay  
    def setAddress(self, address):
        self.address = address
    def getAddress(self):
        return self.address  
    def setPhone(self, phone):
        self.phone = phone
    def getPhone(self):
        return self.phone 
    def setDeptId(self, deptId):
        self.deptId = deptId
    def getDeptId(self):
        return self.deptId  
    def setStatus(self, status):
        self.status = status
    def getStatus(self):
        return self.status  
    def setCreateDate(self, createDate):
        self.createDate = createDate
    def getCreateDate(self):
        return self.createDate  
    def setCreateUser(self, createUser):
        self.createUser = createUser
    def getCreateUser(self):
        return self.createUser  
    def setUpdateDate(self, updateDate):
        self.updateDate = updateDate
    def getUpdateDate(self):
        return self.updateDate  
    def setUpdateUser(self, updateUser):
        self.updateUser = updateUser
    def getUpdateUser(self):
        return self.updateUser  
    def setDeleteDate(self, deleteDate):
        self.deleteDate = deleteDate
    def getDeleteDate(self):
        return self.deleteDate  
    def setDeleteUser(self, deleteUser):
        self.deleteUser = deleteUser
    def getDeleteUser(self):
        return self.deleteUser  
