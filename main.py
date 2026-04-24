"""
main.py — 命令列介面入口

這個檔案是整個程式的入口點。
它負責讀取使用者輸入的指令和參數，
再呼叫對應的函式來執行隱寫操作。

本檔案不包含任何隱寫邏輯，只負責「接收指令 → 呼叫正確的函式」。
"""

import argparse
from src.text_steg import hide_text_in_wav, extract_text_from_wav


def main():
    parser = argparse.ArgumentParser(
        description="Audio LSB Steganography — 音訊 LSB 隱寫工具"
    )

    # 建立子指令系統（每個子指令有自己的參數）
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- 子指令：encode-text ---
    encode_parser = subparsers.add_parser(
        "encode-text",
        help="把文字訊息藏進 WAV 檔案"
    )
    encode_parser.add_argument("--input",   required=True, help="cover WAV 檔案路徑")
    encode_parser.add_argument("--output",  required=True, help="輸出的 stego WAV 路徑")
    encode_parser.add_argument("--message", required=True, help="要藏入的文字訊息")

    # --- 子指令：decode-text ---
    decode_parser = subparsers.add_parser(
        "decode-text",
        help="從 WAV 檔案取出隱藏的文字訊息"
    )
    decode_parser.add_argument("--input", required=True, help="stego WAV 檔案路徑")

    # 解析使用者輸入的指令
    args = parser.parse_args()

    # 根據子指令呼叫對應的函式
    if args.command == "encode-text":
        hide_text_in_wav(args.input, args.output, args.message)

    elif args.command == "decode-text":
        message = extract_text_from_wav(args.input)
        print(f"取出訊息：{message}")


if __name__ == "__main__":
    main()
