import responses
import sqlite3
import discord
from discord.ext import commands

#Calls the Keepa API to fetch data for each of the sellers requested
def fetch_asins():

    #Initialize variables
    api_key = ''
    domain_id = 1
    seller_ids = {'':''}
    seller_asins = {}

    #Parse data and add Asins for each seller to dictonary
    for name in seller_ids:
        storefront = seller_ids.get(name)
        seller_info = responses.get_seller_information(api_key, domain_id, storefront)
        if name not in seller_asins:
            seller_asins[name] = seller_info.get("sellers").get(storefront).get("asinList")

    return seller_asins

#Check if a seller is already in the databases
def check_value(cursor, name):
    cursor.execute("SELECT EXISTS(SELECT 1 FROM sellers WHERE name = ?)", (name,))
    exists = cursor.fetchone()[0]
    return exists

#Inserts each seller into database with ASINS
def insert_value(cursor, conn, name, asins):
    with conn:
        cursor.execute("INSERT INTO sellers VALUES (:name, :asins)", {"name": name, "asins": asins})

#Creates a database and returns all the current info in the database
def create_database(cursor, conn, seller_asins):

    #Check if database is already created
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sellers (
        name TEXT,
        asins TEXT
    )
    ''')

    #Add new sellers and their asins to the database
    for seller in seller_asins:
        if check_value(cursor, seller) == 0:
            asins = ",".join(seller_asins.get(seller))
            insert_value(cursor, conn, seller, asins)

    cursor.execute("SELECT * FROM sellers")
    data = cursor.fetchall()

    return data

#Checks each seller for new asins they have added
def new_asins(data, seller_asins):

    #Compares current asins to asins in database
    new_asins = {}
    for info in data:
        if info[0] not in new_asins:
            new_asins[info[0]] = list(set(seller_asins[info[0]]) - set(info[1].split(",")))
    
    return new_asins

#Updates the database to contain all current seller information
def update_database(cursor, conn, seller_asins):

    #Delete all data and add new ASINS
    cursor.execute("DELETE FROM sellers")
    conn.commit()

    for seller in seller_asins:
        if check_value(cursor, seller) == 0:
            asins = ",".join(seller_asins.get(seller))
            insert_value(cursor, conn, seller, asins)

    cursor.execute("SELECT * FROM sellers")


def main():
    seller_asins = fetch_asins()

    #Initalize database
    conn = sqlite3.connect("sellers.db")
    cursor = conn.cursor()

    data = create_database(cursor, conn, seller_asins)
    added_asins = new_asins(data, seller_asins)

    update_database(cursor, conn, seller_asins)

    client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print("The bot is now ready to use")
        print("---------------------------")

    @client.command()
    async def update(ctx):
        await ctx.send(added_asins)

    #INSET DISCORD TOKEN
    client.run()

if __name__ == "__main__":
    main()