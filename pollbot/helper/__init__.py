"""Some static stuff or helper functions."""
from .enums import VoteType


donations_text = """
Hello there!

My name is Arne Beer (@Nukesor) and I'm the sole developer of the Ultimate PollBot.

This project is non-profit, open-source on [Github](https://github.com/Nukesor/ultimate-poll-bot) and hosted on a server I'm renting from my own money.

I really appreciate anything that helps me out and that keeps me and my server running ☺️.

If you like this project, check my [Patreon](https://www.patreon.com/nukesor) or support me via [Paypal](https://www.paypal.me/arnebeer).

Have great day!
"""


start_text = """*Hi!*

This is the *ULTIMATE* pollbot.
Just type /create or click the button below to start creating polls. Everything is explained underway.

If you have more questions, check out /help.

This project is open-source on [Github](https://github.com/Nukesor/ultimate-poll-bot).
"""

help_text = """There are quite a few settings for your polls:

*Creation:*
1. You can anonymize your poll, which results in no names being displayed!
2. Poll results can be shown only after closing the poll. This is great to avoid tactical voting, which is possible if people can see the intermediate results of a poll.

*Settings:*
1. A poll can be made anonymous retrospectively.
2. The percentage line of options can be hidden in the settings menu.
3. New options can be added and existing options can be removed in the settings menu.
4. The order in which options are displayed in the results can be changed.
5. The order in which names for each option are displayed in the results can be changed.

*Too many votes in the last minute:*
Don't worry about this message. This mechanism is necessary to prevent my bot from being blocked by telegram for spamming messages.
The only effect for you is, that the results won't be displayed immediately.

*My polls won't update:*
In this case you probably have multiple active polls or the same poll twice in a single group.
This is something that a bot cannot detect (telegrams API doesn't allow this). Therefore you need to handle this yourself.
Only have one highly active poll per group and don't send the same poll multiple times in the same group (or delete the old ones for ALL members of the group).

*There is a bug that won't go away!!*
Usually I get a notification as soon as something breaks, but there might be some bugs that go unnoticed! In that case, just write a ticket on [Github](https://github.com/Nukesor/ultimate-poll-bot)
"""


error_text = """An unknown error occurred. I probably just got a notification about this and I'll try to fix it as quickly as possible.
In case this error still occurs in a day or two, please report the bug to me :). The link to the Github repository is in the /start text.
"""


def poll_allows_multiple_votes(poll):
    """Check whether the poll allows multiple votes."""
    multiple_vote_types = [
        VoteType.block_vote.name,
        VoteType.limited_vote.name,
        VoteType.cumulative_vote.name,
    ]

    return poll.vote_type in multiple_vote_types


def poll_has_limited_votes(poll):
    """Check whether the poll has limited votes."""
    vote_type_with_vote_count = [
        VoteType.limited_vote.name,
        VoteType.cumulative_vote.name,
    ]

    return poll.vote_type in vote_type_with_vote_count


def poll_is_cumulative(poll):
    """Check whether this poll's type is cumulative."""
    return poll.vote_type == VoteType.cumulative_vote.name


def calculate_total_votes(poll):
    """Calculate the total number of votes of a poll."""
    total = 0
    for vote in poll.votes:
        total += vote.vote_count

    return total
