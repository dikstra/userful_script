from orm_ope import GetAccount,GetAllAccount,InsertAccount,DeleteAccount
from faker import Factory
import random
import hashlib

faker = Factory.create()

if __name__ == '__main__':
    for i in range(10):
        user = faker.name()
        md5 = hashlib.md5()
        md5.update(faker.word().encode())
        password = md5.hexdigest()
        InsertAccount(user=user,password=password,salary=round(random.random()*10000,2))
