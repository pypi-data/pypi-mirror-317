# (C) 2024 Fujitsu Limited

from typing import List

from qiskit.providers import BackendV2 as Backend
from qiskit.providers import ProviderV1 as Provider
from qiskit.providers.providerutils import filter_backends

from fujitsu_quantum.plugins.qiskit.backends import FujitsuQPUBackend, FujitsuSimulatorBackend


class FujitsuProvider(Provider):

    def __init__(self):
        super().__init__()
        self._backends: List[Backend] = [FujitsuQPUBackend(provider=self),
                                         FujitsuSimulatorBackend(provider=self)]

    def backends(self, name=None, **kwargs) -> List[Backend]:
        if (name):
            backend_candidates = [backend for backend in self._backends if backend.name == name]
        else:
            backend_candidates = self._backends.copy()
        return filter_backends(backend_candidates, **kwargs)
