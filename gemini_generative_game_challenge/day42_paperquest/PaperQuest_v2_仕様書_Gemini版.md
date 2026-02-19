# PaperQuest v2 — 仕様書
**論文ビジュアル学習ツール（GitLab Pages 静的サイト）**
バージョン: 2.1 | 作成日: 2026-02-19 | AI エンジン: Gemini 1.5 Flash（無料）

---

## 1. プロジェクト概要

### 1.1 ビジョン

arXiv の論文 URL を入力するだけで、専門知識ゼロの人でも「何が書いてあるのか」を体感できるインタラクティブ学習体験を自動生成するツール。論文を「読むもの」ではなく「プレイするもの」に変換する。

### 1.2 ゴール

| 項目 | 内容 |
|------|------|
| **入力** | arXiv PDF の URL（例: `https://arxiv.org/pdf/2208.04717`） |
| **出力** | カード形式のビジュアル解説 ＋ インタラクティブ図解 ＋ 理解度クイズ ＋ 効果音演出 |
| **対象ユーザー** | その分野の専門知識を持たない一般の人 |
| **プラットフォーム** | GitLab Pages（完全静的サイト・サーバー不要） |
| **対応デバイス** | スマートフォン・iPad・PC（レスポンシブ） |
| **費用** | **完全無料**（Google アカウントのみ必要） |

### 1.3 コアコンセプト

```
arXiv URL
  → PDF テキスト抽出（PDF.js・ブラウザ内処理）
  → Gemini 1.5 Flash API で構造化（無料枠）
  → ビジュアル体験としてレンダリング
```

---

## 2. AI エンジン：Gemini 1.5 Flash 無料枠

### 2.1 なぜ Gemini 1.5 Flash か

| 比較項目 | Gemini 1.5 Flash（採用） | Claude API | Groq（無料枠） |
|---------|------------------------|-----------|--------------|
| 費用 | **完全無料** | 有料（$0.01〜0.05/論文） | 無料枠あり（制限厳しめ） |
| 必要なもの | Google アカウントのみ | クレジットカード登録 | Groq アカウント |
| 無料リクエスト数 | **1日 1,500回・1分 15回** | なし | 1分 30リクエスト等 |
| コンテキスト長 | **1M トークン**（論文全文 OK） | 200K | モデルによる |
| 日本語品質 | 高品質 | 最高品質 | やや劣る |
| 安定性 | Google インフラ（高い） | Anthropic インフラ（高い） | 変動あり |

**結論**：Gemini 1.5 Flash は無料枠が圧倒的に余裕があり、1M トークンのコンテキストウィンドウにより論文全文をそのまま渡せる。個人利用・学習用途には最適。

### 2.2 API キーの取得方法（ユーザー向け手順）

ツール内に以下のリンクと説明を表示する：

