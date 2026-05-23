import discord
from .accept_ticket import AcceptButton
from .deny_ticket import DenyButton

class AcceptDenyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(AcceptButton())
        self.add_item(DenyButton())