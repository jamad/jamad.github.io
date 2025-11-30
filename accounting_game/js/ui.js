export function showTransaction(t) {
    document.getElementById("transaction").innerText =
        `取引: ${t.description} / 金額: ${t.amount}€`;
    document.getElementById("amount").value = t.amount;
}

export function showResult(text) {
    document.getElementById("result").innerText = text;
}

export function fillAccountSelect(accounts) {
    const debit = document.getElementById("debit");
    const credit = document.getElementById("credit");

    debit.innerHTML = "";
    credit.innerHTML = "";

    Object.keys(accounts).forEach(key => {
        const jp = accounts[key];
        const option = document.createElement("option");
        option.value = key;
        option.textContent = `${key}（${jp}）`;

        debit.appendChild(option.cloneNode(true));
        credit.appendChild(option.cloneNode(true));
    });
}