1. [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセス
2. Google アカウントでログイン
3. 「APIキーを作成」をクリック
4. 生成されたキー（`AIza...` で始まる）をコピー
5. PaperQuest の入力欄に貼り付け（ブラウザに保存される）

**注意事項（UI に明記）**：
- API キーはこのブラウザの `localStorage` にのみ保存され、外部サーバーには送信されない
- 無料枠（1日 1,500 リクエスト）を超えると一時的に制限されるが、翌日リセット
- 商用利用・大量利用には Google の利用規約を確認すること

### 2.3 Gemini API 呼び出し仕様

```javascript
const GEMINI_ENDPOINT =
  'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent';

async function callGemini(apiKey, systemPrompt, userContent) {
  const res = await fetch(`${GEMINI_ENDPOINT}?key=${apiKey}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      system_instruction: { parts: [{ text: systemPrompt }] },
      contents: [{ role: 'user', parts: [{ text: userContent }] }],
      generationConfig: {
        temperature: 0.3,       // 安定した出力のため低めに設定
        maxOutputTokens: 4096,
        responseMimeType: 'application/json'  // JSON モード（パースが確実）
      }
    })
  });
  const data = await res.json();
  return JSON.parse(data.candidates[0].content.parts[0].text);
}
```

**`responseMimeType: 'application/json'` の活用**：Gemini はこのオプションで JSON のみを確実に返す。Claude API にはない機能で、パースエラーが大幅に減少する。

---

## 3. システムアーキテクチャ

### 3.1 全体構成

```
┌──────────────────────────────────────────────────────────┐
│                   ブラウザ（ユーザー端末）                   │
│                                                          │
│  ① URL 入力（arXiv PDF URL）                              │
│       ↓                                                  │
│  ② arXiv API でメタデータ取得（タイトル・著者・Abstract）    │
│     ※ CORS 不要の公式エンドポイントを使用                  │
│       ↓                                                  │
│  ③ CORS Proxy 経由で PDF バイナリを取得                   │
│       ↓                                                  │
│  ④ PDF.js（ブラウザ内 WASM）でテキスト抽出                 │
│       ↓                                                  │
│  ⑤ Gemini 1.5 Flash API へ送信（無料・JSON モード）        │
│       ↓                                                  │
│  ⑥ 構造化 JSON を受信                                     │
│       ↓                                                  │
│  ⑦ レンダリングエンジンでカード・図解・クイズを描画           │
│       ↓                                                  │
│  ⑧ ユーザーがインタラクト（スワイプ・クイズ・用語タップ）      │
└──────────────────────────────────────────────────────────┘
         ↕ 外部アクセス
  ・Gemini API（Google）        無料・HTTPS
  ・arXiv API（Cornell）        無料・CORS 対応
  ・corsproxy.io               無料 CORS Proxy
  ・cdnjs.cloudflare.com       PDF.js
  ・fonts.googleapis.com       Google Fonts
```

### 3.2 arXiv データ取得戦略

arXiv の PDF は CORS 制限があるため、2段階で取得する：

```
Step 1: arXiv API でメタデータ取得（CORS 不要）
  URL: https://export.arxiv.org/api/query?id_list={arxiv_id}
  取得内容: タイトル・著者・Abstract・カテゴリ（XML）
  → これだけで Gemini に渡せる情報の 50% をカバー

Step 2: PDF テキスト取得（CORS Proxy 経由）
  URL: https://corsproxy.io/?url=https://arxiv.org/pdf/{arxiv_id}
  取得内容: PDF バイナリ → PDF.js で本文テキスト抽出
  → フルテキストで残り 50% をカバー

フォールバック:
  Step 2 が失敗した場合 → Abstract + arXiv HTML ページのテキスト抽出で代替
  （論文の主要部分は Abstract に凝縮されているため実用的）
```

### 3.3 ファイル構成（GitLab リポジトリ）

```
paperquest/
├── public/                     # GitLab Pages の公開ルート
│   ├── index.html              # エントリポイント（SPA）
│   ├── app.js                  # メインロジック・状態管理
│   ├── engine/
│   │   ├── arxiv.js            # arXiv API クライアント
│   │   ├── pdf-extract.js      # PDF.js ラッパー
│   │   ├── gemini.js           # Gemini API クライアント
│   │   ├── renderer.js         # カード描画エンジン
│   │   ├── diagrams.js         # SVG インタラクティブ図解
│   │   └── audio.js            # Web Audio API エンジン
│   └── styles/
│       └── main.css
├── .gitlab-ci.yml
└── README.md
```

---

## 4. ユーザーフロー

### 4.1 フロー全体像

```
[ランディング画面]
  └─ 初回: Gemini API Key 入力 → localStorage 保存
  └─ 2回目以降: ヒストリーから選ぶか新しい URL を入力
       ↓ arXiv URL 入力 → 「冒険を始める」
[ロード画面]（推定 10〜20 秒）
  ├─ 🔍 メタデータ取得中...
  ├─ 📖 論文を解読中...
  ├─ 🧠 AI が学習体験を構築中...
  └─ ✨ 完了！
       ↓
[論文マップ画面]
  └─ タイトル・分野・難易度・章構成の俯瞰
       ↓ 「冒険スタート」
[カード学習フロー]
  ├─ CH.0 プロローグ（この研究が解く「日常の謎」）
  ├─ CH.1 問題設定
  ├─ CH.2 手法
  ├─ CH.3 インタラクティブ図解
  ├─ CH.4 結果・発見
  ├─ CH.5 世界への意義
  ├─ [BOSS BATTLE] 理解度クイズ 3 問
  └─ [CLEAR] リワード ＋ お土産フレーズ
