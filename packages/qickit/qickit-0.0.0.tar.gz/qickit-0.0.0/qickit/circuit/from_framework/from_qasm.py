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

""" Converter for quantum circuits from QASM to Qickit.
"""

from __future__ import annotations

__all__ = ["FromQasm"]

from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from qickit.circuit import Circuit
from qickit.circuit.from_framework import FromFramework


class FromQasm(FromFramework):
    """ `qickit.circuit.from_framework.FromQasm` is a class for converting quantum circuits from
    QASM3 to `qickit.circuit.Circuit` class.

    Parameters
    ----------
    `output_framework` : type[Circuit]
        The quantum computing framework to convert the quantum circuit to.

    Attributes
    ----------
    `output_framework` : type[Circuit]
        The quantum computing framework to convert the quantum circuit to.
    `gate_mapping` : dict[str, Callable]
        The mapping of the gates in Qiskit to the gates in Qickit.

    Raises
    ------
    `TypeError`
        - If the `output_framework` is not a subclass of `qickit.circuit.Circuit`.

    Usage
    -----
    >>> qasm_converter = FromQasm(output_framework=TKETCircuit)
    """
    def __init__(
            self,
            output_framework: Type[Circuit]
        ) -> None:

        super().__init__(output_framework=output_framework)