export let currentLang = "ja";  // デフォルト日本語

export const LANG = {
    ja: {
        title: "仕訳トレーニング（T字勘定）",
        debit: "借方（Debit）",
        credit: "貸方（Credit）",
        amount: "金額（Amount）",
        submit: "送信",
        ledger: "T字勘定"
    },
    en: {
        title: "Journal Training (T-Accounts)",
        debit: "Debit",
        credit: "Credit",
        amount: "Amount",
        submit: "Submit",
        ledger: "T-Accounts"
    }
};


/* 取引を表示 */
export function showTransaction(t) {
    document.getElementById("transaction").innerText =
        `${t.description[currentLang]} / ${t.amount}€`;
    document.getElementById("amount").value = t.amount;
}

/* 結果表示 */
export function showResult(text) {
    document.getElementById("result").innerText = text;
}

/* プルダウン更新 */
export function fillAccountSelect(accounts) {
    const debit = document.getElementById("debit");
    const credit = document.getElementById("credit");

    debit.innerHTML = "";
    credit.innerHTML = "";

    Object.keys(accounts).forEach(key => {
        const opt = document.createElement("option");
        opt.value = key;
        opt.textContent = accounts[key][currentLang];

        debit.appendChild(opt.cloneNode(true));
        credit.appendChild(opt.cloneNode(true));
    });
}

/* T字勘定のテンプレート描画 */
export function renderLedger(accounts) {
    const area = document.getElementById("ledger-area");
    area.innerHTML = "";

    Object.keys(accounts).forEach(key => {
        const row = document.createElement("div");
        row.className = "account-row";

        row.innerHTML = `
            <div class="account-title">${accounts[key][currentLang]}</div>
            <div class="account-label">Debit</div>
            <div class="account-label">Credit</div>
        `;

        area.appendChild(row);
    });
}

/* 言語切替 */
export function toggleLang() {
    currentLang = currentLang === "ja" ? "en" : "ja";
}

/* UI 全体更新 */
export function updateUI(accounts) {
    const t = LANG[currentLang];

    document.getElementById("game-title").innerText = t.title;
    document.getElementById("label-debit").innerText = t.debit;
    document.getElementById("label-credit").innerText = t.credit;
    document.getElementById("label-amount").innerText = t.amount;
    document.getElementById("submit").innerText = t.submit;
    document.getElementById("ledger-title").innerText = t.ledger;

    fillAccountSelect(accounts);
    renderLedger(accounts);
}
