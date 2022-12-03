import discord
import interactions
from produto import Product

from discord import app_commands
from table2ascii import table2ascii as t2a, PresetStyle

id_do_servidor =  12345
token_bot="111111"

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False #Nós usamos isso para o bot não sincronizar os comandos mais de uma vez

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #Checar se os comandos slash foram sincronizados 
            await tree.sync(guild = discord.Object(id=id_do_servidor))
            self.synced = True
        print(f"Entramos como {self.user}.")

aclient = client()
tree = app_commands.CommandTree(aclient)


@tree.command(guild = discord.Object(id=id_do_servidor), name = 'add_product', description='Adiciona um produto no estoque')
@app_commands.describe(
    id_product='Id do produto, aceito apenas números',
    product_name='Nome do produto',
    product_description='Descrição do produto',
    initial_quant='Quantidade inicial do produto'
)
async def addProduct(interaction: discord.Interaction, id_product:int,product_name:str,product_description:str,initial_quant:int):
    newProduct = Product()
    newProduct.setAtributes(id_product,product_name,product_description,initial_quant)
    interactions.addProduct(newProduct)
    await interaction.response.send_message(f"{interaction.user} - adicionou um produto!")


@tree.command(guild = discord.Object(id=id_do_servidor), name = 'update_product_quant', description='Atualiza a quantidade de um produto')
@app_commands.describe(
    id_product='Id do produto a ser atualizado',
    new_quant='Nova quantidade do produto A SER ADICIONADA ao estoque atual',
)
async def updateProductQuant(interaction: discord.Interaction, id_product: str, new_quant: int):
    #Cria task e salva no banco
    interactions.updateProductQuant(id_product,new_quant)
    await interaction.response.send_message(f"{interaction.user} - atualizou a quantidade de um produto")


@tree.command(guild = discord.Object(id=id_do_servidor), name = 'update_product_description', description='Atualiza a descrição de um produto')
@app_commands.describe(
    id_product='Id do produto a ser atualizado',
    new_descr='Nova descrição do produto',
)
async def updateProductDescri(interaction: discord.Interaction, id_product: str, new_descr: str):
    #Cria task e salva no banco
    interactions.updateProductDescription(id_product,new_descr)
    await interaction.response.send_message(f"{interaction.user} - atualizou a descrição de um produto")


@tree.command(guild = discord.Object(id=id_do_servidor), name = 'show_all_products', description='Mostra todas os produtos do estoque')
@app_commands.describe(
)
async def showAll(interaction: discord.Interaction):
    bodyList=list()
    allProducts = interactions.viewAllProduct()
    for produc in allProducts:
        bodyList.append([produc.IdProduct,produc.Name,produc.Description,produc.Quant])
    output = t2a(
        header=["Id do Produto", "Nome", "Descrição","Quantidade"],
        body=bodyList,
        style=PresetStyle.thin_compact
    )
    
    await interaction.response.send_message(f"```\n{output}\n```")

@tree.command(guild = discord.Object(id=id_do_servidor), name = 'get_one_products', description='Mostra um produto do estoque')
@app_commands.describe(
    product_id='Id do produto'
)
async def getOne(interaction: discord.Interaction, product_id:int):
    produc = interactions.getProduct(product_id)
    output = t2a(
        header=["Id do Produto", "Nome", "Descrição","Quantidade"],
        body=[[produc.IdProduct,produc.Name,produc.Description,produc.Quant]],
        style=PresetStyle.thin_compact
    )
    
    await interaction.response.send_message(f"```\n{output}\n```")

@tree.command(guild = discord.Object(id=id_do_servidor), name = 'delete_produc', description='Deleta um produto')
@app_commands.describe(
    product_id='Id do produto a ser deletado'
)
async def deleteProduc(interaction: discord.Interaction, product_id: int):
    #Cria task e salva no banco
    interactions.removeProduct(product_id)
    await interaction.response.send_message(f"{interaction.user} - deletou um produto!")

@tree.command(guild = discord.Object(id=id_do_servidor), name = 'show_non_empty', description='Mostra os produtos do estoque com quantidade maior que zero')
@app_commands.describe(
)
async def showNonEmpty(interaction: discord.Interaction):
    bodyList=list()
    allProducts = interactions.getNotEmptyProducts()
    for produc in allProducts:
        bodyList.append([produc.IdProduct,produc.Name,produc.Description,produc.Quant])
    output = t2a(
        header=["Id do Produto", "Nome", "Descrição","Quantidade"],
        body=bodyList,
        style=PresetStyle.thin_compact
    )
    
    await interaction.response.send_message(f"```\n{output}\n```")

@tree.command(guild = discord.Object(id=id_do_servidor), name = 'show_empty', description='Mostra os produtos do estoque em falta')
@app_commands.describe(
)
async def showEmpty(interaction: discord.Interaction):
    bodyList=list()
    allProducts = interactions.getEmptyProducts()
    for produc in allProducts:
        bodyList.append([produc.IdProduct,produc.Name,produc.Description,produc.Quant])
    output = t2a(
        header=["Id do Produto", "Nome", "Descrição","Quantidade"],
        body=bodyList,
        style=PresetStyle.thin_compact
    )
    
    await interaction.response.send_message(f"```\n{output}\n```")

@tree.command(guild = discord.Object(id=id_do_servidor), name = 'quick_sale', description='Faz uma venda, retirando UM da quantidade de produto escolhido')
@app_commands.describe(
    id_product='Id do produto vendido'
)
async def quickSale(interaction: discord.Interaction, id_product: str):
    #Cria task e salva no banco
    interactions.sellOne(id_product)
    await interaction.response.send_message(f"{interaction.user} - Vendeu um produto")

@tree.command(guild = discord.Object(id=id_do_servidor), name = 'make_sale', description='Faz uma venda, retirando a quantidade informada pelo vendedor do estoque do produto escolhido')
@app_commands.describe(
    id_product='Id do produto vendido',
    quant_venda="Quantidade vendida do produto"
)
async def addSale(interaction: discord.Interaction, id_product: str, quant_venda: str):
    #Cria task e salva no banco
    message =interactions.sellProd(id_product,quant_venda)
    await interaction.response.send_message(f"{interaction.user} - {message}")


aclient.run(token_bot)