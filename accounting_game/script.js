/* Ledger Hero - script.js
   - Level 0: Tutorial (fields locked -> press Submit and always correct)
   - Level 1..: gradually add accounts and transactions
   - Ledgers (T-accounts) are auto-generated from accounts list
*/

/* ========== CONFIG: accounts and transactions per level ========== */

/* accountsByLevel: keys = level number (int),
   value = array of { id: "Cash", label: "Cash / 現金" } */
const accountsByLevel = {
    0: [
        { id: "Cash", label: "Cash / 現金" },
        { id: "Sales", label: "Sales / 売上" }
    ],
    1: [
        { id: "Cash", label: "Cash / 現金" },
        { id: "Sales", label: "Sales / 売上" },
        { id: "RentExpense", label: "Rent Expense / 家賃" },
        { id: "Inventory", label: "Inventory / 商品在庫" },
        { id: "AccountsPayable", label: "Accounts Payable / 買掛金" }
    ],
    2: [
        // level2 adds a utilities expense and accounts receivable
        { id: "Cash", label: "Cash / 現金" },
        { id: "Sales", label: "Sales / 売上" },
        { id: "RentExpense", label: "Rent Expense / 家賃" },
        { id: "Inventory", label: "Inventory / 商品在庫" },
        { id: "AccountsPayable", label: "Accounts Payable / 買掛金" },
        { id: "UtilitiesExpense", label: "Utilities Expense / 光熱費" },
        { id: "AccountsReceivable", label: "Accounts Receivable / 売掛金" }
    ]
};

/* transactionsByLevel: array per level.  
   Each transaction: { description, debit, credit, amount } 
   Use account ids (matching the accountsByLevel ids)
*/
const transactionsByLevel = {
    0: [
        { description: "商品売上 / Sales", debit: "Cash", credit: "Sales", amount: 1000 }
    ],
    1: [
        { description: "商品売上 / Sales", debit: "Cash", credit: "Sales", amount: 1000 },
        { description: "家賃支払い / Rent", debit: "RentExpense", credit: "Cash", amount: 500 },
        { description: "商品仕入れ（掛け） / Inventory Purchase (on account)", debit: "Inventory", credit: "AccountsPayable", amount: 800 }
    ],
    2: [
        { description: "商品売上（掛け） / Sales on account", debit: "AccountsReceivable", credit: "Sales", amount: 1200 },
        { description: "支払い：光熱費 / Pay utilities", debit: "UtilitiesExpense", credit: "Cash", amount: 200 },
        { description: "仕入れ支払い（掛け清算） / Pay AP", debit: "AccountsPayable", credit: "Cash", amount: 800 }
    ]
};

/* ========== STATE ========== */
let currentLevel = 0;
let accounts = [];        // array of current account objects
let transactions = [];    // current transaction list
let currentIndex = 0;     // index into transactions
let score = 0;

/* ========== DOM helpers ========== */
const el = id => document.getElementById(id);

/* ========== Initialization ========== */
function initLevel(level) {
    currentLevel = level;
    accounts = (accountsByLevel[level] || []).slice();
    transactions = (transactionsByLevel[level] || []).slice();
    currentIndex = 0;
    score = 0;

    el("level").innerText = level;
    el("level-name").innerText = level === 0 ? "Tutorial" : `Level ${level}`;
    el("score").innerText = score;
    el("progress").innerText = `${currentIndex} / ${transactions.length}`;
    el("result").innerText = "";

    // build ledgers area
    buildLedgers();
    // populate select options
    populateSelectors();

    // set tutorial UI state
    if (level === 0) {
        el("instruction").innerText = "Level 0: Tutorial — fields are locked. Press Submit to see how it works.";
        disableFields(true);
    } else {
        el("instruction").innerText = `Level ${level}: Solve the ${transactions.length} problems.`;
        disableFields(false);
    }

    // show first transaction
    showTransaction();
    // ensure submit enabled
    el("submit").disabled = false;
}

