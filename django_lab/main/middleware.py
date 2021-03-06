

from user_agents import parse


# def mobile_middleware(get_response):
#     # Единовременная настройка и инициализация.
#     def middleware(request):
#         user_agent = parse(request.META['HTTP_USER_AGENT'])
#         request.mobile = user_agent.is_mobile
#         response = get_response(request)
#         # Код должен быть выполнен ответа после view
#         return response
#     return middleware

class CheckIsMobile:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        user_agent = parse(request.META['HTTP_USER_AGENT'])
        request.mobile = user_agent.is_mobile
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
