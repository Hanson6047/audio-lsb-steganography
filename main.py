"""
main.py — 命令列介面入口（支援互動模式與指令模式）

執行方式：
  互動模式：python main.py
  指令模式：python main.py encode-text --input ... --output ... --message ...
            python main.py decode-text --input ...
"""

import argparse
import os
import sys
from src.text_steg import hide_text_in_wav, extract_text_from_wav


# ──────────────────────────────────────────
# 工具函式
# ──────────────────────────────────────────

def list_wav_files(directory: str) -> list:
    """列出指定資料夾內的所有 WAV 檔案名稱（僅檔名，不含路徑）"""
    if not os.path.exists(directory):
        return []
    return [f for f in os.listdir(directory) if f.lower().endswith('.wav')]


def choose_file(directory: str, prompt: str) -> str:
    """
    讓使用者從資料夾中選擇一個 WAV 檔案。
    回傳選擇的完整路徑，如果資料夾是空的則回傳 None。
    """
    files = list_wav_files(directory)
    if not files:
        print(f"  找不到任何 WAV 檔案在 {directory}/")
        return None

    print(f"\n  {prompt}")
    for i, name in enumerate(files, 1):
        print(f"    {i}. {name}")

    while True:
        choice = input("\n  請輸入數字：").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            return os.path.join(directory, files[int(choice) - 1])
        print("  請輸入有效的數字")


# ──────────────────────────────────────────
# 互動模式：各功能流程
# ──────────────────────────────────────────

def interactive_encode_text():
    """互動式文字編碼：引導使用者選擇檔案、輸入句子、設定輸出名稱"""
    print("\n【句子編碼】把文字訊息藏進 WAV 檔案")
    print("-" * 36)

    # 步驟 1：選擇 cover 音訊
    cover_path = choose_file("data/cover", "請選擇要用來藏訊息的音訊檔案（cover）：")
    if cover_path is None:
        return

    # 步驟 2：輸入要隱藏的句子
    message = input("\n  請輸入要隱藏的句子：").strip()
    if not message:
        print("  句子不能為空，操作取消。")
        return

    # 步驟 3：設定輸出檔名（可按 Enter 使用預設值）
    output_name = input("  請輸入輸出檔案名稱（按 Enter 使用預設 stego.wav）：").strip()
    if not output_name:
        output_name = "stego.wav"
    if not output_name.lower().endswith('.wav'):
        output_name += '.wav'

    output_path = os.path.join("data/output", output_name)

    # 執行藏入
    print()
    hide_text_in_wav(cover_path, output_path, message)


def interactive_decode_text():
    """互動式文字解碼：引導使用者選擇 stego 檔案，取出隱藏訊息"""
    print("\n【句子解碼】從 WAV 檔案取出隱藏的文字訊息")
    print("-" * 36)

    # 從 output 資料夾選擇 stego 檔案
    stego_path = choose_file("data/output", "請選擇要解碼的 stego WAV 檔案：")
    if stego_path is None:
        return

    # 執行取出
    print()
    message = extract_text_from_wav(stego_path)
    print(f"  取出訊息：{message}")


def interactive_mode():
    """互動式主選單，讓使用者用數字選擇要執行的功能"""
    print("=" * 40)
    print("   Audio LSB 隱寫工具  互動模式")
    print("=" * 40)

    while True:
        print("\n請選擇功能：")
        print("  1. 句子編碼（把文字藏進音訊）")
        print("  2. 句子解碼（從音訊取出文字）")
        print("  3. 語音藏語音（Stage 6，尚未實作）")
        print("  0. 離開")

        choice = input("\n請輸入數字：").strip()

        if choice == "1":
            interactive_encode_text()
        elif choice == "2":
            interactive_decode_text()
        elif choice == "3":
            print("\n  此功能尚未實作，完成 Stage 6 後即可使用。")
        elif choice == "0":
            print("\n  再見！")
            break
        else:
            print("  請輸入 0 到 3 之間的數字。")


# ──────────────────────────────────────────
# 主程式入口
# ──────────────────────────────────────────

def main():
    # 沒有任何參數 → 進入互動模式
    if len(sys.argv) == 1:
        interactive_mode()
        return

    # 有參數 → 使用原本的指令模式
    parser = argparse.ArgumentParser(
        description="Audio LSB Steganography — 音訊 LSB 隱寫工具"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 子指令：encode-text
    encode_parser = subparsers.add_parser("encode-text", help="把文字訊息藏進 WAV 檔案")
    encode_parser.add_argument("--input",   required=True, help="cover WAV 檔案路徑")
    encode_parser.add_argument("--output",  required=True, help="輸出的 stego WAV 路徑")
    encode_parser.add_argument("--message", required=True, help="要藏入的文字訊息")

    # 子指令：decode-text
    decode_parser = subparsers.add_parser("decode-text", help="從 WAV 檔案取出隱藏的文字訊息")
    decode_parser.add_argument("--input", required=True, help="stego WAV 檔案路徑")

    args = parser.parse_args()

    if args.command == "encode-text":
        hide_text_in_wav(args.input, args.output, args.message)
    elif args.command == "decode-text":
        message = extract_text_from_wav(args.input)
        print(f"取出訊息：{message}")


if __name__ == "__main__":
    main()
