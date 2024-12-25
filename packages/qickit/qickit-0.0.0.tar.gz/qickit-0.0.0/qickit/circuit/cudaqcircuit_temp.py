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

""" Wrapper class for using NVIDIA's cuda-quantum in Qickit SDK.
"""

from __future__ import annotations

__all__ = ["CUDAQCircuit"]

from collections.abc import Sequence
import numpy as np
from numpy.typing import NDArray
from typing import Callable, TYPE_CHECKING

import cudaq # type: ignore

if TYPE_CHECKING:
    from qickit.backend import Backend
from qickit.circuit import Circuit, QiskitCircuit
from qickit.circuit.circuit import GATES
from qickit.synthesis.unitarypreparation import UnitaryPreparation


class CUDAQCircuit(Circuit):
    """ `qickit.circuit.CUDAQCircuit` is the wrapper for using NVIDIA's cuda-quantum in Qickit SDK.

    Notes
    -----
    NVIDIA's cuda-quantum is a quantum computing library that provides a high-performance
    quantum circuit compiler using MLIR (Multi-Level Intermediate Representation).

    For more information on cuda-quantum:
    - Documentation:
    https://nvidia.github.io/cuda-quantum/latest/index.html
    - Source Code:
    https://github.com/NVIDIA/cuda-quantum
    - Publication:
    https://ieeexplore.ieee.org/document/10247886

    Parameters
    ----------
    `num_qubits` : int
        Number of qubits in the circuit.

    Attributes
    ----------
    `num_qubits` : int
        Number of qubits in the circuit.
    `qr` : cudaq.qvector
        The quantum bit register.
    `circuit` : cudaq.kernel
        The circuit.
    `measured_qubits` : set[int]
        The set of measured qubits indices.
    `circuit_log` : list[dict]
        The circuit log.
    `global_phase` : float
        The global phase of the circuit.
    `process_gate_params_flag` : bool
        The flag to process the gate parameters.

    Raises
    ------
    TypeError
        - Number of qubits bits must be integers.
    ValueError
        - Number of qubits bits must be greater than 0.

    Usage
    -----
    >>> circuit = CUDAQCircuit(num_qubits=2)
    """
    def __init__(
            self,
            num_qubits: int
        ) -> None:

        super().__init__(num_qubits=num_qubits)

        self.circuit = cudaq.make_kernel()
        self.qr = self.circuit.qalloc(self.num_qubits)

    @staticmethod
    def _define_gate_mapping() -> dict[str, Callable]:
        gate_mapping = {
            "X": lambda circuit: circuit.cx,
            "U3": lambda circuit: circuit.u3,
        }

        return gate_mapping

    def _gate_mapping(
            self,
            gate: GATES,
            target_indices: int | Sequence[int],
            control_indices: int | Sequence[int] = [],
            angles: Sequence[float] = [0, 0, 0]
        ) -> None:

        # Cuda-quantum only supports `int` type for qubit indices
        target_indices = [target_indices] if isinstance(target_indices, int) else [int(index) for index in target_indices]
        control_indices = [control_indices] if isinstance(control_indices, int) else [int(index) for index in control_indices]
        angles = [float(angle) for angle in angles]

        # Lazily extract the value of the gate from the mapping to avoid
        # creating all the gates at once, and to maintain the polymorphism
        gate_operation = self.gate_mapping[gate](self.circuit)

        if control_indices:
            for target_index in target_indices:
                gate_operation(self.qr[control_indices], self.qr[target_index])
            return

        for target_index in target_indices:
            gate_operation(angles[0], angles[1], angles[2], self.qr[target_index])

    def GlobalPhase(
            self,
            angle: float
        ) -> None:

        self.process_gate_params(gate=self.GlobalPhase.__name__, params=locals())

        global_phase = np.array([
            [np.exp(1j * angle), 0],
            [0, np.exp(1j * angle)]
        ], dtype=np.complex128)

        cudaq.register_operation("global_phase", global_phase)
        self.circuit.global_phase(self.qr[0])
        self.global_phase += angle

    def measure(
            self,
            qubit_indices: int | Sequence[int]
        ) -> None:

        self.process_gate_params(gate=self.measure.__name__, params=locals())

        if isinstance(qubit_indices, int):
            qubit_indices = [qubit_indices]

        if any(qubit_index in self.measured_qubits for qubit_index in qubit_indices):
            raise ValueError("The qubit(s) have already been measured.")

        # Measure the qubits
        for qubit_index in qubit_indices:
            self.circuit.mz(self.qr[qubit_index])

        # Set the measurement as applied
        for qubit_index in qubit_indices:
            self.measured_qubits.add(qubit_index)

    def get_statevector(
            self,
            backend: Backend | None = None,
        ) -> NDArray[np.complex128]:

        # Copy the circuit as the operations are applied inplace
        circuit: CUDAQCircuit = self.copy() # type: ignore

        # Cirq uses MSB convention for qubits, so we need to reverse the qubit indices
        circuit.vertical_reverse()

        if backend is None:
            state_vector = np.array(cudaq.get_state(circuit.circuit))
        else:
            state_vector = backend.get_statevector(circuit)

        return state_vector

    def get_counts(
            self,
            num_shots: int,
            backend: Backend | None = None
        ) -> dict:

        if not(any(self.measured_qubits)):
            raise ValueError("At least one qubit must be measured.")

        # Copy the circuit as the measurement and vertical reverse operations are applied inplace
        circuit: CUDAQCircuit = self.copy() # type: ignore

        # CUDAQ uses MSB convention for qubits, so we need to reverse the qubit indices
        circuit.vertical_reverse()

        if backend is None:
            result = str(cudaq.sample(circuit.circuit, num_shots)).split()[1:-1]
            counts = {pair.split(":")[0]: int(pair.split(":")[1]) for pair in result}

        else:
            counts = backend.get_counts(circuit, num_shots)

        return counts

    def get_depth(self) -> int:
        circuit = self.convert(QiskitCircuit)
        return circuit.get_depth()

    def get_unitary(self) -> NDArray[np.complex128]:
        # Copy the circuit as the operations are applied inplace
        circuit: CUDAQCircuit = self.convert(CUDAQCircuit) # type: ignore

        # Cirq uses MSB convention for qubits, so we need to reverse the qubit indices
        circuit.vertical_reverse()

        N = 2**self.num_qubits

        unitary = np.zeros((N, N), dtype=np.complex128)

        for j in range(N):
            state_j = np.zeros((2**self.num_qubits), dtype=np.complex128)
            state_j[j] = 1.0
            unitary[:, j] = np.array(cudaq.get_state(circuit.circuit, state_j), copy=False)

        return np.array(unitary)

    def reset_qubit(
            self,
            qubit_indices: int | Sequence[int]
        ) -> None:

        qubit_indices = [qubit_indices] if isinstance(qubit_indices, int) else qubit_indices

        for qubit_index in qubit_indices:
            self.circuit.reset(self.qr[qubit_index])

    def transpile(
            self,
            direct_transpile: bool=True,
            synthesis_method: UnitaryPreparation | None = None
        ) -> None:

        # Convert to `qickit.circuit.QiskitCircuit` to transpile the circuit
        qiskit_circuit = self.convert(QiskitCircuit)
        qiskit_circuit.transpile(
            direct_transpile=direct_transpile,
            synthesis_method=synthesis_method
        )

        # Convert back to `qickit.circuit.CUDAQCircuit` to update the circuit
        updated_circuit = qiskit_circuit.convert(CUDAQCircuit)
        self.circuit_log = updated_circuit.circuit_log
        self.circuit = updated_circuit.circuit

    def to_qasm(
            self,
            qasm_version: int=2
        ) -> str:

        return self.convert(QiskitCircuit).to_qasm(qasm_version=qasm_version)

    def draw(self) -> None:
        print(cudaq.draw(self.circuit))

    def copy(self) -> Circuit:
        return self.convert(CUDAQCircuit)