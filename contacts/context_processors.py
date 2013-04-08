from account.models import Account


def account_id(request):
    # # when sending emails we have a request but not a user object
    # if hasattr(request, 'user'):
    #     user = request.user
    #     if user.is_anonymous():
    #         return {}
    #     else:
    #         # TODO update this when we update Accounts to have multiple users
    #         account = Account.objects.get(admin=user)
    #         return {'account_id': account.id}
    return {}