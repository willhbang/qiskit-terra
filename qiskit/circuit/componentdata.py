# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""A wrapper class for the purposes of validating or broadcasting modifications to
circuit components that require it, while maintaining the interface of a python list."""

from collections.abc import MutableSequence


class ComponentData(MutableSequence):
    """A wrapper class for the purposes of validating or broadcasting modifications to
    circuit components that require it, while maintaining the interface of a python list."""

    def __init__(self, component, prop):
        self._component = component
        self._prop = prop

    def __getitem__(self, i):
        return getattr(self._component, self._prop)[i]

    def __setitem__(self, key, value):
        pass

    def insert(self, index, value):
        getattr(self._component, self._prop).insert(index, None)
        self[index] = value

    def __delitem__(self, i):
        del getattr(self._component, self._prop)[i]

    def __len__(self):
        return len(getattr(self._component, self._prop))

    def __cast(self, other):
        return getattr(other._component, self._prop) if isinstance(other, type(self)) else other

    def __repr__(self):
        return repr(getattr(self._component, self._prop))

    def __lt__(self, other):
        return getattr(self._component, self._prop) < self.__cast(other)

    def __le__(self, other):
        return getattr(self._component, self._prop) <= self.__cast(other)

    def __eq__(self, other):
        return getattr(self._component, self._prop) == self.__cast(other)

    def __gt__(self, other):
        return getattr(self._component, self._prop) > self.__cast(other)

    def __ge__(self, other):
        return getattr(self._component, self._prop) >= self.__cast(other)

    def __add__(self, other):
        return getattr(self._component, self._prop) + self.__cast(other)

    def __radd__(self, other):
        return self.__cast(other) + getattr(self._component, self._prop)

    def __mul__(self, n):
        return getattr(self._component, self._prop) * n

    def __rmul__(self, n):
        return n * getattr(self._component, self._prop)

    def sort(self, *args, **kwargs):
        """In-place stable sort. Accepts arguments of list.sort."""
        getattr(self._component, self._prop).sort(*args, **kwargs)

    def copy(self):
        """Returns a shallow copy of instruction list."""
        return getattr(self._component, self._prop).copy()
