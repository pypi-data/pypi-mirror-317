# (C) 2024 Fujitsu Limited

from __future__ import annotations

import json
import re
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from fujitsu_quantum.config import Config
from fujitsu_quantum.requests import FjqRequest
from fujitsu_quantum.results import EstimationResult, Result, SamplingResult


class Task(ABC):

    ENDPOINT: str = Config.api_base + '/tasks'
    DEFAULT_SHOTS: int = 1024

    class Status(str, Enum):
        QUEUED = 'QUEUED',
        RUNNING = 'RUNNING',
        COMPLETED = 'COMPLETED',
        FAILED = 'FAILED',
        CANCELLING = 'CANCELLING',
        CANCELLED = 'CANCELLED'

    class Type(str, Enum):
        SAMPLING = 'sampling',
        ESTIMATION = 'estimation'

    class EstimationMethod(str, Enum):
        SAMPLING = 'sampling',
        STATE_VECTOR = 'state_vector'

    class ROErrorMitigation(str, Enum):
        NONE = 'none',
        PSEUDO_INVERSE = 'pseudo_inverse',
        LEAST_SQUARE = 'least_square'

    @classmethod
    def submit(cls,
               device_id: str,
               code: str,
               **kwargs) -> Self:

        post_req_body = cls._get_post_req_body(device_id, code, kwargs)
        post_resp = FjqRequest.post(status_code=HTTPStatus.CREATED,
                                    url=cls.ENDPOINT,
                                    data=json.dumps(post_req_body)).json()
        return cls({**post_req_body, **post_resp})

    @staticmethod
    def _get_post_req_body(device_id: str,
                           code: str,
                           opt_params: Dict[str, Any]) -> Dict[str, Any]:

        body: Dict[str, Any] = {
            "device": device_id,
            "code": code,
        }

        if ('name' in opt_params and opt_params['name'] is not None):
            body['name'] = opt_params['name']
        if ('skip_transpilation' in opt_params and opt_params['skip_transpilation'] is not None):
            body['skipTranspilation'] = opt_params['skip_transpilation']
        if ('seed_transpilation' in opt_params and opt_params['seed_transpilation'] is not None):
            body['seedTranspilation'] = opt_params['seed_transpilation']
        if ('transpilation_options' in opt_params and opt_params['transpilation_options'] is not None):
            body['transpilationOptions'] = opt_params['transpilation_options']
        if ('description' in opt_params and opt_params['description'] is not None):
            body['note'] = opt_params['description']
        if ('experimental' in opt_params and opt_params['experimental'] is not None):
            body['experimental'] = opt_params['experimental']

        # simulator specific params
        if ('n_nodes' in opt_params and opt_params['n_nodes'] is not None):
            body['nNodes'] = opt_params['n_nodes']
        if ('n_per_node' in opt_params and opt_params['n_per_node'] is not None):
            body['nPerNode'] = opt_params['n_per_node']
        if ('seed_simulation' in opt_params and opt_params['seed_simulation'] is not None):
            body['seedSimulation'] = opt_params['seed_simulation']
        if ('svsim_optimization' in opt_params and opt_params['svsim_optimization'] is not None):
            body['svsimOptimization'] = opt_params['svsim_optimization']

        # quantum device specific params
        if ('qubit_allocation' in opt_params and opt_params['qubit_allocation'] is not None):
            body['qubitAllocation'] = opt_params['qubit_allocation']
        if ('ro_error_mitigation' in opt_params and opt_params['ro_error_mitigation'] is not None):
            body['roErrorMitigation'] = opt_params['ro_error_mitigation']

        return body

    def __init__(self,
                 task_def: Dict[str, Any]):

        self._task_id: UUID = UUID(task_def['taskId'])

        self._device_id: str = task_def['device']
        self._code: str = task_def['code']

        self._type: Task.Type = Task.Type(task_def['type'])
        self._init_type_params(task_def)

        self._status: Task.Status = Task.Status(task_def['status'])
        self._created_at: datetime = datetime.strptime(task_def['createdAt'], '%Y-%m-%d %H:%M:%S')

        self._name: str = task_def['name']
        self._skip_transpilation: bool = task_def.get('skipTranspilation', False)
        self._seed_transpilation: Optional[int] = task_def.get('seedTranspilation', None)
        self._transpilation_options: Optional[Dict[str, Any]] = task_def.get('transpilationOptions', None)

        self._description: Optional[str] = task_def.get('note', None)
        self._experimental: Optional[Dict[str, Any]] = task_def.get('experimental', None)

        self._n_nodes: Optional[int] = task_def.get('nNodes', None)
        self._n_per_node: Optional[int] = task_def.get('nPerNode', None)
        self._seed_simulation: Optional[int] = task_def.get('seedSimulation', None)
        self._svsim_optimization: Optional[Dict[str, Any]] = task_def.get('svsimOptimization', None)

        self._qubit_allocation: Optional[Dict[str, int]] = task_def.get('qubitAllocation', None)
        ro_err_mit = task_def.get('roErrorMitigation', None)
        if (ro_err_mit is not None):
            self._ro_error_mitigation: Optional[Task.ROErrorMitigation] = Task.ROErrorMitigation(ro_err_mit)
        else:
            self._ro_error_mitigation = None

        self._result: Optional[Result] = None

    @abstractmethod
    def _init_type_params(self, task_def: Dict[str, Any]):
        pass

    @property
    def task_id(self) -> UUID:
        return self._task_id

    @property
    def device_id(self) -> str:
        return self._device_id

    @property
    def code(self) -> str:
        return self._code

    @property
    def type(self) -> Type:
        return self._type

    @property
    def status(self) -> Status:
        if (self._status not in [Task.Status.COMPLETED,
                                 Task.Status.FAILED,
                                 Task.Status.CANCELLED]):
            self._status = Task.Status(FjqRequest.get(url=self.ENDPOINT + '/' + str(self._task_id),
                                                      params={'fields': 'status'})
                                       .json()['status'])

        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def name(self) -> str:
        return self._name

    @property
    def skip_transpilation(self) -> bool:
        return self._skip_transpilation

    @property
    def seed_transpilation(self) -> Optional[int]:
        return self._seed_transpilation

    @property
    def transpilation_options(self) -> Optional[Dict[str, Any]]:
        return self._transpilation_options

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def experimental(self) -> Optional[Dict[str, Any]]:
        return self._experimental

    @property
    def n_nodes(self) -> Optional[int]:
        return self._n_nodes

    @property
    def n_per_node(self) -> Optional[int]:
        return self._n_per_node

    @property
    def seed_simulation(self) -> Optional[int]:
        return self._seed_simulation

    @property
    def svsim_optimization(self) -> Optional[Dict[str, Any]]:
        return self._svsim_optimization

    @property
    def qubit_allocation(self) -> Optional[Dict[str, int]]:
        return self._qubit_allocation

    @property
    def ro_error_mitigation(self) -> Optional[ROErrorMitigation]:
        return self._ro_error_mitigation

    def result(self, polling_interval: Optional[float] = None):
        if ((polling_interval is not None)
                and ((not isinstance(polling_interval, float)) or (polling_interval < 1))):
            raise ValueError(f'polling_interval must be a floating-point number greater than or equal to 1, but {polling_interval} is specified.')

        # the argument 'polling_interval' is used over the config value
        if polling_interval is None:
            actual_polling_interval = Config.result_polling_interval
        else:
            actual_polling_interval = polling_interval

        if self._result is None:
            while (self.status not in [Task.Status.COMPLETED,
                                       Task.Status.FAILED,
                                       Task.Status.CANCELLED]):
                # self.status checks status value in API
                time.sleep(actual_polling_interval)

            resp = FjqRequest.get(url=Task.ENDPOINT + '/' + str(self._task_id),
                                  params={'fields': ','.join(Result.FIELDS)})
            if self._type == Task.Type.SAMPLING:
                self._result = SamplingResult(self, resp.json())
            else:
                self._result = EstimationResult(self, resp.json())

        return self._result

    def cancel(self) -> None:
        FjqRequest.post(status_code=HTTPStatus.OK,
                        url=self.ENDPOINT + '/' + str(self._task_id) + '/cancel')

    def delete(self) -> None:
        FjqRequest.delete(url=self.ENDPOINT + '/' + str(self._task_id))

    def __repr__(self):
        attr_dict = {}
        for (k, v) in self.__dict__.items():
            if isinstance(v, Result):
                attr_dict[k[1:]] = json.loads(repr(v))
            elif type(v) in [UUID, datetime]:
                attr_dict[k[1:]] = str(v)
            else:
                attr_dict[k[1:]] = v

        return json.dumps(attr_dict, indent=4, sort_keys=True)


