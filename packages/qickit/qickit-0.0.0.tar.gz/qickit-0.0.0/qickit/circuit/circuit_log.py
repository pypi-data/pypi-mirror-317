# Copyright 2023-2024 Qualition Computing LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://github.com/Qualition/QICKIT/blob/main/LICENSE
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

__all__ = ["CircuitLog"]

import numpy as np
from typing import Any, Sequence, SupportsIndex, SupportsFloat

# Define the epsilon value for floating point comparisons
EPSILON = 1e-10

""" Set the frozensets for the keys to be used:
- Decorator `Circuit.gatemethod()`
- Method `Circuit.vertical_reverse()`
- Method `Circuit.horizontal_reverse()`
- Method `Circuit.add()`
- Method `Circuit.change_mapping()`
"""
QUBIT_KEYS = frozenset([
    "qubit_index", "control_index", "target_index", "first_qubit_index",
    "second_qubit_index", "first_target_index", "second_target_index"
])
QUBIT_LIST_KEYS = frozenset(["qubit_indices", "control_indices", "target_indices"])
ANGLE_KEYS = frozenset(["angle", "angles"])
ALL_QUBIT_KEYS = QUBIT_KEYS.union(QUBIT_LIST_KEYS)


class CircuitLog:
    """ `qickit.circuit.CircuitLog` is a class that logs the operations of a quantum circuit.

    Parameters
    ----------
    `num_qubits` : int
        The number of qubits in the circuit.

    Attributes
    ----------
    `log` : list[dict]
        A list of dictionaries that represent the operations of the quantum circuit.
    `num_qubits` : int
        The number of qubits in the circuit.
    """
    def __init__(
            self,
            num_qubits: int
        ) -> None:
        self.log: list[dict] = []
        self.num_qubits: int = num_qubits

    def _convert_param_type(
            self,
            value: Any
        ) -> int | float | list:
        """ Convert parameter types for consistency.

        Parameters
        ----------
        `value` : Any
            The value to convert.

        Returns
        -------
        `value` : int | float | list
            The converted value.
        """
        match value:
            case range() | tuple() | Sequence():
                value = list(value)
            case np.ndarray():
                value = value.tolist()
            case SupportsIndex():
                value = int(value)
            case SupportsFloat():
                value = float(value)
        return value

    def _validate_qubit_index(
            self,
            name: str,
            value: Any
        ) -> int | list[int]:
        """ Validate qubit indices are within the valid range.

        Parameters
        ----------
        `name` : str
            The name of the parameter.
        `value` : Any
            The value of the parameter.

        Returns
        -------
        `value` : int | list[int]

        Raises
        ------
        TypeError
            - Qubit index must be an integer.
        IndexError
            - Qubit index out of range.
        """
        if name in ALL_QUBIT_KEYS:
            match value:
                case list():
                    if len(value) == 1:
                        value = value[0]

                        if not isinstance(value, int):
                            raise TypeError(f"Qubit index must be an integer. Unexpected type {type(value)} received.")

                        if value >= self.num_qubits or value < -self.num_qubits:
                            raise IndexError(f"Qubit index {value} out of range {self.num_qubits-1}.")

                        value = value if value >= 0 else self.num_qubits + value

                    else:
                        for i, index in enumerate(value):
                            if not isinstance(index, int):
                                raise TypeError(f"Qubit index must be an integer. Unexpected type {type(value)} received.")

                            if index >= self.num_qubits or index < -self.num_qubits:
                                raise IndexError(f"Qubit index {index} out of range {self.num_qubits-1}.")

                            value[i] = index if index >= 0 else self.num_qubits + index

                case int():
                    if value >= self.num_qubits or value < -self.num_qubits:
                        raise IndexError(f"Qubit index {value} out of range {self.num_qubits-1}.")

                    value = value if value >= 0 else self.num_qubits + value

        return value

    def _validate_angle(
            self,
            name: str,
            value: Any
        ) -> None | float | list[float]:
        """ Ensure angles are valid and not effectively zero.

        Parameters
        ----------
        `name` : str
            The name of the parameter.
        `value` : Any
            The value of the parameter.

        Returns
        -------
        `value` : None | float | list[float]
            The value of the parameter. If the value is effectively zero, return None.
            This is to indicate that no operation is needed.

        Raises
        ------
        TypeError
            - Angle must be a number.
        """
        if name in ANGLE_KEYS:
            match value:
                case list():
                    for angle in value:
                        if not isinstance(angle, (int, float)):
                            raise TypeError(f"Angle must be a number. Unexpected type {type(angle)} received.")
                        if np.isclose(angle, EPSILON) or np.isclose(angle % (2 * np.pi), EPSILON):
                            angle = 0
                    if all(angle == 0 for angle in value):
                        # Indicate no operation needed
                        return None
                case _:
                    if not isinstance(value, (int, float)):
                        raise TypeError(f"Angle must be a number. Unexpected type {type(value)} received.")
                    if np.isclose(value, EPSILON) or np.isclose(value % (2 * np.pi), EPSILON):
                        # Indicate no operation needed
                        return None

        return value

    def add(
            self,
            gate: str,
            params: dict
        ) -> None:
        """ Add an operation to the log.

        Parameters
        ----------
        `gate` : str
            The name of the gate operation.
        `params` : dict
            A dictionary of parameters for the operation.
        """
        # Remove the "self" key from the dictionary to avoid the inclusion of str(circuit)
        # in the circuit log
        params.pop("self", None)

        for name, value in params.items():
            value = self._convert_param_type(value)
            value = self._validate_qubit_index(name, value)

            if value is None:
                continue

            value = self._validate_angle(name, value)

            # Indicate no operation needed
            if value is None:
                return

            params[name] = value

        self.log.append({"gate": gate, "params": params})

    def change_mapping(
            self,
            qubit_indices: list[int]
        ) -> None:
        """ Change the mapping of the circuit.

        Parameters
        ----------
        `qubit_indices` : Sequence[int]
            The updated order of the qubits.

        Raises
        ------
        TypeError
            - Qubit indices must be a collection.
            - All qubit indices must be integers.
        ValueError
            - The number of qubits must match the number of qubits in the circuit.
        """
        match qubit_indices:
            case Sequence():
                qubit_indices = list(qubit_indices)
            case np.ndarray():
                qubit_indices = qubit_indices.tolist()

        if not isinstance(qubit_indices, Sequence):
            raise TypeError("Qubit indices must be a collection.")

        if not all(isinstance(index, int) for index in qubit_indices):
            raise TypeError("All qubit indices must be integers.")

        if self.num_qubits != len(qubit_indices):
            raise ValueError("The number of qubits must match the number of qubits in the circuit.")

        # Update the qubit indices
        for operation in self.log:
            for key in set(operation.keys()).intersection(ALL_QUBIT_KEYS):
                match operation[key]:
                    case list():
                        operation[key] = [qubit_indices[index] for index in operation[key]]
                    case _:
                        operation[key] = qubit_indices[operation[key]]

    def vertical_reverse(self) -> None:
        """ Perform a vertical reverse operation.
        """
        self.change_mapping(list(range(self.num_qubits))[::-1])

    def horizontal_reverse(
            self,
            adjoint: bool=True
        ) -> None:
        """ Perform a horizontal reverse operation. This is equivalent
        to the adjoint of the circuit if `adjoint=True`. Otherwise, it
        simply reverses the order of the operations.

        Parameters
        ----------
        `adjoint` : bool
            Whether or not to apply the adjoint of the circuit.

        Raises
        ------
        TypeError
            - Adjoint must be a boolean.
        """
        if not isinstance(adjoint, bool):
            raise TypeError("Adjoint must be a boolean.")

        # Reverse the order of the operations
        self.log = self.log[::-1]

        # If adjoint is True, then multiply the angles by -1
        if adjoint:
            # Iterate over every operation, and change the index accordingly
            for operation in self.log:
                if "angle" in operation:
                    operation["angle"] = -operation["angle"]
                elif "angles" in operation:
                    operation["angles"] = [-operation["angles"][0], -operation["angles"][2], -operation["angles"][1]]
                elif operation["gate"] in ["Sdg", "Tdg", "CSdg", "CTdg", "MCSdg", "MCTdg"]:
                    operation["gate"] = operation["gate"].replace("dg", "")
                elif operation["gate"] in ["S", "T", "CS", "CT", "MCS", "MCT"]:
                    operation["gate"] = operation["gate"] + "dg"