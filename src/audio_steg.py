"""
audio_steg.py — 音訊 LSB 隱寫邏輯（語音藏語音）

這個模組負責把一個短 WAV 檔案的所有 bytes 藏進另一個長 WAV 的 LSB，
並能從 stego WAV 中取出還原成可播放的 WAV 檔案。

藏入格式（與 text_steg 相同）：
    [32-bit 長度標頭][secret WAV 的所有 bits]
    前 32 個樣本的 LSB 記錄 payload 有幾個 bits，
    接下來的樣本依序藏入 secret WAV 的每一個 bit。
"""

from src.bit_utils import bytes_to_bits, bits_to_bytes, int_to_32_bits, bits_to_int
from src.wav_utils import read_wav, write_wav, check_capacity


def hide_audio_in_wav(cover_wav: str, secret_wav: str, output_wav: str, lsb_count: int = 1) -> None:
    """
    把一個短 WAV 檔案藏進另一個長 WAV 檔案的 LSB。

    Args:
        cover_wav:  原始音訊路徑（用來藏東西的容器）
        secret_wav: 要隱藏的音訊路徑（必須夠小）
        output_wav: 輸出的 stego WAV 路徑
        lsb_count:  使用幾個 LSB（預設 1）
    """
    # 步驟 1：把整個 secret WAV 檔案讀成 bytes
    with open(secret_wav, 'rb') as f:
        secret_bytes = f.read()

    # 步驟 2：把 bytes 轉成 bits 串列
    payload_bits = bytes_to_bits(secret_bytes)

    # 步驟 3：製作 32-bit 長度標頭（告訴解碼器要讀幾個 bits）
    header_bits = int_to_32_bits(len(payload_bits))

    # 步驟 4：合併標頭 + payload
    all_bits = header_bits + payload_bits

    # 步驟 5：讀取 cover WAV
    params, samples = read_wav(cover_wav)

    # 步驟 6：確認空間夠用
    check_capacity(len(all_bits), samples, lsb_count)

    # 步驟 7：把每個 bit 藏進對應樣本的最低位元（LSB）
    for i, bit in enumerate(all_bits):
        samples[i] = (samples[i] & ~1) | bit

    # 步驟 8：寫出 stego WAV
    write_wav(output_wav, params, samples)
    print(f"藏入完成：{output_wav}")
    print(f"secret 大小：{len(secret_bytes):,} bytes，共 {len(payload_bits):,} bits")


def extract_audio_from_wav(stego_wav: str, output_secret_wav: str, lsb_count: int = 1) -> None:
    """
    從 stego WAV 中取出隱藏的音訊，還原成可播放的 WAV 檔案。

    Args:
        stego_wav:        stego WAV 檔案路徑
        output_secret_wav: 還原後的 secret WAV 輸出路徑
        lsb_count:        使用幾個 LSB（預設 1）
    """
    # 步驟 1：讀取 stego WAV
    params, samples = read_wav(stego_wav)

    # 步驟 2：從前 32 個樣本的 LSB 取出長度標頭
    header_bits = [int(samples[i]) & 1 for i in range(32)]
    payload_length = bits_to_int(header_bits)

    # 步驟 3：確認長度合理
    if payload_length <= 0 or payload_length > (len(samples) - 32):
        raise ValueError(f"無效的 payload 長度：{payload_length}，檔案可能未藏入任何音訊")

    # 步驟 4：從第 33 個樣本開始，取出 payload_length 個 LSB
    payload_bits = [int(samples[32 + i]) & 1 for i in range(payload_length)]

    # 步驟 5：把 bits 還原成 bytes
    secret_bytes = bits_to_bytes(payload_bits)

    # 步驟 6：把 bytes 直接寫成 WAV 檔案
    with open(output_secret_wav, 'wb') as f:
        f.write(secret_bytes)

    print(f"取出完成：{output_secret_wav}")
    print(f"還原大小：{len(secret_bytes):,} bytes")
