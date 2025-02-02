import discord
import random
import datetime

from discord.ext import commands

from mk8d_stats_tracker.config import Config
from mk8d_stats_tracker.database import db

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


class RaceInputModal(discord.ui.Modal):
    placement = discord.ui.TextInput(label='Placement (1-12)', min_length=1, max_length=2)
    track_name = discord.ui.TextInput(label='Track Name')

    async def on_submit(self, interaction: discord.Interaction):
        placement = self.placement.value
        track_name = self.track_name.value

        if not placement or (int(placement) < 1 or int(placement) > 12):
            await interaction.response.send_message('Invalid placement.', ephemeral=True)
            return

        db.add_race(interaction.user.id, placement, track_name)
        await interaction.response.send_message('Race recorded successfully.', ephemeral=True)


class CCModeButtons(discord.ui.View):
    async def record_race(self, interaction: discord.Interaction, cc_mode: str):
        print('record_race', type(interaction))
        await interaction.response.send_modal(RaceInputModal(title='Record Race'))

    @discord.ui.button(label="100cc", style=discord.ButtonStyle.primary)
    async def select_100cc(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.record_race(interaction, "100cc")

    @discord.ui.button(label="150cc", style=discord.ButtonStyle.primary)
    async def select_150cc(self, interaction: discord.Interaction, button: discord.ui.Button):
        print('select_150cc', type(interaction))
        await self.record_race(interaction, "150cc")

    @discord.ui.button(label="200cc", style=discord.ButtonStyle.primary)
    async def select_200cc(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.record_race(interaction, "200cc")

    @discord.ui.button(label="Mirror", style=discord.ButtonStyle.primary)
    async def select_mirror(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.record_race(interaction, "Mirror")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def start_session(ctx, start_vr: int = None):
    if start_vr is None:
        await ctx.send('Starting a session needs an initial VR. Please provide a VR value.')
        return

    if start_vr < 0:
        await ctx.send('Invalid VR. Please enter a positive number.')
        return

    user_id = ctx.author.id
    today = datetime.date.today().isoformat()
    existing_session = db.get_session(user_id, today)
    if existing_session:
        await ctx.send('You already have a session for today.')
        return

    db.start_session(user_id, today, start_vr)
    await ctx.send('Session started.')


@bot.command()
async def record(ctx: commands.Context):
    await ctx.send('Select the CC mode:', view=CCModeButtons())


if __name__ == '__main__':
    bot.run(Config.DISCORD_TOKEN)