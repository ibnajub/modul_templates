from datetime import datetime, timedelta
from django.contrib.auth import logout


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Если пользователь аутентифицирован,
        if request.user.is_authenticated:
            # Проверяем, прошла ли 1 минута с момента последнего действия
            if 'last_action' in request.session:
                last_action_time = datetime.fromtimestamp(request.session['last_action'])
                if datetime.now() - last_action_time > timedelta(minutes=1):
                    logout(request)
                # обновляем время последнего действия
            request.session['last_action'] = datetime.now().timestamp()
        
        return response
