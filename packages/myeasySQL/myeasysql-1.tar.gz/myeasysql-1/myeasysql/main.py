import mysql.connector

def isEven(n):
    if n % 2 == 0:
        return True
    else:
        return False

def connect(host,user,password,database):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )



def command(cnx,querry):
    cursur=cnx.cursor()

    cursur.execute(querry)



    results = cursur.fetchall()
    for row in results:
        row=str(row)
        row=row.replace("(","")
        row=row.replace(")","")
        row=row.replace("'","")
        row=row.replace('"',"")
        return row
    
    cursur.close()

def getColumn(cnx,table,column):

    count=command(cnx,"SELECT count(*) from %s"%(table))
    count=count.replace(",","")
    count=int(count)
    data=[]

    temp=command(cnx,"SELECT %s from %s limit 1"%(column,table))
    temp=str(temp)
    temp=temp[:-1]
    data.append(temp)

    for name in range(0,count):
        temp=command(cnx,"SELECT %s from %s limit %d,%d" %(column,table,name,name))
        temp=str(temp)
        temp=temp[:-1]
        data.append(temp)

    for item in range (0,len(data)-1):
        if data[item]==None:
            data.remove(None)
        elif data[item]=="Non":
            data.remove("Non")
    return data

def getCell(cnx,table,column,rowIndex):
    resault=getColumn(cnx,table,column)
    resault=str(resault[rowIndex-1])
    return resault.replace(",","")
    