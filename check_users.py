from commonconf.backends import use_configparser_backend
from commonconf import settings
from argparse import ArgumentParser
from dao.zoom import (
    get_sub_accounts, get_account_pro_users, update_account_user_basic)
from dao.groups import get_group_members
from logging import getLogger
from email.message import EmailMessage
from smtplib import SMTP
import argparse
import os

logger = getLogger(__name__)


def notify_admins(message):
    email_message = EmailMessage()
    email_message['Subject'] = 'Summary of changes to Zoom user licenses'
    email_message['From'] = getattr(settings, 'EMAIL_SENDER')
    email_message['To'] = getattr(settings, 'EMAIL_RECIPIENT')
    email_message['Cc'] = getattr(settings, 'EMAIL_CC')
    email_message['Bcc'] = getattr(settings, 'EMAIL_BCC')
    email_message.set_content(message)

    with SMTP(getattr(settings, 'EMAIL_HOST')) as smtp:
        smtp.set_debuglevel(1)
        smtp.send_message(email_message)


def reconcile_account_users(account=None, update=False):
    changed = []
    if account is None:
        group_id = getattr(settings, 'ZOOM_ACCOUNT_GROUP', '')
    else:
        group_id = getattr(settings, 'ZOOM_SUBACCOUNT_GROUP_' + account.id, '')

    if not len(group_id):
        logger.info('SKIPPED {}: Group not configured'.format(
            account.account_name))
        return changed

    group_members = get_group_members(group_id)
    for user in get_account_pro_users(account):
        if user.email not in group_members:
            if update:
                update_account_user_basic(user, account)
            changed.append({'user': user.email, 'group': group_id})
    return changed


def make_message(account_name, data):
    return ('\n\nAccount: {}\n\n'.format(account_name) +
            '\n'.join('{} Not present in {}'.format(
                d['user'].ljust(24), d['group']) for d in data))


def run(update):
    message = ''
    changed = reconcile_account_users(update=update)  # Main account
    if len(changed):
        message += make_message('UW Zoom Main', changed)

    for account in get_sub_accounts():
        changed = reconcile_account_users(account, update=update)
        if len(changed):
            message += make_message(account.account_name, changed)

    if len(message):
        message = ('\nThese Zoom users have been downgraded from '
                   'Pro to Basic:{}\n\n').format(message)
        if update:
            notify_admins(message)
        else:
            print(message)


if __name__ == '__main__':
    settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'settings.cfg')
    use_configparser_backend(settings_path, 'ZOOM')
    parser = ArgumentParser()
    parser.add_argument(
        '--update', action='store_true', default=False, help='Updates users')
    args = parser.parse_args()
    run(args.update)
