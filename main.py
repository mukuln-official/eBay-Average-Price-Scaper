from bs4 import BeautifulSoup
from requests_html import HTMLSession
from webdriver import keep_alive
import discord

from discord.ext import commands

bot = commands.Bot(command_prefix='!')
bot.remove_command("help")

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=""))
	print(f'Logged in as {bot.user.name}')

@commands.command(name="ebay")
async def ebay(ctx, *args):
	session = HTMLSession()
	url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw={}".format('+'.join(args))
	url2 = "&_sacat=0&LH_TitleDesc=0&rt=nc&LH_Sold=1&LH_Complete=1" 
	mainurl = str(url) + url2
	print(mainurl)
	nice = discord.Embed(title='Processing...', description="**Please wait. This could take up to 30 seconds**\n\n **Your Item:** __{}__".format(' '.join(args)), color=0x32a852)
	await ctx.send(embed=nice)
	response = session.get(mainurl)
	soup = BeautifulSoup(response.content, 'html.parser')
	question = soup.select('.s-item__price')
	question = str(question)
	soup = BeautifulSoup(question,'html.parser')
	a_tag=soup('span')
	cool = []
	for tag in a_tag:
		coolness = tag.text.strip()
		cool.append(coolness)
	ool = []
	for item in cool:
		nice = item.replace('$', '' )
		coosl = nice.replace(',', '' )
		if 'to' in coosl:
			print("'to' detected....ignoring")
		else:
			ool.append(float(coosl))
	items = len(ool)
	total = sum(map(float, ool))
	average = total/items
	average = round(average, 2)
	cooless = discord.Embed(title='Success!', description="**Average Price on Ebay**: ${}\n\n**Items Indexed:** __{}__ **Your Item:** __{}__\n\n **Listing Page: **{}".format(average, items, ' '.join(args), mainurl), color=0x32a852)
	await ctx.send(embed = cooless)

bot.add_command(ebay)


keep_alive()

bot.run('')

