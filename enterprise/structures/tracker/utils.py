from .models import Tracker


def log_tracker(request, purpose=""):
    user = getattr(request, "user")
    useragent = getattr(request, "useragent")
