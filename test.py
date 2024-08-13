import numpy as np

crc_type = 16
g = 0x1B09
bin_g = bin(g)

matrix_f = np.zeros((1,crc_type,crc_type))