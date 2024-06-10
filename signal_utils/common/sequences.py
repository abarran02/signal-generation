import random

import numpy as np
from numpy.typing import NDArray
from signal_utils.common.generate_bpsk import generate_bpsk

"""
https://web.archive.org/web/20110806114215/http://homepage.mac.com/afj/taplist.html
https://in.ncu.edu.tw/ncume_ee/digilogi/prbs.htm

**note: subtract 1 for 0 based indexing

4-bits:
- 2 taps: [4,3]

5-bits:
- 2 taps: [5,3]
- 4 taps: [5,4,3,2], [5,4,3,1]

6-bits:
- 2 taps: [6,5]
- 4 taps: [6,5,4,1], [6,5,3,2]

7-bits:
- 2 taps: [7,6], [7,4]
- 4 taps: [7,6,5,4], [7,6,5,2], [7,6,4,2], [7,6,4,1], [7,5,4,3]
- 6 taps: [7,6,5,4,3,2], [7,6,5,4,2,1]

8-bits:
- 4 taps: [8,7,6,1], [8,7,5,3], [8,7,3,2], [8,6,5,4], [8,6,5,3], [8,6,5,2]
- 6 taps: [8,7,6,5,4,2], [8,7,6,5,2,1]

9-bits:
- 2 taps: [9,5]
- 4 taps: [9,8,7,2], [9,8,6,5], [9,8,5,4], [9,8,5,1], [9,8,4,2], [9,7,6,4], [9,7,5,2], [9,6,5,3]
- 6 taps: [9,8,7,6,5,3], [9,8,7,6,5,1], [9,8,7,6,4,3], [9,8,7,6,4,2], [9,8,7,6,3,2], [9,8,7,6,3,1], [9,8,7,6,2,1],
          [9,8,7,5,4,3], [9,8,7,5,4,2], [9,8,6,5,4,1], [9,8,6,5,3,2], [9,8,6,5,3,1], [9,7,6,5,4,3], [9,7,6,5,4,2]
- 8 taps: [9,8,7,6,5,4,3,1]
"""

def random_tap_sequence(num_bits: int) -> list[list[int]]:
    max_uniques = {
        4: [[4,3]],
        5: [[5,4,3,2], [5,4,3,1]],
        6: [[6,5,4,1], [6,5,3,2]],
        7: [[7,6,5,4], [7,6,5,2], [7,6,4,2], [7,6,4,1], [7,5,4,3]],
        8: [[8,7,6,1], [8,7,5,3], [8,7,3,2], [8,6,5,4], [8,6,5,3], [8,6,5,2]],
        9: [[9,8,7,6,5,3], [9,8,7,6,5,1], [9,8,7,6,4,3], [9,8,7,6,4,2], [9,8,7,6,3,2], [9,8,7,6,3,1], [9,8,7,6,2,1],
            [9,8,7,5,4,3], [9,8,7,5,4,2], [9,8,6,5,4,1], [9,8,6,5,3,2], [9,8,6,5,3,1], [9,7,6,5,4,3], [9,7,6,5,4,2]]
    }

    possible_seqs = max_uniques[num_bits]
    # inefficient subtraction on-the-fly but we can fix the data later
    return [x-1 for x in random.choice(possible_seqs)] #1-indexing

def generate_iq_taps(num_bits, sample_rate, bit_length, pri):
    iq = []
    for i in range(num_bits-1):
        taps = random_tap_sequence(num_bits)
        mls = maximal_length_sequence(num_bits, np.array(taps))
        temp = generate_bpsk(mls, sample_rate, bit_length)
        n_zeros = pri - temp
        new_val = temp - n_zeros
        iq.append(new_val)
    return iq


def maximal_length_sequence(num_bits: int, taps: NDArray[np.int_]) -> NDArray[np.int_]:

    register = np.zeros([num_bits])
    register[0] = 1

    sr_size = 2**num_bits - 1
    SR = np.zeros([sr_size])

    for idx in range(sr_size):
        SR[idx] = register[-1]

        tmp_sum = 0
        for jdx in range(taps.shape[0]):
            tmp_sum += register[taps[jdx]]

        register[1:] = register[0:-1]
        register[0] = tmp_sum % 2

    SR = 2*SR - 1
    return SR

def barker_code(code_length: int) -> NDArray[np.int_]:

    if(code_length == 2):
        data = np.array([1, -1])
    elif(code_length == 3):
        data = np.array([1, 1, -1])
    elif(code_length == 4):
        data = np.array([1, 1, -1, 1])
    elif(code_length == 5):
        data = np.array([1, 1, 1, -1, 1])
    elif(code_length == 7):
        data = np.array([1, 1, 1, -1, -1, 1, -1])
    elif(code_length == 11):
        data = np.array([1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1])
    elif(code_length == 13):
        data = np.array([1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1])
    else:
        data = np.array([1, 1, 1, -1, 1])
        print("code length supplied is not a valid barker code length.  Setting code length to 5")

    return data
