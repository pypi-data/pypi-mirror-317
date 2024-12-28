# (C) 2024 Fujitsu Limited

from __future__ import annotations

import json
import warnings
from abc import ABC, abstractmethod
from ast import literal_eval
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from fujitsu_quantum.config import Config
from fujitsu_quantum.requests import FjqRequest
from fujitsu_quantum.tasks import EstimationTask, SamplingTask, Task
from fujitsu_quantum.warnings import FjqWarning


class Device(ABC):

    ENDPOINT: str = Config.api_base + '/devices'

    class Type(str, Enum):
        SIMULATOR = 'simulator',
        QPU = 'QPU'

    class Status(str, Enum):
        AVAILABLE = 'AVAILABLE',
        NOT_AVAILABLE = 'NOT_AVAILABLE'

    def __init__(self, device_info: Dict[str, Any]):
        self._device_id: str = device_info['deviceId']
        self._device_type: Device.Type = Device.Type(device_info['deviceType'])
        self._status: Device.Status = Device.Status(device_info['status'])

        restart_at_str: Optional[str] = device_info.get('restartAt', None)
        if (restart_at_str is not None):
            self._restart_at: Optional[datetime] = datetime.strptime(restart_at_str, '%Y-%m-%d %H:%M:%S')
        else:
            self._restart_at = None

        self._n_pending_tasks: int = device_info['nPendingTasks']
        self._n_qubits: int = device_info['nQubits']
        self._basis_gates: List[str] = device_info['basisGates']
        self._supported_instructions: List[str] = device_info['supportedInstructions']
        self._description: str = device_info['description']

        self._init_device_specific_data(device_info)

    @abstractmethod
    def _init_device_specific_data(self, device_info: Dict[str, Any]) -> None:
        pass

    @property
    def device_id(self) -> str:
        return self._device_id

    @property
    def device_type(self) -> Type:
        return self._device_type

    @property
    def status(self) -> Status:
        return self._status

    @property
    def restart_at(self) -> Optional[datetime]:
        return self._restart_at

    @property
    def n_pending_tasks(self) -> int:
        return self._n_pending_tasks

    @property
    def n_qubits(self) -> int:
        return self._n_qubits

    @property
    def basis_gates(self) -> List[str]:
        return self._basis_gates

    @property
    def supported_instructions(self) -> List[str]:
        return self._supported_instructions

    @property
    def description(self) -> str:
        return self._description

    def submit_sampling_task(self,
                             code: str,
                             n_shots: int = Task.DEFAULT_SHOTS,
                             name: Optional[str] = None,
                             skip_transpilation: bool = False,
                             seed_transpilation: Optional[int] = None,
                             transpilation_options: Optional[Dict[str, Any]] = None,
                             description: Optional[str] = None,
                             experimental: Optional[Dict[str, Any]] = None,
                             **kwargs) -> SamplingTask:

        return SamplingTask.submit(self.device_id,
                                   code,
                                   n_shots=n_shots,
                                   name=name,
                                   skip_transpilation=skip_transpilation,
                                   seed_transpilation=seed_transpilation,
                                   transpilation_options=transpilation_options,
                                   description=description,
                                   experimental=experimental,
                                   **kwargs)

    def submit_estimation_task(self,
                               code: str,
                               method: Task.EstimationMethod,
                               operator: List[List[Union[str, List[float], float]]],
                               n_shots: Optional[int] = None,
                               name: Optional[str] = None,
                               skip_transpilation: bool = False,
                               seed_transpilation: Optional[int] = None,
                               transpilation_options: Optional[Dict[str, Any]] = None,
                               description: Optional[str] = None,
                               experimental: Optional[Dict[str, Any]] = None,
                               **kwargs) -> EstimationTask:

        estimation_task_params = {
            'method': method,
            'operator': operator,
            'n_shots': n_shots,
            'name': name,
            'skip_transpilation': skip_transpilation,
            'seed_transpilation': seed_transpilation,
            'transpilation_options': transpilation_options,
            'description': description,
            'experimental': experimental,
            **kwargs
        }

        if (method == Task.EstimationMethod.SAMPLING):
            if (estimation_task_params['n_shots'] is None):
                estimation_task_params['n_shots'] = Task.DEFAULT_SHOTS
        else:
            if (estimation_task_params.pop('n_shots') is not None):
                raise TypeError('submit_estimation_task(): invalid keyword argument '
                                'for method \'state_vector\': \'n_shots\'')

        return EstimationTask.submit(self.device_id,
                                     code,
                                     **estimation_task_params)


