export function createLedger(accounts) {
    const ledger = document.getElementById("ledger");
    ledger.innerHTML = "";

    Object.keys(accounts).forEach(key => {
        const jp = accounts[key];

        const div = document.createElement("div");
        div.className = "account-box";

        div.innerHTML = `
            <div class="account-title">${key}（${jp}）</div>
            <div class="ledger-table">
                <div class="ledger-side">
                    <div>Debit</div>
                    <ul id="${key}-debit-list"></ul>
                </div>
                <div class="ledger-side">
                    <div>Credit</div>
                    <ul id="${key}-credit-list"></ul>
                </div>
            </div>
        `;

        ledger.appendChild(div);
    });
}


export function addLedgerEntry(account, side, description, amount) {
    const id = `${account}-${side}-list`;
    const ul = document.getElementById(id);
    if (!ul) return;

    const li = document.createElement("li");
    li.textContent = `${amount} (${description})`;
    ul.appendChild(li);
}
