# (C) 2024 Fujitsu Limited

from typing import List, Tuple

from openfermion import QubitOperator
from qiskit.quantum_info import SparsePauliOp


def to_qiskit_operator(qubit_operator: QubitOperator, n_qubits: int,
                       ignore_small_coef: bool = True, small_coef_tol: float = 1e-8) -> SparsePauliOp:
    """Converts an OpenFermion QubitOperator to a Qiskit SparsePauliOp."""

    pauli_coef_list: List[Tuple[str, List[int], complex]] = []
    for term, coef in sorted(qubit_operator.terms.items()):
        if ignore_small_coef and qubit_operator._issmall(coef, small_coef_tol):
            continue

        pauli_str_list = []
        pauli_index_list = []
        for factor in term:
            index, action = factor
            action_str = qubit_operator.action_strings[qubit_operator.actions.index(action)]
            pauli_str_list.append(action_str)
            pauli_index_list.append(index)

        if not pauli_str_list:
            pauli_str_list.append('I')
            pauli_index_list.append(0)

        pauli_coef_list.append((''.join(pauli_str_list), pauli_index_list, coef))

    return SparsePauliOp.from_sparse_list(pauli_coef_list, num_qubits=n_qubits)
