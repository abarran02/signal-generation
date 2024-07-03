import struct
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

''' Read in binary uint32 data from a file in little endian order '''
def read_binary_image(filename: Path):
    with open(filename, 'rb') as file_id:
        height = np.fromfile(file_id, '<u4', 1, "")
        width = np.fromfile(file_id, '<u4', 1, "")

        data = np.fromfile(file_id, '<u4', -1, "")

        data = data.reshape(height[0], width[0])

    return data

''' Write numpy array to uint32 binary data file '''
def write_binary_image(filename: Path, data):
    with open(filename, 'wb') as file_id:
        height = data.shape[0]
        width = data.shape[1]

        file_id.write(struct.pack('<I', height))
        file_id.write(struct.pack('<I', width))

        #data.astype('<u4').tofile(file_id)
        #file_id.write(struct.pack('<I', data))
        np.array(data, dtype=np.uint32).tofile(file_id)

def interleave_iq(data: NDArray[np.complex64]) -> NDArray[np.int16]:
    data_flat = np.empty(2 * len(data))
    data_flat[0::2] = np.real(data)
    data_flat[1::2] = np.imag(data)

    return np.array(data_flat, dtype=np.int16)

def get_iq_bytes(data: NDArray[np.complex64]) -> bytes:
    data_flat = interleave_iq(data)

    return data_flat.tobytes()

def write_binary_iq_data(filename: Path, data: NDArray[np.complex64]) -> None:
    data_flat = interleave_iq(data)

    with open(filename, 'wb') as file_id:
        data_flat.tofile(file_id)
