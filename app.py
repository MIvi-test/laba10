import sys


def hamming_parity_count(data_len: int) -> int:
    r = 0
    while (2**r) < (data_len + r + 1):
        r += 1
    return r


def insert_parity_positions(data_block: str, parity_count: int):
    result = []
    data_index = 0
    total_len = len(data_block) + parity_count
    for pos in range(1, total_len + 1):
        if (pos & (pos - 1)) == 0:
            result.append("0")
            # гениальная вставка нуля в биты
        else:
            result.append(data_block[data_index])
            data_index += 1
    return "".join(result)


def compute_parity_bits(word: str, parity_count: int):
    bits = [0] * parity_count
    for i in range(parity_count):
        parity_pos = 2**i
        parity = 0
        for j, bit in enumerate(word, start=1):
            if j & parity_pos:
                parity ^= int(bit)
        bits[i] = parity
    return bits


def set_parity_bits(word: str, parity_bits: list[int]):
    w = list(word)
    for i, parity in enumerate(parity_bits):
        w[2**i - 1] = str(parity)
    return "".join(w)


def coding_bit(data: str, len_block: int):
    if len_block <= 0:
        raise ValueError("len_block must be > 0")
    parity_count = hamming_parity_count(len_block)
    result = []
    for offset in range(0, len(data), len_block):
        block = data[offset: offset + len_block]
        if len(block) < len_block:
            block = block.zfill(len_block)
        with_parity = insert_parity_positions(block, parity_count)
        parity_bits = compute_parity_bits(with_parity, parity_count)
        encoded = set_parity_bits(with_parity, parity_bits)
        result.append(encoded)
    return "".join(result)


def encoding_bit(data: str, len_block: int):
    if len_block <= 0:
        raise ValueError("len_block must be > 0")
    parity_count = hamming_parity_count(len_block)
    block_len = len_block + parity_count
    result = []
    for offset in range(0, len(data), block_len):
        block = data[offset: offset + block_len]
        if len(block) < block_len:
            block = block.ljust(block_len, "0")
        syndrome = 0
        for i in range(parity_count):
            parity_pos = 2**i
            parity = 0
            for j, bit in enumerate(block, start=1):
                if j & parity_pos:
                    parity ^= int(bit)
            if parity:
                syndrome += parity_pos
        if syndrome:
            idx = syndrome - 1
            if 0 <= idx < len(block):
                flipped = "1" if block[idx] == "0" else "0"
                block = block[:idx] + flipped + block[idx + 1:]
        data_bits = [bit for j, bit in enumerate(
            block, start=1) if (j & (j - 1)) != 0]
        result.append("".join(data_bits))
    return "".join(result)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 app.py <len block>")
        sys.exit(1)

    if not sys.argv[1].isdigit() or int(sys.argv[1]) <= 0:
        print("ошибка размера блока")
        sys.exit(1)
    data_bytes = None
    len_block = int(sys.argv[1])
    while (True):
        action = input("(1) закодировать файл text.txt\n\
                    (2) раскодировать файл code_file.txt в файл encode_file.txt\n\
                    (3) выход из программы(exit)\n\
                    выберите что хотите сделать(цифра): ")
        if (not action.isdigit()):
            print("ошибка выбора действия, попробуй ещё раз")
            continue

        if int(action) == 1:
            with open("text.txt", "rb") as f:
                data_bytes = f.read()

            data = "".join(format(byte, "08b") for byte in data_bytes)
            encoded = coding_bit(data, len_block)

            encoded_bytes = bytearray()
            for bits in range(0, len(encoded), 8):
                chunk = encoded[bits:bits + 8]
                if len(chunk) < 8:
                    chunk = chunk.ljust(8, "0")
                encoded_bytes.append(int(chunk, 2))

            with open("code_file.txt", "wb") as f:
                f.write(encoded_bytes)

        if int(action) == 2:
            try:
                with open("code_file.txt", "rb") as f:
                    db = f.read()
            except FileNotFoundError:
                print("Ошибка: нет закодированного файла.")
                continue

            data = "".join(format(byte, "08b") for byte in db)
            decoded = encoding_bit(data, len_block)

            decoded_bytes = bytearray()
            for bits in range(0, len(decoded), 8):
                chunk = decoded[bits:bits + 8]
                if len(chunk) < 8:
                    chunk = chunk.ljust(8, "0")
                decoded_bytes.append(int(chunk, 2))

            with open("encode_file.txt", "wb") as f:
                f.write(decoded_bytes)
        if (action == 'exit') or int(action) == 3:
            break
