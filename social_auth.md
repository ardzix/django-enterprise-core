# Social Auth

Add To settings

```python
INSTALLED_APPS = [
    ....
    "social_django",
]

MIDDLEWARE = [
    ...
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [...],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
               ....,
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "your key"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "your secret"


AUTHENTICATION_BACKENDS = (
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)


SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_AUTH_URL_NAMESPACE = "social"
SOCIAL_AUTH_LOGIN_URL = "/auth/login/?next=/google-oauth2/"
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/account"
SOCIAL_AUTH_LOGIN_ERROR_URL = "/login/?next=/"
SOCIAL_AUTH_POSTGRES_JSONFIELD = True

LOGIN_REDIRECT_URL = "/"

SOCIAL_AUTH_FACEBOOK_SCOPE = ["email"]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    "fields": "id,name,email",
}

SOCIAL_AUTH_FACEBOOK_API_VERSION = "2.10"


SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ["r_basicprofile", "r_emailaddress"]
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = [
    "email-address",
    "formatted-name",
    "public-profile-url",
]
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [
    ("id", "id"),
    ("formattedName", "name"),
    ("emailAddress", "email_address"),
    ("publicProfileUrl", "profile_url"),
]
```