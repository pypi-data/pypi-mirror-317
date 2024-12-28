# (C) 2024 Fujitsu Limited

from typing import Dict, Optional, Tuple, Union, cast

from qiskit.circuit import Barrier, Measure
from qiskit.circuit.library import IGate, RZGate, SXGate
from qiskit.circuit.parameter import Parameter
from qiskit.providers import Options
from qiskit.providers import ProviderV1 as Provider
from qiskit.providers import QubitProperties
from qiskit.pulse.calibration_entries import CalibrationEntry
from qiskit.pulse.schedule import Schedule, ScheduleBlock
from qiskit.transpiler import InstructionProperties, Target

from fujitsu_quantum.devices import QPU, Devices
from fujitsu_quantum.plugins.qiskit import __version__
from fujitsu_quantum.plugins.qiskit.backends import FujitsuBackend
from fujitsu_quantum.plugins.qiskit.library import RZX90Gate


class FujitsuQPUCalibrationError(Exception):
    pass


class FujitsuQPUQubitProperties(QubitProperties):

    __slots__ = ('ro_error',)

    def __init__(self,
                 t1: float,
                 t2: float,
                 ro_error: float,
                 frequency: Optional[float] = None):

        super().__init__(t1, t2, frequency)
        self.ro_error = ro_error

    def __repr__(self):
        return f'QubitProperties(t1={self.t1}, ' \
            f't2={self.t2}, ' \
            f'ro_error={self.ro_error}, ' \
            f'frequency={self.frequency})'


class FujitsuQPUMeasureInstructionProperties(InstructionProperties):

    __slots__ = ("meas_prob_0_as_1", "meas_prob_1_as_0")

    def __init__(self,
                 duration: float,
                 meas_prob_0_as_1: float,
                 meas_prob_1_as_0: float,
                 calibration: Optional[Union[Schedule, ScheduleBlock, CalibrationEntry]] = None):

        super().__init__(duration=duration,
                         error=(meas_prob_0_as_1 + meas_prob_1_as_0) / 2,
                         calibration=calibration)
        self.meas_prob_0_as_1 = meas_prob_0_as_1
        self.meas_prob_1_as_0 = meas_prob_1_as_0

    def __repr__(self):
        return f'InstructionProperties(duration={self.duration}, ' \
            f'error={self.error}, ' \
            f'meas_prob_0_as_1={self.meas_prob_0_as_1}, ' \
            f'meas_prob_1_as_0={self.meas_prob_1_as_0}, ' \
            f'calibration={self._calibration})'


