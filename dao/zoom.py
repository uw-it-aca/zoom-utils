from uw_zoom.accounts import Accounts
from uw_zoom.users import Users
from uw_zoom.models import ZoomUser


def get_sub_accounts():
    return Accounts().get_sub_accounts()


def get_pro_users():
    users = []
    for user in Users().get_users():
        if user.type == ZoomUser.TYPE_PRO:
            users.append(user)
    return users


def get_account_pro_users(account):
    users = []
    for user in Accounts().get_account_users(account.id):
        if user.type == ZoomUser.TYPE_PRO:
            users.append(user)
    return users


def update_user_basic(user):
    Users().update_user_type(user.id, ZoomUser.TYPE_BASIC)
