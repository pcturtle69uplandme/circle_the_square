#!/usr/bin/env node
// Tracks Higgsfield credit usage by polling `higgsfield account transactions`.
// Two modes:
//   node usage-tracker.js watch [intervalSeconds=15]   -- live counter, prints each new spend as it happens
//   node usage-tracker.js report                        -- one-shot summary of everything logged so far

const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const STATE_FILE = path.join(__dirname, ".usage-state.json");
const LOG_FILE = path.join(__dirname, "usage-log.jsonl");

function hf(args) {
  // .cmd shims on Windows can't be exec'd directly without `shell: true` (which
  // triggers a Node deprecation warning for unescaped args). Routing through
  // cmd.exe /c explicitly avoids both: no shell option needed, and each arg is
  // still passed as its own array element instead of being string-concatenated.
  const fullArgs = process.platform === "win32"
    ? ["/c", "higgsfield.cmd", ...args, "--json"]
    : [...args, "--json"];
  const bin = process.platform === "win32" ? "cmd.exe" : "higgsfield";
  const out = execFileSync(bin, fullArgs, { encoding: "utf8" });
  return JSON.parse(out);
}

function loadState() {
  if (!fs.existsSync(STATE_FILE)) return { lastSeen: null };
  return JSON.parse(fs.readFileSync(STATE_FILE, "utf8"));
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function appendLog(tx) {
  fs.appendFileSync(LOG_FILE, JSON.stringify(tx) + "\n");
}

function loadLog() {
  if (!fs.existsSync(LOG_FILE)) return [];
  return fs
    .readFileSync(LOG_FILE, "utf8")
    .split("\n")
    .filter(Boolean)
    .map((l) => JSON.parse(l));
}

function fetchNewTransactions(lastSeen) {
  const res = hf(["account", "transactions", "--size", "100"]);
  const items = res.items || [];
  // API returns newest first; keep only ones after lastSeen, oldest first for readable output
  const fresh = items.filter((t) => !lastSeen || new Date(t.created_at) > new Date(lastSeen));
  fresh.reverse();
  return fresh;
}

function fmtCredits(n) {
  const sign = n > 0 ? "+" : "";
  return `${sign}${n}`;
}

function printTx(t, runningSpent, balance) {
  const time = new Date(t.created_at).toLocaleTimeString();
  const label = t.action === "spend" ? t.display_name : `${t.display_name} (${t.action})`;
  console.log(
    `[${time}] ${label.padEnd(28)} ${fmtCredits(t.credits).padStart(8)} credits` +
      (balance != null ? `   balance: ${balance}` : "") +
      (runningSpent != null ? `   session spent: ${runningSpent}` : "")
  );
}

function watch(intervalSeconds) {
  console.log(`Watching Higgsfield usage every ${intervalSeconds}s. Ctrl+C to stop.\n`);
  let state = loadState();
  let sessionSpent = 0;
  let first = true;

  const tick = () => {
    let status;
    try {
      status = hf(["account", "status"]);
    } catch (e) {
      console.error("Failed to fetch account status:", e.message);
      return;
    }
    if (first) {
      console.log(`Current balance: ${status.credits} credits (${status.subscription_plan_type} plan)`);
      console.log("Waiting for new generations...\n");
      first = false;
    }
    let fresh;
    try {
      fresh = fetchNewTransactions(state.lastSeen);
    } catch (e) {
      console.error("Failed to fetch transactions:", e.message);
      return;
    }
    for (const t of fresh) {
      if (t.action === "spend") sessionSpent += -t.credits;
      appendLog(t);
      printTx(t, Number(sessionSpent.toFixed(2)), status.credits);
      state.lastSeen = t.created_at;
    }
    if (fresh.length) saveState(state);
  };

  tick();
  setInterval(tick, intervalSeconds * 1000);
}

function report() {
  const log = loadLog();
  if (!log.length) {
    console.log("No usage logged yet. Run `node usage-tracker.js watch` while you generate.");
    return;
  }
  const byModel = {};
  let totalSpent = 0;
  let totalGranted = 0;
  for (const t of log) {
    if (t.action === "spend") {
      totalSpent += -t.credits;
      byModel[t.display_name] = (byModel[t.display_name] || 0) + -t.credits;
    } else {
      totalGranted += t.credits;
    }
  }
  let status;
  try {
    status = hf(["account", "status"]);
  } catch {
    status = null;
  }

  console.log("=== Higgsfield usage report ===");
  if (status) console.log(`Current balance: ${status.credits} credits (${status.subscription_plan_type} plan)\n`);
  console.log("Spent by model:");
  for (const [model, credits] of Object.entries(byModel).sort((a, b) => b[1] - a[1])) {
    console.log(`  ${model.padEnd(28)} ${credits.toFixed(2)} credits`);
  }
  console.log(`\nTotal spent (logged): ${totalSpent.toFixed(2)} credits`);
  console.log(`Total granted (logged): ${totalGranted} credits`);
  console.log(`Generations logged: ${log.filter((t) => t.action === "spend").length}`);
}

const [, , mode, arg] = process.argv;

if (mode === "watch") {
  watch(Number(arg) || 15);
} else if (mode === "report") {
  report();
} else {
  console.log("Usage:");
  console.log("  node usage-tracker.js watch [intervalSeconds=15]   Live counter while you generate");
  console.log("  node usage-tracker.js report                       Summary of everything logged so far");
}