class FujitsuQPUBackend(FujitsuBackend):

    DEVICE_NAME: str = 'SC'

    def __init__(self, provider: Provider = None):

        super().__init__(provider=provider,
                         name=FujitsuQPUBackend.DEVICE_NAME,
                         backend_version=__version__)

        self._dev: QPU = cast(QPU, self._dev)

        self.options.set_validator('qubit_allocation',
                                   dict)
        self.options.set_validator('ro_error_mitigation',
                                   ['none', 'pseudo_inverse', 'least_square'])

        self.description = f'Backend for the Fujitsu superconducting quantum computer with {self._dev.n_qubits} qubits'

    def _init_device(self) -> QPU:
        return Devices.get(FujitsuQPUBackend.DEVICE_NAME)

    def _init_target(self) -> Target:

        qubit_properties = None

        if (self._dev.has_calibration):
            if (self._dev.t1.keys() == self._dev.t2.keys() == self._dev.ro_error.keys()):
                qubit_properties = [FujitsuQPUQubitProperties(t1=self._dev.t1[q],
                                                              t2=self._dev.t2[q],
                                                              ro_error=self._dev.ro_error[q])
                                    for q in self._dev.t1.keys()]
            else:
                raise FujitsuQPUCalibrationError('Inconsistent qubit indices in qubit properties '
                                                 'of device\'s calibration data.')

        target = Target(num_qubits=self._dev.n_qubits,
                        qubit_properties=qubit_properties)

        target.add_instruction(SXGate(), self._get_1q_gate_properties('sx'))
        target.add_instruction(IGate(), self._get_1q_gate_properties('id'))
        target.add_instruction(RZGate(Parameter('phi')), self._get_1q_gate_properties('rz'))
        target.add_instruction(RZX90Gate(), self._get_2q_gate_properties('rzx90'))
        target.add_instruction(Barrier, name='barrier')
        target.add_instruction(Measure(), self._get_measure_properties())

        return target

    def _get_1q_gate_properties(self, gate_name: str) -> Optional[Dict[Tuple, InstructionProperties]]:
        props = None

        if (self._dev.has_calibration):
            if (gate_name in self._dev.gate_duration and gate_name in self._dev.gate_error):
                if (self._dev.gate_duration[gate_name].keys() == self._dev.gate_error[gate_name].keys()):
                    props = {
                        (q,): InstructionProperties(duration=self._dev.gate_duration[gate_name][q],
                                                    error=self._dev.gate_error[gate_name][q])
                        for q in self._dev.gate_duration[gate_name].keys()
                    }
                else:
                    raise FujitsuQPUCalibrationError('Inconsistent qubit indices in {0} instruction properties '
                                                     'of device\'s calibration data.'.format(gate_name))
            else:
                raise FujitsuQPUCalibrationError('Missing {0} instruction properties '
                                                 'of device\'s calibration data.'.format(gate_name))
        return props

    def _get_2q_gate_properties(self, gate_name: str) -> Optional[Dict[Tuple, InstructionProperties]]:
        props = None

        if (self._dev.has_calibration):
            if (gate_name in self._dev.gate_duration and gate_name in self._dev.gate_error):
                if (self._dev.qubit_connectivity ==
                   list(self._dev.gate_duration[gate_name].keys()) ==
                   list(self._dev.gate_error[gate_name].keys())):
                    props = {
                        conn: InstructionProperties(duration=self._dev.gate_duration[gate_name][conn],
                                                    error=self._dev.gate_error[gate_name][conn])
                        for conn in self._dev.qubit_connectivity
                    }
                else:
                    raise FujitsuQPUCalibrationError('Inconsistent qubit connecitons in {0} instruction properties '
                                                     'of device\'s calibration data.'.format(gate_name))
            else:
                raise FujitsuQPUCalibrationError('Missing {0} instruction properties '
                                                 'of device\'s calibration data.'.format(gate_name))
        return props

    def _get_measure_properties(self) -> Optional[Dict[Tuple, InstructionProperties]]:
        props = None

        if (self._dev.has_calibration):
            if ('measure' in self._dev.gate_duration):
                if (self._dev.gate_duration['measure'].keys() ==
                   self._dev.meas_prob_0_as_1.keys() ==
                   self._dev.meas_prob_1_as_0.keys()):
                    props = {
                        (q,): FujitsuQPUMeasureInstructionProperties(duration=self._dev.gate_duration['measure'][q],
                                                                     meas_prob_0_as_1=self._dev.meas_prob_0_as_1[q],
                                                                     meas_prob_1_as_0=self._dev.meas_prob_1_as_0[q])
                        for q in self._dev.meas_prob_0_as_1.keys()
                    }
                else:
                    raise FujitsuQPUCalibrationError('Inconsistent qubit indices in {0} instruction properties '
                                                     'of device\'s calibration data.'.format('measure'))
            else:
                raise FujitsuQPUCalibrationError('Missing {0} instruction duration '
                                                 'of device\'s calibration data.'.format('measure'))
        return props

    @classmethod
    def _default_options(cls) -> Options:
        options = super()._default_options()
        options.update_options(qubit_allocation=None,
                               ro_error_mitigation='none')
        return options

    def update_calibration_data(self):
        self._dev.update_calibration_data()
        # re-initialize target
        self._target = self._init_target()
