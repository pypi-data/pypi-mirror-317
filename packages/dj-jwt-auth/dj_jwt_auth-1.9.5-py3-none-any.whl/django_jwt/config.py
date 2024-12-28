import json
from enum import StrEnum
from functools import cache
from urllib.parse import urljoin

import requests
from jwt.algorithms import ECAlgorithm, RSAAlgorithm

from django_jwt import settings
from django_jwt.exceptions import AlgorithmNotSupportedException, ConfigException


class SupportedAlgorithms(StrEnum):
    ES256 = "ES256"
    RS256 = "RS256"


def ensure_well_known(url: str) -> str:
    if url.endswith(".well-known/openid-configuration"):
        return url
    return urljoin(url, ".well-known/openid-configuration")


class Config:
    def __init__(self):
        self.route = settings.OIDC_CONFIG_ROUTES

    @cache
    def cfg(self, alg: str) -> dict:
        if not self.route:
            raise ConfigException("OIDC_CONFIG_ROUTES is not set")

        if alg not in self.route:
            raise AlgorithmNotSupportedException(f"Algorithm {alg} is not supported")

        response = requests.get(ensure_well_known(self.route[alg]))
        response.raise_for_status()
        return response.json()

    @cache
    def get_public_key(self, alg: str) -> str:
        certs_data_response = requests.get(self.cfg(alg)["jwks_uri"])
        certs_data_response.raise_for_status()

        certs_data = certs_data_response.json()
        for key_data in certs_data["keys"]:
            if key_data["alg"] == alg:
                algorithm = RSAAlgorithm if key_data["kty"] == "RSA" else ECAlgorithm
                return algorithm.from_jwk(json.dumps(key_data))


config = Config()
