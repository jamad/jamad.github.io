// ui.js - UI helpers and i18n rendering
export let currentLang = "ja"; // default

export let uiText = {}; // loaded from data/ui.json

export function setUIText(json) { uiText = json; }

/* simple getter */
export function t(key) {
    if (!uiText || !uiText[key]) return key;
    return uiText[key][currentLang] ?? uiText[key].en ?? key;
}

/* show current transaction */
export function showTransaction(tobj) {
    const descr = tobj.description[currentLang] ?? tobj.description.en ?? "";
    document.getElementById("transaction").innerText = `${descr} — ${tobj.amount}€`;
    if (!document.getElementById("amount").readOnly) document.getElementById("amount").value = tobj.amount;
}

/* show result message (use keys from ui.json) */
export function showResultMessage(key) {
    document.getElementById("result").innerText = t(key);
}

/* fill account selects (accounts: { id: {ja,en} }) */
export function fillAccountSelect(accounts) {
    const debit = document.getElementById("debit");
    const credit = document.getElementById("credit");
    debit.innerHTML = ""; credit.innerHTML = "";

    Object.keys(accounts).forEach(id => {
        const label = accounts[id][currentLang] ?? accounts[id].en ?? id;
        const opt = document.createElement("option");
        opt.value = id;
        opt.textContent = label;
        debit.appendChild(opt.cloneNode(true));
        credit.appendChild(opt.cloneNode(true));
    });
}

/* render ledgers area */
export function renderLedgers(accounts) {
    const area = document.getElementById("ledger-area");
    area.innerHTML = "";

    Object.keys(accounts).forEach(id => {
        const box = document.createElement("div");
        box.className = "ledger-box";
        box.innerHTML = `<h3>${accounts[id][currentLang] ?? accounts[id].en ?? id}</h3>
      <div class="ledger">
        <div class="col"><h4>${t("debit")}</h4><ul id="${id}-debit-list"></ul></div>
        <div class="col"><h4>${t("credit")}</h4><ul id="${id}-credit-list"></ul></div>
      </div>`;
        area.appendChild(box);
    });
}

/* add one ledger entry (account id, side: 'debit'|'credit', desc, amount) */
export function addLedgerEntry(accountId, side, description, amount) {
    const ul = document.getElementById(`${accountId}-${side}-list`);
    if (!ul) return;
    const li = document.createElement("li");
    const descText = typeof description === "string" ? description : (description[currentLang] ?? description.en ?? "");
    li.textContent = `${amount} (${descText})`;
    ul.appendChild(li);
}

/* update textual UI */
export function updateStaticUI(accounts) {
    document.getElementById("game-title").innerText = t("trainingTitle");
    document.getElementById("label-debit").firstChild.textContent = t("debit") + " ";
    document.getElementById("label-credit").firstChild.textContent = t("credit") + " ";
    document.getElementById("label-amount").firstChild.textContent = t("amount") + " ";
    document.getElementById("submit").innerText = t("submit");
    document.getElementById("lang-label").innerText = currentLang === "ja" ? "日本語" : "English";
    // selectors and ledger titles must be refreshed too
    fillAccountSelect(accounts);
    renderLedgers(accounts);
}
