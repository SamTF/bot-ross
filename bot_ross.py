### IMPORTS        ############################################################
### My modules
import art_generator

### Discord
import discord
from discord.ext import commands, tasks
from discord import app_commands

import time


###### CONSTANTS        ##########################################################
TOKEN_FILE = '.bot_ross.token'


###### DISCORD STUFF ############################################################
### Creating the bot!
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='🖌️', intents=intents)

    # on_ready event l think
    async def setup_hook(self) -> None:
        await self.tree.sync(guild=discord.Object(id=349267379991347200))
        print(f'Synced slash commands for {self.user} @ server 349267379991347200')
    
    # error handling
    async def on_command_error(self, ctx, error) -> None:
        print('ERROR WTF')
        print(error)
        await ctx.reply(error, ephemeral=True)

bot = Bot()


###### EVENTS        ##########################################################
# Runs this when the bot becomes online
@bot.event
async def on_ready():
    print("Ready to generate happy lil accidents")
    print(bot.user.name)

    await bot.change_presence(activity=discord.Game('happy lil accidents'))


###### COMMANDS        #######################################################
### /commission
@bot.hybrid_command(name='commission', description='Commission the bot to draw something for you')
@app_commands.describe(prompt = '🖌️ What do you want the bot to draw for you?')
@app_commands.guilds(discord.Object(id=349267379991347200))
async def commission(ctx, prompt:str):
    # removing trailing white spaces
    prompt = prompt.strip()

    # console logging
    print(f'>>> User {ctx.author} requesting commission: {prompt}')

    # # error handling
    # if not prompt:
    #     raise ValueError('Prompt cannot be empty')
    
    # generating an image using the Stable Diffusion API
    await ctx.reply(f'*drawing {prompt}...*')
    img = art_generator.generate_img(prompt, save_to_disk=False)
    
    # we need this here otherwise l get errors for some reason :(
    time.sleep(3)

    # sending the image from memory
    img.seek(0)
    await ctx.send(file=discord.File(img, f'{prompt}.png'))

    print(f'>>> {ctx.author}\'s commission sent!')


###### RUNNING THE BOT #################################################
if __name__ == "__main__":
    print("_____________CONCERT BUDDY INITIALISED_____________")
    with open(TOKEN_FILE, 'r') as f:
        token = f.read()
    
    bot.run(token)