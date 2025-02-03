import discord
import datetime

from discord import app_commands

from mk8d_stats_tracker.config import Config
from mk8d_stats_tracker.database import db
from mk8d_stats_tracker.util import placement_to_string

# class MK8DBot(commands.Bot):
class MK8DBot(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=Config.GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

intents = discord.Intents.default()
intents.message_content = True

# bot = commands.Bot(command_prefix='/', intents=intents)
bot = MK8DBot(intents=intents)

class EndVRModal(discord.ui.Modal):
    end_vr = discord.ui.TextInput(label='Ending VR', min_length=1, max_length=8)

    async def on_submit(self, interaction: discord.Interaction):
        end_vr = int(self.end_vr.value)
        session = db.get_session(interaction.user.id, datetime.date.today().isoformat())

        session['end_vr'] = end_vr
        db.sessions.update(session, doc_ids=[session.doc_id])

        vr_diff = end_vr - session['start_vr']

        if vr_diff > 0:
            msg = f'VR change: +{vr_diff} :tada:'
        else:
            msg = f'VR change: -{vr_diff} :sob:'

        await interaction.response.send_message(msg + f'\n\nCome back tomorrow for your next session!', ephemeral=True)

class TrackSelectView(discord.ui.View):
    def __init__(self, categories, cc_mode, placement: int):
        super().__init__()
        self.cc_mode = cc_mode
        self.placement = placement

        for category_name, tracks in categories.items():
            options = [discord.SelectOption(label=track['name'], value=track['name']) for track in tracks]
            select = discord.ui.Select(placeholder=f'Select a track ({category_name})', options=options, max_values=1)
            select.callback = self.select_callback
            self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        selected_track = interaction.data['values'][0]
        session = db.get_session(interaction.user.id, datetime.date.today().isoformat())
        races = len(session.get('races'))
        ended = False

        if races == 9:
            ended = True

        db.add_race(interaction.user.id, self.placement, selected_track)

        if self.placement <= 6:
            msg = f'_Congrats!_ :partying_face: \n\nRegistered {placement_to_string(self.placement)} place for {self.cc_mode} in **{selected_track}**'
        else:
            msg = f'_You\'ll get better next time!_ :muscle: \n\nRegistered {placement_to_string(self.placement)} place for {self.cc_mode} in **{selected_track}**'

        if not ended:
            await interaction.response.send_message(msg, ephemeral=True)
        else:
            await interaction.response.send_modal(EndVRModal(title='Enter your ending VR'))

class CCModeButtons(discord.ui.View):
    def __init__(self, placement: int):
        super().__init__()
        self.placement = placement

    @discord.ui.button(label="100cc", style=discord.ButtonStyle.primary)
    async def select_100cc(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_track_select(interaction, "100cc")

    @discord.ui.button(label="150cc", style=discord.ButtonStyle.primary)
    async def select_150cc(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_track_select(interaction, "150cc")

    @discord.ui.button(label="200cc", style=discord.ButtonStyle.primary)
    async def select_200cc(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_track_select(interaction, "200cc")

    @discord.ui.button(label="Mirror", style=discord.ButtonStyle.primary)
    async def select_mirror(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_track_select(interaction, "Mirror")

    async def show_track_select(self, interaction: discord.Interaction, cc_mode: str):
        categories = {
            "Handheld": [track for track in db.tracks.all() if track['category'] == 'handheld'],
            "Retro": [track for track in db.tracks.all() if track['category'] == 'retro'],
            "Tour": [track for track in db.tracks.all() if track['category'] == 'tour'],
            "SNES + DLC": [track for track in db.tracks.all() if track['category'] == 'snes_dlc'],
        }
        await interaction.response.send_message(f'Select the track for {cc_mode}:', view=TrackSelectView(categories, cc_mode, self.placement), ephemeral=True)

class PlacementView(discord.ui.View):
    def __init__(self):
        super().__init__()

    async def show_cc_select(self, interaction: discord.Interaction, placement: int):
        await interaction.response.send_message('Select the CC mode:', view=CCModeButtons(placement))

    # TODO: refactor this part into a for loop with add_item()
    @discord.ui.button(label="1st", style=discord.ButtonStyle.primary)
    async def select_1st(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_cc_select(interaction, 1)

    @discord.ui.button(label="2nd", style=discord.ButtonStyle.primary)
    async def select_2nd(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_cc_select(interaction, 2)

    @discord.ui.button(label="3rd", style=discord.ButtonStyle.primary)
    async def select_3rd(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_cc_select(interaction, 3)

    @discord.ui.button(label="4th", style=discord.ButtonStyle.primary)
    async def select_4th(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_cc_select(interaction, 4)

    @discord.ui.button(label="5th", style=discord.ButtonStyle.primary)
    async def select_5th(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_cc_select(interaction, 5)

    @discord.ui.button(label="6th", style=discord.ButtonStyle.primary)
    async def select_6th(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_cc_select(interaction, 6)

    @discord.ui.button(label="7th", style=discord.ButtonStyle.primary)
    async def select_7th(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_cc_select(interaction, 7)

    @discord.ui.button(label="8th", style=discord.ButtonStyle.primary)
    async def select_8th(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_cc_select(interaction, 8)

    @discord.ui.button(label="9th", style=discord.ButtonStyle.primary)
    async def select_9th(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_cc_select(interaction, 9)

    @discord.ui.button(label="10th", style=discord.ButtonStyle.primary)
    async def select_10th(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_cc_select(interaction, 10)

    @discord.ui.button(label="11th", style=discord.ButtonStyle.primary)
    async def select_11th(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_cc_select(interaction, 11)

    @discord.ui.button(label="12th", style=discord.ButtonStyle.primary)
    async def select_12th(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_cc_select(interaction, 12)

class StartSessionModal(discord.ui.Modal):

    def __init__(self, title, user_id):
        super().__init__(title=title)

        self.user_id = user_id

    # TODO: add option to define a date (historical registering)
    start_vr = discord.ui.TextInput(label='Starting VR', min_length=1, max_length=8)

    async def on_submit(self, interaction: discord.Interaction):
        start_vr = int(self.start_vr.value)

        if start_vr < 0:
            await interaction.response.send_message('Invalid VR. Please enter a positive number.', ephemeral=True)
            return

        today = datetime.date.today().isoformat()
        db.start_session(self.user_id, today, start_vr)

        await interaction.response.send_message('Session started! Good luck!', ephemeral=True)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.tree.command(name='start_session', description='Start a new session')
async def start_session(interaction: discord.Interaction):
    user_id = interaction.user.id
    today = datetime.date.today().isoformat()
    existing_session = db.get_session(user_id, today)

    if existing_session:
        await interaction.response.send_message('You already have a session for today.')
        return

    await interaction.response.send_modal(StartSessionModal('Input your starting VR', user_id))

@bot.tree.command(name='record')
async def record(interaction: discord.Interaction):
    await interaction.response.send_message('Select Your Placement:', view=PlacementView())


if __name__ == '__main__':
    bot.run(Config.DISCORD_TOKEN)