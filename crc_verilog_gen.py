import argparse
# This code is used to generate a verilog module for CRC calculation.
def matrix_multiply(A, B):
    # Get the dimensions of the matrices
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    # Check if the matrices can be multiplied
    if cols_A != rows_B:
        raise ValueError("Number of columns in matrix A must be equal to the number of rows in matrix B")

    # Initialize the result matrix with zeros
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    # Perform galois field multiplication
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] = result[i][j] ^ (A[i][k] * B[k][j])

    return result

def generate_generator_matrix(g_coeffs):
    """
    Generate an n x n generator matrix from a given polynomial coefficients.

    Parameters:
    g_coeffs (list): Coefficients of the polynomial in descending order of powers.

    Returns:
    numpy.ndarray: Generator matrix.
    """

    n =len(g_coeffs)

    # Initialize the generator matrix G
    G = [[0 for _ in range(n)] for _ in range(n)]

    # Fill the identity matrix part
    for i in range(n-1):
        G[i][i+1] = 1

    # Fill the P matrix part using the polynomial coefficients
    for i in range(n):
        G[i][0] = g_coeffs[i]

    return G

def matrix_iterate(A, n):
    if n == 1:
        return A
    else:
        result = A
        for i in range(n-1):
            result = matrix_multiply(A, result)
        return result
    

def crc_verilog_gen(g_coeffs,n,data_width):
    """
    Generate a Verilog module for CRC calculation.

    Parameters:
    g_coeffs (list): Coefficients of the polynomial in descending order of powers.
        for example: g_coeffs = [1,1,0,1,0] represents CRC-5 with polynomial x^5 + x^4 + x^2 + 1
    n (int): Number of bits in the CRC.
    data_width (int): Width of the data input.

    Returns:
    str(file): Verilog module code.
    """

    # Check if the length of g_coeffs matches the expected number of parity bits
    if len(g_coeffs) != n:
        raise ValueError("The length of g_coeffs must be equal to n")
    
    shifted_g_coeffs = [0] * n
    for i in range(n-1):
        shifted_g_coeffs[i] = g_coeffs[i+1]
    shifted_g_coeffs[-1] = 1

    g_coeffs = shifted_g_coeffs;
    # Generate the generator matrix
    G = generate_generator_matrix(g_coeffs)

    a, b = divmod(data_width, n)
    if b == 0:
        matrix_count = a
    else:
        matrix_count = a + 1

    matrices = []
    for i in range(matrix_count):
        if b == 0:
            matrix = matrix_iterate(G, (i+1)*n)
        else:
            matrix = matrix_iterate(G, b+i*n)
        matrices.append(matrix)

    # Generate the Verilog module code
    module_name = f"crc{n}_d{data_width}"

    verilog_code = f"""
    //---------------------------------------------------------------------------
    //---------------------------------------------------------------------------
    // this file is automatically generated by crc_verilog_gen.py
    // CRC{n} with data_width:{data_width}
    // polynomial: x^{n} + {' + '.join(f'x^{n-1-i}' for i in range(n-1) if g_coeffs[i] == 1)} + 1
    // data_width: {data_width}
    // convention: the first serial bit is d[{data_width-1}]
    //---------------------------------------------------------------------------
    //---------------------------------------------------------------------------
    // d:  calculated data,{data_width} bits
    // ci: current crc status,{n} bits
    // co: next crc status,{n} bits
    //------------------------------------------
    //------------------------------------------
    module {module_name} (
        input [{data_width-1}:0] d,
        input [{n-1}:0] ci,
        output [{n-1}:0] co
    );\n"""

    for i in range(n):
        verilog_code += f"      assign co[{n-1-i}] = "
        first_bit = True
        for matrix_index, matrix in reversed(list(enumerate(matrices))):
            if matrix_index == len(matrices) - 1 :
                for bit_index, bit in enumerate(matrix[i]):
                    if bit == 1:
                        if not first_bit:
                            verilog_code += " ^ "
                        verilog_code += f"ci[{n-1-bit_index}]"
                        first_bit = False
                        
            for bit_index, bit in enumerate(matrix[i]):
                if bit == 1:
                    if b !=0 and (matrix_index*n + b-1-bit_index) < 0:
                        break
                    if not first_bit :
                        verilog_code += " ^ "
                    if b == 0:
                        verilog_code += f"d[{matrix_index*n + (n-1-bit_index)}]"
                    else:
                        verilog_code += f"d[{matrix_index*n + (b-1-bit_index)}]"
                    first_bit = False
        verilog_code += f";\n"

    verilog_code += """
    endmodule
    """      
    # Generate the file name based on n and data_width
    file_name = f"{module_name}.v"

    # Save the verilog_code to a file
    with open(file_name, "w") as file:
        file.write(verilog_code)
    return verilog_code

def main():
    parser = argparse.ArgumentParser(description="Generate Verilog module for CRC calculation.")
    parser.add_argument("-p", type=str, required=True, help="Coefficients of the polynomial in descending order of powers, e.g., '1,1,0,1,0' represents CRC-5 with polynomial x^5 + x^4 + x^2 + 1")
    parser.add_argument("-n", type=int, required=True, help="Number of bits in the CRC")
    parser.add_argument("-w", type=int, required=True, help="Width of the data input")

    args = parser.parse_args()

    g_coeffs = [int(x) for x in args.p.split(',')]
    n = args.n
    data_width = args.w

    verilog_code = crc_verilog_gen(g_coeffs, n, data_width)
    print(verilog_code)

if __name__ == "__main__":
    main()   