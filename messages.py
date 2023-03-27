answers = {}


async def message_filter(message, user):
    print(f'{message.author} typed "{message.content.lower()}"')

    if message.author == user:
        return

    # if message.content.lower().replace(" ", "") in answers:
    #     await message.channel.send(answers[message.content.lower().replace(" ", "")])

    mess = message.content.lower().replace(" ", "")
    keys = list(answers.keys())

    for i in range(len(keys)):
        if mess.find(keys[i]) != -1:
            await message.channel.send(answers[keys[i]])
