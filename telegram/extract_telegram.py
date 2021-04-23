from telethon.sync import TelegramClient, events
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

api_id = "4876840"
api_hash = "2ffa118e2b07152b05739393d981c60f"

client = TelegramClient('noon', api_id, api_hash)

# async def main():
#     # Getting information about yourself
#     me = await client.get_me()
#
#     # "me" is a user object. You can pretty-print
#     # any Telegram object with the "stringify" method:
#     print(me.stringify())
#
#     # When you print something, you see a representation of it.
#     # You can access all attributes of Telegram objects with
#     # the dot operator. For example, to get the username:
#     username = me.username
#     print(username)
#     print(me.phone)
#
#     # You can print all the dialogs/conversations that you are part of:
#     async for dialog in client.iter_dialogs():
#         print(dialog.name, 'has ID', dialog.id)
#
#     # You can send messages to yourself...
#     # await client.send_message('me', 'Hello, myself!')
#     # # ...to some chat ID
#     # await client.send_message(-100123456, 'Hello, group!')
#     # # ...to your contacts
#     # await client.send_message('+34600123123', 'Hello, friend!')
#     # # ...or even to any username
#     # await client.send_message('username', 'Testing Telethon!')
#
#     # You can, of course, use markdown in your messages:
#     message = await client.send_message(
#         'me',
#         'This message has **bold**, `code`, __italics__ and '
#         'a [nice website](https://example.com)!',
#         link_preview=False
#     )
#
#     # Sending a message returns the sent message object, which you can use
#     print(message.raw_text)
#
#     # You can reply to messages directly if you have a message object
#     await message.reply('Cool!')

# @client.on(events.NewMessage(outgoing=True))
# async def handler(event):
#     # Good
#     chat = await event.get_chat()
#     sender = await event.get_sender()
#     chat_id = event.chat_id
#     sender_id = event.sender_id

# client.start()
# client.run_until_disconnected(get_name_dialogs())

async def get_name_dialogs():
    # You can print all the dialogs/conversations that you are part of:
    async for dialog in client.iter_dialogs():
            print(dialog.name, 'has ID', dialog.id)

    await client.get_messages('me', ids=1794504718)


with client:
    client.loop.run_until_complete(get_name_dialogs())

# if (__name__ == "__main__"):
#     main()
#     client.run_until_disconnected()
# with TelegramClient('name', api_id, api_hash) as client:
#     client.send_message('me', 'Hello, myself!')
#     print(client.download_profile_photo('me'))
#
#
#     @client.on(events.NewMessage(pattern='(?i).*Hello'))
#     async def handler(event):
#         await event.reply('Hey!')
#
#
# client.run_until_disconnected()
