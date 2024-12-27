from django.template.loader import render_to_string
from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token


from .models import SessionUser


class SessionSwitcherMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Only process HTML responses
        if not request.user.is_authenticated:
            return response

        if "text/html" not in response.get("Content-Type", ""):
            return response

        if getattr(response, "streaming", False):
            return response

        username = request.user.username
        user = SessionUser.objects.filter(username=username)

        if not user:
            return response

        switchable_users = SessionUser.objects.all()
        context = {
            "request": request,
            "users": switchable_users,
            "csrf_token": get_token(request),
        }

        # Render your template
        html = render_to_string("toolbar.html", context=context)

        # Decode response content
        content = response.content.decode(response.charset)

        # Inject your content before the closing </body> tag
        insert_at = content.lower().rfind("</body>")
        if insert_at == -1:
            return response

        content = content[:insert_at] + html + content[insert_at:]
        response.content = content.encode(response.charset)
        response["Content-Length"] = len(response.content)

        return response
