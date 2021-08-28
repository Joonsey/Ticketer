import discord, asyncio
from discord import embeds
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
    embed.add_field(name="added entry: ",value=f"**id: ** {t.id} \n **date: **{t.date[0:10]}  \n **time: **{t.date[10:]} \n **context: **{t.context} \n **author: **{t.author} \n **solved: ** {str(t.solved)}", inline=False)
    embed.set_thumbnail(url=checked_box)
    await ctx.reply(embed=embed)




@client.command(aliases=["rmv","delete","del"])
async def remove(ctx, arg):
    arg = int(arg)
    embed = discord.Embed(title="Remove ticket.")
    if fetchTicket(arg):
        removeTicketById(arg)
        embed.set_thumbnail(url=rocket_box)
        embed.color = MAIN_COLOR
        embed.add_field(name="Succesful!", value="Ticket has been removed from the database")
    else:
        embed.set_thumbnail(url=rocket_box) # TODO get a error image
        embed.color = ERROR_COLOR
        embed.add_field(name="Failed!", value="Ticket with that ID does not exist.")

    await ctx.reply(embed=embed)
    

@client.command(aliases=["list", "show"])
async def entries(ctx):
    embed = discord.Embed(title="All entries in table", description="""**id | date | time | context | author | state**""", color=MAIN_COLOR)
    async with ctx.channel.typing():
        d = list(fetchAllTickets())
        if len(d) > 0:
            #data = ""
            #for i in d:
            #    data += str(i) + "\n "
            for x, y in enumerate(d):
                embed.add_field(name="> Ticket #" + str(x+1), 
                value=f"**id: ** {y[0]} \n **date: ** {y[1][0:10]} \n **time: **{y[1][10:]} \n **context: **{y[2]} \n **author: **{y[3]} \n **solved: ** {y[4]}", inline=True)
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


@client.command(aliases=['change', 'swap'])
async def update(ctx, *args):
    """expects: ( id : int, type : (ctx || author || state), newInput : str)"""
    if args[1].lower() in ["context", "kontekst", "ctx", "info", "data"]:
        changeCtx(int(args[0]), args[2])
    elif args[1].lower() in ['author', 'eier', 'auth', 'owner']:
        changeAuth(int(args[0]), args[2])
    elif args[1].lower() in ['state','solved','løst','solvedstate','solved_state','issolved','ferdig','fikset']:
        try:
            changeSolved(int(args[0]), args[2].lower().capitalize())
        except ValueError:
            await ctx.send('Provide either True or False for this value.')
    else:
        await ctx.send('Please give a valid input')

    # TODO embed
    # verification
    # error message
    # help UI with example


@client.command(hidden=True)
async def embed_test(ctx):
    embed = discord.Embed(title="Sample Embed",
    url="https://github.com/Joonsey/Ticketer",
    description="This is an embed",
    color=discord.Color.dark_purple())
    await ctx.send(embed=embed)


if __name__ == "__main__":
    client.run(TOKEN)  