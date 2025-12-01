import { loadTransactions } from "./transactions.js";
import { createLedger, addLedgerEntry } from "./ledger.js";
import { showTransaction, showResult, fillAccountSelect } from "./ui.js";

// 全体変数
let transactions = [];
let current = 0;
let score = 0;
let accounts = {}; // 勘定科目

// 勘定科目 JSON を読み込む
async function loadAccounts() {
    const res = await fetch("./data/accounts.json");
    accounts = await res.json();
}

async function init(level = 1) {
    await loadAccounts();                // 勘定科目ロード
    createLedger(accounts);              // T字勘定作成
    fillAccountSelect(accounts);         // プルダウン作成
    transactions = await loadTransactions(level); // 取引ロード

    current = 0;
    score = 0;

    showTransaction(transactions[current]);
}

import { toggleLang, updateUI } from "./ui.js";

document.getElementById("toggle-lang").addEventListener("click", () => {
    toggleLang();
    updateUI();      // 表示全体を再描画
});


// 送信ボタン処理
document.getElementById("submit").addEventListener("click", () => {
    const t = transactions[current];

    const debit = document.getElementById("debit").value;
    const credit = document.getElementById("credit").value;
    const amount = Number(document.getElementById("amount").value);

    if (debit === t.debit && credit === t.credit && amount === t.amount) {
        showResult("🎉 正解！");
        addLedgerEntry(debit, "debit", t.description, t.amount);
        addLedgerEntry(credit, "credit", t.description, t.amount);
        score++;
    } else {
        showResult(`❌ 不正解！ 正解は ${t.debit} / ${t.credit} / ${t.amount}€`);
    }

    current++;

    if (current >= transactions.length) {
        showResult("✨ 全ての問題が終了しました！");
        return;
    }

    showTransaction(transactions[current]);
});

// レベル1で開始
init(1);
