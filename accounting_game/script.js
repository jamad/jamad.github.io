// サンプル取引リスト
const transactions = [
    { description: "商品売上", debit: "Cash", credit: "Sales", amount: 1000 },
    { description: "家賃支払い", debit: "Rent Expense", credit: "Cash", amount: 500 },
    { description: "商品仕入れ", debit: "Inventory", credit: "Accounts Payable", amount: 800 }
];

let current = 0;
let score = 0;

function showTransaction() {
    const t = transactions[current];
    document.getElementById("transaction").innerText = `取引: ${t.description}, 金額: ${t.amount} €`;
    document.getElementById("amount").value = t.amount;
    document.getElementById("result").innerText = "";
}

document.getElementById("submit").addEventListener("click", () => {
    const debit = document.getElementById("debit").value;
    const credit = document.getElementById("credit").value;
    const amount = parseInt(document.getElementById("amount").value);

    const t = transactions[current];

    if (debit === t.debit && credit === t.credit && amount === t.amount) {
        document.getElementById("result").innerText = "✅ 正解！";
        score += 1;
    } else {
        document.getElementById("result").innerText = `❌ 間違い！正解は ${t.debit} / ${t.credit} ${t.amount} €`;
    }

    current = (current + 1) % transactions.length;
    document.getElementById("score").innerText = score;
    showTransaction();
});

// 最初の取引表示
showTransaction();
