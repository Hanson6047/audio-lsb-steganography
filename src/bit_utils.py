"""
bit_utils.py — 文字與位元之間的轉換工具

在 LSB 隱寫中，任何要藏入音訊的資料都必須先變成 0/1 序列（bits）。
這個模組提供所有與 bits 轉換有關的工具函式。
"""


def bytes_to_bits(data: bytes) -> list[int]:
    """
    把 bytes 物件轉成由 0 和 1 組成的串列。

    例如：b'H'（ASCII 72 = 01001000）→ [0, 1, 0, 0, 1, 0, 0, 0]

    Args:
        data: 要轉換的 bytes 物件

    Returns:
        由 0 和 1 組成的串列，長度 = len(data) * 8
    """
    bits = []
    for byte in data:
        # 從最高位元（第 7 位）到最低位元（第 0 位）逐一取出
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def bits_to_bytes(bits: list[int]) -> bytes:
    """
    把由 0 和 1 組成的串列還原回 bytes 物件。

    bits 的長度必須是 8 的倍數。

    Args:
        bits: 由 0 和 1 組成的串列

    Returns:
        還原後的 bytes 物件
    """
    if len(bits) % 8 != 0:
        raise ValueError(f"bits 長度必須是 8 的倍數，目前長度為 {len(bits)}")

    result = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i + 8]  # 每 8 個 bits 為一組
        # 把 8 個 bits 合併成一個整數（0~255）
        byte_value = 0
        for bit in byte_bits:
            byte_value = (byte_value << 1) | bit
        result.append(byte_value)

    return bytes(result)


def text_to_bits(text: str) -> list[int]:
    """
    把文字字串轉成由 0 和 1 組成的串列（使用 UTF-8 編碼）。

    Args:
        text: 要轉換的文字字串

    Returns:
        由 0 和 1 組成的串列
    """
    # 先把文字編碼成 bytes，UTF-8 支援英文、中文等多語言
    encoded = text.encode("utf-8")
    return bytes_to_bits(encoded)


def bits_to_text(bits: list[int]) -> str:
    """
    把由 0 和 1 組成的串列還原回文字字串（使用 UTF-8 解碼）。

    Args:
        bits: 由 0 和 1 組成的串列

    Returns:
        還原後的文字字串
    """
    raw_bytes = bits_to_bytes(bits)
    return raw_bytes.decode("utf-8")


def int_to_32_bits(value: int) -> list[int]:
    """
    把一個整數轉成長度為 32 的 0/1 串列。

    用途：製作 payload 長度的標頭（header），
    讓解碼器知道後面有多少 bits 需要讀取。

    Args:
        value: 要轉換的整數（範圍：0 ~ 4294967295）

    Returns:
        長度為 32 的 0/1 串列
    """
    if value < 0 or value > 0xFFFFFFFF:
        raise ValueError(f"value 必須在 0 ~ {0xFFFFFFFF} 之間，目前為 {value}")

    bits = []
    for i in range(31, -1, -1):  # 從第 31 位元到第 0 位元
        bits.append((value >> i) & 1)
    return bits


def bits_to_int(bits: list[int]) -> int:
    """
    把長度為 32 的 0/1 串列還原成整數。

    Args:
        bits: 長度為 32 的 0/1 串列

    Returns:
        還原後的整數
    """
    if len(bits) != 32:
        raise ValueError(f"bits 長度必須為 32，目前為 {len(bits)}")

    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


if __name__ == "__main__":
    # --- 測試 1：文字轉換 ---
    original_text = "Hello"
    bits = text_to_bits(original_text)
    recovered_text = bits_to_text(bits)

    print("=== 測試文字轉換 ===")
    print(f"原始文字：{original_text}")
    print(f"轉成 bits（前 16 個）：{bits[:16]}")
    print(f"還原文字：{recovered_text}")
    print(f"轉換正確：{original_text == recovered_text}")
    print()

    # --- 測試 2：32-bit 長度標頭 ---
    length = len(bits)
    header_bits = int_to_32_bits(length)
    recovered_length = bits_to_int(header_bits)

    print("=== 測試 32-bit 長度標頭 ===")
    print(f"payload 長度：{length}")
    print(f"32-bit 標頭：{header_bits}")
    print(f"還原長度：{recovered_length}")
    print(f"長度正確：{length == recovered_length}")