class SamplingTask(Task):

    @staticmethod
    def _get_post_req_body(device_id: str, code: str, opt_params: Dict[str, Any]) -> Dict[str, Any]:
        body = Task._get_post_req_body(device_id, code, opt_params)
        body['type'] = Task.Type.SAMPLING
        body['nShots'] = opt_params.get('n_shots', Task.DEFAULT_SHOTS)
        return body

    def _init_type_params(self,
                          task_def: Dict[str, Any]) -> None:
        self._n_shots: int = task_def['nShots']

    @property
    def n_shots(self) -> int:
        return self._n_shots


class EstimationTask(Task):

    @staticmethod
    def _get_post_req_body(device_id: str, code: str, opt_params: Dict[str, Any]) -> Dict[str, Any]:
        body = Task._get_post_req_body(device_id, code, opt_params)

        body['type'] = Task.Type.ESTIMATION
        body['method'] = opt_params['method']

        if (body['method'] == Task.EstimationMethod.SAMPLING):
            body['nShots'] = opt_params.get('n_shots', Task.DEFAULT_SHOTS)
        else:
            if ('n_shots' in opt_params):
                raise TypeError('_get_post_req_body(): invalid keyword argument '
                                'for method \'state_vector\': \'n_shots\'')

        if ('operator' in opt_params):
            body['operator'] = opt_params['operator']
        else:
            raise TypeError('_get_post_req_body() missing 1 required keyword argument: \'operator\'')

        return body

    def _init_type_params(self,
                          task_def: Dict[str, Any]) -> None:
        self._method: Task.EstimationMethod = Task.EstimationMethod(task_def['method'])
        self._n_shots: Optional[int] = task_def.get('nShots', None)
        self._operator: List[List[Union[str, List[float], float]]] = task_def['operator']

    @property
    def method(self) -> Task.EstimationMethod:
        return self._method

    @property
    def n_shots(self) -> Optional[int]:
        return self._n_shots

    @property
    def operator(self) -> List[List[Union[str, List[float], float]]]:
        return self._operator


