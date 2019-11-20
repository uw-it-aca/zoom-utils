from commonconf.backends import use_configparser_backend
from commonconf import settings
from dao.zoom import get_sub_accounts, get_account_pro_users
from dao.groups import get_group_members
from logging import getLogger
import os

logger = getLogger(__name__)


def reconcile_account_users(account=None):
    if account is None:
        group_id = getattr(settings, 'ZOOM_ACCOUNT_GROUP', '')
        account_name = 'UW Zoom Main'
    else:
        group_id = getattr(settings, 'ZOOM_SUBACCOUNT_GROUP_' + account.id, '')
        account_name = account.account_name

    if not len(group_id):
        print('SKIPPED {}: Group not configured'.format(account_name))
        return

    group_members = get_group_members(group_id)
    for user in get_account_pro_users(account):
        if user.email not in group_members:
            print('{}: Pro user {} not present in {}'.format(
                account_name, user.email, group_id))


def run():
    reconcile_account_users()  # Main account
    for account in get_sub_accounts():
        reconcile_account_users(account)


if __name__ == '__main__':
    settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'settings.cfg')
    use_configparser_backend(settings_path, 'ZOOM')
    run()
