from datetime import datetime, timezone
from functools import cache
from logging import getLogger

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db import transaction
from django.db.utils import IntegrityError
from django.http.request import HttpRequest

from django_jwt import settings
from django_jwt.utils import oidc_handler

utc = timezone.utc
log = getLogger(__name__)

model = get_user_model()


def mapper(user_data: dict) -> dict:
    if callable(settings.OIDC_USER_MAPPING):
        return settings.OIDC_USER_MAPPING(user_data)
    return {ca_key: user_data[kc_key] for kc_key, ca_key in settings.OIDC_USER_MAPPING.items() if kc_key in user_data}


class UserHandler:
    modified_at = None
    userdata_collected = False

    def __init__(self, payload: dict, request: HttpRequest, access_token: str):
        self.payload = payload
        self.kwargs = settings.OIDC_USER_DEFAULTS.copy()
        self.kwargs[settings.OIDC_USER_UID] = payload[settings.OIDC_TOKEN_USER_UID]

        modified_at = payload.get(settings.OIDC_TOKEN_MODIFIED_FIELD, None)
        if modified_at and isinstance(modified_at, int):
            self.modified_at = datetime.fromtimestamp(modified_at, utc)

        self.on_create = settings.OIDC_USER_ON_CREATE
        self.on_update = settings.OIDC_USER_ON_UPDATE
        self.request = request
        self.access_token = access_token

    def _collect_user_data(self):
        """Collect user data from KeyCloak"""

        if not self.userdata_collected:
            user_data = oidc_handler.get_user_info(self.access_token)
            log.debug(f"[OIDC] User data: {user_data}")
            self.kwargs["email"] = user_data["email"].lower()
            self.kwargs.update(mapper(user_data))
            self.userdata_collected = True

    def _update_user(self, user):
        """Update user fields if they are changed"""

        self._collect_user_data()
        if hasattr(user, settings.OIDC_USER_MODIFIED_FIELD):
            self.kwargs[settings.OIDC_USER_MODIFIED_FIELD] = self.modified_at
        for key, val in self.kwargs.items():
            if getattr(user, key) != val:
                setattr(user, key, val)
        user.save(update_fields=self.kwargs.keys())

    def _create_new_user(self) -> model:
        """Create new user if user is not found in database even by email."""

        email = self.kwargs.pop("email")
        user, created = model.objects.get_or_create(email=email, defaults=self.kwargs)
        if created and self.on_create:
            self.on_create(user, self.request, self.payload)
        return user

    def _get_by_email(self) -> model:
        """Get user from database by email and update to resave kc_id."""

        self._collect_user_data()
        user = model.objects.get(email=self.kwargs["email"])
        self._update_user(user)
        if self.on_update:
            self.on_update(user, self.request, self.payload)
        return user

    def _update_existing_user(self, user):
        """Check modified_at and update user if it is changed in KeyCloak."""

        user_modified_at = getattr(user, settings.OIDC_USER_MODIFIED_FIELD, None)
        if user_modified_at:
            if not user_modified_at.tzinfo:
                user_modified_at = user_modified_at.replace(tzinfo=utc)
            is_modified = user_modified_at < self.modified_at

            if self.modified_at and is_modified:
                self._update_user(user)
                if self.on_update:
                    self.on_update(user, self.request, self.payload)

    def _clean_kc_id(self):
        model.objects.filter(**{settings.OIDC_USER_UID: self.kwargs[settings.OIDC_USER_UID]}).update(
            **{settings.OIDC_USER_UID: None}
        )

    def get_user(self) -> model:
        """
        Get user from database by kc_id or email.
        If user is not found, create new user.
        Update user fields if they are changed in KeyCloak.
        """

        try:
            with transaction.atomic():
                user = model.objects.get(**{settings.OIDC_USER_UID: self.kwargs[settings.OIDC_USER_UID]})
                self._update_existing_user(user)
            return user

        except IntegrityError:
            # User with this email already exists
            self._clean_kc_id()
            return self._get_by_email()  # Will update kc_id

        except model.DoesNotExist:
            self._collect_user_data()
            try:
                return self._get_by_email()
            except model.DoesNotExist:
                return self._create_new_user()

        except model.MultipleObjectsReturned:
            log.warning(
                f"[OIDC] Multiple users found by {settings.OIDC_USER_UID}: {self.kwargs[settings.OIDC_USER_UID]}"
            )
            # clear kc_id if multiple users found
            self._clean_kc_id()
            return self._get_by_email()


class RoleHandler:
    """
    Process user roles and permissions from access token.
    Token be like:
    ...
    "resource_access": {
        "complete_anatomy": {
            "roles": [
                "admin"
            ]
        }
    },
    """

    @property
    def roles(self) -> dict:
        return {role.name: role for role in settings.OIDC_ADMIN_ROLES}

    @cache
    def get_permissions(self, role_name: str) -> Permission:
        return Permission.objects.filter(codename__in=self.roles[role_name].permissions)

    @cache
    def get_groups(self, role_name: str) -> Group:
        return Group.objects.filter(name__in=self.roles[role_name].groups)

    def apply(self, user: model, access_token: dict) -> list[str]:
        token_roles = access_token.get("resource_access", {}).get(settings.OIDC_ADMIN_CLIENT_ID, {}).get("roles", [])
        for role_name in token_roles:
            if role_name in self.roles:
                role = self.roles[role_name]
                user.groups.add(*self.get_groups(role_name))
                user.user_permissions.add(*self.get_permissions(role_name))
                user.is_staff = True
                if role.is_superuser != user.is_superuser:
                    user.is_superuser = role.is_superuser
                user.save(update_fields=["is_superuser", "is_staff"])
                break

        return token_roles


role_handler = RoleHandler()
