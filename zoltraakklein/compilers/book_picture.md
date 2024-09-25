目的：下記の「要求内容」を満たす絵本の要件定義書を「フォーマット」にしたがって作成してください。

要求内容：{prompt}

条件：
- 3歳のこどもが楽しめる内容とすること。
- ストーリーに起承転結があること。
- 最大10ページとすること。

フォーマット：

# タイトル
- タイトルをひらがなで書くこと

## あらすじ

## 登場キャラクター
- 下記のフォーマットで出力
```characters
名前：キャラクター設定
```

## 見出し構成
- 各ページの見出しを下記の一覧形式で出力
```list
headline: 見出し
```

## 画像生成向けプロンプト
- Translate the abstract in English here in a single line.
- Do not include any violent keywords.
- Add 'Japanese cartoon style;' and 'suitable for a 3-year-old;' at the end.
- Do not line-feed.
