"""
text_steg.py — 文字 LSB 隱寫邏輯

這個模組負責把文字訊息藏進 WAV 音訊的 LSB，
以及從 stego WAV 中取出隱藏的文字訊息。

藏入格式：
    [32-bit 長度標頭][payload bits]
    前 32 個樣本的 LSB 記錄 payload 有幾個 bits，
    接下來的樣本依序藏入實際訊息的每一個 bit。
"""

from src.bit_utils import text_to_bits, bits_to_text, int_to_32_bits, bits_to_int
from src.wav_utils import read_wav, write_wav, check_capacity


def hide_text_in_wav(input_wav: str, output_wav: str, message: str, lsb_count: int = 1) -> None:
    """
    把文字訊息藏進 WAV 音訊檔案的 LSB。

    Args:
        input_wav: 原始 WAV 檔案路徑（cover）
        output_wav: 輸出的 stego WAV 檔案路徑
        message: 要隱藏的文字訊息
        lsb_count: 使用幾個 LSB（預設 1）
    """
    # 步驟 1：把文字轉成 bits
    payload_bits = text_to_bits(message)

    # 步驟 2：製作 32-bit 長度標頭（讓解碼器知道要讀幾個 bits）
    header_bits = int_to_32_bits(len(payload_bits))

    # 步驟 3：合併標頭 + payload，這是要藏入的全部 bits
    all_bits = header_bits + payload_bits

    # 步驟 4：讀取 cover WAV
    params, samples = read_wav(input_wav)

    # 步驟 5：確認音訊空間夠用，不夠就報錯
    check_capacity(len(all_bits), samples, lsb_count)

    # 步驟 6：把每個 bit 藏進對應樣本的最低位元（LSB）
    for i, bit in enumerate(all_bits):
        # (samples[i] & ~1)：清除最低位元（變成 0）
        # | bit：把秘密 bit 放進最低位元
        samples[i] = (samples[i] & ~1) | bit

    # 步驟 7：寫出 stego WAV
    write_wav(output_wav, params, samples)
    print(f"藏入完成：{output_wav}")
    print(f"訊息長度：{len(message)} 個字元，共 {len(payload_bits)} bits")


def extract_text_from_wav(stego_wav: str, lsb_count: int = 1) -> str:
    """
    從 stego WAV 音訊檔案中取出隱藏的文字訊息。

    Args:
        stego_wav: stego WAV 檔案路徑
        lsb_count: 使用幾個 LSB（預設 1）

    Returns:
        取出的文字訊息
    """
    # 步驟 1：讀取 stego WAV
    params, samples = read_wav(stego_wav)

    # 步驟 2：從前 32 個樣本的 LSB 取出長度標頭
    header_bits = [int(samples[i]) & 1 for i in range(32)]
    payload_length = bits_to_int(header_bits)

    # 步驟 3：確認長度合理，避免讀到垃圾資料
    if payload_length <= 0 or payload_length > len(samples) - 32:
        raise ValueError(f"無效的 payload 長度：{payload_length}，檔案可能未藏入任何訊息")

    # 步驟 4：從第 33 個樣本開始，取出 payload_length 個 LSB
    payload_bits = [int(samples[32 + i]) & 1 for i in range(payload_length)]

    # 步驟 5：把 bits 還原成文字
    return bits_to_text(payload_bits)


if __name__ == "__main__":
    import sys
    import os

    cover_path = "data/cover/cover.wav"
    stego_path = "data/output/stego.wav"
    os.makedirs("data/output", exist_ok=True)

    # 可在執行時帶入自訂訊息，例如：python -m src.text_steg "我的秘密"
    message = sys.argv[1] if len(sys.argv) > 1 else "Hello, LSB!"

    print(f"原始訊息：{message}")
    print()

    # --- 藏入 ---
    hide_text_in_wav(cover_path, stego_path, message)

    # --- 取出 ---
    recovered = extract_text_from_wav(stego_path)
    print(f"取出訊息：{recovered}")
    print(f"驗證正確：{message == recovered}")
