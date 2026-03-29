import sys


def hamming_parity_count(data_len: int) -> int:
    r = 0
    while (2**r) < (data_len + r + 1):
        r += 1
    return r


def coding_bit(data_bits: str, len_block: int):
    parity_count = hamming_parity_count(len_block)
    encoded_total = ""

    for i in range(0, len(data_bits), len_block):
        block = data_bits[i : i + len_block]
        if len(block) < len_block:
            block = block.ljust(len_block, "0")

        res_list = []
        data_idx = 0
        for pos in range(1, len_block + parity_count + 1):
            if (pos & (pos - 1)) == 0:
                res_list.append("0")
            else:
                res_list.append(block[data_idx])
                data_idx += 1

        for i_p in range(parity_count):
            p_pos = 2**i_p
            parity_value = 0
            for j, bit in enumerate(res_list, start=1):
                if j & p_pos:
                    parity_value ^= int(bit)
            res_list[p_pos - 1] = str(parity_value)

        encoded_total += "".join(res_list)
    return encoded_total


def decoding_bit(encoded_bits: str, len_block: int):
    parity_count = hamming_parity_count(len_block)
    block_len_full = len_block + parity_count
    decoded_data = ""

    num_blocks = len(encoded_bits) // block_len_full
    for b_idx in range(num_blocks):
        start = b_idx * block_len_full
        block_str = encoded_bits[start : start + block_len_full]
        block = list(block_str)

        syndrome = 0
        for i in range(parity_count):
            p_pos = 2**i
            group_parity = 0
            for j, bit in enumerate(block, start=1):
                if j & p_pos:
                    group_parity ^= int(bit)
            if group_parity != 0:
                syndrome += p_pos

        if syndrome != 0:
            if syndrome <= len(block):
                print(
                    f"[*] Блок {b_idx}: ошибка в бите {syndrome}."
                )
                block[syndrome - 1] = "1" if block[syndrome - 1] == "0" else "0"
            else:
                print(f"[!] Блок {b_idx}: Синдром {syndrome} вне диапазона")

        for j, bit in enumerate(block, start=1):
            if (j & (j - 1)) != 0:
                decoded_data += bit

    return decoded_data


if __name__ == "__main__":

    print(coding_bit("1000111011101010", len("1000111011101010")))

    if len(sys.argv) != 2:
        print("Usage: python3 app.py <len block>")
        sys.exit(1)

    len_block = int(sys.argv[1])

    while True:
        action = input("\n1-Код, 2-Декод, 3-Выход: ")

        if action == "1":
            with open("text.txt", "rb") as f:
                content = f.read()

            bits = "".join(format(b, "08b") for b in content)
            encoded_str = coding_bit(bits, len_block)

            with open("code_file.txt", "wb") as f:
                for i in range(0, len(encoded_str), 8):
                    byte_str = encoded_str[i : i + 8].ljust(8, "0")
                    f.write(bytes([int(byte_str, 2)]))
            print("Закодировано.")

        elif action == "2":
            with open("code_file.txt", "rb") as f:
                content = f.read()
            bits = "".join(format(b, "08b") for b in content)
            decoded_bits = decoding_bit(bits, len_block)

            final_bytes = bytearray()
            for i in range(0, len(decoded_bits), 8):
                chunk = decoded_bits[i : i + 8]
                if len(chunk) == 8:
                    final_bytes.append(int(chunk, 2))

            with open("encode_file.txt", "wb") as f:
                f.write(final_bytes)
            print("Раскодировано.")
        elif action == "3":
            break
