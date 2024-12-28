# (C) 2024 Fujitsu Limited

from __future__ import annotations

import sys
import typing
from abc import abstractmethod
from typing import Any, Dict, List, Optional, Union, cast
from uuid import UUID

from qiskit import QuantumCircuit, qasm3
from qiskit.providers import JobStatus, JobV1
from qiskit.quantum_info import SparsePauliOp
from qiskit.result import Result

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

if typing.TYPE_CHECKING:
    from fujitsu_quantum.plugins.qiskit.backends import FujitsuBackend

from fujitsu_quantum.results import EstimationResult, SamplingResult
from fujitsu_quantum.tasks import EstimationTask, SamplingTask, Task


class FujitsuJob(JobV1):

    __STATUS_MAP: Dict[Task.Status, JobStatus] = {
        Task.Status.QUEUED: JobStatus.QUEUED,
        Task.Status.RUNNING: JobStatus.RUNNING,
        Task.Status.CANCELLING: JobStatus.RUNNING,
        Task.Status.COMPLETED: JobStatus.DONE,
        Task.Status.FAILED: JobStatus.ERROR,
        Task.Status.CANCELLED: JobStatus.CANCELLED
    }

    def __init__(self,
                 backend: FujitsuBackend,
                 job_id: str,
                 circuits: List[QuantumCircuit],
                 **options):
        super().__init__(backend, job_id)

        if typing.TYPE_CHECKING:
            self._backend: FujitsuBackend = cast(FujitsuBackend, self._backend)

        if (backend.max_circuits is not None):
            if (len(circuits) > backend.max_circuits):
                raise ValueError('Requested number of experiments exceeds maximum supported by backend '
                                 '(\'backend.max_circuits\'={0})'.format(backend.max_circuits))

        # currently backend.max_circuits = 1
        self._circuit: QuantumCircuit = circuits[0]
        self._options: Dict[str, Any] = options

        self._task: Optional[Task] = None
        self._result: Optional[Result] = None

        self._submitted: bool = False
        self._final_status: Optional[JobStatus] = None

    """
        List of task_ids related to this job's experiments
    """
    @property
    def task_ids(self) -> List[UUID]:
        return [self._task.task_id] if self._task is not None else []

    def submit(self):
        """
            Raises:
                RuntimeError
                qiskit.qasm3.QASM3ExporterError
                fujitsu_quantum.requests.FjqRequestError
        """

        if (self._submitted):
            raise RuntimeError('Job already submitted')

        self._task = self._submit_task()

        # print(f'Submitted task: {self._task.task_id}')
        self._submitted = True

    @abstractmethod
    def _submit_task(self) -> Task:
        pass

    def result(self) -> Result:
        if not self._submitted:
            raise RuntimeError('Job not submitted')

        if self._result is None:
            # not deleted and result not fetched
            self._result = self._get_result()

        return self._result

    @abstractmethod
    def _get_result(self) -> Result:
        pass

    def cancel(self):
        if not self._submitted:
            raise RuntimeError('Job not submitted')

        if self._task is not None and self._task.status in [Task.Status.QUEUED, Task.Status.RUNNING]:
            # not deleted and has valid state for cancellation
            self._task.cancel()
        else:
            # task already completd/deleted - ignore
            pass

    def delete(self):
        if not self.in_final_state():
            raise RuntimeError('Job is not in final state')

        if self._task is not None:
            # make job result and status available even if task is deleted
            self.result()
            self._final_status = self.status()

            self._task.delete()
            self._task = None
        else:
            # task already deleted - ignore
            pass

    def status(self) -> JobStatus:
        if self._task is not None:
            return self.__STATUS_MAP[self._task.status]
        else:
            if (not self._submitted):
                return JobStatus.INITIALIZING
            else:
                # task deleted
                return self._final_status

    @staticmethod
    def _create_experiment_header(qiskit_circ: QuantumCircuit) -> dict:
        clbit_labels = []
        creg_sizes = []
        memory_slots = 0
        for creg in qiskit_circ.cregs:
            for i in range(creg.size):
                clbit_labels.append([creg.name, i])
            creg_sizes.append([creg.name, creg.size])
            memory_slots += creg.size

        qubit_labels = []
        qreg_sizes = []
        num_qubits = 0
        for qreg in qiskit_circ.qregs:  # 'qregs' includes ancilla registers
            for i in range(qreg.size):
                qubit_labels.append([qreg.name, i])
            qreg_sizes.append([qreg.name, qreg.size])
            num_qubits += qreg.size

        header = {
            'clbit_labels': clbit_labels,
            'creg_sizes': creg_sizes,
            'global_phase': float(qiskit_circ.global_phase),
            'memory_slots': memory_slots,
            'metadata': qiskit_circ.metadata,
            'n_qubits': num_qubits,
            'name': qiskit_circ.name,
            'qreg_sizes': qreg_sizes,
            'qubit_labels': qubit_labels,
        }

        return header


