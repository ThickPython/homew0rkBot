import calendar
import discord
from devutil import *

client = discord.Client()

async def avy(message):
    if message.mentions != []:
        for user in message.mentions:
            await message.channel.send(user.avatar_url)
        return
    split = message.content.split(' ')
    if len(split) == 1:
        await message.channel.send(message.author.avatar_url)
    else:
        split.remove(split[0])
        if split != []:
            for arg in split:
                try:
                    int(arg)
                except ValueError:
                    await message.channel.send("Invalid format or invalid ID")
                    return
                int_id = int(arg)
                await message.channel.send(client.get_user(int_id).avatar_url)

async def ping(message):
    await message.channel.send("Pong!")

async def evaluate(message):
    await client.wait_until_ready()
    eval_this = message.content.split(' ')
    eval_this.remove(eval_this[0])
    eval_this = ' '.join(eval_this)

    eval_result = str(eval(eval_this))

    await message.channel.send(f"```\n{eval_result}\n```")

async def warn(message):
    if message.mentions == []:
        await message.channel.send("Mention a user to warn!")
    else:
        user_id = message.mentions[0].id
        reason = message.content.split(" ")
        reason = ' '.join(reason[2:])
        await message.channel.send(f"Warned <@{user_id}> for `{' '.join(message.content[2:])}`")