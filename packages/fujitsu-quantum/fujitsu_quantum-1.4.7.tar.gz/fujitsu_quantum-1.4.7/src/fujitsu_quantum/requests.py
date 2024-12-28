# (C) 2024 Fujitsu Limited

import traceback
from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

from requests import HTTPError, RequestException, Response, Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from fujitsu_quantum import logging
from fujitsu_quantum.auth import FjqAuthBoto3, FjqAuthError
from fujitsu_quantum.config import Config


class FjqRequestError(Exception):
    """
    Attributes:
        code: Response status code. It can be None if, for example, network errors occur.
        message: Error message.
    """

    def __init__(self, code, message):
        super().__init__(code, message)
        self.code = code
        self.message = message

    def __str__(self):
        if self.code is None:
            return self.message
        else:
            return f'HTTP {self.code}: {self.message}'


class FjqRequest:

    _RETRY_STATUS_FORCE_LIST = [429, 500, 502, 503, 504]

    @staticmethod
    def _new_session() -> Session:
        session = Session()
        # TODO enable users to change the retry parameters via the config file
        # TODO botocore with Python < 3.10 requires urllib3 ver.1.x that does not support the backoff_max parameter.
        #  In urllib3 ver.1.x, it needs to use Retry.DEFAULT_BACKOFF_MAX instead of the backoff_max parameter; the class
        #  attribute can be changed from other libraries. To avoid that, after botocore supports urllib3 ver.2.x, use
        #  use the backoff_max parameter instead of overwriting Retry.DEFAULT_BACKOFF_MAX.

        # The values of backoff_max and backoff_factor are consistent with the boto3 standard retry mode
        Retry.DEFAULT_BACKOFF_MAX = 20
        retries = Retry(total=Config.retry_max_attempts, backoff_factor=0.5,  # backoff_max=16,
                        allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "POST"],
                        status_forcelist=FjqRequest._RETRY_STATUS_FORCE_LIST,
                        raise_on_status=False)
        session.mount('https://', HTTPAdapter(max_retries=retries))
        auth = FjqAuthBoto3()
        session.auth = auth

        def _refresh_auth_hook(r: Response, *args, **kwargs):
            if r.status_code == HTTPStatus.UNAUTHORIZED:
                auth.refresh_auth()
                auth.update_authorization_header(r.request)

                # Because session.send(...) does not respect the environment variables, we need to manually merge it.
                # https://requests.readthedocs.io/en/latest/user/advanced/#prepared-requests
                settings = session.merge_environment_settings(r.request.url, proxies={}, stream=None, verify=None, cert=None)
                r = session.send(r.request, **settings)

            return r

        session.hooks['response'].append(_refresh_auth_hook)
        return session

    @staticmethod
    def _write_error_log(e: Union[RequestException, Exception], additional_info: Optional[str] = None) -> str:
        """Writes the error details to an error log file.

        Returns:
            str: The error log file path.
        """

        err_msg_header = f'FjqRequestError occurred at {str(datetime.utcnow())} UTC.\n----------------------------\n'

        err_msg = ''
        if isinstance(e, RequestException):
            request = e.request
            if request is None:
                err_msg += 'Request: None\n----------------------------\n'
            else:
                err_msg += (f'Request: {request.method} {request.url}\n----------------------------\n'
                            f'Request header: {request.headers}\n----------------------------\n')
                if hasattr(request, 'body'):
                    err_msg += f'Request body: {str(request.body)}\n----------------------------\n'

            response = e.response
            if response is None:
                err_msg += 'Response: None\n----------------------------\n'
            else:
                err_msg += (f'Response status code: {response.status_code}\n----------------------------\n'
                            f'Response header: {response.headers}\n----------------------------\n'
                            f'Response body: {response.json()}\n----------------------------\n')

        if additional_info is not None:
            err_msg += f'Additional info: {additional_info}\n----------------------------\n'

        exception_details = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        err_msg += f'Exception info: \n{exception_details}\n'

        return logging.write_error_log(f'{err_msg_header}{err_msg}')

    @staticmethod
    def __request(method: str, exp_status_code: HTTPStatus, **kwargs: Any) -> Response:
        """
        Parameters:
            method (str): HTTP method to use.
            exp_status_code (HTTPStatus): expected HTTP response status code.
            kwargs (Any): Additional parameters to pass to requests.
        """

        if 'timeout' not in kwargs:
            kwargs['timeout'] = (Config.connect_timeout, Config.read_timeout)

        # TODO Re-design the SDK entirely to support Session instead of creating a new session every time.
        #  Notice: Session is not process-safe. Do not share one Session object among multi-processes.
        session = FjqRequest._new_session()
        try:
            resp: Response = getattr(session, method)(**kwargs)
        except FjqAuthError:
            # This error occurs if, e.g., refresh token has been expired
            # re-throw
            raise
        except Exception as e:
            # e.g., a too-many-redirections error comes into this clause
            log_file_path = FjqRequest._write_error_log(e)
            request_path = method.upper() + ' ' + kwargs.get('url', 'unknown URL')
            raise FjqRequestError(None, f'Request failed: {request_path}\n'
                                        f'Error details have been saved to {log_file_path}')
        else:
            try:
                # In addition to checking the response status code against the expected one,
                # call raise_for_status() to construct a better error message for a 4xx or 5xx response.
                resp.raise_for_status()
                if resp.status_code != exp_status_code:
                    raise HTTPError(f'Unexpected HTTP response code (expected {exp_status_code},'
                                    f' but got {resp.status_code}) for url {resp.url}', response=resp)

                return resp
            except RequestException as e:  # this clause catches HTTPError
                log_file_path = FjqRequest._write_error_log(e)
                request_path = method.upper() + ' ' + kwargs.get('url', 'unknown URL')
                response_err_msg = resp.json().get('error', '')
                err_msg = (f'Request failed: {request_path}\n'
                           f'{response_err_msg}\n'
                           f'Error details have been saved to {log_file_path}')
                raise FjqRequestError(resp.status_code, err_msg) from None

    @staticmethod
    def get(url: str, params: Optional[Dict[str, Any]] = None):
        return FjqRequest.__request('get', exp_status_code=HTTPStatus.OK, url=url, params=params)

    @staticmethod
    def post(status_code: HTTPStatus, url: str, data: str = ''):
        return FjqRequest.__request('post', exp_status_code=status_code, url=url, data=data)

    @staticmethod
    def delete(url: str):
        return FjqRequest.__request('delete', exp_status_code=HTTPStatus.NO_CONTENT, url=url)