class FujitsuSamplingJob(FujitsuJob):

    def __init__(self,
                 backend: FujitsuBackend,
                 job_id: str,
                 circuits: List[QuantumCircuit],
                 shots: int,
                 **options):

        super().__init__(backend,
                         job_id,
                         circuits,
                         **options)

        self._options['n_shots'] = shots

    def _submit_task(self) -> SamplingTask:
        return self._backend._dev.submit_sampling_task(qasm3.dumps(self._circuit, allow_aliasing=True),
                                                       **self._options)

    def _get_result(self) -> Result:
        if self._task is not None:
            exp_result: SamplingResult = self._task.result()

            if (exp_result.task_status == Task.Status.COMPLETED):
                exp_data = {'counts': exp_result.counts}
                exp_status = 'Experiment was successful'
            else:
                exp_data = {}
                exp_status = f'Experiment was not successful: {exp_result.message}'

            experiment_result = {
                'task_id': str(self._task.task_id),
                'header': FujitsuJob._create_experiment_header(self._circuit),
                'shots': self._options.get('n_shots'),
                'seed': self._options.get('seed_simulation', None),
                'success': exp_result.task_status == Task.Status.COMPLETED,
                'data': exp_data,
                'status': exp_status
            }

            return Result.from_dict({
                'backend_name': self._backend.name,
                'backend_version': self._backend.backend_version,
                'qobj_id': 'N/A',
                'job_id': self._job_id,
                'success': experiment_result['success'],
                'results': [
                    experiment_result
                ],
                'status': exp_result.task_status
            })

        else:
            # should not happen
            raise RuntimeError('Undefined error')


class FujitsuEstimationJob(FujitsuJob):

    EstimationMethod: TypeAlias = Task.EstimationMethod

    def __init__(self,
                 backend: FujitsuBackend,
                 job_id: str,
                 circuits: List[QuantumCircuit],
                 method: EstimationMethod,
                 observables: List[SparsePauliOp],
                 **options):

        super().__init__(backend,
                         job_id,
                         circuits,
                         **options)

        self._options['method'] = method

        # currently backend.max_circuits = 1
        self._observables = observables[0]
        self._options['operator'] = FujitsuEstimationJob._observable_to_operator(self._observables)

        self._options['n_shots'] = None

        if (self._options['method'] == FujitsuEstimationJob.EstimationMethod.SAMPLING):
            if ('shots' in self._options):
                self._options['n_shots'] = self._options.get('shots')
            else:
                raise AttributeError('Missing mandatory option for estimation job sampling method: \'shots\'')
        else:
            if ('shots' in self._options):
                raise AttributeError('Invalid option for estimation job state_vector method: \'shots\'')

    @staticmethod
    def _observable_to_operator(observables: SparsePauliOp) -> List[List[Union[str, List[float], float]]]:
        if not isinstance(observables, SparsePauliOp):
            raise TypeError('\'observables\' option must be SparsePauliOp')

        paulis_api_str = [FujitsuEstimationJob._convert_pauli_label(k.to_label()) for k in observables.paulis]

        return [[k, [v.real, v.imag]] for k, v in zip(paulis_api_str, observables.coeffs)]

    @staticmethod
    def _convert_pauli_label(pauli_in: str) -> str:
        pauli_out = ''
        for (s, index) in zip(reversed(pauli_in), range(len(pauli_in))):
            # omit 'I' labels to reduce the payload size
            pauli_out += (s + ' ' + str(index) + ' ') if s != 'I' else ''

        pauli_out = pauli_out[:-1]  # delete the last space

        # If the given pauli string consists of 'I' labels only, pauli_out becomes an empty string.
        # In that case, one of the most simplified forms that is equal to the given pauli label is 'I 0'.
        if len(pauli_out) == 0:
            pauli_out = 'I 0'

        return pauli_out

    def _submit_task(self) -> EstimationTask:
        return self._backend._dev.submit_estimation_task(qasm3.dumps(self._circuit, allow_aliasing=True),
                                                         **self._options)

    def _get_result(self) -> Result:
        if self._task is not None:
            exp_result: EstimationResult = self._task.result()

            if (exp_result.task_status == Task.Status.COMPLETED):
                exp_data = {'exp_val': exp_result.exp_val}
                exp_status = 'Experiment was successful'
            else:
                exp_data = {}
                exp_status = f'Experiment was not successful: {exp_result.message}'

            experiment_result = {
                'task_id': str(self._task.task_id),
                'header': FujitsuJob._create_experiment_header(self._circuit),
                'method': self._options.get('method'),
                'observables': self._observables,
                'operator': self._options.get('operator'),
                'shots': self._options.get('n_shots'),
                'seed': self._options.get('seed_simulation', None),
                'success': exp_result.task_status == Task.Status.COMPLETED,
                'data': exp_data,
                'status': exp_status
            }

            return Result.from_dict({
                'backend_name': self._backend.name,
                'backend_version': self._backend.backend_version,
                'qobj_id': 'N/A',
                'job_id': self._job_id,
                'success': experiment_result['success'],
                'results': [
                    experiment_result
                ],
                'status': exp_result.task_status
            })

        else:
            # should not happen
            raise RuntimeError('Undefined error')
