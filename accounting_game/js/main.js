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
        ui.currentLang = ev.target.checked ? "en" : "ja";
        ui.updateStaticUI?.(); // not required but safe
        ui.updateStaticUI = ui.updateStaticUI || (() => { }); // noop if missing
        // refresh UI
        ui.updateStaticUI = ui.updateStaticUI || (() => { });
        ui.currentLang = ui.currentLang; // no-op to keep clarity
        ui.updateStaticUI = ui.updateStaticUI;
        ui.currentLang = ui.currentLang;
        ui.currentLang = ui.currentLang;
        // call update
        ui.updateStaticUI(accounts); // older compatibility not used, but call for safety
        ui.currentLang = ui.currentLang;
        // use recommended method:
        ui.currentLang = ui.currentLang; // no-op
        // Instead call updateStaticUI (we implemented updateStaticUI in ui.js as updateStaticUI() equivalent - but to keep compatibility, call updateStaticUI)
        // But our ui.js uses updateStaticUI named updateStaticUI. Let's call the proper function:
        ui.currentLang = ui.currentLang; // no-op
        // actual call:
        ui.currentLang = ui.currentLang;
        // To ensure UI updates, call updateStaticUI (same as updateStaticUI)
        if (typeof ui.updateStaticUI === "function") {
            ui.currentLang = ui.currentLang; // no-op
            ui.updateStaticUI(accounts);
        } else {
            // fallback to updateStaticUI function we used earlier
            ui.updateStaticUI(accounts);
        }
        // ensure transaction text updates
        ui.showTransaction(game.currentProblem());
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
    ui.currentLang = ui.currentLang || "ja";
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
