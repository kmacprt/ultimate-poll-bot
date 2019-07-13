"""Callback functions needed during creation of a Poll."""
from pollbot.i18n import i18n
from pollbot.helper import poll_required
from pollbot.helper.creation import create_poll
from pollbot.helper.enums import PollType, ExpectedInput
from pollbot.telegram.keyboard import (
    get_change_poll_type_keyboard,
    get_init_keyboard,
    get_options_entered_keyboard,
    get_creation_datepicker_keyboard,
    get_open_datepicker_keyboard,
)
from pollbot.helper.display.creation import (
    get_init_text,
    get_poll_type_help_text,
    get_datepicker_text,
)

from pollbot.models import Poll


@poll_required
def skip_description(session, context, poll):
    """Skip description creation step."""
    context.user.expected_input = ExpectedInput.options.name
    session.commit()
    context.query.message.edit_text(
        'Now send me the first option (Or send multiple options at once, each option on a new line)',
        reply_markup=get_open_datepicker_keyboard(poll)
    )

    return


def show_poll_type_keyboard(session, context):
    """Show to vote type keyboard."""
    poll = session.query(Poll).get(context.payload)

    keyboard = get_change_poll_type_keyboard(poll)
    context.query.message.edit_text(get_poll_type_help_text(poll), parse_mode='markdown', reply_markup=keyboard)


@poll_required
def change_poll_type(session, context, poll):
    """Change the vote type."""
    if poll.created:
        context.query.answer('The poll has already been created')
        return
    poll.poll_type = PollType(context.action).name

    keyboard = get_init_keyboard(poll)
    context.query.message.edit_text(
        get_init_text(poll),
        parse_mode='markdown',
        reply_markup=keyboard
    )


@poll_required
def toggle_anonymity(session, context, poll):
    """Change the anonymity settings of a poll."""
    if poll.created:
        context.query.answer('The poll has already been created')
        return
    poll.anonymous = not poll.anonymous

    keyboard = get_init_keyboard(poll)
    context.query.message.edit_text(
        get_init_text(poll),
        parse_mode='markdown',
        reply_markup=keyboard
    )
    context.query.answer('Anonymity setting changed')


@poll_required
def toggle_results_visible(session, context, poll):
    """Change the results visible settings of a poll."""
    if poll.created:
        context.query.answer('The poll has already been created')
        return
    poll.results_visible = not poll.results_visible

    keyboard = get_init_keyboard(poll)
    context.query.message.edit_text(
        get_init_text(poll),
        parse_mode='markdown',
        reply_markup=keyboard
    )
    context.query.answer('Visibility setting changed')


@poll_required
def all_options_entered(session, context, poll):
    """All options are entered the poll is created."""
    if poll is None:
        return

    if poll.poll_type in [PollType.limited_vote.name, PollType.cumulative_vote.name]:
        context.query.message.edit_text('All options have been added.')
        context.user.expected_input = ExpectedInput.vote_count.name
        context.query.message.chat.send_message('Send me the amount of allowed votes per user.')

        return

    create_poll(session, poll, context.user, context.query.message.chat, context.query.message)


@poll_required
def open_creation_datepicker(session, context, poll):
    """All options are entered the poll is created."""
    keyboard = get_creation_datepicker_keyboard(poll)
    # Switch from new option by text to new option via datepicker

    if context.user.expected_input != ExpectedInput.options.name:
        context.query.message.edit_text('All options have already been added')
        return

    context.user.expected_input = ExpectedInput.date.name

    context.query.message.edit_text(
        get_datepicker_text(poll),
        parse_mode='markdown',
        reply_markup=keyboard
    )

    return


@poll_required
def close_creation_datepicker(session, context, poll):
    """All options are entered the poll is created."""
    user = context.user
    if len(poll.options) == 0:
        text = i18n.t('creation.option.first', locale=user.locale)
        keyboard = get_open_datepicker_keyboard(poll)
    else:
        text = i18n.t('creation.option.next', locale=user.locale)
        keyboard = get_options_entered_keyboard(poll)

    # Replace the message completely, since all options have already been entered
    if user.expected_input != ExpectedInput.date.name:
        context.query.message.edit_text(i18n.t('creation.option.finished', locale=user.locale))
        return

    user.expected_input = ExpectedInput.options.name
    context.query.message.edit_text(
        text,
        parse_mode='markdown',
        reply_markup=keyboard
    )

    return


def cancel_creation(session, context):
    """Cancel the creation of a bot."""
    if context.poll is None:
        context.query.answer(i18n.t('delete.doesnt_exist', locale=context.user.locale))
        return

    session.delete(context.poll)
    context.query.message.edit_text(i18n.t('delete.previous_deleted', locale=context.user.locale))
