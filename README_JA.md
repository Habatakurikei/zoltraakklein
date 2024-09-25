![Zoltraak Klein Logo](https://repository-images.githubusercontent.com/828559799/cf060405-3975-49a2-987b-6d22ee7528cc)

こちらは ver. 0.1.0 デモバージョンの日本語解説です。最新バージョンは使い方が異なるのでご注意ください。

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

### 基本的な使用例

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

### 解説

`provider` は `anthropic`, `openai`, `google`, `groq`, `perplexity` から指定してください。

`model` は各社のAPIドキュメントで定義されているモデル名称を指定してください。例： `claude-3-5-sonnet-20240620`, `gemini-1.5-flash`

`compiler` についてはこちらの [コンパイラリスト](https://github.com/Habatakurikei/zoltraakklein/tree/main/zoltraakklein/compiler) に全コンパイラが保管されています。ローカル魔法図書館とでも呼びましょうか。

ただし多くて何を選べばわからないと思います。 [ウェブアプリ](https://zoltraak.app) で使用しているコンパイラのリストがこちらになります。この中からお選びいただくだけでかなり活用できると思います。

- 企画書 (`general_proposal`): 企画書を生成します。各種ビジネス、イベント、プロジェクト、教育・研究、芸術・文化、非営利活動、政策立案などに活用できます。
- 戦略的コンサル資料 (`biz_consult`): ビジネスコンサルティングに関する資料を生成します。課題出し、評価方法、クラス図、収益モデル、計画、フェルミ推定などを生成します。
- 市場調査 (`marketing_research`): 市場規模、成長率、トレンド、潜在顧客とニーズ、競合調査、ステークスホルダーの情報を生成します。
- 商談資料（段取り） (`business_negotiation`): 商談をスムーズに進めるための顧客理解、競合、ヒヤリング案、事前準備、契約条件、スケジュール、予算、シナリオを生成します。
- プレゼン資料 (`presentation_reveal`): プレゼン資料の構成と納期や予算を提案します。領域展開で Reveal.js によるスライド一式を生成します。
- 書籍 (`book_epub`): 書籍を執筆します。ビジネス書、小説などジャンルは問いません。概要、想定読者、目次などを提案します。領域展開で本文を含む EPUB 形式の電子書籍パッケージも生成できます。
- ネット記事アイデア出し (`web_article`): ブログ、解説、ニュースなどのネット記事のアイデアを生成。タイトル、図解、見出し構成、読者から共感を得られるポイントなどを提案します。
- キャラクター設定生成 (`virtual_human`): VTuber, AIモデル, 小説の登場人物, アバターなどキャラクター設定情報を生成します。名前、年齢、性別、出身地、職業、役割、外見、性格、口癖、交友関係、能力などを提案します。
- プロジェクト要件定義 (`general_def`): 一般的な開発タスクに関する要件定義書を生成します。
- ソフトウェア (`dev_sw`): 一般的なソフトウェアを生成します。細かく指定したい場合は「 Python, JavaScript, C++, PyPI, Wordpress, ウェブアプリ, スマホアプリ」などをプロンプトで指定します。領域展開で複数ファイルとディレクトリ一式を生成します。
- ホームページ (`dev_hp`): ホームページの全体構成について要件定義書を生成します。デザイン、素材、UI構造などを提案します。領域展開で関連コードを一式生成します。
- MVPシステム開発提案 (`dev_akirapp`): 何かを開発したいけどどうしたらいいのかわからない場合このコンパイラを使います。必要最小限の機能を持ったプロダクト (MVP: Minimum Viable Product) の考え方に基づいて提案します。 Special Thanks あきらパパさん
- レシピ考案 (`cooking_recipe`): 料理のレシピを考案します。コンセプト、味、見た目、材料、調理時間、調理方法、器具、予算、保存方法などを提案します。
- コーディネート相談 (`outfit_idea`): シチュエーションに合わせた服装、ヘアスタイル、お化粧のポイント、持ち物、アクセサリー類などを提案をします。
- 旅のしおり (`travel_plan`): 国内・国外の旅行計画を提案します。目的、交通手段、宿泊先、予算、観光スポット、現地グルメ、持ち物、現地で気を付けるべきマナーなどを提案します。


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

- [`LLMMaster`](https://github.com/Habatakurikei/llmmaster) をベースに作成しているため複数のAIモデルで要件定義書複数並列生成もできます。この場合、最初に指定したモデルの生成物のみが`self.file_name`と`self.requirement_path`に格納されます。ただしこれは上級者向けなのであまり真似しないでください。
- 領域展開機能は現在開発中です。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、[LICENSE](LICENSE)ファイルを参照してください。

## コントリビューション

プロジェクトへの貢献に興味がある方は、イシューやプルリクエストを歓迎します。

## サポート

問題や質問がある場合は、GitHubのイシューを作成してください。
