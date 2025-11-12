import discord
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Google Gemini API Key

# Initialize Google GenAI client
# The client will use the provided GEMINI_API_KEY from the environment
genai_client = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Bot nyala sebagai {client.user}')


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!"):
        user_input = message.content.replace("!", "").strip()

        await message.channel.send("Sedang memproses pertanyaanmu...")

        try:
            # Use Gemini model via the new Google GenAI client
            response = genai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input,
            )

            reply = response.text

            # Potong reply jika terlalu panjang untuk Discord
            if len(reply) > 2000:
                reply = reply[:1997] + "..."

            await message.channel.send(reply)

        except Exception as e:
            print("Error:", e)
            await message.channel.send("⚠️ Gagal memproses pertanyaan, coba lagi nanti.")

client.run(DISCORD_TOKEN)