/* buildLedger: create ledger blocks for each account */
function buildLedgers() {
    const container = el("ledgers-container");
    container.innerHTML = ""; // clear
    accounts.forEach(acc => {
        const wrapper = document.createElement("div");
        wrapper.className = "ledger-wrapper";
        wrapper.id = `${acc.id}-ledger-wrapper`;

        const title = document.createElement("h3");
        title.innerText = acc.label;
        wrapper.appendChild(title);

        const ledger = document.createElement("div");
        ledger.className = "ledger";
        ledger.id = `${acc.id}-ledger`;

        // Debit column
        const colD = document.createElement("div");
        colD.className = "col debit-col";
        const hd = document.createElement("h4");
        hd.innerText = "Debit / 借方";
        const ulD = document.createElement("ul");
        ulD.id = `${acc.id}-debit-list`;
        colD.appendChild(hd); colD.appendChild(ulD);

        // Credit column
        const colC = document.createElement("div");
        colC.className = "col credit-col";
        const hc = document.createElement("h4");
        hc.innerText = "Credit / 貸方";
        const ulC = document.createElement("ul");
        ulC.id = `${acc.id}-credit-list`;
        colC.appendChild(hc); colC.appendChild(ulC);

        ledger.appendChild(colD);
        ledger.appendChild(colC);
        wrapper.appendChild(ledger);
        container.appendChild(wrapper);
    });
}

/* populate the debit/credit selectors with current accounts */
function populateSelectors() {
    const debitSel = el("debit");
    const creditSel = el("credit");
    debitSel.innerHTML = "";
    creditSel.innerHTML = "";
    accounts.forEach(acc => {
        const optD = document.createElement("option");
        optD.value = acc.id;
        optD.innerText = acc.label;
        debitSel.appendChild(optD);

        const optC = document.createElement("option");
        optC.value = acc.id;
        optC.innerText = acc.label;
        creditSel.appendChild(optC);
    });
}

/* disable or enable fields (used by tutorial) */
function disableFields(flag) {
    el("debit").disabled = flag;
    el("credit").disabled = flag;
    el("amount").readOnly = flag;
    if (flag) {
        // set tutorial defaults: matching correct answer
        const t = transactions[0];
        if (t) {
            el("debit").value = t.debit;
            el("credit").value = t.credit;
            el("amount").value = t.amount;
        }
    }
}

/* show current transaction text */
function showTransaction() {
    const t = transactions[currentIndex];
    if (!t) {
        el("transaction").innerText = "No transaction.";
        return;
    }
    el("transaction").innerText = `取引: ${t.description}, 金額: ${t.amount} €`;
    // if not tutorial, pre-fill amount
    if (!el("amount").readOnly) el("amount").value = t.amount;
    el("progress").innerText = `${currentIndex} / ${transactions.length}`;
}

/* add entry to ledger (safe) */
function addLedgerEntry(accountId, side, description, amount) {
    const listId = `${accountId}-${side}-list`;
    const ul = el(listId);
    if (!ul) {
        console.warn("Missing ledger ul:", listId);
        return;
    }
    const li = document.createElement("li");
    li.textContent = `${amount} (${description})`;
    ul.appendChild(li);
}

/* handle submit */
el("submit").addEventListener("click", () => {
    const debit = el("debit").value;
    const credit = el("credit").value;
    const amount = parseInt(el("amount").value, 10) || 0;
    const t = transactions[currentIndex];

    // tutorial: always correct for level 0
    const correct = currentLevel === 0
        ? true
        : (debit === t.debit && credit === t.credit && amount === t.amount);

    if (correct) {
        el("result").innerText = `✅ 正解！ (${t.debit} / ${t.credit} / ${t.amount} €)`;
        score += 1;
        addLedgerEntry(t.debit, "debit", t.description, t.amount);
        addLedgerEntry(t.credit, "credit", t.description, t.amount);
    } else {
        el("result").innerText = `❌ 間違い！正解は ${t.debit} / ${t.credit} / ${t.amount} €`;
    }

    // advance
    currentIndex++;
    // update score/progress
    el("score").innerText = score;
    el("progress").innerText = `${currentIndex} / ${transactions.length}`;

    // if finished
    if (currentIndex >= transactions.length) {
        el("result").innerText += " 🎉 全ての問題が終了しました！";
        el("submit").disabled = true;
        return;
    }

    // show next
    showTransaction();
});

/* next level button */
el("next-level").addEventListener("click", () => {
    // simple level progression: 0 -> 1 -> 2
    if (currentLevel < 2) {
        initLevel(currentLevel + 1);
    } else {
        alert("No higher level in this demo. You are at the highest level.");
    }
});

/* initialize demo */
initLevel(0);
