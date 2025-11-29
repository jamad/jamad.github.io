const transactions = [
    { description: "商品売上 / Sales", debit: "Cash", credit: "Sales", amount: 1000 },
    { description: "家賃支払い / Rent", debit: "RentExpense", credit: "Cash", amount: 500 },
    { description: "商品仕入れ / Inventory Purchase", debit: "Inventory", credit: "AccountsPayable", amount: 800 }
];


let current = 0;
let score = 0;

function showTransaction() {
    const t = transactions[current];
    document.getElementById("transaction").innerText =
        `取引: ${t.description}, 金額: ${t.amount} €`;
    document.getElementById("amount").value = t.amount;
}
function addLedgerEntry(account, side, description, amount) {
    const safeAccount = account.replace(/\s|\//g, ''); // id と一致させる
    const listId = `${safeAccount}-${side}-list`;
    const ul = document.getElementById(listId);
    if (!ul) {
        console.warn(`Ledger list not found: ${listId}`);
        return;
    }
    const li = document.createElement("li");
    li.textContent = `${amount} (${description})`;
    ul.appendChild(li);
}


document.getElementById("submit").addEventListener("click", () => {
    const debit = document.getElementById("debit").value;
    const credit = document.getElementById("credit").value;
    const amount = parseInt(document.getElementById("amount").value);
    const t = transactions[current];

    if (debit === t.debit && credit === t.credit && amount === t.amount) {
        document.getElementById("result").innerText =
            `✅ 正解！ (${t.debit} / ${t.credit} / ${t.amount} €)`;
        score += 1;

        // T字勘定に反映
        addLedgerEntry(debit, "debit", t.description, amount);
        addLedgerEntry(credit, "credit", t.description, amount);

    } else {
        document.getElementById("result").innerText =
            `❌ 間違い！正解は ${t.debit} / ${t.credit} / ${t.amount} €`;
    }

    current++;
    if (current >= transactions.length) {
        document.getElementById("result").innerText += " 🎉 全ての問題が終了しました！";
        document.getElementById("submit").disabled = true;  // 送信ボタン無効化
        return;
    }


    document.getElementById("score").innerText = score;
    showTransaction();
});

// 最初の取引表示
showTransaction();
