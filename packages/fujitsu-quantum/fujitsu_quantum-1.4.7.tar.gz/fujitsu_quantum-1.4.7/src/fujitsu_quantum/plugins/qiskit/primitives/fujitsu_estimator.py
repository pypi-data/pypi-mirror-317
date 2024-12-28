# (C) 2024 Fujitsu Limited

# This file provides a functionality to compute expectation values using Fujitsu backends,
# which has been implemented by modifying the BackendSampler-related code in Qiskit.
# The original Qiskit code:
# - https://github.com/Qiskit/qiskit/blob/0.45.3/qiskit/primitives/backend_sampler.py
# - https://github.com/Qiskit/qiskit/blob/0.45.3/qiskit/primitives/backend_estimator.py

# This code is part of Qiskit.
#
# (C) Copyright IBM 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# Modifications (C) 2024, Fujitsu Limited

from __future__ import annotations

from uuid import uuid4

from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.primitives import BaseEstimator, EstimatorResult
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit.primitives.utils import _circuit_key, _observable_key, init_observable
from qiskit.providers import Options
from qiskit.quantum_info.operators.base_operator import BaseOperator
from qiskit.result import Result
from qiskit.transpiler.passmanager import PassManager

from fujitsu_quantum.plugins.qiskit import FujitsuEstimationJob
from fujitsu_quantum.plugins.qiskit.backends import FujitsuBackend


def _run_circuits(backend: FujitsuBackend,
                  circuits: QuantumCircuit | list[QuantumCircuit],
                  observables: BaseOperator | tuple[BaseOperator, ...],
                  method: FujitsuEstimationJob.EstimationMethod,
                  **run_options,) -> list[Result]:

    if isinstance(circuits, QuantumCircuit):
        circuits = [circuits]

    max_circuits = backend.max_circuits

    if max_circuits:
        jobs = [FujitsuEstimationJob(backend,
                                     str(uuid4()),
                                     circuits[pos: pos + max_circuits],
                                     method=method,
                                     observables=list(observables)[pos: pos + max_circuits],
                                     **run_options)
                for pos in range(0, len(circuits), max_circuits)]
    else:
        jobs = [FujitsuEstimationJob(backend,
                                     str(uuid4()),
                                     circuits,
                                     method=method,
                                     observables=list(observables),
                                     **run_options)]

    for job in jobs:
        job.submit()

    return [job.result() for job in jobs]


class FujitsuEstimator(BaseEstimator[PrimitiveJob[EstimatorResult]]):

    def __init__(self,
                 backend: FujitsuBackend,
                 options: dict | None = None,
                 bound_pass_manager: PassManager | None = None,
                 skip_transpilation: bool = False):

        """
        Initialize a new FujitsuEstimator instance

        Args:
            backend: Required: the backend to run the primitive on
            options: Default options.
            bound_pass_manager: An optional pass manager to run after
                parameter binding.
            skip_transpilation: If this is set to True the internal compilation
                of the input circuits is skipped and the circuit objects
                will be directly executed when this object is called.
        """
        super().__init__(options=options)

        self._backend: FujitsuBackend = backend

        self._transpile_options = Options()
        self._transpiled_circuits: list[QuantumCircuit] = []

        self._bound_pass_manager: PassManager = bound_pass_manager

        self._skip_transpilation: bool = skip_transpilation

        self._circuit_ids: dict[tuple, int] = {}
        self._observable_ids: dict[tuple, int] = {}

    @property
    def backend(self) -> FujitsuBackend:
        """
        Returns:
            The backend which this estimator object based on
        """
        return self._backend

    @property
    def preprocessed_circuits(self) -> list[QuantumCircuit]:
        """
        Preprocessed quantum circuits produced by preprocessing
        Returns:
            List of the transpiled quantum circuit
        Raises:
            QiskitError: if the instance has been closed.
        """
        return list(self._circuits)

    @property
    def transpile_options(self) -> Options:
        """
        Return the transpiler options for transpiling the circuits.
        """
        return self._transpile_options

    def set_transpile_options(self, **fields):
        """
        Set the transpiler options for transpiler.
        Args:
            **fields: The fields to update the options
        """
        self._transpile_options.update_options(**fields)

    @property
    def transpiled_circuits(self) -> list[QuantumCircuit]:
        """
        Transpiled quantum circuits.
        Returns:
            List of the transpiled quantum circuit
        Raises:
            QiskitError: if the instance has been closed.
        """
        if self._skip_transpilation:
            self._transpiled_circuits = list(self._circuits)
        elif len(self._transpiled_circuits) < len(self._circuits):
            # transpile only circuits that are not transpiled yet
            self._transpile()
        return self._transpiled_circuits

    def _transpile(self):
        start = len(self._transpiled_circuits)
        self._transpiled_circuits.extend(
            transpile(
                self.preprocessed_circuits[start:],
                self.backend,
                **self.transpile_options.__dict__,
            ),
        )

    def _bound_pass_manager_run(self, circuits):
        if self._bound_pass_manager is None:
            return circuits
        else:
            output = self._bound_pass_manager.run(circuits)
            if not isinstance(output, list):
                output = [output]
            return output

    def _call(self,
              circuit_indices: list[int],
              observable_indices: list[int],
              parameter_values: tuple[tuple[float, ...], ...],
              method: FujitsuEstimationJob.EstimationMethod,
              **run_options,) -> EstimatorResult:

        transpiled_circuits = self.transpiled_circuits
        bound_circuits = [
            transpiled_circuits[i]
            if len(value) == 0
            else transpiled_circuits[i].assign_parameters((dict(zip(self._parameters[i], value))))
            for i, value in zip(circuit_indices, parameter_values)
        ]
        bound_circuits = self._bound_pass_manager_run(bound_circuits)
        observables = [self._observables[i] for i in observable_indices]

        results = _run_circuits(self._backend, bound_circuits, observables, method, **run_options)

        # _postprocessing
        expval_list = [result.data()['exp_val'] for result in results]

        return EstimatorResult(expval_list, [{}]*len(expval_list))

    def _run(self,
             circuits: tuple[QuantumCircuit, ...],
             observables: tuple[BaseOperator, ...],
             parameter_values: tuple[tuple[float, ...], ...],
             method: FujitsuEstimationJob.EstimationMethod,
             **run_options,) -> PrimitiveJob:

        circuit_indices = []
        for circuit in circuits:
            index = self._circuit_ids.get(_circuit_key(circuit))
            if index is not None:
                circuit_indices.append(index)
            else:
                circuit_indices.append(len(self._circuits))
                self._circuit_ids[_circuit_key(circuit)] = len(self._circuits)
                self._circuits.append(circuit)
                self._parameters.append(circuit.parameters)

        observable_indices = []
        for observable in observables:
            observable = init_observable(observable)
            index = self._observable_ids.get(_observable_key(observable))
            if index is not None:
                observable_indices.append(index)
            else:
                observable_indices.append(len(self._observables))
                self._observable_ids[_observable_key(observable)] = len(self._observables)
                self._observables.append(observable)

        job = PrimitiveJob(
            self._call, circuit_indices, observable_indices, parameter_values, method, **run_options
        )
        job.submit()

        return job
