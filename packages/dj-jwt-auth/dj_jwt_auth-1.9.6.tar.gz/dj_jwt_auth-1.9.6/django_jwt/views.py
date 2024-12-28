import base64
from logging import getLogger
from urllib.parse import urlencode

from django.contrib.auth import login
from django.core.cache import cache
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from requests.exceptions import HTTPError

from django_jwt import settings as jwt_settings
from django_jwt.config import SupportedAlgorithms, config
from django_jwt.exceptions import BadRequestException, ConfigException
from django_jwt.pkce import PKCESecret
from django_jwt.user import UserHandler, role_handler
from django_jwt.utils import get_access_token, get_random_string, oidc_handler

log = getLogger(__name__)


def silent_sso_check(request):
    return HttpResponse("<html><body><script>parent.postMessage(location.href, location.origin)</script></body></html>")


def index_response(request, msg, status=400):
    logout_url = config.cfg(SupportedAlgorithms.ES256).get("end_session_endpoint")
    return render(
        request,
        "django-jwt-index.html",
        {
            "error_message": msg,
            "login_url": reverse("start_oidc_auth"),
            "logout_url": logout_url,
            "redirect_uri": request.build_absolute_uri(reverse("start_oidc_auth")),
        },
        status=status,
    )


class InitiateView(View):
    callback_view_name = "receive_redirect_view"
    client_id = None
    scope = "openid"
    params = {}
    algorithm = SupportedAlgorithms.ES256

    def get(self, request):
        pkce_secret = PKCESecret()
        redirect_uri = request.build_absolute_uri(reverse(self.callback_view_name))
        authorization_endpoint = config.cfg(self.algorithm).get("authorization_endpoint")
        state = base64.urlsafe_b64encode(get_random_string().encode()).decode()
        self.params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": state,
            "scope": self.scope,
            "code_challenge": pkce_secret.challenge,
            "code_challenge_method": pkce_secret.challenge_method,
            "ui_locales": "en",
            "nonce": get_random_string(),
        }
        cache.set(state, str(pkce_secret), timeout=600)
        log.info(f"OIDC Initiate: {authorization_endpoint}?{urlencode(self.params)}")
        return redirect(f"{authorization_endpoint}?{urlencode(self.params)}")


class CallbackView(View):
    callback_view_name = "receive_redirect_view"
    client_id = None
    user = None
    payload = None

    def fail(self, request, msg):
        raise BadRequestException(msg)

    def dispatch(self, request, *args, **kwargs):
        code = request.GET.get("code")
        state = request.GET.get("state")
        if not code or not state:
            log.warning(f"OIDC No code or state in the request {request.GET}")
            return self.fail(request, "No code or state in the request")

        redirect_uri = request.build_absolute_uri(reverse(self.callback_view_name))
        if state := cache.get(state):
            token = get_access_token(code, redirect_uri, state, self.client_id)
            self.payload = oidc_handler.decode_token(token)
            self.user = UserHandler(self.payload, request, token).get_user()
            return super().dispatch(request, *args, **kwargs)
        return self.fail(request, "No PKCE secret found in cache")


class StartOIDCAuthView(InitiateView):
    client_id = jwt_settings.OIDC_ADMIN_CLIENT_ID
    scope = jwt_settings.OIDC_ADMIN_SCOPE


class ReceiveRedirectView(CallbackView):
    client_id = jwt_settings.OIDC_ADMIN_CLIENT_ID

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except HTTPError as exc:
            log.warning(f"OIDC Admin HTTPError: {exc}")
            return index_response(request=request, msg=exc.response.text, status=exc.response.status_code)
        except ConfigException as exc:
            return HttpResponse(content=str(exc), status=500)
        except BadRequestException as exc:
            return index_response(request=request, msg=str(exc))
        except Exception as exc:
            return index_response(request=request, msg=str(exc))

    def get(self, request):
        log.info(f"OIDC Admin login: {self.user}", extra={"data": self.payload})
        roles = role_handler.apply(self.user, self.payload)
        if not self.user.is_staff:
            raise BadRequestException(f"User {self.user.email} is not staff\nRoles: {roles}")
        login(request, self.user, backend=jwt_settings.OIDC_AUTHORIZATION_BACKEND)
        return redirect("admin:index")


class LogoutView(View):
    def get(self, request):
        return index_response(request, "Logged out", status=401)