class Simulator(Device):

    def _init_device_specific_data(self, device_info: Dict[str, Any]) -> None:
        self._n_nodes: int = device_info['nNodes']

    @property
    def n_nodes(self) -> int:
        return self._n_nodes

    def __repr__(self):
        return json.dumps({k[1:]: (v if type(v) != datetime else str(v)) for (k, v) in self.__dict__.items()
                           if v is not None},
                          indent=4, sort_keys=True)

    def submit_sampling_task(self,
                             code: str,
                             n_shots: int = Task.DEFAULT_SHOTS,
                             name: Optional[str] = None,
                             skip_transpilation: bool = False,
                             seed_transpilation: Optional[int] = None,
                             transpilation_options: Optional[Dict[str, Any]] = None,
                             description: Optional[str] = None,
                             experimental: Optional[Dict[str, Any]] = None,
                             n_nodes: Optional[int] = None,
                             n_per_node: int = 1,
                             seed_simulation: Optional[int] = None,
                             svsim_optimization: Optional[Dict[str, Any]] = None,
                             **kwargs) -> SamplingTask:

        return super().submit_sampling_task(code,
                                            n_shots=n_shots,
                                            name=name,
                                            skip_transpilation=skip_transpilation,
                                            seed_transpilation=seed_transpilation,
                                            transpilation_options=transpilation_options,
                                            description=description,
                                            experimental=experimental,
                                            n_nodes=n_nodes,
                                            n_per_node=n_per_node,
                                            seed_simulation=seed_simulation,
                                            svsim_optimization=svsim_optimization)

    def submit_estimation_task(self,
                               code: str,
                               method: Task.EstimationMethod,
                               operator: List[List[Union[str, List[float], float]]],
                               n_shots: Optional[int] = None,
                               name: Optional[str] = None,
                               skip_transpilation: bool = False,
                               seed_transpilation: Optional[int] = None,
                               transpilation_options: Optional[Dict[str, Any]] = None,
                               description: Optional[str] = None,
                               experimental: Optional[Dict[str, Any]] = None,
                               n_nodes: Optional[int] = None,
                               n_per_node: int = 1,
                               seed_simulation: Optional[int] = None,
                               svsim_optimization: Optional[Dict[str, Any]] = None,
                               **kwargs) -> EstimationTask:

        return super().submit_estimation_task(code,
                                              method=method,
                                              operator=operator,
                                              n_shots=n_shots,
                                              name=name,
                                              skip_transpilation=skip_transpilation,
                                              seed_transpilation=seed_transpilation,
                                              transpilation_options=transpilation_options,
                                              description=description,
                                              experimental=experimental,
                                              n_nodes=n_nodes,
                                              n_per_node=n_per_node,
                                              seed_simulation=seed_simulation,
                                              svsim_optimization=svsim_optimization,
                                              **kwargs)


