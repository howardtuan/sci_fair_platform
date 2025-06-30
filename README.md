# 🎓 線上科展系統 Online Science Fair Platform

這是一個以 Django 開發的線上科展平台，提供學生上傳專題、瀏覽其他組別成果、留言評論，並支援助教評分與留言監控功能。

## ✅ 功能簡介

### 👨‍🎓 學生端功能
- 註冊、登入系統（僅學生身分）
- 加入課程（透過課程代碼）
- 上傳專題成果（影片、簡報）
- 瀏覽其他組成果與留言互動

### 🧑‍🏫 助教端功能
- 建立新課程（自動生成課程代碼）
- 查看所有留言紀錄（留言監控）
- 評分各組成果

## 🔧 技術架構

- **後端框架**：Django 5
- **資料庫**：SQLite（預設）
- **前端樣式**：Bootstrap 5
- **檔案上傳**：支援影片與簡報（PDF）

## 🛠️ 開發與執行

### 建立虛擬環境

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 執行專案
``` bash
cd sciapp
python manage.py migrate
python manage.py runserver
```
#### 然後打開瀏覽器前往：
👉 http://127.0.0.1:8000/

## 📌 注意事項
* 登入後才能進行任何課程相關操作
* 助教功能需手動設定帳號或透過管理者後台建立
