import discord, asyncio
from discord.ext import commands, tasks
from Tickets import Ticket
from database import *
from secrets import TOKEN, USER_IDS


client = commands.Bot(command_prefix='.')

# Embed color(s).
MAIN_COLOR = 0x87CEEB
ERROR_COLOR = 0x992d22


# IMG URLS
open_box = "https://cdns.iconmonstr.com/wp-content/assets/preview/2019/240/iconmonstr-product-3.png"
checked_box = "https://cdns.iconmonstr.com/wp-content/assets/preview/2019/240/iconmonstr-product-9.png"
normal_box = "https://cdns.iconmonstr.com/wp-content/assets/preview/2019/240/iconmonstr-product-1.png"
rocket_box = "https://cdns.iconmonstr.com/wp-content/assets/preview/2019/240/iconmonstr-product-5.png"
box_hand = "https://cdns.iconmonstr.com/wp-content/assets/preview/2019/240/iconmonstr-product-13.png"
box_idea = "https://cdns.iconmonstr.com/wp-content/assets/preview/2019/240/iconmonstr-product-7.png"
# Bless you iconmonstr.com


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

    auth = str(ctx.author)
    solvedState = False

    id = get_id()
    t = Ticket(id, auth, data.lower(), solvedState)

    #TODO author.id in a hashtable is optimal 

    embed = discord.Embed(title=f"Entry added to table with id {id}.", color=MAIN_COLOR)
    embed.add_field(name="added entry: ",value=f"**id: ** {t.id} \n **date and time: **{t.date} \n **context: **{t.context} \n **author: **{t.author} \n **solved: ** {str(t.solved)}", inline=False)
    embed.set_thumbnail(url=checked_box)
    await ctx.reply(embed=embed)




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
    embed = discord.Embed(title="All entries in table", description="""**id | date & time | context | author | state**""", color=MAIN_COLOR)
    async with ctx.channel.typing():
        d = list(fetchAllTickets())
        if len(d) > 0:
            #data = ""
            #for i in d:
            #    data += str(i) + "\n "
            for x, y in enumerate(d):
                embed.add_field(name="entry #" + str(x+1), 
                value=f"**id: ** {y[0]} \n **date and time: **{y[1]} \n **context: **{y[2]} \n **author: **{y[3]} \n **solved: ** {y[4]}", inline=True)
                embed.set_thumbnail(url=open_box)
            await ctx.send(embed=embed)
            #await ctx.send("""**id | date | time | context | author | state** \n""" + data)
        else:
            await ctx.send('Table is empty.')

@client.command(aliases=["reset","wipe"])
async def reset_data(ctx):
    if ctx.author.id == 150306246866632704:
        x = len(fetchAllTickets())
        wipeDB()

        # TODO make a embed

        await ctx.reply(f'Database wiped. ({x}) amount of entries deleted')
    else:
        await ctx.reply('insufficient permitions.')


@client.command()
async def embed_test(ctx):
    embed = discord.Embed(title="Sample Embed",
    url="https://github.com/Joonsey/Ticketer",
    description="This is an embed",
    color=discord.Color.dark_purple())
    await ctx.send(embed=embed)


if __name__ == "__main__":
    client.run(TOKEN)  