import * as ui from "./ui.js";
import * as game from "./game.js";

/* DOM要素取得ヘルパー */
const el = id => document.getElementById(id);

/* 現在のレベル情報を保持（言語切り替え時のタイトル再描画用） */
let currentLevelMeta = null;

/**
 * 初期化処理
 */
async function init() {
    try {
        // アカウント情報とUI用テキストを並行してロード
        const [accounts, uiJson] = await Promise.all([
            game.loadAccounts(),
            game.loadUIJson()
        ]);

        // UIテキスト辞書をセット
        ui.setUIText(uiJson);

        // レベル選択プルダウンの生成 (デモ用: 1〜3)
        const levelSelect = el("level-select");
        [1, 2, 3].forEach(n => {
            const opt = document.createElement("option");
            opt.value = n;
            opt.textContent = `Level ${n}`;
            levelSelect.appendChild(opt);
        });

        // 初期言語設定（未設定なら "ja"）
        if (!ui.currentLang) {
            ui.setCurrentLang("ja");
        }

        // イベントリスナーの設定
        setupEventListeners(accounts);

        // 初期レベル(1)を開始
        await loadAndStartLevel(1);

    } catch (err) {
        console.error("Init failed:", err);
    }
}

/**
 * イベントリスナーをまとめて設定
 */
function setupEventListeners(accounts) {

    // --- 回答送信ボタン ---
    el("submit").addEventListener("click", () => {
        const d = el("debit").value;
        const c = el("credit").value;
        const amount = Number(el("amount").value);

        // ゲームロジックで判定
        const res = game.answerCurrent(d, c, amount);

        if (res.correct) {
            // 正解時の処理
            ui.showResultMessage("correct");
            // 帳簿(Ledger)に行を追加
            ui.addLedgerEntry(d, "debit", res.correctAns.description, res.correctAns.amount);
            ui.addLedgerEntry(c, "credit", res.correctAns.description, res.correctAns.amount);
        } else {
            // 不正解時の処理
            const msg = `${ui.t("incorrect")} — ${res.correctAns.debit} / ${res.correctAns.credit} / ${res.correctAns.amount}€`;
            el("result").innerText = msg;
        }

        // 共通のUI更新（スコア・進行度）
        updateStatusDisplay(res.finished);

        // 次の問題へ、または終了処理
        if (!res.finished) {
            ui.showTransaction(game.currentProblem());
        }
    });

    // --- スキップボタン ---
    el("skip").addEventListener("click", () => {
        const res = game.skipCurrent();
        updateStatusDisplay(res.finished);

        if (!res.finished) {
            ui.showTransaction(game.currentProblem());
        }
    });

    // --- 言語切り替えスイッチ ---
    el("lang-switch").addEventListener("change", (ev) => {
        const newLang = ev.target.checked ? "en" : "ja";

        // 1. 言語設定を更新 (Setter関数経由)
        ui.setCurrentLang(newLang);

        // 2. 固定UI（勘定科目名など）を更新
        if (typeof ui.updateStaticUI === "function") {
            ui.updateStaticUI(accounts);
        }

        // 3. 現在の問題文を更新
        if (game.currentProblem) {
            ui.showTransaction(game.currentProblem());
        }

        // 4. レベルのタイトル(Instruction)を更新
        updateLevelTitle();

        // 5. 結果メッセージが表示中なら翻訳しなおす（オプション）
        // el("result").innerText = ... 必要に応じて実装
    });

    // --- レベル選択 ---
    el("level-select").addEventListener("change", async (e) => {
        const level = Number(e.target.value);
        await loadAndStartLevel(level);
    });
}

/**
 * レベルをロードしてUIをリセットする
 */
async function loadAndStartLevel(level) {
    // ゲームデータをロードし、メタデータを保持
    currentLevelMeta = await game.loadLevel(level);

    // UIリセット
    ui.fillAccountSelect(game.accounts);
    ui.renderLedgers(game.accounts);

    // 固定UIの更新
    if (typeof ui.updateStaticUI === "function") {
        ui.updateStaticUI(game.accounts);
    }

    // 最初の問題を表示
    ui.showTransaction(game.currentProblem());

    // スコア・進行度・ボタン状態のリセット
    el("submit").disabled = false;
    el("result").innerText = ""; // 結果メッセージクリア
    updateStatusDisplay(false);
    updateLevelTitle();
}

/**
 * スコアと進行状況の表示を更新する共通関数
 */
function updateStatusDisplay(isFinished) {
    el("score").innerText = game.score;
    el("progress").innerText = `${game.index} / ${game.problems.length}`;

    if (isFinished) {
        el("result").innerText += ` ${ui.t("finished")}`;
        el("submit").disabled = true;
    }
}

/**
 * レベルのタイトル（Instruction）を現在の言語で表示
 */
function updateLevelTitle() {
    const instrEl = el("instruction");
    // currentLevelMeta があり、かつ現在の言語用のタイトルがある場合
    if (currentLevelMeta && currentLevelMeta.title && currentLevelMeta.title[ui.currentLang]) {
        instrEl.innerText = currentLevelMeta.title[ui.currentLang];
    } else {
        instrEl.innerText = "";
    }
}

// 起動
window.addEventListener("DOMContentLoaded", init);