import {
    showTransaction,
    showResult,
    fillAccountSelect,
    renderLedger,
    updateUI,
    toggleLang,
    currentLang
} from "./ui.js";

let accounts = {};
let transactions = [];
let current = 0;
let score = 0;

/* JSON 読み込み */
async function loadAccounts() {
    const res = await fetch("./data/accounts.json");
    accounts = await res.json();
}

async function loadTransactions() {
    const res = await fetch("./data/transactions.json");
    transactions = await res.json();
}

/* 初期化 */
async function init() {
    await loadAccounts();
    await loadTransactions();

    fillAccountSelect(accounts);
    renderLedger(accounts);
    updateUI(accounts);
    showTransaction(transactions[current]);
}

/* 仕訳チェック＆進行 */
document.getElementById("submit").addEventListener("click", () => {
    const d = document.getElementById("debit").value;
    const c = document.getElementById("credit").value;
    const amount = Number(document.getElementById("amount").value);

    const t = transactions[current];

    if (d === t.debit && c === t.credit && amount === t.amount) {
        showResult("⭕ 正解！");
        score++;
    } else {
        showResult(`❌ 間違い！ 正解は ${t.debit} / ${t.credit} / ${t.amount}€`);
    }

    current++;
    document.getElementById("score").innerText = score;

    if (current >= transactions.length) {
        showResult("🎉 全て終了！");
        document.getElementById("submit").disabled = true;
        return;
    }

    showTransaction(transactions[current]);
});

/* 言語切替 */
document.getElementById("lang-switch").addEventListener("change", () => {
    toggleLang();
    updateUI(accounts);
    showTransaction(transactions[current]);
});

/* 実行 */
init();
