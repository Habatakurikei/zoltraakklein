# Zoltraak Klein

Zoltraak Klein は、大規模言語モデル（LLM）を活用して要件定義書を生成するPythonライブラリです。本プロジェクトは、より大規模なZoltraakプロジェクトのエッセンスを抽出し、コンパクトで理解しやすい形に再構築したものです。

ゾルトラーク・クライン（小さいゾルトラーク）は、ゾルトラークのエッセンスを取り出してコンパクトなクラスにしました。ゾルトラークがどのように動いているのか学習できるように日本語解説付けました。

## 主な機能

1. **要件定義書ファイル名の生成**: ユーザーの入力（プロンプト）に基づいて、適切な要件定義書のファイル名を自動生成します。

2. **要件定義書本文の生成**: 指定されたコンパイラ（テンプレート）を使用して、要件定義書の本文を生成します。

3. **領域展開**: 要件定義書をベースにファイル生成します。（将来実装予定）

4. **マルチモデル対応**: 複数のAIモデルを並行して使用し、結果を比較することができます。

## ZoltraakKleinクラスの詳細

### 初期化

```python
def __init__(self, request='', compiler='', expand=False, **kwargs):
```

- `request`: 要件定義のリクエスト内容（プロンプト）
- `compiler`: 使用するコンパイラ（テンプレート）の名前（*.md）
- `expand`: 領域展開を行うかどうか（現在は未実装）
- `**kwargs`: 使用するAI（LLM）の情報

### 主要メソッド

1. `cast_zoltraak()`: 
   - 要件定義書の生成プロセス全体を実行します。
   - ファイル名の生成、要件定義書本文の生成、（将来的に）領域展開を順に行います。

2. `name_for_requirement()`:
   - 要件定義書のファイル名を生成します。
   - 生成されたファイル名は `self.file_name` に格納されます。

3. `generate_requirement()`:
   - 要件定義書の本文を生成します。
   - 生成された要件定義書のパスは `self.requirement_path` に格納されます。

4. `expand_domain()`:
   - （未実装）領域展開を行う予定の機能です。

### 内部メソッド

- `_check_folders_exist()`: 必要なフォルダ構造を確認・作成します。
- `_generate_naming_prompt()`: ファイル名生成用のプロンプトを作成します。
- `_generate_requirement_prompt()`: 要件定義書本文生成用のプロンプトを作成します。

### 事前環境設定

実行前に使用したいAIモデルのAPIキーを環境変数に設定してください。

Mac/Linux,

```
export ANTHROPIC_API_KEY="your_anthropic_key"
export GEMINI_API_KEY="your_gemini_key"
export GROQ_API_KEY="your_groq_key"
export OPENAI_API_KEY="your_openai_key"
export PERPLEXITY_API_KEY="your_perplexity_key"
```

Windows,

```
SET ANTHROPIC_API_KEY=your_anthropic_key
SET GEMINI_API_KEY=your_gemini_key
SET GROQ_API_KEY=your_groq_key
SET OPENAI_API_KEY=your_openai_key
SET PERPLEXITY_API_KEY=your_perplexity_key
```

### 使用例

```python
from zoltraakklein import ZoltraakKlein

# インスタンスの作成
# 'anthropic' はラベルなので任意の文字列を入力可能
zk = ZoltraakKlein(
    request="生成AIとチャットできるスマホアプリの要件定義",
    compiler="dev_sw",
    anthropic={
        "provider": "anthropic",
        "model": "claude-3-opus-20240229",
        "temperature": 0.7
    }
)

zk.cast_zoltraak()

print(f"生成されたファイル名: {zk.file_name}")
print(f"生成された要件定義書のパス: {zk.requirement_path}")
```

### 注意点

- 複数のAIモデルを指定した場合、最初に指定したモデルの結果のみが `self.file_name` と `self.requirement_path` に格納されます。
- 全モデルの結果にアクセスするには、`self.master_naming.results` と `self.master_requirement.results` を使用します。
- 領域展開機能（`expand_domain()`）は現在実装中です。

## 設定

`config.py`ファイルで、デフォルトの言語モデル、各種パス、プロンプトファイルなどの設定を行うことができます。

## 注意事項

- 複数のAIモデルを使用する場合、最初に指定したモデルの生成結果のみが`self.file_name`と`self.requirement_path`に格納されます。
- 全モデルの生成結果にアクセスするには、各`LLMMaster`インスタンスの`results`属性を参照してください。

## 貢献

プロジェクトへの貢献を歓迎します。イシューの報告、プルリクエストの送信など、どんな形でも構いません。

## ライセンス

このプロジェクトのライセンス情報については、[LICENSE](LICENSE)ファイルを参照してください。
