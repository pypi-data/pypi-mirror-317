import numpy as np

def mk_epsilon_array():
    arr = np.zeros((4, 4, 4, 4,), dtype = np.int8)
    def setv(i, j, k, l):
        setw(i, j, k, l, 1)
        setw(i, j, l, k, -1)
    def setw(i, j, k, l, val):
        arr[i, j, k, l] = val;
        arr[j, k, l, i] = -val;
        arr[k, l, i, j] = val;
        arr[l, i, j, k] = -val;
    setv(0, 1, 2, 3)
    setv(0, 2, 3, 1);
    setv(0, 3, 1, 2);
    return arr

epsilon_array = mk_epsilon_array()

def epsilon_tensor(i, j, k, l=3):
    """
    epsilon_tensor(0, 1, 2, 3) == 1
    """
    return epsilon_array[i, j, k, l].item()
