import mysql.connector
import getPredictions
from getPredictions import getPredictions
import pandas as pd
import pyodbc


mydb = mysql.connector.connect(

    host = "localhost",
    user = "padfoot",
    password = "03051998@Sanu",
    database = "CompanyDetails"
)
# companyName = "niravmodi"

mycursor = mydb.cursor()
if mydb.is_connected:
    print("database connected ")
else:
    print("not yet")

def companyAlreadyPresent(companyName):
       q1 = "select * from PreviousCompanyDetails where companyName = %s"
       mycursor.execute(q1, (companyName,))
       myresult = mycursor.fetchall()
       if len(myresult) == 0:
           return False
       else:
           return True

# print(companyAlreadyPresent(companyName))     

def creatingNewtable(companyName):
    q2 = """CREATE TABLE `% s` (urls varchar(500), label varchar(50))"""%(companyName)

    if companyAlreadyPresent(companyName) == False:
        mycursor.execute(q2)
    else:
        print("companyAlreadyPresent")

# creatingNewtable(companyName)

def insertDataInCompanyAlreadyPresent(companyName):
    try:
        q3 = """ INSERT INTO PreviousCompanyDetails(companyName , done) VALUES(%s , %s)"""
        valueTuple = (companyName , 100)
        mycursor.execute(q3 , valueTuple)
        mydb.commit()
        print("values Inserted")
        return True
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
        return False
    
# insertDataInCompanyAlreadyPresent(companyName);
# companyData = pd.DataFrame(columns= ('url','label'))
# companyData = "abcd";

def insertCvsData(companyName , companyData):
   
    for row in companyData.itertuples():
        #  print(row.url , row.label)
         urlInput = row.url
         labelInput = row.label
         q4 = "INSERT INTO "+companyName+" (urls , label) VALUES (%s , %s)"
         valueTuple = (urlInput,labelInput)
         mycursor.execute(q4 , valueTuple)
    
    mydb.commit()
    print("data Inserted")

# def insertCvsDataCheck(companyName , companyData):
#     urlInput = "ajfkjdbbgbjjbdfg"
#     labelInput = "dbbfdjbgdb"
#     q4 = "INSERT INTO "+companyName+" (urls , label) VALUES (%s , %s)"
#     valueTuple = (urlInput,labelInput)
#     mycursor.execute(q4 , valueTuple)
#     mydb.commit()
#     print("data Inserted")

# insertCvsDataCheck(companyName , companyData)

#algo behind the seen

#first company name inserted in form
#then code check it is is already present or scanned previously 
#if it is present it will not scan that company
#if it is not the it scan the url and create a new table in database of company name with atributes urls and lable
#also inserted company name in companyAlreadyPresent table for the track recode
 


def finalAlgorithm(companyName):
    if companyAlreadyPresent(companyName):
        print("already Scanned")
    else:
        print("url Fetching Start")
        companyData = getPredictions(companyName)
        print("Url fetching done and data insertion start")
        print("creating table")
        creatingNewtable(companyName)
        print("table created")
        print("data insertion start")
        insertCvsData(companyName , companyData)
        print("data insertion done")
        insertDataInCompanyAlreadyPresent(companyName)



def multipleCompany(multipledata):
    for row in multipledata:
        print(row)
        finalAlgorithm(row)
        print("next")

#display data of companies

# companyName = "niravmodi"
# displayType = "all"

def displayDatas(companyName , displayType):
    print(companyName + " " + displayType)
    if companyAlreadyPresent(companyName):
        if displayType == "all":
            sqlSentexDisplay = "SELECT urls from "+ companyName
            mycursor.execute(sqlSentexDisplay)
            myresult = mycursor.fetchall()
            print(myresult)
            return myresult
        else:
            sqlSentexDisplay = "SELECT urls from "+ companyName + " where label = %s"
            mycursor.execute(sqlSentexDisplay , (displayType,))
            myresult = mycursor.fetchall()
            print(myresult)
            return myresult
    else:
        print("you Demand worng Things ")

# displayDatas(companyName , displayType)

def loginDetails(emId , password):
       q1 = "select * from employDetail where eId = %s"
       mycursor.execute(q1, (emId,))
       myresult = mycursor.fetchall()
       if len(myresult) != 0 and myresult[0][2] == password:
            return True
       else:
           return False


def registerDetail(name , eId , password):
    q4 = "INSERT INTO employDetail (name , eId, password) VALUES (%s , %s , %s)"
    valueTuple = (name , eId,password)
    mycursor.execute(q4 , valueTuple)
    mydb.commit()
    print("data Inserted")


def allCompanySearched():
       q1 = "select companyName from PreviousCompanyDetails"
       mycursor.execute(q1)
       myresult = mycursor.fetchall()
       return myresult

def selectNameOfUser(empId):
       q1 = "select name from employDetail where eId = %s"
       mycursor.execute(q1, (empId,))
       myresult = mycursor.fetchall()
       return myresult