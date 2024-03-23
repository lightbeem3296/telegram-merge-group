import asyncio
from pprint import pprint
from telegram import Bot, Chat

TOKEN = "6845432310:AAHMVIOWayOBk9JEtiZNWZEOo7f539FOlAU"

async def main():
    async with Bot(TOKEN)as bot:
        chat = await bot.get_chat("@django_community")
        chat = Chat()
        pprint(chat)
        pprint(await chat.get_member_count())

if __name__ =="__main__":
    asyncio.run(main())
