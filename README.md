# OpenSCENARIO Creator

AIチャットを通じてASAM OpenSCENARIO 1.2形式のシナリオXMLを対話的に作成するStreamlitアプリです。

## セットアップ

```bash
pip install -r requirements.txt
```

## 環境変数

Gemini APIキーを設定してください：

```bash
export GEMINI_API_KEY="your_api_key_here"
```

または `.streamlit/secrets.toml` に記述：

```toml
GEMINI_API_KEY = "your_api_key_here"
```

APIキーは [Google AI Studio](https://aistudio.google.com/apikey) から取得できます。

## 起動

```bash
streamlit run openscenario_creator.py
```

## 機能

- 💬 **チャット形式** でシナリオを対話的に構築
- ⚡ **クイックテンプレート**（車線変更、歩行者横断、急停止、悪天候）
- 📄 **リアルタイムXMLプレビュー**（シンタックスハイライト付き）
- 🕒 **バージョン履歴**（過去5件のシナリオに戻れる）
- ⬇ **.xoscファイルのダウンロード**
- 💾 **会話履歴のJSON保存**

## 使い方

1. チャット欄に作りたいシナリオを日本語（または英語）で入力
2. AIが質問しながらシナリオを構築
3. 右パネルでXMLをリアルタイム確認
4. 「Download」タブから .xosc ファイルを保存
