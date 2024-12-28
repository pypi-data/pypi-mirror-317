# (C) 2024 Fujitsu Limited

from __future__ import annotations

import json
import typing
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from uuid import UUID

if typing.TYPE_CHECKING:
    from fujitsu_quantum.tasks import Task


class Result(ABC):

    FIELDS: List[str] = [
        'result',
        'message',
        'transpiledCode',
        'actualQubitAllocation'
    ]

    def __init__(self, task: Task, result_info: Dict[str, Any]):
        self._task = task

        self._init_action_spec_result(result_info)
        self._message: Optional[str] = result_info.get('message', None)

        self._transpiled_code: Optional[str] = result_info.get('transpiledCode', None)

        self._actual_qubit_allocation: Optional[Dict[str, int]] = result_info.get('actualQubitAllocation', None)

    @abstractmethod
    def _init_action_spec_result(self, result_info: Dict[str, Any]) -> None:
        pass

    def __repr__(self):
        attr_dict = {}
        for (k, v) in self.__dict__.items():
            if k == '_task':  # Note we cannot write 'isinstance(v, Task)' here due to circular import
                attr_dict[k[1:]] = f'{v.name} (task_id: {v.task_id})'
            else:
                attr_dict[k[1:]] = str(v)

        return json.dumps(attr_dict, indent=4, sort_keys=True)

    @property
    def task(self) -> Task:
        return self._task

    @property
    def task_id(self) -> UUID:
        return self._task.task_id

    @property
    def task_status(self) -> Task.Status:
        return self._task.status

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def transpiled_code(self) -> Optional[str]:
        return self._transpiled_code

    @property
    def actual_qubit_allocation(self) -> Optional[Dict[str, int]]:
        return self._actual_qubit_allocation


class SamplingResult(Result):

    def _init_action_spec_result(self, result_info: Dict[str, Any]) -> None:
        self._counts: Optional[Dict[str, int]] = result_info.get('result', None)

    @property
    def counts(self) -> Optional[Dict[str, int]]:
        return self._counts


class EstimationResult(Result):

    def _init_action_spec_result(self, result_info: Dict[str, Any]) -> None:
        result = result_info.get('result', None)

        self._exp_val: Optional[complex]

        if (result is not None):
            if (len(result) != 2):
                raise TypeError('Received malformed value from server: {0}'.format(result))
            self._exp_val = complex(result[0], result[1])
        else:
            self._exp_val = None

    @property
    def exp_val(self) -> Optional[complex]:
        return self._exp_val
