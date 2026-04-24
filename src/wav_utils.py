"""
wav_utils.py — WAV 檔案讀取與寫入工具

這個模組負責把 WAV 音訊檔案讀進來，轉成可以操作的 NumPy 陣列，
以及把修改後的陣列寫回 WAV 檔。
"""

import wave
import numpy as np


# 根據每個樣本佔幾個 bytes，對應到 NumPy 的資料型別
SAMPLE_DTYPE = {
    1: np.uint8,   # 8-bit WAV
    2: np.int16,   # 16-bit WAV（最常見）
    4: np.int32,   # 32-bit WAV
}


def read_wav(path: str):
    """
    讀取 WAV 檔案，回傳音訊參數與樣本陣列。

    Args:
        path: WAV 檔案路徑

    Returns:
        params: 包含聲道數、取樣率、位元深度等資訊的具名元組
        audio_samples: NumPy 陣列，每個元素代表一個音訊樣本
    """
    with wave.open(path, 'r') as wav:
        params = wav.getparams()
        frames = wav.readframes(params.nframes)  # 讀取所有音訊原始資料

    sample_width = params.sampwidth  # 每個樣本佔幾個 bytes

    if sample_width not in SAMPLE_DTYPE:
        raise ValueError(f"不支援的樣本寬度：{sample_width} bytes")

    dtype = SAMPLE_DTYPE[sample_width]
    # frombuffer 把原始 bytes 解讀成數字陣列
    # .copy() 是因為 frombuffer 回傳唯讀陣列，後續修改 LSB 需要可寫版本
    audio_samples = np.frombuffer(frames, dtype=dtype).copy()

    return params, audio_samples


def write_wav(path: str, params, audio_samples) -> None:
    """
    把音訊樣本陣列寫入 WAV 檔案。

    Args:
        path: 輸出的 WAV 檔案路徑
        params: 從 read_wav 取得的音訊參數
        audio_samples: NumPy 陣列，包含要寫入的音訊樣本
    """
    with wave.open(path, 'w') as wav:
        wav.setparams(params)
        wav.writeframes(audio_samples.tobytes())  # 陣列轉回 bytes 再寫入


def calculate_capacity_bits(audio_samples, lsb_count: int = 1) -> int:
    """
    計算此音訊最多可以藏多少 bits。

    每個樣本可以貢獻 lsb_count 個 bits（預設 1 個 LSB）。

    Args:
        audio_samples: NumPy 陣列，音訊樣本
        lsb_count: 使用幾個 LSB 來藏資料（預設 1）

    Returns:
        可藏入的最大 bits 數量
    """
    return len(audio_samples) * lsb_count


def check_capacity(payload_bits_count: int, audio_samples, lsb_count: int = 1) -> None:
    """
    檢查音訊是否有足夠空間容納指定數量的 bits。
    若空間不足則拋出錯誤。

    Args:
        payload_bits_count: 需要藏入的 bits 數量
        audio_samples: NumPy 陣列，音訊樣本
        lsb_count: 使用幾個 LSB（預設 1）
    """
    capacity = calculate_capacity_bits(audio_samples, lsb_count)
    if payload_bits_count > capacity:
        raise ValueError(
            f"空間不足：需要 {payload_bits_count} bits，"
            f"但音訊只能容納 {capacity} bits"
        )


if __name__ == "__main__":
    import os
    import sys

    # 可以在執行時指定 WAV 路徑，例如：python -m src.wav_utils data/cover/UCRoger.wav
    # 沒有指定的話就用預設的 cover.wav
    input_path = sys.argv[1] if len(sys.argv) > 1 else "data/cover/cover.wav"

    # 輸出檔名自動加上 test_ 前綴，例如 cover.wav → test_cover.wav
    original_filename = os.path.basename(input_path)
    output_path = f"data/output/test_{original_filename}"
    os.makedirs("data/output", exist_ok=True)

    # --- 步驟 1：讀取 WAV ---
    params, samples = read_wav(input_path)

    print("=== 音訊基本資訊 ===")
    print(f"聲道數：{params.nchannels}（1=單聲道，2=立體聲）")
    print(f"取樣率：{params.framerate} Hz")
    print(f"位元深度：{params.sampwidth * 8} bit")
    print(f"樣本數量：{len(samples)}")
    print(f"前 5 個樣本值：{samples[:5]}")

    # --- 步驟 2：計算容量 ---
    capacity = calculate_capacity_bits(samples)
    print(f"\n=== 容量計算 ===")
    print(f"可藏入的 bits 數：{capacity:,}")
    print(f"換算約：{capacity // 8:,} bytes")
    print(f"換算約：{capacity // 8 // 1024:,} KB 的文字")

    # --- 步驟 3：複製寫入 ---
    write_wav(output_path, params, samples)
    print(f"\n複製完成：{output_path}")
    print("請播放此檔案，確認聲音與原版相同。")
