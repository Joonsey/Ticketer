import discord, asyncio
from discord.ext import commands, tasks
from Tickets import Ticket
from database import *
from secrets import TOKEN

client = commands.Bot(command_prefix='.')





@client.event
async def on_ready():
    print('Logged in as', client.user.name)


@client.command(aliases=["sub","post"])
async def submit(ctx, *args):

    def get_id():
        enum = []
        for x in list(fetchAllTickets()):
            enum.append(x[0])
        
        if len(enum):
            return max(enum) +1 
        else:
            return 1


    data = " "
    for i in args:
        data += i+" "

    id = get_id()
    Ticket(id, str(ctx.author), data.lower(), False)

    #TODO author.id in a hashtable is optimal 


    await ctx.reply(f"Entry added to table with id {id}.")



@client.command(aliases=["rmv","delete","del"])
async def remove(ctx, arg):
    arg = int(arg)
    if fetchTicket(arg):
        removeTicketById(arg)
        await ctx.reply('removal succesful!')
    else:
        await ctx.reply('removal unsuccsesful, ticket does not exist.')
    

@client.command(aliases=["list", "show"])
async def entries(ctx):
    async with ctx.channel.typing():
        d = list(fetchAllTickets())
        if len(d) > 0:
            data = ""
            for i in d:
                data += str(i) + "\n "
            
            await ctx.send("""**id | date | time | context | author | state** \n""" + data)
        else:
            await ctx.send('Table is empty.')

@client.command(aliases=["reset","wipe"])
async def reset_data(ctx):
    if ctx.author.id == 150306246866632704:
        wipeDB()
        await ctx.reply('Database wiped.')
    else:
        await ctx.reply('insufficient permitions.')



if __name__ == "__main__":
    client.run(TOKEN)  