from gam import LinearCongruentialGenerator

IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17,  9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
           39, 7, 47, 15, 55, 23, 63, 31,
           38, 6, 46, 14, 54, 22, 62, 30,
           37, 5, 45, 13, 53, 21, 61, 29,
           36, 4, 44, 12, 52, 20, 60, 28,
           35, 3, 43, 11, 51, 19, 59, 27,
           34, 2, 42, 10, 50, 18, 58, 26,
           33, 1, 41,  9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10,11,12,13,
     12,13,14,15,16,17,
     16,17,18,19,20,21,
     20,21,22,23,24,25,
     24,25,26,27,28,29,
     28,29,30,31,32,1]

P = [16,7,20,21,
     29,12,28,17,
     1,15,23,26,
     5,18,31,10,
     2,8,24,14,
     32,27,3,9,
     19,13,30,6,
     22,11,4,25]

PC1 = [57,49,41,33,25,17,9,
       1,58,50,42,34,26,18,
       10,2,59,51,43,35,27,
       19,11,3,60,52,44,36,
       63,55,47,39,31,23,15,
       7,62,54,46,38,30,22,
       14,6,61,53,45,37,29,
       21,13,5,28,20,12,4]

PC2 = [14,17,11,24,1,5,
       3,28,15,6,21,10,
       23,19,12,4,26,8,
       16,7,27,20,13,2,
       41,52,31,37,47,55,
       30,40,51,45,33,48,
       44,49,39,56,34,53,
       46,42,50,36,29,32]

SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2,
                  1, 2, 2, 2, 2, 2, 2, 1]

S_BOX = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8], [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ]],       
                [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10], [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5], [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15], [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ]],
                [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8], [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1], [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7], [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]],
                [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15], [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9], [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4], [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14 ]],
                [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9], [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6], [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14], [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]],
                [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8], [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6], [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13 ]],
                [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1], [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6], [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2], [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12 ]],
                [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7], [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2], [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8], [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11 ]]]


def permute(bits, table):
    return [bits[x-1] for x in table]

def xor(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def shift_left(bits, n):
    return bits[n:] + bits[:n]

def add_parity_bits(key56bits):
    key_with_parity = []
    for i in range(0, 56, 7):
        block = key56bits[i:i+7]
        parity_bit = 0 if sum(block) % 2 else 1
        key_with_parity.extend(block + [parity_bit])
    return key_with_parity


def generate_keys(key64):
    key56 = permute(key64, PC1)
    C, D = key56[:28], key56[28:]
    keys = []
    for shift in SHIFT_SCHEDULE:
        C, D = shift_left(C, shift), shift_left(D, shift)
        keys.append(permute(C + D, PC2))
    return keys

def sbox_substitution(bits):
    result = []
    for i in range(8):
        block = bits[i*6:(i+1)*6]
        row = int(f"{block[0]}{block[5]}", 2)
        col = int(''.join(map(str, block[1:5])), 2)
        val = S_BOX[i][row][col]
        result.extend([int(x) for x in format(val, '04b')])
    return result

def f(R, K):
    expanded = permute(R, E)
    tmp = xor(expanded, K)
    return permute(sbox_substitution(tmp), P)

def des_round(L, R, K):
    newL = R
    newR = xor(L, f(R, K))
    return newL, newR

def des_block_encrypt(block64, keys):
    block = permute(block64, IP)
    L, R = block[:32], block[32:]
    for K in keys:
        L, R = des_round(L, R, K)
    return permute(R + L, IP_INV)

def des_block_decrypt(block64, keys):
    return des_block_encrypt(block64, keys[::-1])

def decrypt(enc_bits, key):
    keys = generate_keys(key)
    decrypted_bits = []
    
    for i in range(0, len(enc_bits), 64):
        block = enc_bits[i:i+64]
        dec_bits = des_block_decrypt(block, keys)
        decrypted_bits.extend(dec_bits)
    
    byte_data = bytes(int(''.join(map(str, decrypted_bits[i:i+8])), 2) for i in range(0, len(decrypted_bits), 8))
    return byte_data.rstrip(b' ').decode('utf-8', errors='ignore')


def encrypt_bytes_with_key(data: bytes, key):
    keys = generate_keys(key)
    padded_data = data + b'\x00' * ((8 - len(data) % 8) % 8)

    encrypted_bits = []
    for i in range(0, len(padded_data), 8):
        block = padded_data[i:i+8]
        bits = [int(b) for byte in block for b in format(byte, '08b')]
        encrypted_bits.extend(des_block_encrypt(bits, keys))

    return encrypted_bits

def decrypt_bytes(enc_bits, key):
    keys = generate_keys(key)
    decrypted_bits = []
    for i in range(0, len(enc_bits), 64):
        block = enc_bits[i:i+64]
        decrypted_bits.extend(des_block_decrypt(block, keys))
    decrypted_bytes = bytes(int(''.join(map(str, decrypted_bits[i:i+8])), 2) for i in range(0, len(decrypted_bits), 8))
    return decrypted_bytes.rstrip(b'\x00')


def generate_des_key(seed, a, c, m):
    lcg = LinearCongruentialGenerator(seed=seed, a=a, c=c, m=m)
    key56 = []
    for byte in lcg.generate(7):
        key56.extend([int(bit) for bit in format(byte, '08b')])
    key56 = key56[:56]
    return add_parity_bits(key56)

def encrypt_with_key(plaintext, key):
    keys = generate_keys(key)
    data = plaintext.encode('utf-8')
    padded_data = data + b' ' * ((8 - len(data) % 8) % 8)

    encrypted_bits = []
    for i in range(0, len(padded_data), 8):
        block = padded_data[i:i+8]
        bits = [int(bit) for byte in block for bit in format(byte, '08b')]
        enc_bits = des_block_encrypt(bits, keys)
        encrypted_bits.extend(enc_bits)
    return encrypted_bits
