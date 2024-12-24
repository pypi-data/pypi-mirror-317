from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import reaction_types


@dataclass(repr=False)
class ReactionTypeEmoji(Type):
    emoji: str
    type: str = reaction_types.EMOJI
