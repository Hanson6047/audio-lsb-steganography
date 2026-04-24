# Audio LSB Steganography

使用 LSB（最低有效位元）技術，將文字訊息或音訊檔案藏入 WAV 音訊的 Python 專案。

---

## 什麼是 LSB 隱寫術？

每個音訊樣本（sample）是一個數字，用二進位表示，例如：

```
10110110
```

LSB 技術只修改最後 1 個位元（最低有效位元）：

```
原始樣本：10110110
藏入 1 後：10110111  ← 只差最後一位
```

這樣的改變極小，人耳幾乎無法察覺，但足以藏入資訊。

### 藏入格式

```
[32-bit 長度標頭] + [payload bits]
```

前 32 個樣本的 LSB 記錄 payload 有幾個 bits，接著的樣本依序藏入實際資料。

---

## 專案結構

```
audio_lsb_steganography/
├── main.py           # CLI 入口（支援互動模式與指令模式）
├── requirements.txt  # 依賴套件
├── README.md         # 本文件
├── data/
│   ├── cover/        # 原始音訊（用來藏資料的容器）
│   ├── secret/       # 要隱藏的秘密音訊
│   └── output/       # 輸出結果
│       └── audio/    # 語音藏語音的輸出結果
└── src/
    ├── bit_utils.py  # 位元轉換工具
    ├── wav_utils.py  # WAV 讀寫工具
    ├── text_steg.py  # 文字隱寫邏輯
    └── audio_steg.py # 音訊隱寫邏輯
```

---

## 安裝步驟

**1. 複製專案**

```bash
git clone https://github.com/Hanson6047/audio-lsb-steganography.git
cd audio-lsb-steganography
```

**2. 安裝依賴套件**

```bash
pip install -r requirements.txt
```

---

## 使用方式

### 互動模式（推薦）

直接執行 `main.py`，程式會顯示選單引導你操作：

```bash
python main.py
```

```
========================================
   Audio LSB 隱寫工具  互動模式
========================================

請選擇功能：
  1. 句子編碼（把文字藏進音訊）
  2. 句子解碼（從音訊取出文字）
  3. 語音藏語音（藏入 / 取出）
  0. 離開
```

選擇功能後，程式會列出可用的音訊檔案供你選擇，並一步一步引導完成操作。

---

### 指令模式

適合腳本或自動化使用。

**文字編碼（把句子藏進音訊）**

```bash
python main.py encode-text --input data/cover/cover.wav --output data/output/stego.wav --message "Hello LSB"
```

**文字解碼（從音訊取出句子）**

```bash
python main.py decode-text --input data/output/stego.wav
```

---

## 功能說明

| 功能 | 說明 |
|---|---|
| 文字編碼 | 把文字訊息藏進 WAV 音訊的 LSB |
| 文字解碼 | 從 stego WAV 取出隱藏的文字訊息 |
| 語音藏語音 — 藏入 | 把短 WAV 音訊完整藏進長 WAV 音訊 |
| 語音藏語音 — 取出 | 從 stego WAV 還原隱藏的音訊檔案 |

---

## 目前限制

1. 只支援 WAV 格式，不支援 MP3
2. secret 音訊必須小於 cover 音訊的容量
3. 沒有加密，任何人取得 stego 檔案都能解出內容
4. 若 stego WAV 被轉成 MP3，隱藏資料會被破壞
5. 不支援隨機化藏入位置

---

## 未來改進方向

1. AES 加密，保護藏入的內容
2. 以密碼控制隨機藏入位置
3. 支援 2-bit、3-bit LSB 模式（提高容量）
4. 音質分析（MSE、SNR）
5. 波形比較視覺化
6. 支援藏入圖片、PDF、ZIP 等其他格式
7. GUI 圖形介面

---

## 開發環境

- Python 3.12
- NumPy
