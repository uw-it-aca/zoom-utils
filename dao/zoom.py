from uw_zoom.accounts import Accounts
from uw_zoom.users import Users
from uw_zoom.models import ZoomUser


def get_sub_accounts():
    return Accounts().get_sub_accounts()


def get_account_pro_users(account=None):
    if account is None:
        all_users = Users().get_users()  # Main account
    else:
        all_users = Accounts().get_account_users(account.id)

    pro_users = []
    for user in all_users:
        if user.type == ZoomUser.TYPE_PRO:
            pro_users.append(user)
    return pro_users


def update_account_user_basic(user, account=None):
    if account is None:
        Users().update_user_type(user.id, ZoomUser.TYPE_BASIC)
    else:
        Accounts().update_account_user_type(
            account.id, user.id, ZoomUser.TYPE_BASIC)
