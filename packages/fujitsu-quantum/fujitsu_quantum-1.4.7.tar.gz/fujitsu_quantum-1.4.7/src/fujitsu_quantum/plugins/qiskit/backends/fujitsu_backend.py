# (C) 2024 Fujitsu Limited

from abc import abstractmethod
from copy import copy
from typing import List, Optional, Union
from uuid import uuid4

from qiskit import QuantumCircuit
from qiskit.providers import BackendV2 as Backend
from qiskit.providers import Options
from qiskit.providers import ProviderV1 as Provider
from qiskit.transpiler import Target

from fujitsu_quantum.devices import Device
from fujitsu_quantum.plugins.qiskit import FujitsuJob, FujitsuSamplingJob


class FujitsuBackend(Backend):

    _MAX_CIRCUITS = 1

    _DEFAULT_SHOTS = 1024
    _MAX_SHOTS = 1e7

    def __init__(self,
                 provider: Provider,
                 name: str,
                 backend_version: str):

        super().__init__(provider=provider,
                         name=name,
                         backend_version=backend_version)

        self._dev: Device = self._init_device()
        self._target: Target = self._init_target()

        self.options.set_validator("shots",
                                   (1, FujitsuBackend._MAX_SHOTS))
        self.options.set_validator('name',
                                   str)
        self.options.set_validator('description',
                                   str)
        self.options.set_validator('skip_transpilation',
                                   bool)
        self.options.set_validator('seed_transpilation',
                                   int)

    @abstractmethod
    def _init_device(self) -> Device:
        pass

    @abstractmethod
    def _init_target(self) -> Target:
        pass

    @classmethod
    def _default_options(cls) -> Options:
        return Options(shots=FujitsuBackend._DEFAULT_SHOTS,
                       name=None,
                       description=None,
                       skip_transpilation=False,
                       seed_transpilation=None)

    def set_options(self, **fields):
        skip_transpilation = fields.get('skip_transpilation',
                                        self.options.skip_transpilation)

        seed_transpilation = fields.get('seed_transpilation',
                                        self.options.seed_transpilation)

        if (skip_transpilation is True and
           seed_transpilation is not None):
            raise ValueError('Options misconfiguration: can\'t set \'seed_transpilation\' '
                             'when \'skip_transpilation\'=True')

        return super().set_options(**fields)

    @property
    def max_circuits(self) -> Optional[int]:
        return FujitsuBackend._MAX_CIRCUITS

    @property
    def target(self) -> Target:
        return self._target

    def run(self, circuits: Union[QuantumCircuit, List[QuantumCircuit]], **run_options) -> FujitsuJob:
        if not isinstance(circuits, list):
            circuits = [circuits]

        valid_options = {key: value for key, value in run_options.items() if key in self.options}
        unknown_options = set(run_options) - set(valid_options)

        if unknown_options:
            for opt in unknown_options:
                raise AttributeError(f'Options field {opt} is not valid for this backend')

        actual_options = copy(self.options)
        actual_options.update_options(**valid_options)

        if (actual_options.skip_transpilation is True and
           actual_options.seed_transpilation is not None):
            raise ValueError('Options misconfiguration: can\'t set \'seed_transpilation\' '
                             'when \'skip_transpilation\'=True')

        job = FujitsuSamplingJob(backend=self,
                                 job_id=str(uuid4()),
                                 circuits=circuits,
                                 **actual_options)
        job.submit()

        return job
