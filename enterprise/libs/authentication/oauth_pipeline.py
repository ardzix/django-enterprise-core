from django.contrib.auth import get_user_model
from social_django.models import UserSocialAuth

USER_FIELDS = ["username", "email"]


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {"is_new": False}

    fields = dict(
        (name, kwargs.get(name, details.get(name)))
        for name in backend.setting("USER_FIELDS", USER_FIELDS)
    )
    if not fields:
        return

    # get or create user
    email = fields.get("email")
    user = get_user_model().objects.filter(email__iexact=email).last()
    if not user:
        user = strategy.create_user(**fields)
    
    try:
        user.email = email.lower()
        user.save()
    except:
        pass

    return {"is_new": True, "user": user}


def update_user(backend, details, uid, response, *args, **kwargs):
    """Update Full Name to local user"""

    user_exist = UserSocialAuth.objects.filter(uid=uid).first()

    email = details.get("email", "")
    full_name = details.get("fullname", "")

    try:
        if user_exist:
            user_exist = user_exist.user

        if not user_exist:
            user_exist = get_user_model().objects.filter(email=email).last()

        if user_exist:
            if not user_exist.full_name:
                user_exist.full_name = full_name or uid

            if not user_exist.nick_name:
                user_exist.nick_name = full_name or uid

            user_exist.is_active = True
            user_exist.save()

            # login if user new
            users = list(
                backend.strategy.storage.user.get_users_by_email(user_exist.email)
            )
            return {"user": users[0], "is_new": False}

    except Exception as e:
        print(str(e))
