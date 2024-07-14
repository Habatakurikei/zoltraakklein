![Zoltraak Klein Logo](https://repository-images.githubusercontent.com/828559799/cf060405-3975-49a2-987b-6d22ee7528cc)

# ZoltraakKlein

ZoltraakKleinは、大規模言語モデル（LLM）を使用して要件定義書を生成するためのPythonライブラリです。このライブラリは、ユーザーのリクエストに基づいて要件定義書のファイル名と内容を自動生成し、必要に応じて領域展開を行うことができます。

ZoltraakKleinは「小さいゾルトラーク」を意味し、ゾルトラークのエッセンスを取り出してコンパクトなクラスにしたものです。ゾルトラークがどのように動いているのか学習できるように日本語解説が付けられています。

## 特徴

- 複数のAIモデル（OpenAI、Anthropicなど）をサポート
- カスタマイズ可能なプロンプトとコンパイラ
- 要件定義書のファイル名自動生成
- 要件定義書の内容自動生成
- 将来的な領域展開機能（開発中）

## インストール

```bash
pip install zoltraakklein
```

## 事前環境設定

使用したい言語モデルのAPIキーを環境変数に設定してください。

Mac/Linux:

   ```
   export ANTHROPIC_API_KEY="your_anthropic_key"
   export GEMINI_API_KEY="your_gemini_key"
   export GROQ_API_KEY="your_groq_key"
   export OPENAI_API_KEY="your_openai_key"
   export PERPLEXITY_API_KEY="your_perplexity_key"
   ```

Windows:

   ```
   SET ANTHROPIC_API_KEY=your_anthropic_key
   SET GEMINI_API_KEY=your_gemini_key
   SET GROQ_API_KEY=your_groq_key
   SET OPENAI_API_KEY=your_openai_key
   SET PERPLEXITY_API_KEY=your_perplexity_key
   ```

## 使用方法

基本的な使用例：

```python
from zoltraakklein import ZoltraakKlein

# ZoltraakKleinのインスタンスを作成
# 'anthropic' はラベルなので任意の文字列をセット可能
zk = ZoltraakKlein(
    request="ウェブアプリケーションの要件定義書を作成してください",
    compiler="dev_sw",
    anthropic={
        "provider": "anthropic",
        "model": "claude-3-opus-20240229",
        "temperature": 0.5
    }
)

# 要件定義書の生成
zk.cast_zoltraak()

# 生成された要件定義書のパスを表示
print(f"生成された要件定義書: {zk.requirement_path}")
```

## 主要なクラスと関数

### ZoltraakKlein

メインクラスで、要件定義書の生成プロセスを管理します。

#### メソッド

- `__init__(self, request='', compiler='', expand=False, **kwargs)`: インスタンスを初期化します。
- `cast_zoltraak(self)`: 要件定義書の生成プロセス全体を実行します。
- `name_for_requirement(self)`: 要件定義書のファイル名を生成します。
- `generate_requirement(self)`: 要件定義書の内容を生成します。
- `expand_domain(self)`: 領域展開を行います（現在開発中）。

### その他の機能

- `seek_compiler(name='')`: 指定されたコンパイラファイルを検索します。

## 設定

`config.py`ファイルで以下の設定を変更できます：

- デフォルトのAIプロバイダーとモデル
- 各種パスの設定
- プロンプトファイルの指定
- 領域展開可能なコンパイラのリスト

## 注意事項

- 複数のAIモデルを使用する場合、最初に指定したモデルの生成物のみが`self.file_name`と`self.requirement_path`に格納されます。
- 領域展開機能は現在開発中です。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、[LICENSE](LICENSE)ファイルを参照してください。

## コントリビューション

プロジェクトへの貢献に興味がある方は、イシューやプルリクエストを歓迎します。

## サポート

問題や質問がある場合は、GitHubのイシューを作成してください。