class Tasks:

    class Order(str, Enum):
        ASC = 'ASC'
        DESC = 'DESC'

    @dataclass
    class Pagination:
        # start_page: int = 1
        per_page: int = 10

    @dataclass
    class Filters:
        start_time: Optional[datetime] = None
        end_time: Optional[datetime] = None
        q: Optional[str] = None

    page_url_regex = re.compile('page=(?P<page>\\d+)')

    def __init__(self,
                 order: Order = Order.DESC,
                 pagination: Optional[Pagination] = None,
                 filtering: Optional[Filters] = None):

        self._order: Tasks.Order = order
        self._pagination: Tasks.Pagination = pagination if pagination is not None else Tasks.Pagination()
        self._filtering: Tasks.Filters = filtering if filtering is not None else Tasks.Filters()

        self._url_params = {
            'order': self._order,
            'perPage': self._pagination.per_page
        }
        if (self._filtering.start_time is not None):
            self._url_params['startTime'] = self._filtering.start_time.strftime('%Y-%m-%d %H:%M:%S')
        if (self._filtering.end_time is not None):
            self._url_params['endTime'] = self._filtering.end_time.strftime('%Y-%m-%d %H:%M:%S')
        if (self._filtering.q is not None and len(self._filtering.q) != 0):
            self._url_params['q'] = self._filtering.q

        self._page_tasks: List[Task] = []
        self._page_tasks_index: int = 0
        # self._next_page: Optional[int] = self._pagination.start_page
        self._next_page: Optional[int] = 1

    def _fetch_next_page(self):
        self._url_params['page'] = self._next_page

        resp = FjqRequest.get(url=Task.ENDPOINT,
                              params=self._url_params)

        self._page_tasks = [SamplingTask(task) if task['type'] == 'sampling' else
                            EstimationTask(task)
                            for task in resp.json()]
        self._page_tasks_index = 0

        self._next_page = None
        if ('Link' in resp.headers):
            try:
                for entry in reversed(resp.headers['Link'].split(',')):
                    url, rel = tuple(entry.split(';'))
                    if (rel.find('next') != -1):
                        match = Tasks.page_url_regex.search(url)
                        if (match is not None):
                            self._next_page = int(match.group('page'))
                        else:
                            raise RuntimeError('Malformed response from API. Malformed \'Link\' header: \'{0}\''.
                                               format(resp.headers['Link']))
            except Exception:
                raise RuntimeError('Malformed response from API. Malformed \'Link\' header: \'{0}\''.
                                   format(resp.headers['Link']))
        else:
            raise RuntimeError('Malformed response from API. Missing \'Link\' header')

    def __iter__(self) -> Tasks:
        return self

    def __next__(self) -> Task:
        if (self._page_tasks_index < len(self._page_tasks)):
            self._page_tasks_index += 1
            return self._page_tasks[self._page_tasks_index - 1]
        else:
            if (self._next_page is not None):
                self._fetch_next_page()
                return self.__next__()
            else:
                raise StopIteration

    @staticmethod
    def list(order: Order = Order.DESC,
             pagination: Optional[Pagination] = None,
             filtering: Optional[Filters] = None) -> Tasks:
        return Tasks(order, pagination, filtering)
