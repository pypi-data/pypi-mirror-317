# (C) 2024 Fujitsu Limited

from typing import List, Union

from qulacs import GeneralQuantumOperator


def to_operator_list(operator: GeneralQuantumOperator) -> List[List[Union[str, List[float], float]]]:
    """Converts a Qulacs GeneralQuantumOperator to an operator list compatible with the 'operator' parameter of
    Fujitsu Quantum Cloud Web APIs.
    """
    operator_list: List[List[Union[str, List[float], float]]] = []
    for ti in range(operator.get_term_count()):
        term = operator.get_term(ti)
        pauli_str = term.get_pauli_string()
        if not pauli_str:
            pauli_str = 'I'

        coef = term.get_coef()
        operator_list.append([pauli_str, [coef.real, coef.imag]])

    return operator_list