```

### 4.2 ロード画面の演出（待ち時間を楽しくする）

```
🔍 論文を発見中...        [███░░░░░░░]  効果音: ピンポン
📖 ページを読み込み中...   [██████░░░░]  効果音: 紙をめくる音
🧠 AI が知識を整理中...    [████████░░]  効果音: 電子音アルペジオ
✨ 冒険の準備完了！        [██████████]  効果音: ファンファーレ
```

各ステップにランダムな「トリビア」を表示（例：「arXiv には毎日約 2,000 本の論文が投稿されます」）

---

## 5. コンテンツ生成（Gemini プロンプト設計）

### 5.1 送信データの構成

```
[システムプロンプト]
  ・出力は JSON のみ（responseMimeType で強制）
  ・読者は「その分野を全く知らない日本の高校生」
  ・専門用語は必ず日常の比喩で定義
  ・インタラクティブ図解のパラメータを具体的に設計

[ユーザーコンテンツ]
  ・arXiv メタデータ（タイトル・著者・Abstract・カテゴリ）
  ・本文テキスト（最大 50,000 文字、Gemini の 1M トークン枠に収まる）
```

### 5.2 生成される JSON スキーマ

```json
{
  "meta": {
    "title_ja": "論文タイトル（日本語訳）",
    "title_en": "原題",
    "authors": ["著者1", "著者2"],
    "year": 2022,
    "field": "機械学習",
    "field_emoji": "🤖",
    "one_line": "1行要約（30字以内）",
    "difficulty": 3,
    "estimated_minutes": 8
  },
  "cards": [
    {
      "id": "intro",
      "type": "story",
      "chapter": "プロローグ",
      "title": "カードタイトル",
      "hook": "読み手を引き込む問いかけ",
      "body": "本文（改行は \\n）",
      "highlight": "強調フレーズ",
      "visual_type": "illustration | comparison | timeline | none",
      "visual_description": "図解の内容指示",
      "terms": [
        {
          "word": "専門用語",
          "emoji": "💡",
          "subtitle": "〇〇で例えると",
          "explanation": "比喩を使った説明"
        }
      ],
      "sfx": "section_start | term_unlock | diagram_boot | none"
    },
    {
      "id": "interactive",
      "type": "interactive_diagram",
      "chapter": "CH.3 体験",
      "title": "動かして理解する",
      "diagram": {
        "type": "slider | toggle | comparison",
        "params": [
          {
            "id": "p1",
            "label": "ラベル",
            "unit": "単位",
            "min": 0, "max": 100, "default": 50
          }
        ],
        "outputs": [
          {
            "id": "o1",
            "label": "出力ラベル",
            "formula_js": "p1 * 2",
            "unit": "単位",
            "color": "cyan"
          }
        ],
        "narrative": "{{p1}} のとき {{o1}} になります。"
      }
    }
  ],
  "quiz": [
    {
      "question": "問題文",
      "options": ["A", "B", "C"],
      "correct": 0,
      "feedback_correct": "正解時の解説",
      "feedback_wrong": "不正解時の解説（正答を含む）"
    }
  ],
  "souvenir": "お土産フレーズ（40字以内）",
  "related_questions": ["派生する問い1", "派生する問い2"]
}
```

### 5.3 インタラクティブ図解の自動生成

Gemini が返した `diagram` 定義に基づき、レンダリングエンジンが SVG を動的構築する。

| diagram.type | 典型的な使用例 | 生成内容 |
|--------------|--------------|---------|
| `slider` | 精度 vs 速度のトレードオフ、数式の変数 | スライダー ＋ リアルタイム計算表示 |
| `comparison` | 従来手法 vs 新手法 | 左右 2 カラム比較 |
| `timeline` | 実験の手順、学習の流れ | 横スクロール年表 |
| `toggle` | ON/OFF で結果が変わる要素 | スイッチ ＋ ビフォーアフター |
| `bar_chart` | 実験結果のスコア比較 | アニメーション棒グラフ |

---

## 6. UI/UX 設計

### 6.1 画面レイアウト（カード学習画面）

```
┌─────────────────────────────────┐
│ [🔇] PaperQuest  CH.2  [XP████] │  ← ヘッダー固定（ミュートボタン付き）
├─────────────────────────────────┤
│                                 │
│         カードエリア              │  ← 縦スクロール可・横スワイプで移動
│    （スワイプ / キー操作）         │
│                                 │
├─────────────────────────────────┤
│  [◀ 戻る]   3 / 8   [次へ ▶]   │  ← フッター固定・タップ領域大きめ
└─────────────────────────────────┘
```

### 6.2 デザインシステム

```css
/* カラーパレット */
--bg:       #030310;   /* 深宇宙ネイビー */
--surface:  #0a0d2e;
--cyan:     #00e5ff;   /* メインアクセント */
--gold:     #ffd54f;   /* XP・強調 */
--pink:     #ff79c6;   /* 用語チップ */
--green:    #69ff47;   /* 正解 */
--red:      #ff4444;   /* 不正解 */

