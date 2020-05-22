from devutil import *

async def gnapadd():
    channel = message.channel
    the_message = message.content.split(' ')
    if (message.author.name == "Rez" or
        message.author.name == "NapKat"):
        add_word = the_message[1]
        add_def = ' '.join(the_message[2:])
        gnap_list = get_file('gnap.json')
        if add_word in gnap_list:
            await channel.send("You've already added this word")
            return
        gnap_list[add_word] = add_def
        with open('gnap.json', 'w') as gnap_list_json:
            gnap_list_json.seek(0)
            json.dump(gnap_list, gnap_list_json, indent = 4)
            gnap_list_json.truncate()
        upload_file(gnap_list, 'gnap.json')
        await channel.send("added word")
    else:
        await channel.send("you're not gnap")
        return
    
async def gt():
    channel = message.channel
    the_message = message.content.split(' ')
    translate_this = ' '.join(the_message[1:])
    gnap_list = get_file('gnap.json')
    for word in gnap_list:
        if word == translate_this:
            await channel.send(f'{translate_this} = {gnap_list[word]}')
            return
    await channel.send(f"{translate_this} is not a word!")

async def gtreverse():
    channel = message.channel
    the_message = message.content.split(' ')
    translate_this = ' '.join(the_message[1:])
    print(translate_this)
    gnap_list = get_file('gnap.json')
    for word in gnap_list:
        if gnap_list[word].lower() == translate_this.lower():
            await channel.send(f'{translate_this} = {word}')
            return
    await channel.send(f"{translate_this} doesn't have any Gnap equivalent!")