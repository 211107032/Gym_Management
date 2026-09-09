from .models import GymSetting

def gym_info(request):
    try:
        settings_obj = GymSetting.get_settings()
    except Exception:
        settings_obj = None
    return {
        'gym_info': settings_obj
    }
