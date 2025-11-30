export async function loadTransactions(level = 1) {
    const res = await fetch(`../data/level${level}.json`);
    return await res.json();
}
