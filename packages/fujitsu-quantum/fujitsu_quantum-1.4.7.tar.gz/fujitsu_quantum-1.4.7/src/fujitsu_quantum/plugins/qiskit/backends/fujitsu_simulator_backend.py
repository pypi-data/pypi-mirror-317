# (C) 2024 Fujitsu Limited

from typing import cast

from qiskit.circuit import Barrier, Measure, Reset
from qiskit.circuit.library.standard_gates import get_standard_gate_name_mapping
from qiskit.providers import Options
from qiskit.providers import ProviderV1 as Provider
from qiskit.transpiler import Target

from fujitsu_quantum.devices import Devices, Simulator
from fujitsu_quantum.plugins.qiskit import __version__
from fujitsu_quantum.plugins.qiskit.backends import FujitsuBackend


class FujitsuSimulatorBackend(FujitsuBackend):

    # _DEFAULT_CONFIG: Dict[str, Any] = {
    #     'backend_name': 'SVSim', -> name
    #     'backend_version': __version__, -> backend_version
    #     'n_qubits': 39, -> target.num_qubits
    #     'basis_gates': sorted(['x', 'y', 'z', 'h', 's', 'sdg', 't', 'tdg',
    #                            'rx', 'ry', 'rz',
    #                            'cx', 'cz', 'swap',
    #                            'u1', 'u2', 'u3', 'u',
    #                            'p',
    #                            'id', 'sx', 'sxdg']), -> operations
    #     'gates': [], -> not used in V1
    #     'local': True, -> no V2 equivalent property
    #     'simulator': True, -> no V2 equivalent property
    #     'conditional': False, -> no V2 equivalent property
    #     'open_pulse': False, -> no V2 equivalent property
    #     'memory': False, -> no V2 equivalent property
    #     'max_shots': int(1e7), -> no V2 equivalent property
    #     'coupling_map': None, -> coupling_map
    #     'description': 'Fujitsu version of Qulacs Simulator', -> description
    # }

    DEVICE_NAME: str = 'SVSim'

    def __init__(self, provider: Provider = None):

        super().__init__(provider=provider,
                         name=FujitsuSimulatorBackend.DEVICE_NAME,
                         backend_version=__version__)

        self._dev: Simulator = cast(Simulator, self._dev)

        self.options.set_validator('n_nodes',
                                   (1, 1024))
        self.options.set_validator('n_per_node',
                                   (1, 48))
        self.options.set_validator('seed_simulation',
                                   int)
        # TODO improve validation
        self.options.set_validator('svsim_optimization',
                                   dict)

        self.description = 'State vector-based quantum circuit simulator'

    def _init_device(self) -> Simulator:
        return Devices.get(FujitsuSimulatorBackend.DEVICE_NAME)

    def _init_target(self) -> Target:
        target = Target(num_qubits=self._dev.n_qubits)

        gate_name_mapping = get_standard_gate_name_mapping().copy()

        # The name of the U gate in Qiskit is 'u' while that in OpenQASM is 'U'.
        # gate_name_mapping uses Qiskit-based names while self._dev.basis_gates uses OpenQASM gate names.
        # For consistency, it needs to make gate_name_mapping have a mapping of 'U'.
        gate_name_mapping['U'] = gate_name_mapping['u']
        for gate in sorted(self._dev.basis_gates):
            target.add_instruction(gate_name_mapping[gate])

        target.add_instruction(Barrier, name='barrier')
        target.add_instruction(Reset())
        target.add_instruction(Measure())

        return target

    @classmethod
    def _default_options(cls) -> Options:
        options = super()._default_options()
        options.update_options(n_nodes=None,
                               n_per_node=1,
                               seed_simulation=None,
                               svsim_optimization=None)
        return options
