# (C) 2024 Fujitsu Limited

import base64
import hashlib
import hmac
import json
import os
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

import requests
from botocore.exceptions import ClientError
from filelock import BaseFileLock, FileLock
from requests.auth import AuthBase

from fujitsu_quantum import aws_utils


class FjqAuthError(Exception):
    @property
    def msg(self) -> str:
        return self.args[0]


class FjqAuth(ABC, AuthBase):
    CREDENTIALS_DIR: str = ".fujitsu-quantum/"
    CREDENTIALS_FILE: str = "credentials.json"
    CREDENTIALS_FILEPATH: Path = Path(Path.home() / CREDENTIALS_DIR / CREDENTIALS_FILE)
    CREDENTIALS_FILE_LOCK_PATH: Path = CREDENTIALS_FILEPATH.with_suffix(CREDENTIALS_FILEPATH.suffix + ".lock")
    TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    def __init__(self) -> None:
        self._load_credentials()

    @staticmethod
    def store_credentials(client_id: str,
                          username: str,
                          access_token: str,
                          access_token_expiration_time: datetime,
                          refresh_token: str,
                          refresh_token_expiration_time: datetime,
                          device_key: Optional[str]) -> None:

        if not os.path.exists(Path.home() / FjqAuth.CREDENTIALS_DIR):
            os.makedirs(Path.home() / FjqAuth.CREDENTIALS_DIR)

        try:
            lock = FileLock(FjqAuth.CREDENTIALS_FILE_LOCK_PATH)
            with lock:
                with os.fdopen(
                    os.open(FjqAuth.CREDENTIALS_FILEPATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w"
                ) as cred_json_file:
                    cred_json = {
                        "ClientId": client_id,
                        "Username": username,
                        "AccessToken": access_token,
                        "AccessTokenExpirationTime": access_token_expiration_time.strftime(FjqAuth.TIME_FORMAT),
                        "RefreshToken": refresh_token,
                        "RefreshTokenExpirationTime": refresh_token_expiration_time.strftime(FjqAuth.TIME_FORMAT),
                    }

                    if device_key is not None:
                        cred_json["DeviceKey"] = device_key

                    cred_json_file.write(json.dumps(cred_json, indent=4))
        except FileNotFoundError:
            raise FjqAuthError(f"Unable to open credentials file lock: {FjqAuth.CREDENTIALS_FILE_LOCK_PATH}")

    def _read_credential_file(self, parent_lock: Optional[BaseFileLock] = None) -> Dict[str, str]:
        try:
            lock = parent_lock
            if lock is None:
                lock = FileLock(FjqAuth.CREDENTIALS_FILE_LOCK_PATH)

            with lock:
                try:
                    with open(self.CREDENTIALS_FILEPATH, 'r') as cred_json_file:
                        return json.load(cred_json_file)

                except FileNotFoundError:
                    raise FjqAuthError(
                        "Credentials not found."
                        " Please run `fujitsu-quantum login` to configure credentials.",
                    )

                except json.JSONDecodeError:
                    raise FjqAuthError("The credential data is corrupted."
                                       " Please run `fujitsu-quantum login` to configure credentials.")

        except FileNotFoundError:
            raise FjqAuthError(f"Unable to open credentials file lock: {FjqAuth.CREDENTIALS_FILE_LOCK_PATH}")

    def _load_credentials(self, parent_lock: Optional[BaseFileLock] = None) -> None:
        cred_json = self._read_credential_file(parent_lock)
        try:
            self._client_id: str = cred_json["ClientId"]
            self._username: str = cred_json["Username"]
            self._access_token: str = cred_json["AccessToken"]
            self._access_token_expiration_time: str = cred_json["AccessTokenExpirationTime"]
            self._refresh_token: str = cred_json["RefreshToken"]
            self.refresh_token_expiration_time: str = cred_json["RefreshTokenExpirationTime"]
            self._device_key: Optional[str] = cred_json.get("DeviceKey", None)
        except KeyError:
            raise FjqAuthError("The credentials are outdated."
                               " Please run `fujitsu-quantum login` to update the credentials.")

    @abstractmethod
    def refresh_auth(self, force: bool = False) -> None:
        raise NotImplementedError()

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        r.headers["authorization"] = "Bearer " + self._access_token
        return r

    def update_authorization_header(self, r: requests.PreparedRequest):
        r.headers["authorization"] = "Bearer " + self._access_token


class FjqAuthBoto3(FjqAuth):
    # TODO some error handling
    def refresh_auth(self, force: bool = False) -> None:
        """
        Refreshes the access token.
        If there is still time before the access token expires, this method does not refresh the access token to avoid
        excessive token refresh requests.
        """
        try:
            lock = FileLock(FjqAuth.CREDENTIALS_FILE_LOCK_PATH)
            with lock:
                if not force:
                    # Other threads or processes may have updated the credential file; it should reload the file.
                    self._load_credentials(lock)
                    expiration_time = datetime.strptime(self._access_token_expiration_time, FjqAuth.TIME_FORMAT)
                    if expiration_time - datetime.now() > timedelta(minutes=10):
                        return

                # refresh the access token with the refresh token
                client = aws_utils.get_client("cognito-idp", region_name="ap-northeast-1")

                new_hmac = hmac.new(bytes(self._username + self._client_id, "utf-8"),
                                    digestmod=hashlib.sha256).digest()
                secret_hash = base64.b64encode(new_hmac).decode()

                auth_params = {
                    "USERNAME": self._username,
                    "SECRET_HASH": secret_hash,
                    "REFRESH_TOKEN": self._refresh_token,
                }

                if self._device_key is not None:
                    auth_params["DEVICE_KEY"] = self._device_key

                try:
                    current_time = datetime.now()
                    response = client.initiate_auth(
                        ClientId=self._client_id,
                        AuthFlow="REFRESH_TOKEN_AUTH",
                        AuthParameters=auth_params,
                    )
                    self._access_token = response["AuthenticationResult"]["AccessToken"]
                    access_token_expires_in = response["AuthenticationResult"]["ExpiresIn"]
                    self._access_token_expiration_time = current_time + timedelta(seconds=access_token_expires_in)
                except ClientError as e:
                    if e.response["Error"]["Code"] == 'NotAuthorizedException':
                        raise FjqAuthError('The credentials have expired.'
                                           ' Please run `fujitsu-quantum login` to update the credentials.')
                    else:
                        raise e

                # update the credentials file
                cred_json = self._read_credential_file(lock)
                cred_json["AccessToken"] = self._access_token
                cred_json["AccessTokenExpirationTime"] = self._access_token_expiration_time.strftime(FjqAuth.TIME_FORMAT)
                with open(self.CREDENTIALS_FILEPATH, "w") as cred_json_file:
                    cred_json_file.write(json.dumps(cred_json, indent=4))

        except FileNotFoundError:
            raise FjqAuthError(f"Unable to open credentials file lock: {FjqAuth.CREDENTIALS_FILE_LOCK_PATH}")

    def logout(self) -> None:
        client = aws_utils.get_client("cognito-idp", region_name="ap-northeast-1")
        client.revoke_token(Token=self._refresh_token, ClientId=self._client_id)
