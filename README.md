# Audio LSB Steganography

使用 LSB（最低有效位元）技術，將文字或音訊藏入 WAV 音訊檔案的 Python 專案。

## 什麼是 LSB 隱寫術？

每個音訊樣本（sample）是一個數字，例如 `10110110`。
LSB 技術只修改最後 1 個位元：`10110110` → `10110111`
這樣的改變人耳幾乎無法察覺，但可以藏入資訊。

## 專案結構

```
audio_lsb_steganography/
├── main.py          # CLI 入口
├── requirements.txt # 依賴套件
├── README.md        # 本文件
├── data/
│   ├── cover/       # 原始封面音訊（用來藏資料）
│   ├── secret/      # 要藏入的秘密音訊
│   └── output/      # 輸出結果
└── src/
    ├── bit_utils.py  # 位元轉換工具
    ├── wav_utils.py  # WAV 讀寫工具
    ├── text_steg.py  # 文字隱寫邏輯
    └── audio_steg.py # 音訊隱寫邏輯
```

## 功能（開發中）

- [ ] 文字轉 bits
- [ ] WAV 讀寫
- [ ] 文字 LSB 隱寫 / 還原
- [ ] CLI 操作介面
- [ ] 音訊 LSB 隱寫 / 還原


---

