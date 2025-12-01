// =========================
// 画面に取引情報を表示
// =========================
export function showTransaction(t) {
    document.getElementById("transaction").innerText =
        `取引: ${t.description} / 金額: ${t.amount}€`;
    document.getElementById("amount").value = t.amount;
}

// =========================
// 結果テキストの表示
// =========================
export function showResult(text) {
    document.getElementById("result").innerText = text;
}

// =========================
// 借方・貸方のセレクトボックスへ科目を流し込む
// =========================
export function fillAccountSelect(accounts) {
    const debit = document.getElementById("debit");
    const credit = document.getElementById("credit");

    // 既存クリア
    debit.innerHTML = "";
    credit.innerHTML = "";

    Object.entries(accounts).forEach(([key, jp]) => {
        const option = document.createElement("option");
        option.value = key;
        option.textContent = `${key}（${jp}）`;

        // cloneNode の方が若干高速で安全
        debit.appendChild(option.cloneNode(true));
        credit.appendChild(option.cloneNode(true));
    });
}

// =========================
// 多言語データ
// =========================
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

export let currentLang = "ja";

// =========================
// 言語トグル
// =========================
export function toggleLang() {
    currentLang = currentLang === "ja" ? "en" : "ja";
}

// =========================
// UI のテキスト更新
// =========================
export function updateUI() {
    const t = LANG[currentLang];

    document.querySelector("#game-title").innerText = t.title;

    document.querySelector("#label-debit").innerText = t.debit;
    document.querySelector("#label-credit").innerText = t.credit;
    document.querySelector("#label-amount").innerText = t.amount;

    document.querySelector("#submit").innerText = t.submit;

    document.querySelector("#ledger-title").innerText = t.ledger;
}
