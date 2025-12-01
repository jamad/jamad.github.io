// game.js - level management and problem flow
export let accounts = {};
export let currentLevel = 1;
export let levelMeta = null;
export let problems = [];
export let index = 0;
export let score = 0;

export async function loadAccounts() {
    const res = await fetch("./data/accounts.json");
    accounts = await res.json();
    return accounts;
}

export async function loadUIJson() {
    const res = await fetch("./data/ui.json");
    return await res.json();
}

export async function loadLevel(level) {
    const res = await fetch(`./data/levels/level${level}.json`);
    levelMeta = await res.json();
    problems = levelMeta.problems || [];
    index = 0;
    score = 0;
    currentLevel = level;
    return levelMeta;
}

export function currentProblem() {
    return problems[index];
}

export function answerCurrent(debit, credit, amount) {
    const t = currentProblem();
    if (!t) return false;
    const correct = (debit === t.debit && credit === t.credit && Number(amount) === Number(t.amount));
    if (correct) score++;
    index++;
    return { correct, nextIndex: index, finished: index >= problems.length, correctAns: t };
}

export function skipCurrent() {
    index++;
    return { finished: index >= problems.length, nextIndex: index };
}