class QPU(Device):

    def _init_device_specific_data(self, device_info: Dict[str, Any]) -> None:

        cal_data = device_info.get('calibrationData', None)

        if (cal_data is not None):
            self._has_calibration = True

            self._qubit_connectivity: List[Tuple[int, int]] = [
                literal_eval(elem) for elem in cal_data['qubitConnectivity']
            ]

            self._t1: Dict[int, float] = {
                int(k): v for (k, v) in cal_data['t1'].items()
            }

            self._t2: Dict[int, float] = {
                int(k): v for (k, v) in cal_data['t2'].items()
            }

            self._ro_error: Dict[int, float] = {
                int(k): v for (k, v) in cal_data['roError'].items()
            }

            self._gate_error: Dict[str, Dict[Union[int, Tuple[int, int]], float]] = {
                gate: {(literal_eval(k)): v for (k, v) in values.items()}
                for (gate, values) in cal_data['gateError'].items()}

            self._meas_prob_0_as_1: Dict[int, float] = {
                int(k): v for (k, v) in cal_data['measProb0As1'].items()
            }

            self._meas_prob_1_as_0: Dict[int, float] = {
                int(k): v for (k, v) in cal_data['measProb1As0'].items()
            }

            self._gate_duration: Dict[str, Dict[Union[int, Tuple[int, int]], float]] = {
                gate: {(literal_eval(k)): v for (k, v) in values.items()}
                for (gate, values) in cal_data['gateDuration'].items()
            }

            self._calibrated_at: datetime = datetime.strptime(device_info['calibratedAt'], '%Y-%m-%d %H:%M:%S')

        else:
            self._has_calibration = False

    @property
    def has_calibration(self) -> bool:
        return self._has_calibration

    @property
    def qubit_connectivity(self) -> List[Tuple[int, int]]:
        return self._qubit_connectivity

    @property
    def t1(self) -> Dict[int, float]:
        return self._t1

    @property
    def t2(self) -> Dict[int, float]:
        return self._t2

    @property
    def ro_error(self) -> Dict[int, float]:
        return self._ro_error

    @property
    def gate_error(self) -> Dict[str, Dict[Union[int, Tuple[int, int]], float]]:
        return self._gate_error

    @property
    def meas_prob_0_as_1(self) -> Dict[int, float]:
        return self._meas_prob_0_as_1

    @property
    def meas_prob_1_as_0(self) -> Dict[int, float]:
        return self._meas_prob_1_as_0

    @property
    def gate_duration(self) -> Dict[str, Dict[Union[int, Tuple[int, int]], float]]:
        return self._gate_duration

    @property
    def calibrated_at(self) -> datetime:
        return self._calibrated_at

    def __repr__(self):
        return json.dumps({k[1:]: (v if type(v) != datetime else str(v)) for (k, v) in self.__dict__.items()
                           if (v is not None and
                               k[1:] not in ['qubit_connectivity', 't1', 't2', 'ro_error', 'gate_error',
                                             'meas_prob_0_as_1', 'meas_prob_1_as_0', 'gate_duration'])},
                          indent=4, sort_keys=True)

    def update_calibration_data(self) -> None:
        resp = FjqRequest.get(Device.ENDPOINT + "/" + str(self.device_id))
        self._init_device_specific_data(resp.json())

    def submit_sampling_task(self, code: str,
                             n_shots: int = Task.DEFAULT_SHOTS,
                             name: Optional[str] = None,
                             skip_transpilation: bool = False,
                             seed_transpilation: Optional[int] = None,
                             transpilation_options: Optional[Dict[str, Any]] = None,
                             description: Optional[str] = None,
                             experimental: Optional[Dict[str, Any]] = None,
                             qubit_allocation: Optional[Dict[str, int]] = None,
                             ro_error_mitigation: Task.ROErrorMitigation = Task.ROErrorMitigation.NONE,
                             **kwargs) -> SamplingTask:

        if (qubit_allocation is not None):
            warnings.warn('\'qubit_allocation\' is currently not supported.'
                          ' It will be supported in a future version.',
                          FjqWarning)

        return super().submit_sampling_task(code,
                                            n_shots=n_shots,
                                            name=name,
                                            skip_transpilation=skip_transpilation,
                                            seed_transpilation=seed_transpilation,
                                            transpilation_options=transpilation_options,
                                            description=description,
                                            experimental=experimental,
                                            qubit_allocation=qubit_allocation,
                                            ro_error_mitigation=ro_error_mitigation)

    def submit_estimation_task(self,
                               code: str,
                               method: Task.EstimationMethod,
                               operator: List[List[Union[str, List[float], float]]],
                               n_shots: Optional[int] = None,
                               name: Optional[str] = None,
                               skip_transpilation: bool = False,
                               seed_transpilation: Optional[int] = None,
                               transpilation_options: Optional[Dict[str, Any]] = None,
                               description: Optional[str] = None,
                               experimental: Optional[Dict[str, Any]] = None,
                               qubit_allocation: Optional[Dict[str, int]] = None,
                               ro_error_mitigation: Task.ROErrorMitigation = Task.ROErrorMitigation.NONE,
                               **kwargs) -> EstimationTask:

        if (method != Task.EstimationMethod.SAMPLING):
            raise ValueError("submit_estimation_task(): invalid estimation method for QPU device: '{0}'".
                             format(method))

        if (qubit_allocation is not None):
            warnings.warn('\'qubit_allocation\' is currently not supported.'
                          ' It will be supported in a future version.',
                          FjqWarning)

        return super().submit_estimation_task(code,
                                              method=method,
                                              operator=operator,
                                              n_shots=n_shots,
                                              name=name,
                                              skip_transpilation=skip_transpilation,
                                              seed_transpilation=seed_transpilation,
                                              transpilation_options=transpilation_options,
                                              description=description,
                                              experimental=experimental,
                                              qubit_allocation=qubit_allocation,
                                              ro_error_mitigation=ro_error_mitigation,
                                              **kwargs)


class Devices:

    def __init__(self, devices: List[Device]):
        self._devices = devices
        self._devices_iter = iter(self._devices)

    def __iter__(self) -> Devices:
        return self

    def __next__(self) -> Device:
        return next(self._devices_iter)

    @staticmethod
    def list() -> Devices:
        resp = FjqRequest.get(Device.ENDPOINT)
        return Devices([Devices.__createDevice(device_info) for device_info in resp.json()])

    @staticmethod
    def get(device_id: str):
        resp = FjqRequest.get(Device.ENDPOINT + "/" + device_id)
        return Devices.__createDevice(resp.json())

    @staticmethod
    def __createDevice(device_info: Dict[str, Any]):
        if (device_info['deviceType'] == Device.Type.SIMULATOR):
            return Simulator(device_info)
        elif (device_info['deviceType'] == Device.Type.QPU):
            return QPU(device_info)
        else:
            raise TypeError("Received unknown device type from server: '{0}', '{1}'\"}}"
                            .format(device_info['deviceId'], device_info['deviceType']))

    @staticmethod
    def get_QPU(device_id: str) -> QPU:
        resp = FjqRequest.get(Device.ENDPOINT + "/" + device_id)
        if (resp.json()['deviceType'] != Device.Type.QPU):
            raise TypeError('Invalid type of requested device: \'{0}\' is \'{1}\''.
                            format(device_id, resp.json()['deviceType']))
        return QPU(resp.json())

    @staticmethod
    def get_simulator(device_id: str) -> Simulator:
        resp = FjqRequest.get(Device.ENDPOINT + "/" + device_id)
        if (resp.json()['deviceType'] != Device.Type.SIMULATOR):
            raise TypeError('Invalid type of requested device: \'{0}\' is \'{1}\''.
                            format(device_id, resp.json()['deviceType']))
        return Simulator(resp.json())
