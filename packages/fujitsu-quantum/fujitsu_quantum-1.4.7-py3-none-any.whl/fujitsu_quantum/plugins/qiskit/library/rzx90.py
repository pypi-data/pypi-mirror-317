# (C) 2024 Fujitsu Limited

from typing import Optional

from numpy import array, pi, sqrt
from qiskit.circuit import InstructionSet, QuantumCircuit, QuantumRegister
from qiskit.circuit.equivalence_library import SessionEquivalenceLibrary
from qiskit.circuit.gate import Gate
from qiskit.circuit.library import (CXGate, CZGate, ECRGate, HGate, RXGate, RZGate, RZXGate, SdgGate, SGate, SwapGate,
                                    SXGate)
from qiskit.circuit.quantumcircuit import QubitSpecifier
from qiskit.dagcircuit import DAGCircuit
from qiskit.transpiler.passes import GateDirection


class RZX90Gate(Gate):

    def __init__(self, label: Optional[str] = None):
        super().__init__("rzx90", 2, [], label=label)

    def _define(self):
        qc = QuantumCircuit(2)
        qc.rzx(pi / 2, 0, 1)
        self.definition = qc

    def inverse(self):
        return RZXGate(-pi / 2)

    def __array__(self, dtype=None):
        return (1 / sqrt(2)) * array([[1, 0, -1j, 0],
                                      [0, 1, 0, 1j],
                                      [-1j, 0, 1, 0],
                                      [0, 1j, 0, 1]],
                                     dtype=dtype)


def define_rzx90():
    def rzx90(self, qubit1: QubitSpecifier, qubit2: QubitSpecifier) -> InstructionSet:
        return self.append(RZX90Gate(), [qubit1, qubit2], [])

    QuantumCircuit.rzx90 = rzx90


def define_rzx90_equivalence_relation():
    # cx == rz, rzx90, irx90 (inversed-rx90)
    q = QuantumRegister(2, "q")
    def_rzx90_cnot = QuantumCircuit(q)
    def_rzx90_cnot.append(RZGate(-pi / 2), [q[0]], [])
    def_rzx90_cnot.append(RZX90Gate(), [q[0], q[1]], [])
    # irx90
    def_rzx90_cnot.append(RZGate(pi), [q[1]], [])
    def_rzx90_cnot.append(RXGate(pi / 2), [q[1]], [])
    def_rzx90_cnot.append(RZGate(pi), [q[1]], [])

    SessionEquivalenceLibrary.add_equivalence(CXGate(), def_rzx90_cnot)

    # rzx90 == rzx(pi/2)
    circuit_rzx = QuantumCircuit(2)
    circuit_rzx.append(RZXGate(pi / 2), [0, 1])

    SessionEquivalenceLibrary.add_equivalence(RZX90Gate(), circuit_rzx)


def define_rzx90_gate_direction_flipping():
    # Modify methods in qiskit.transpiler.passes.GateDirection to support flipping of Rzx90.
    # The following method init(...) is a modified versions of the GateDirection.__init__(...) in Qiskit 0.45.0.
    # https://github.com/Qiskit/qiskit/blob/0.45.0/qiskit/transpiler/passes/utils/gate_direction.py

    # This code is part of Qiskit.
    #
    # (C) Copyright IBM 2017, 2021.
    #
    # This code is licensed under the Apache License, Version 2.0. You may
    # obtain a copy of this license in the LICENSE.txt file in the root directory
    # of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
    #
    # Any modifications or derivative works of this code must retain this
    # copyright notice, and modified files need to carry a notice indicating
    # that they have been altered from the originals.

    # Modifications (C) 2024, Fujitsu Limited

    def init(self, coupling_map, target=None):
        """GateDirection pass.

        Args:
            coupling_map (CouplingMap): Directed graph represented a coupling map.
            target (Target): The backend target to use for this pass. If this is specified
                it will be used instead of the coupling map
        """
        super(GateDirection, self).__init__()
        self.coupling_map = coupling_map
        self.target = target

        # Create the replacement dag and associated register.
        self._cx_dag = DAGCircuit()
        qr = QuantumRegister(2)
        self._cx_dag.add_qreg(qr)
        self._cx_dag.apply_operation_back(HGate(), [qr[0]], [])
        self._cx_dag.apply_operation_back(HGate(), [qr[1]], [])
        self._cx_dag.apply_operation_back(CXGate(), [qr[1], qr[0]], [])
        self._cx_dag.apply_operation_back(HGate(), [qr[0]], [])
        self._cx_dag.apply_operation_back(HGate(), [qr[1]], [])

        # This is done in terms of less-efficient S/SX/Sdg gates instead of the more natural
        # `RY(pi /2)` so we have a chance for basis translation to keep things in a discrete basis
        # during resynthesis, if that's what's being asked for.
        self._ecr_dag = DAGCircuit()
        qr = QuantumRegister(2)
        self._ecr_dag.global_phase = -pi / 2
        self._ecr_dag.add_qreg(qr)
        self._ecr_dag.apply_operation_back(SGate(), [qr[0]], [])
        self._ecr_dag.apply_operation_back(SXGate(), [qr[0]], [])
        self._ecr_dag.apply_operation_back(SdgGate(), [qr[0]], [])
        self._ecr_dag.apply_operation_back(SdgGate(), [qr[1]], [])
        self._ecr_dag.apply_operation_back(SXGate(), [qr[1]], [])
        self._ecr_dag.apply_operation_back(SGate(), [qr[1]], [])
        self._ecr_dag.apply_operation_back(ECRGate(), [qr[1], qr[0]], [])
        self._ecr_dag.apply_operation_back(HGate(), [qr[0]], [])
        self._ecr_dag.apply_operation_back(HGate(), [qr[1]], [])

        self._cz_dag = DAGCircuit()
        qr = QuantumRegister(2)
        self._cz_dag.add_qreg(qr)
        self._cz_dag.apply_operation_back(CZGate(), [qr[1], qr[0]], [])

        self._swap_dag = DAGCircuit()
        qr = QuantumRegister(2)
        self._swap_dag.add_qreg(qr)
        self._swap_dag.apply_operation_back(SwapGate(), [qr[1], qr[0]], [])

        self._rzx90_dag = DAGCircuit()
        qr = QuantumRegister(2)
        self._rzx90_dag.add_qreg(qr)
        self._rzx90_dag.apply_operation_back(HGate(), [qr[0]], [])
        self._rzx90_dag.apply_operation_back(HGate(), [qr[1]], [])
        self._rzx90_dag.apply_operation_back(RZX90Gate(), [qr[1], qr[0]], [])
        self._rzx90_dag.apply_operation_back(HGate(), [qr[0]], [])
        self._rzx90_dag.apply_operation_back(HGate(), [qr[1]], [])

        # If adding more replacements (either static or dynamic), also update the class variable
        # `_KNOWN_REPLACMENTS` to include them in the error messages.
        self._static_replacements = {
            "cx": self._cx_dag,
            "cz": self._cz_dag,
            "ecr": self._ecr_dag,
            "swap": self._swap_dag,
            "rzx90": self._rzx90_dag,
        }

    GateDirection._KNOWN_REPLACEMENTS = frozenset(
        ["cx", "cz", "ecr", "swap", "rzx", "rzx90", "rxx", "ryy", "rzz"]
    )
    GateDirection.__init__ = init


define_rzx90()
define_rzx90_equivalence_relation()
define_rzx90_gate_direction_flipping()
