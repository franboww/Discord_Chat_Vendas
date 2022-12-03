from produto import Product
import sqlite3

def insertProduct(product):
    query = "INSERT INTO productList (id_product,name,description,quant) VALUES (?,?,?,?)"
    val = (product.IdProduct,product.Name,product.Description,product.Quant)
    execute(query,val)

def updateProduct(product):
    query = '''UPDATE productList SET description=?,quant =? WHERE id_product = ?'''
    val =(product.Description,product.Quant,product.IdProduct)
    execute(query,val)


def deleteProduct(idProduct):
    query = '''DELETE FROM productList WHERE id_product = ?'''
    val = (idProduct,)
    execute(query,val)

def showAllProduct():
    query='''SELECT * FROM productList'''
    return featchAll(query)

def showEmptyProducts(queryVal):
    query='''SELECT * FROM productList WHERE quant ''' + queryVal
    return featchAll(query)

def getOneProduct(idProduct):
    query='''SELECT * FROM productList WHERE id_product = ?'''
    val=(idProduct,)
    return featchOne(query,val)

def sellOneProduct(idProduct):
    query='''UPDATE productList SET quant = case when (quant - 1) >0 then (quant - 1) else quant end WHERE id_product = ?'''
    val=(idProduct,)
    execute(query,val)
    

def execute(query,val):
    try:
        sqliteConnection = sqlite3.connect('DB_Estoque.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        cursor.execute(query,val)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        raise Exception("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def featchAll(query):
    try:
        sqliteConnection = sqlite3.connect('DB_Estoque.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        cursor.execute(query)
        records= cursor.fetchall()
        productList = list()
        for row in records:
            producSelected = Product()
            producSelected.setAtributes(row[0],row[1],row[2],row[3])
            productList.append(producSelected)
        cursor.close()

        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return productList
    except sqlite3.Error as error:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        raise Exception("Error while connecting to sqlite", error)

def featchOne(query,val):
    try:
        sqliteConnection = sqlite3.connect('DB_Estoque.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        cursor.execute(query,val)
        records= cursor.fetchall()
        producSelected=Product()

        for row in records:
            producSelected.setAtributes(row[0],row[1],row[2],row[3])
        cursor.close()
    except sqlite3.Error as error:
        raise Exception("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
            return producSelected


# query de create
#query = '''CREATE TABLE productList (
#  id_product INTEGER PRIMARY KEY,
#  name TEXT NOT NULL,
#  description TEXT,
#  quant INTEGER
#);'''
#sqliteConnection = sqlite3.connect('DB_Estoque.db')
#cursor = sqliteConnection.cursor()
#print("Successfully Connected to SQLite")
#cursor.execute(query)
#cursor.close()
#sqliteConnection.commit()
#sqliteConnection.close()
