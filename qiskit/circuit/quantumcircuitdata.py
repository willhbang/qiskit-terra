# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""A wrapper class for the purposes of validating modifications to
QuantumCircuit.data while maintaining the interface of a python list."""

from qiskit.circuit.exceptions import CircuitError
from qiskit.circuit.instruction import Instruction
from qiskit.circuit.componentdata import ComponentData


class QuantumCircuitData(ComponentData):
    """A wrapper class for the purposes of validating modifications to
    QuantumCircuit.data while maintaining the interface of a python list."""

    def __init__(self, circuit):
        super().__init__(circuit, '_data')
        self._circuit = self._component

    def __setitem__(self, key, value):
        instruction, qargs, cargs = value

        if not isinstance(instruction, Instruction) \
           and hasattr(instruction, 'to_instruction'):
            instruction = instruction.to_instruction()

        expanded_qargs = [self._circuit.qbit_argument_conversion(qarg)
                          for qarg in qargs or []]
        expanded_cargs = [self._circuit.cbit_argument_conversion(carg)
                          for carg in cargs or []]

        broadcast_args = list(instruction.broadcast_arguments(expanded_qargs,
                                                              expanded_cargs))

        if len(broadcast_args) > 1:
            raise CircuitError('QuantumCircuit.data modification does not '
                               'support argument broadcasting.')

        qargs, cargs = broadcast_args[0]

        if not isinstance(instruction, Instruction):
            raise CircuitError('object is not an Instruction.')

        self._circuit._check_dups(qargs)
        self._circuit._check_qargs(qargs)
        self._circuit._check_cargs(cargs)

        self._circuit._data[key] = (instruction, qargs, cargs)

        self._circuit._update_parameter_table(instruction)
