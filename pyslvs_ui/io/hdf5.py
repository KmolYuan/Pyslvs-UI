# -*- coding: utf-8 -*-

from __future__ import annotations

"""HDF5 format processing function."""

from typing import Mapping, Union, Any
from zlib import compress, decompress
from h5py import File, Dataset, Group
from numpy import ndarray, array, int8, void
from qtpy.QtWidgets import QMessageBox
from .format_editor import FormatEditor


def _compress(b: bytes) -> ndarray:
    """Compress bytes."""
    return void(compress(b, level=9))


def _decompress(b: ndarray) -> bytes:
    """Decompress bytes."""
    return decompress(b.tobytes())


def _h5py_dump(f: File, d: Mapping[str, Any], *, prefix: str = ''):
    """Dump function for h5py."""
    for k, v in d.items():
        if prefix:
            key = prefix + '/' + k
        else:
            key = k
        if isinstance(v, dict):
            _h5py_dump(f, v, prefix=key)
        elif isinstance(v, bytes):
            f[key] = _compress(v)
        elif isinstance(v, str):
            f[key] = _compress(b's' + v.encode('utf-8'))
        elif isinstance(v, (int, float)):
            f[key] = v
        else:
            try:
                a = array(v, dtype=int8)
            except (ValueError, TypeError):
                # Use eval function
                f[key] = _compress(f"!{v!r}".encode('utf-8'))
            else:
                f[key] = a


def _h5py_load(f: Group) -> Mapping[str, Any]:
    """Load function for h5py."""
    data = {}
    for k, v in f.items():  # type: str, Union[Group, Dataset]
        if isinstance(v, Group):
            data[k] = _h5py_load(v)
        elif isinstance(v, Dataset):
            value = v[()]
            if isinstance(value, void):
                value = _decompress(value)
                if value.startswith(b's'):
                    value = value.decode('utf-8')[1:]
                elif value.startswith(b'!'):
                    value = eval(value.decode('utf-8')[1:])
            data[k] = value
    return data


class HDF5Editor(FormatEditor):
    """HDF5 reader and writer."""

    def __init__(self, *args):
        super(HDF5Editor, self).__init__(*args)

    @staticmethod
    def test(file_name: str) -> bool:
        """Test the file is valid."""
        try:
            File(file_name, 'r')
        except OSError:
            return False
        else:
            return True

    def save(self, file_name: str) -> None:
        """Save HDF5 file."""
        data = self.save_data()
        with File(file_name, 'w') as f:
            try:
                _h5py_dump(f, data)
            except Exception as e:
                QMessageBox.warning(self._parent, "Save error", f"{e}")

    def load(self, file_name: str) -> None:
        """Load HDF5 file."""
        with File(file_name, 'r') as f:
            try:
                data = _h5py_load(f)
            except Exception as e:
                QMessageBox.warning(self._parent, "Load error", f"{e}")
                return
        self.load_data(file_name, data)