/* フォント */
見出し: Orbitron（Google Fonts）
本文:   Noto Sans JP（Google Fonts）
```

### 6.3 モバイル・iPad 対応

| 要件 | 実装方法 |
|------|---------|
| スワイプ操作 | `touchstart` / `touchend` でカード移動 |
| ピンチズーム | 図解エリアに `touch-action: pinch-zoom` |
| 親指操作 | ナビゲーションは画面下部、最低 48×48px タップ領域 |
| PC キーボード | `ArrowLeft` / `ArrowRight` / `Space` キー対応 |
| フォントサイズ | `clamp(14px, 2.5vw, 18px)` で自動調整 |
| 高さ | `100dvh`（スマホのブラウザバー考慮） |

---

## 7. 効果音設計（Web Audio API・ファイルレス）

すべての効果音を Web Audio API でプログラム合成。**外部音声ファイルなし**、**追加ライブラリなし**。

### 7.1 効果音一覧

| # | イベント | 音の性格 | 合成パラメータ（概要） | 演出意図 |
|---|---------|---------|---------------------|---------|
| 1 | PDF 取得完了 | ピンポン♪ | サイン波 523→659Hz | 「発見！」 |
| 2 | AI 処理完了 | 電子ファンファーレ | 矩形波アルペジオ C-E-G | 「準備完了」 |
| 3 | セクション読了 | シャキーン！ | 矩形波 440→880→1100Hz 上昇 | 達成感・次への意欲 |
| 4 | 用語タップ | 柔らかいポーン | サイン波ベル 523→659Hz | 知恵獲得の肯定感 |
| 5 | 図解起動 | ウィーン（上昇） | ノコギリ波 200→800Hz スイープ | インタラクション開始 |
| 6 | スライダー操作中 | チキチキ | 短いクリック（100ms 間引き） | リアリティ・操作感 |
| 7 | クイズ正解 | 明るいチャイム | サイン波 C-E-G 和音 | 「やった！」の喜び |
| 8 | クイズ不正解 | 低いブー | ノコギリ波 200Hz 短め | 驚きだが深刻でない |
| 9 | 全問クリア | ファンファーレ | 矩形波 C-E-G-C' メロディー | 論文攻略の達成感 |
| 10 | 用語ポップアップ閉じる | キラリ | 高速サイン波アルペジオ | 理解の「定着」 |

### 7.2 音響設計の原則

- 初回ユーザー操作後に `AudioContext` を生成（ブラウザ自動再生制限への対応）
- すべての音は **0.5 秒以内**（学習を中断しない）
- スライダー操作音は `throttle(100ms)` で間引き
- ヘッダーに **ミュートトグルボタン** を常設（アクセシビリティ）
- `localStorage` にミュート設定を保存

---

## 8. データ永続化（localStorage）

```javascript
{
  "pq_gemini_key": "AIza...",        // Gemini API Key
  "pq_mute": false,                  // ミュート設定

  "pq_history": [                    // 処理済み論文（最大 10 件）
    {
      "arxiv_id": "2208.04717",
      "title_ja": "論文タイトル",
      "field_emoji": "🤖",
      "processed_at": "2026-02-19T12:00:00Z",
      "content": { /* 生成 JSON 全体 */ }  // キャッシュ（再処理不要）
    }
  ]
}
```

**キャッシュ戦略**：同じ `arxiv_id` が再入力された場合、API を呼ばずキャッシュを使用。Gemini の無料枠を節約しつつ即座に再生できる。

---

## 9. エラーハンドリング

| エラー種別 | 対処方法 |
|-----------|---------|
| arXiv ID の形式不正 | 入力時にリアルタイムバリデーション ＋ ガイド表示 |
| PDF 取得失敗（CORS Proxy 障害） | Abstract のみで処理を継続（品質は下がるが動作する） |
| Gemini API Key 無効 | エラーメッセージ ＋ API Key 再入力フォームへ誘導 |
| Gemini 無料枠上限 | 「本日の制限に達しました。明日また試してください」と表示 |
| JSON 不完全（稀） | Gemini の JSON モードで基本防止。失敗時はリトライ（最大 2 回） |
| タイムアウト（30 秒） | 「処理中です。もう少しお待ちください」＋ キャンセルボタン |

---

## 10. GitLab Pages デプロイ

### 10.1 `.gitlab-ci.yml`

```yaml
pages:
  stage: deploy
  script:
    - mkdir -p public
    - cp -r src/* public/
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

ビルドステップなし（Vanilla JS）。`main` ブランチへの push で自動デプロイ。

### 10.2 外部依存（CDN のみ）

```html
<!-- PDF.js（ブラウザ内 PDF 処理） -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js">

<!-- フォント -->
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900
            &family=Noto+Sans+JP:wght@300;400;700">
```

Gemini API・Web Audio API・Canvas API・fetch API はすべてブラウザネイティブ。**追加 npm パッケージ・バンドラー不要**。

---

## 11. 開発フェーズ

### Phase 1 — コアパイプライン
- [ ] ランディング画面 ＋ URL・API Key 入力フォーム
- [ ] arXiv API でメタデータ取得
- [ ] PDF.js でテキスト抽出
- [ ] Gemini API 呼び出し（JSON モード）＋ パース
- [ ] 基本カード描画エンジン
- [ ] スワイプ・キーボードナビゲーション

### Phase 2 — インタラクティブ要素
- [ ] 用語ポップアップ（下から出現）
- [ ] SVG 図解自動生成（slider / comparison / bar_chart）
- [ ] クイズエンジン（正解・不正解アニメーション）
- [ ] Web Audio API 効果音エンジン（全 10 種）

### Phase 3 — 仕上げ
- [ ] ロード画面の演出（トリビア表示付き）
- [ ] 論文マップ画面
- [ ] localStorage キャッシュ ＋ ヒストリー UI
- [ ] エラーハンドリング全般
- [ ] iPad・スマートフォン実機テスト

---

## 12. 制約と注意事項

### 技術的制約
- arXiv PDF の CORS 制限により、パブリック CORS Proxy（`corsproxy.io`）を使用。Proxy がダウンした場合は Abstract のみで動作するフォールバックを実装する
- PDF.js の数式抽出は不完全になる場合があるが、Gemini の 1M トークン枠により **論文全文をそのまま渡せる**ため、文脈での補完が可能
- Gemini の無料枠は 1 日 1,500 リクエスト。通常の個人利用では上限に達しない

### 倫理・法的注意事項
- arXiv の論文はオープンアクセスだが、著作権は著者に帰属。本ツールは「理解の補助」であることを UI に明記する
- Gemini が生成したコンテンツの正確性は保証されない旨を表示する
- Gemini API Key はブラウザの `localStorage` のみに保存。外部サーバーには一切送信されない

---

## 13. 成功指標

| 指標 | 目標値 |
|------|-------|
| 論文 1 本の処理時間 | 20 秒以内 |
| 生成カード数 | 6〜9 枚 |
| クイズ生成品質 | 3 問すべてが論文内容に基づくこと |
| モバイル操作性 | タップ・スワイプが 100% 応答すること |
| エラー自動回復率 | 主要エラーの 90% を自動リカバリー |
| 無料枠消費 | 1 日 50 論文処理しても無料枠（1,500 req）内に収まること |

---

*PaperQuest v2.1 仕様書 — Gemini 無料枠で、誰もが論文を冒険できる場所へ*
