from commonconf.backends import use_configparser_backend
from commonconf import settings
from dao.zoom import (
    get_sub_accounts, get_pro_users, get_account_pro_users, update_user_basic)
from dao.groups import get_group_members
from logging import getLogger
import os

logger = getLogger(__name__)


def reconcile_main_account():
    group_id = getattr(settings, 'ZOOM_ACCOUNT_GROUP')
    group_members = get_group_members(group_id)

    for user in get_pro_users():
        if user.email not in group_members:
            print('UPDATE {} in Main account'.format(user.email))
            # update_user_basic(user)


def reconcile_sub_account(account):
    group_id = getattr(settings, 'ZOOM_SUBACCOUNT_GROUP_{}'.format(account.id))
    if not group_id:
        return

    group_members = get_group_members(group_id)
    for user in get_account_pro_users(account):
        if user.email not in group_members:
            print('UPDATE {} in {} account'.format(
                user.email, account.account_name))
            # update_user_basic(user)


def reconcile_users():
    reconcile_main_account()

    for account in get_sub_accounts():
        reconcile_sub_account(account)


if __name__ == '__main__':
    settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'settings.cfg')
    use_configparser_backend(settings_path, 'ZOOM')
    reconcile_users()
