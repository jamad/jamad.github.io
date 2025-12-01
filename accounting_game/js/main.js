import * as ui from "./ui.js";
import * as game from "./game.js";

/* DOM shortcuts */
const el = id => document.getElementById(id);

/* initialize everything */
async function init() {
    // load accounts and ui text
    const [accounts, uiJson] = await Promise.all([
        game.loadAccounts(),
        game.loadUIJson()
    ]);
    ui.setUIText(uiJson);

    // populate level selector by scanning data/levels (simple fixed list for demo)
    // For production you could fetch an index; here we provide 3 levels
    const levelSelect = el("level-select");
    [1, 2, 3].forEach(n => {
        const opt = document.createElement("option");
        opt.value = n; opt.textContent = `Level ${n}`;
        levelSelect.appendChild(opt);
    });

    // load initial level
    await loadAndStartLevel(1);

    // set event listeners
    el("submit").addEventListener("click", () => {
        const d = el("debit").value;
        const c = el("credit").value;
        const amount = Number(el("amount").value);
        const res = game.answerCurrent(d, c, amount);

        if (res.correct) {
            ui.showResultMessage("correct");
            ui.addLedgerEntry(d, "debit", res.correctAns.description, res.correctAns.amount);
            ui.addLedgerEntry(c, "credit", res.correctAns.description, res.correctAns.amount);
        } else {
            el("result").innerText = `${ui.t("incorrect")} — ${res.correctAns.debit} / ${res.correctAns.credit} / ${res.correctAns.amount}€`;
        }
        el("score").innerText = game.score;
        el("progress").innerText = `${game.index} / ${game.problems.length}`;

        if (res.finished) {
            el("result").innerText += ` ${ui.t("finished")}`;
            el("submit").disabled = true;
        } else {
            const next = game.currentProblem();
            ui.showTransaction(next);
        }
    });

    el("skip").addEventListener("click", () => {
        const sres = game.skipCurrent();
        el("progress").innerText = `${game.index} / ${game.problems.length}`;
        if (sres.finished) {
            el("result").innerText = ui.t("finished");
            el("submit").disabled = true;
        } else {
            ui.showTransaction(game.currentProblem());
        }
    });

    el("lang-switch").addEventListener("change", (ev) => {
        // 1. 言語設定を更新 (Setter関数を使用)
        // これが一番重要です
        ui.setCurrentLang(ev.target.checked ? "en" : "ja");

        // 2. UIの静的テキスト（ラベルなど）を更新
        // updateStaticUI が関数として存在しているか確認してから実行します
        if (typeof ui.updateStaticUI === "function") {
            ui.updateStaticUI(accounts);
        }

        // 3. 現在表示中のトランザクション（問題文）を更新
        if (game && typeof game.currentProblem === "function") {
            ui.showTransaction(game.currentProblem());
        }
    });

    levelSelect.addEventListener("change", async (e) => {
        const level = Number(e.target.value);
        await loadAndStartLevel(level);
    });
}

/* load a level and prepare UI */
async function loadAndStartLevel(level) {
    // load level file
    const meta = await game.loadLevel(level);
    // prepare UI
    // すでに値があればそのまま、なければ関数を使って "ja" をセットする
    if (!ui.currentLang) {
        ui.setCurrentLang("ja");
    }
    ui.fillAccountSelect(game.accounts);
    ui.renderLedgers(game.accounts);
    ui.updateStaticUI?.(game.accounts);
    // show first problem
    ui.showTransaction(game.currentProblem());
    el("progress").innerText = `${game.index} / ${game.problems.length}`;
    el("score").innerText = game.score;
    // enable submit if disabled
    el("submit").disabled = false;
    // instruction from level meta (if exists)
    if (meta.title && meta.title[ui.currentLang]) {
        el("instruction").innerText = meta.title[ui.currentLang];
    } else {
        el("instruction").innerText = "";
    }
}

window.addEventListener("DOMContentLoaded", init);
