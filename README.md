![Zoltraak Klein Logo](https://repository-images.githubusercontent.com/828559799/cf060405-3975-49a2-987b-6d22ee7528cc)

# Zoltraak Klein

Zoltraak Klein （ゾルトラーク・クライン）は「小さいゾルトラーク」を意味し、ゾルトラークのエッセンスを取り出してコンパクトなクラスにしたものです。ゾルトラークがどのように動いているのか学習できるように日本語解説が付けられています。

Zoltraak は大規模言語モデル (LLM) を使用して要件定義書を生成するための Python ライブラリです。このライブラリはユーザーのリクエストに基づいて要件定義書のファイル名と内容を自動生成し、必要に応じてコード生成（領域展開）を行うことができます。

## どうやって動く？

![how-zoltraak-works](https://github.com/user-attachments/assets/2a620fed-bb82-491d-ae33-62d053a0299c)

Zoltraak の基本動作はこの3ステップです。

1. リクエスト内容を反映した要件定義書 **ファイル名命名**
2. リクエスト内容を反映した要件定義書の **本文生成**
3. 要件定義書を元に **コード等一括生成** （領域展開）

さらに細かい動作まで解説すると上図のようになります。

Zoltraak Klein は各ステップをクラスメソッドにして処理をできるだけ簡略化しました。 Zoltraak の動作を学べるように配慮しました。

もちろん動くのであなたが欲しい要件定義書を生成することができます。

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

APIキーを環境変数に設定してください。

あなたが使いたいプロバイダーのAPIだけをセットしてください。下記のすべてをセットする必要はありません。

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
# llm はただの識別ラベルなので任意の文字列をセット可能
# request, compiler, provider の3つは必須
# model, temperature, max_tokens は無くても動きます
zk = ZoltraakKlein(
    request="腕時計比較ウェブサイトの要件定義書を作成してください",
    compiler="dev_sw",
    llm={
        "provider": "openai",
        "model": "gpt-4o",
        "max_tokens": 4096,
        "temperature": 0.5
    }
)

# 要件定義書の生成
zk.cast_zoltraak()

# 生成された要件定義書のパスを表示、生成物の中身を確認してください
# 'C:\\Users\\daisuke\\Downloads\\zoltraakklein\\requirements\\def_watch_website.md' など
print(f"生成された要件定義書: {zk.requirement_path}")
```

プロバイダーは `anthropic`, `openai`, `google`, `groq`, `perplexity` から指定してください。

`model` は各社のAPIドキュメントで定義されているモデル名称を指定してください。例： `claude-3-5-sonnet-20240620`, `gemini-1.5-flash`

## 主要なクラスと関数

### ZoltraakKlein

メインクラスで、要件定義書の生成プロセスを管理します。

#### メソッド

- `__init__(self, request='', compiler='', expand=False, **kwargs)`: インスタンスを初期化します。
- `cast_zoltraak(self)`: 要件定義書の生成プロセス全体を実行します。
- `name_for_requirement(self)`: 要件定義書のファイル名を生成します。
- `generate_requirement(self)`: 要件定義書の内容を生成します。
- `expand_domain(self)`: 領域展開を行います（現在開発中）。

メインは `cast_zoltraak()` ですが各メソッド単体でも呼び出しできます。ただし自己責任でご利用ください。

### その他の機能

- `seek_compiler(name='')`: 指定されたコンパイラファイルを検索します。

## 設定

`config.py`ファイルで以下の設定を変更できます：

- デフォルトのAIプロバイダーとモデル
- 各種パスの設定
- プロンプトファイルの指定
- 領域展開可能なコンパイラのリスト

## 注意事項

- 複数のAIモデルで並列生成する場合、最初に指定したモデルの生成物のみが`self.file_name`と`self.requirement_path`に格納されます。ただしこれは上級者向けなのであまり真似しないでください。
- 領域展開機能は現在開発中です。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、[LICENSE](LICENSE)ファイルを参照してください。

## コントリビューション

プロジェクトへの貢献に興味がある方は、イシューやプルリクエストを歓迎します。

## サポート

問題や質問がある場合は、GitHubのイシューを作成してください。
