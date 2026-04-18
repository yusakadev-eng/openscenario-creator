# OpenSCENARIO Creator

Gemini APIを使ったチャット形式のOpenSCENARIOシナリオ自動生成ツールです。

---

## 📌 概要

- チャット形式でAIと対話しながらOpenSCENARIO 1.2形式のXMLを生成できる
- 回答後にGemini APIがリアルタイムでシナリオXMLを生成・更新
- クイックテンプレート（車線変更・歩行者横断・急停止・悪天候）で即座に開始可能
- Streamlit で動作するローカルアプリ

---

## 🖼️ デモ

![デモ](docs/OpenScenario_demo.gif)

---

## 🛠️ 技術スタック

| 項目 | 内容 |
|------|------|
| 言語 | Python 3.11 |
| フレームワーク | Streamlit |
| AI API | Gemini API（google-genai） |
| シナリオ形式 | ASAM OpenSCENARIO 1.2 |
| APIキー管理 | .streamlit/secrets.toml |

---

## 📁 ファイル構成

```
openscenario-creator/
├── openscenario_creator.py   # Streamlitメインアプリ
├── docs/
│   └── OpenScenario_demo.gif    # デモ動画
├── .streamlit/
│   └── secrets.toml          # APIキー（GitHubに上げない）
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 セットアップ・起動手順

### 1. リポジトリをクローン

```bash
git clone https://github.com/yusakadev-eng/openscenario-creator.git
cd openscenario-creator
```

### 2. ライブラリをインストール

```bash
pip install -r requirements.txt
```

### 3. Gemini APIキーを取得

[Google AI Studio](https://aistudio.google.com/apikey) でAPIキーを取得します。

### 4. secrets.tomlファイルを作成

`.streamlit/secrets.toml` を作成し、以下を記述します。

```toml
GEMINI_API_KEY = "your_api_key_here"
```

### 5. アプリを起動

```bash
streamlit run openscenario_creator.py
```

ブラウザで `http://localhost:8501` を開くと起動します。

---

## 📝 シナリオの作成方法

チャット欄に作りたいシナリオを日本語（または英語）で入力するだけです。

```
例：高速道路で自車が80km/hで走行中、隣車線の車両が前方に割り込むシナリオを作成してください。
```

AIが質問しながらシナリオを構築し、右パネルにXMLがリアルタイムで表示されます。
完成したら「Download」タブから `.xosc` ファイルを保存できます。

---

## 🤖 AI活用について

このアプリは以下の用途でAIを活用しています。

- **シナリオ生成**：Gemini APIがユーザーの要件をもとにOpenSCENARIO 1.2準拠のXMLを生成
- **開発支援**：ClaudeとChatGPTを使って設計・実装・ドキュメント作成を進めました

---

## ⚠️ 注意事項

- `.streamlit/secrets.toml` はGitHubに上げないでください（APIキーが含まれます）
- Gemini APIは無料枠の範囲内で使用しています

---

## 📄 ライセンス

MIT License
