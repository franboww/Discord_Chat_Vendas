from produto import Product
import inventoryDB

def addProduct(product):
    inventoryDB.insertProduct(product)

def updateProductDescription(id_product, new_description):
    product = getProduct(id_product)
    product.Description=new_description
    inventoryDB.updateProduct(product)

def updateProductQuant(id_product,new_quant):
    product = getProduct(id_product)
    product.Quant+=new_quant
    inventoryDB.updateProduct(product)

def removeProduct(idProduct):
    inventoryDB.deleteProduct(idProduct)

def getProduct(idProduct):
    return inventoryDB.getOneProduct(idProduct)
def getEmptyProducts():
    return inventoryDB.showEmptyProducts('<= 0')

def getNotEmptyProducts():
    return inventoryDB.showEmptyProducts('> 0')

def viewAllProduct():
    return inventoryDB.showAllProduct()
    
def sellOne(idProduct):
    inventoryDB.sellOneProduct(idProduct)