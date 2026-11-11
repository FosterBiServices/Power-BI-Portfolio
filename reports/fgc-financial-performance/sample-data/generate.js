// Foster Golf Co: financial sample data.
// Runs the Foster BI Toolkit Sample Data Maker engine (copied unchanged into ./vendor) in Node and uses its
// seeded random numbers, word lists and Date table, then builds a golf retailer's three statements on top:
// monthly sales by store, product and customer; labor; the general ledger (P&L and balance sheet); cash flow;
// receivables aging; inventory; and capital projects. Actual Jan 2023 to Oct 2026, Budget FY2024 to FY2026,
// and a rolling Forecast Nov 2026 to Dec 2027. Every statement ties: P&L to the sales and labor detail,
// the balance sheet balances every month, and cash flow explains the change in cash.
//   node generate.js            writes ./csv/*.csv and ./csv/_checks.json
const fs = require('fs'), path = require('path'), vm = require('vm');
const V = path.join(__dirname, 'vendor');
const src = ['sd_names.js', 'sd_core.js', 'sd_ind.js'].map(f => fs.readFileSync(path.join(V, f), 'utf8')).join('\n');
const ctx = {}; vm.createContext(ctx);
vm.runInContext(src + '\n;this.SD = SD; this.SD_IND = SD_IND;', ctx);
const { SD } = ctx;

const SEED = 2026, STORE_SEED = 2012;
const R = (k, s) => SD.rand(k, s, SEED);                 // the toolkit's seeded hash: 0 up to 1
const N = (k, s, a) => 1 + (R(k, s) * 2 - 1) * a;        // noise around 1, +/- a
const r0 = x => Math.round(x), r2 = x => Math.round(x * 100) / 100;

/* ---------- calendar ---------- */
const MONTHS = [];
for (let i = 0; i < 60; i++) {
  const y = 2023 + Math.floor(i / 12), m = (i % 12) + 1;
  const end = new Date(Date.UTC(y, m, 0));
  MONTHS.push({ i, y, m, date: end.toISOString().slice(0, 10) });
}
const LAST_ACTUAL = 45;               // Oct 2026
const isAct = i => i <= LAST_ACTUAL;
const BUD_FROM = 12, BUD_TO = 47;     // FY2024 to FY2026
const FC_FROM = 46, FC_TO = 59;       // Nov 2026 to Dec 2027

/* ---------- locations: the 12 stores are the same seeded stores as FGC Financials and the survey ---------- */
const REG = ['North', 'South', 'East', 'West', 'Central'];
const LOC = [];
for (let k = 1; k <= 12; k++) {
  const c = Math.floor(SD.rand(k, 1, STORE_SEED) * 25), t = SD.rand(k, 2, STORE_SEED);
  const city = SD.LISTS.City[c];
  const fmt = t < 0.35 ? 'Mall' : t < 0.7 ? 'Street' : t < 0.9 ? 'Outlet' : 'Street';
  LOC.push({ key: k, name: 'Store ' + String(k).padStart(2, '0') + ' ' + city, type: 'Store', channel: 'Stores', city, region: REG[c % 5], format: fmt,
    sqft: r0((fmt === 'Outlet' ? 9000 : fmt === 'Mall' ? 11000 : 14000) * N(k, 3, 0.15) / 100) * 100,
    base: (fmt === 'Outlet' ? 2.7 : fmt === 'Mall' ? 3.4 : 3.9) * N(k, 4, 0.18) * 1e6,
    rent: (fmt === 'Outlet' ? 14500 : fmt === 'Mall' ? 22000 : 19500) * N(k, 5, 0.12),
    sim: [1, 3, 5, 10].includes(k), opened: 2009 + Math.floor(R(k, 6) * 12) });
}
LOC.push({ key: 13, name: 'E-commerce', type: 'E-commerce', channel: 'E-commerce', city: 'Dayton', region: 'National', format: 'Online', sqft: 60000, base: 8.6e6, rent: 41000, sim: false, opened: 2016 });
LOC.push({ key: 14, name: 'Commercial Accounts', type: 'Commercial', channel: 'Commercial', city: 'Dayton', region: 'National', format: 'B2B', sqft: 0, base: 0, rent: 0, sim: false, opened: 2012 });
LOC.push({ key: 15, name: 'Corporate', type: 'Corporate', channel: 'Corporate', city: 'Dayton', region: 'National', format: 'Office', sqft: 18000, base: 0, rent: 34000, sim: false, opened: 2009 });
const STORES = LOC.filter(l => l.type === 'Store');
const ECOM = LOC[12], COMM = LOC[13], CORP = LOC[14];

/* ---------- products ---------- */
// [name, category, list price, unit cost share, store mix, ecom mix, commercial mix, season profile]
const SEAS = {
  hard:  [0.55, 0.65, 1.00, 1.35, 1.45, 1.35, 1.15, 1.00, 0.90, 0.80, 0.85, 1.15],
  balls: [0.55, 0.65, 0.95, 1.20, 1.35, 1.40, 1.35, 1.20, 1.00, 0.85, 0.70, 0.80],
  soft:  [0.60, 0.65, 0.95, 1.25, 1.35, 1.25, 1.10, 1.00, 0.95, 0.85, 0.90, 1.30],
  svc:   [0.85, 0.90, 1.15, 1.30, 1.25, 1.10, 0.95, 0.90, 0.95, 0.95, 0.85, 0.85],
  sim:   [1.55, 1.45, 1.20, 0.85, 0.65, 0.55, 0.55, 0.60, 0.75, 1.05, 1.35, 1.45],
  comm:  [0.70, 1.35, 1.60, 1.45, 1.10, 0.90, 0.80, 0.85, 1.05, 0.95, 0.65, 0.60]
};
Object.values(SEAS).forEach(a => { const s = a.reduce((x, y) => x + y, 0) / 12; a.forEach((v, i) => { a[i] = v / s; }); });
const PRODUCTS = [
  ['Drivers', 'Clubs', 520, 0.67, 0.100, 0.070, 0.020, 'hard'],
  ['Fairway Woods', 'Clubs', 330, 0.66, 0.040, 0.030, 0.000, 'hard'],
  ['Hybrids', 'Clubs', 270, 0.65, 0.035, 0.025, 0.000, 'hard'],
  ['Iron Sets', 'Clubs', 1150, 0.69, 0.140, 0.050, 0.030, 'hard'],
  ['Wedges', 'Clubs', 165, 0.61, 0.035, 0.030, 0.010, 'hard'],
  ['Putters', 'Clubs', 290, 0.59, 0.045, 0.035, 0.010, 'hard'],
  ['Pre-Owned Clubs', 'Clubs', 180, 0.55, 0.030, 0.025, 0.000, 'hard'],
  ['Premium Golf Balls', 'Balls', 52, 0.71, 0.080, 0.130, 0.220, 'balls'],
  ['Value Golf Balls', 'Balls', 28, 0.66, 0.030, 0.050, 0.090, 'balls'],
  ['Gloves', 'Accessories & Tech', 24, 0.50, 0.030, 0.050, 0.090, 'balls'],
  ['Golf Bags', 'Accessories & Tech', 260, 0.62, 0.045, 0.050, 0.050, 'hard'],
  ['Push Carts', 'Accessories & Tech', 240, 0.65, 0.025, 0.040, 0.000, 'hard'],
  ['Rangefinders & GPS', 'Accessories & Tech', 330, 0.73, 0.050, 0.100, 0.020, 'hard'],
  ['Training Aids', 'Accessories & Tech', 45, 0.52, 0.020, 0.040, 0.040, 'hard'],
  ['Headwear & Accessories', 'Accessories & Tech', 30, 0.48, 0.025, 0.040, 0.100, 'soft'],
  ['Golf Shoes', 'Footwear & Apparel', 150, 0.60, 0.060, 0.080, 0.020, 'soft'],
  ["Men's Apparel", 'Footwear & Apparel', 65, 0.52, 0.090, 0.090, 0.180, 'soft'],
  ["Women's Apparel", 'Footwear & Apparel', 62, 0.52, 0.050, 0.060, 0.080, 'soft'],
  ['Outerwear', 'Footwear & Apparel', 110, 0.54, 0.040, 0.040, 0.040, 'soft'],
  ['Club Fitting', 'Services', 150, 0.30, 0, 0, 0, 'svc'],
  ['Golf Lessons', 'Services', 95, 0.38, 0, 0, 0, 'svc'],
  ['Simulator Bays', 'Services', 55, 0.20, 0, 0, 0, 'sim'],
  ['Repairs & Regripping', 'Services', 40, 0.40, 0, 0, 0, 'svc']
].map((p, i) => ({ key: i + 1, name: p[0], cat: p[1], price: p[2], cost: p[3], mix: { s: p[4], e: p[5], c: p[6] }, seas: p[7],
  group: p[1] === 'Services' ? 'Services' : p[1] === 'Footwear & Apparel' ? 'Soft Goods' : 'Hard Goods' }));
['s', 'e', 'c'].forEach(ch => { const t = PRODUCTS.reduce((a, p) => a + p.mix[ch], 0); PRODUCTS.forEach(p => { p.mix[ch] /= t; }); });
const SVC = PRODUCTS.filter(p => p.cat === 'Services');
const APPAREL = new Set(["Men's Apparel", "Women's Apparel", 'Outerwear', 'Headwear & Accessories']);

/* ---------- commercial customers: golf clubs, resorts, universities, corporate event buyers ---------- */
const CTYPE = [['Country Club', 'Country Club', 30], ['Golf Resort', 'Resort', 18], ['Golf Club', 'Golf Club', 22], ['Municipal Course', 'Public Course', 12], ['University Athletics', 'University', 8], ['Corporate Events', 'Corporate', 10]];
const CUST = [];
const NCOMM = 40;
for (let k = 1; k <= NCOMM; k++) {
  let t = R(k, 21) * 100, ti = 0; for (; ti < CTYPE.length - 1 && t > CTYPE[ti][2]; ti++) t -= CTYPE[ti][2];
  const a = SD.LISTS.CompanyA[Math.floor(R(k, 22) * 20)], b = SD.LISTS.CompanyB[Math.floor(R(k, 23) * 16)];
  let name = a + ' ' + b + ' ' + CTYPE[ti][0];
  while (CUST.some(c => c.name === name)) name = SD.LISTS.CompanyA[Math.floor(R(k + CUST.length, 24) * 20)] + ' ' + b + ' ' + CTYPE[ti][0];
  // a Pareto spread: a few large accounts and a long tail
  const w = Math.pow(1 / k, 0.95) * N(k, 25, 0.12);
  const terms = k <= 6 ? 60 : R(k, 26) < 0.5 ? 30 : 45;
  CUST.push({ key: 100 + k, name, type: 'Commercial', segment: CTYPE[ti][1], region: REG[Math.floor(R(k, 27) * 5)], terms, w, since: 2008 + Math.floor(R(k, 28) * 15) });
}
const wsum = CUST.reduce((a, c) => a + c.w, 0); CUST.forEach(c => { c.w /= wsum; });
// the story accounts: #2 cuts orders from Jun 2026 (moves to a direct vendor program); #1 and #4 pay slowly in 2026
const LOST = CUST[1], SLOW = [CUST[0], CUST[3], CUST[8]];
CUST.unshift({ key: 2, name: 'E-commerce Shoppers', type: 'Consumer', segment: 'Online', region: 'National', terms: 0, w: 0, since: 2016 });
CUST.unshift({ key: 1, name: 'In-Store Shoppers', type: 'Consumer', segment: 'Retail', region: 'National', terms: 0, w: 0, since: 2009 });
const COMMS = CUST.filter(c => c.type === 'Commercial');

/* ---------- drivers by month ---------- */
// company growth (real volume), price inflation, and the 2026 story
const volGrowth = i => { const y = 2023 + Math.floor(i / 12); return y === 2023 ? 1 : y === 2024 ? 1.04 : y === 2025 ? 1.085 : y === 2026 ? 1.12 : 1.16; };
const priceIdx = i => Math.pow(1.025, i / 12);
const BUD_GROWTH = { 2024: 1.06, 2025: 1.07, 2026: 1.075 };     // what each year's budget planned over the year before

function actualShock(p, ch, i, loc) {
  // returns { vol, price, disc, cost } multipliers for actuals (and forecast) only
  const y = 2023 + Math.floor(i / 12), mo = (i % 12) + 1, t26 = y > 2026 || (y === 2026);
  let vol = 1, price = 1, disc = 0, cost = 1;
  // apparel: bought for +12% in 2026, sold below plan, cleared with markdowns from Jul 2026 to Jan 2027
  if (APPAREL.has(p.name) && t26) { vol *= 0.90; if (i >= 42 && i <= 49) disc += [0.07, 0.10, 0.13, 0.15, 0.12, 0.10, 0.08, 0.05][i - 42]; }
  // golf balls: 6% price increase in Mar 2026 held, volume flat
  if (p.cat === 'Balls' && i >= 38) { price *= 1.06; vol *= 0.985; }
  // fitting-led club sales: premium mix lifts clubs' average price and margin from 2025
  if (p.cat === 'Clubs' && i >= 27) { price *= 1.045; vol *= 1.03; cost *= 0.985; }
  // rangefinders: a vendor cost increase in 2026 (tariffs) not passed on
  if (p.name === 'Rangefinders & GPS' && i >= 36) cost *= 1.09;
  // services: fitting and lessons demand up; simulator bays opened Mar 2026 in four stores
  if (p.cat === 'Services' && i >= 30) vol *= 1.12;
  if (p.name === 'Simulator Bays' && loc && loc.sim && i >= 38) vol *= 3.2;
  // e-commerce: stronger than plan
  if (ch === 'e' && i >= 30) vol *= 1.06;
  return { vol, price, disc, cost };
}
const baseDisc = p => p.cat === 'Services' ? 0.02 : APPAREL.has(p.name) ? 0.08 : p.cat === 'Clubs' ? 0.05 : 0.04;

/* ---------- sales ---------- */
const COST_SCALE = 0.865;
const SALES = [];   // { i, scen, loc, prod, cust, units, gross, disc, net, cogs }
function addSale(i, scen, loc, p, cust, rev, d) {
  // rev: expected gross revenue for the row; d: { price, disc, cost }
  if (rev <= 0) return;
  const price = p.price * priceIdx(i) * d.price;
  const units = Math.max(0, Math.round(rev / price));
  if (!units) return;
  const gross = units * price, disc = gross * Math.min(0.45, d.disc), net = gross - disc;
  const cogs = units * p.price * priceIdx(i) * p.cost * COST_SCALE * d.cost;
  const G = r0(gross), Dd = r0(disc);
  SALES.push({ i, scen, loc: loc.key, prod: p.key, cust, units, gross: G, disc: Dd, net: G - Dd, cogs: r0(cogs) });
}
// expected yearly revenue of a channel/location in year-index terms
function storeProductRev(loc, p, i, scen) {
  const seas = SEAS[p.seas][i % 12];
  const g = scen === 'Budget' ? budgetGrowth(i) : volGrowth(i);
  return loc.base * p.mix.s * g * priceIdx(i) * seas / 12;
}
function budgetGrowth(i) { const y = 2023 + Math.floor(i / 12); let g = 1; for (let yy = 2024; yy <= y; yy++) g *= BUD_GROWTH[yy] || 1.07; return g / Math.pow(1.025, (y - 2023)) * (y > 2023 ? 1 : 1); }
const SVC_BASE = { 'Club Fitting': 105000, 'Golf Lessons': 120000, 'Simulator Bays': 45000, 'Repairs & Regripping': 52000 };

function genSales(i, scen) {
  const fc = scen === 'Forecast';
  const act = scen !== 'Budget';
  for (const loc of STORES.concat([ECOM])) {
    const ch = loc.type === 'E-commerce' ? 'e' : 's';
    for (const p of PRODUCTS) {
      let rev;
      if (p.cat === 'Services') {
        if (ch === 'e') continue;
        const scale = loc.base / 3.4e6;
        rev = SVC_BASE[p.name] * scale * SEAS[p.seas][i % 12] / 12 * priceIdx(i) * (scen === 'Budget' ? budgetGrowth(i) : volGrowth(i));
        if (p.name === 'Simulator Bays' && !loc.sim) rev *= 0.25;      // a single bay in the other stores
        if (scen === 'Budget' && p.name === 'Simulator Bays' && loc.sim && i >= 38) rev *= 2.6;  // the plan counted on the new bays
        if (scen === 'Budget' && p.cat === 'Services' && i >= 36) rev *= 1.05;
      } else {
        const mix = ch === 'e' ? p.mix.e : p.mix.s;
        rev = loc.base * mix * SEAS[p.seas][i % 12] / 12 * priceIdx(i) * (scen === 'Budget' ? budgetGrowth(i) : volGrowth(i));
        if (ch === 'e') rev *= scen === 'Budget' ? Math.pow(1.10, (i - 12) / 12) : Math.pow(1.14, i / 12) / Math.pow(1.04, i / 12) * 1.0;
      }
      let d = { price: 1, disc: baseDisc(p), cost: 1 };
      if (act) {
        const s = actualShock(p, ch, i, loc);
        rev *= s.vol; d = { price: s.price, disc: d.disc + s.disc, cost: s.cost };
        // stores 07 and 11: understaffed in 2026, fewer fittings and slower service
        if ((loc.key === 7 || loc.key === 11) && i >= 36) rev *= p.cat === 'Services' ? 0.86 : 0.95;
        if (!fc) rev *= N(i * 1000 + loc.key * 50 + p.key, 31, 0.07);
        else rev *= 0.995;
      } else {
        // budget: plan prices and costs as they stood when the budget was set
        if (p.cat === 'Balls' && i >= 38) d.price = 1.03;            // planned a smaller ball price increase
        if (APPAREL.has(p.name) && i >= 36) rev *= 1.12 / 1.0;       // planned apparel growth (the buy)
      }
      addSale(i, scen, loc, p, loc.type === 'E-commerce' ? 2 : 1, rev * d.price, d);
    }
  }
  // commercial accounts
  const commBase = 7.4e6;
  for (const c of COMMS) {
    for (const p of PRODUCTS) {
      if (p.mix.c <= 0) continue;
      if (R(c.key * 100 + p.key, 41) > 0.55 + c.w * 6) continue;        // smaller accounts buy fewer lines
      let rev = commBase * c.w * p.mix.c / (0.55 + 0.3) * SEAS.comm[i % 12] / 12 * priceIdx(i) * (scen === 'Budget' ? budgetGrowth(i) : volGrowth(i));
      let d = { price: 1, disc: 0.12, cost: 1 };                       // trade discount
      if (act) {
        const s = actualShock(p, 'c', i, null);
        rev *= s.vol; d = { price: s.price, disc: 0.12 + s.disc * 0.5, cost: s.cost };
        if (c === LOST && i >= 41) rev *= 0.35;                          // lost most of this account from Jun 2026
        if (!fc) rev *= N(i * 1000 + c.key * 50 + p.key, 32, 0.12);
      }
      addSale(i, scen, COMM, p, c.key, rev * d.price, d);
    }
  }
}
for (let i = 0; i <= LAST_ACTUAL; i++) genSales(i, 'Actual');
for (let i = BUD_FROM; i <= BUD_TO; i++) genSales(i, 'Budget');
for (let i = FC_FROM; i <= FC_TO; i++) genSales(i, 'Forecast');

/* ---------- labor ---------- */
// departments: Sales Floor, Fitting & Instruction, Store Management, Fulfillment, Corporate
const LABOR = [];
const sumSales = (i, scen, f) => SALES.filter(s => s.i === i && s.scen === scen && f(s)).reduce((a, s) => a + s.net, 0);
const salesIdx = {};
SALES.forEach(s => { const k = s.i + '|' + s.scen + '|' + s.loc; const o = salesIdx[k] || (salesIdx[k] = { all: 0, svc: 0, prod: 0 }); o.all += s.net; if (PRODUCTS[s.prod - 1].cat === 'Services') o.svc += s.net; else o.prod += s.net; });
const wage = (base, i) => base * Math.pow(1.04, i / 12);
function genLabor(i, scen) {
  const act = scen !== 'Budget', fc = scen === 'Forecast';
  for (const loc of LOC) {
    const s = salesIdx[i + '|' + scen + '|' + loc.key] || { all: 0, svc: 0, prod: 0 };
    const rows = [];
    if (loc.type === 'Store') {
      // productivity: new scheduling tool from Jul 2025 cuts sales-floor hours per dollar by 7% (the plan expected 4% from 2026)
      let eff = act ? (i >= 30 ? 0.93 : 1) : (i >= 36 ? 0.96 : 1);
      let floorH = s.prod / (wage(1, i) * 265) * eff + 330;            // fixed coverage hours
      let fitH = s.svc / (wage(1, i) * 88);
      const mgmtH = 2 * 173;
      let ot = 0.03;
      if (act && (loc.key === 7 || loc.key === 11) && i >= 36) { ot = 0.13 + R(i * 7 + loc.key, 51) * 0.04; floorH *= 1.04; }
      if (act && !fc) { floorH *= N(i * 31 + loc.key, 52, 0.04); fitH *= N(i * 37 + loc.key, 53, 0.05); ot *= N(i * 41 + loc.key, 54, 0.25); }
      rows.push(['Sales Floor', floorH, 18.5, ot], ['Fitting & Instruction', fitH, 27, ot * 0.6], ['Store Management', mgmtH, 31, 0]);
    } else if (loc.type === 'E-commerce') {
      let h = s.all / (wage(1, i) * 260) + 600; let ot = 0.05;
      if (act && i >= 42 && i <= 45) ot = 0.09;
      if (act && !fc) h *= N(i * 43, 55, 0.05);
      rows.push(['Fulfillment', h, 18, ot], ['Store Management', 2 * 173, 33, 0]);
    } else if (loc.type === 'Commercial') {
      rows.push(['Account Management', 5 * 173, 34, 0]);
    } else {
      rows.push(['Corporate', (act ? 29 : 28) * 173, 41, 0]);
    }
    for (const [dept, hrs, rate, otp] of rows) {
      if (hrs <= 0) continue;
      const h = Math.round(hrs), oth = Math.round(h * otp), r = wage(rate, i);
      const wages = (h - oth) * r + oth * r * 1.5;
      LABOR.push({ i, scen, loc: loc.key, dept, hours: h, ot: oth, wages: r2(wages), benefits: r2(wages * (dept === 'Corporate' ? 0.24 : 0.19)), fte: r2(h / 173) });
    }
  }
}
for (let i = 0; i <= LAST_ACTUAL; i++) genLabor(i, 'Actual');
for (let i = BUD_FROM; i <= BUD_TO; i++) genLabor(i, 'Budget');
for (let i = FC_FROM; i <= FC_TO; i++) genLabor(i, 'Forecast');

/* ---------- capital projects ---------- */
// [id, project, type, location, budget, start idx, planned end idx, actual end idx (null = open), cost factor, annual benefit, status note]
const PROJ = [
  ['CP-01', 'Website Replatform', 'Technology', 13, 650000, 12, 20, 21, 1.04, 380000],
  ['CP-02', 'Store Fixtures Refresh', 'Maintenance', 15, 420000, 14, 22, 22, 0.97, 0],
  ['CP-03', 'Fitting Studios (3 stores)', 'Growth', 15, 540000, 24, 31, 31, 0.94, 260000],
  ['CP-04', 'Simulator Bays Phase 1', 'Growth', 15, 1600000, 30, 38, 38, 0.95, 720000],
  ['CP-05', 'POS & ERP Upgrade', 'Technology', 15, 1200000, 33, 43, null, 1.33, 310000],
  ['CP-06', 'Store 04 Remodel', 'Growth', 4, 900000, 37, 42, 43, 1.18, 190000],
  ['CP-07', 'E-commerce DC Automation', 'Growth', 13, 750000, 40, 47, null, 1.00, 240000],
  ['CP-08', 'HVAC & Roof Replacements', 'Maintenance', 15, 380000, 36, 45, 44, 1.06, 0],
  ['CP-09', 'Delivery Van Fleet', 'Maintenance', 14, 260000, 39, 41, 41, 0.98, 0],
  ['CP-10', 'Simulator Bays Phase 2', 'Growth', 15, 1400000, 50, 57, null, 1.00, 600000],
  ['CP-11', 'Maintenance Capex (ongoing)', 'Maintenance', 15, 0, 0, 59, null, 1.00, 0]
];
const CAPEX = [];   // { i, scen, proj, amount }
const capexBy = {}; // `${scen}|${i}` -> amount
function addCapex(i, scen, id, amt) { if (amt <= 0) return; CAPEX.push({ i, scen, proj: id, amount: r0(amt) }); const k = scen + '|' + i; capexBy[k] = (capexBy[k] || 0) + r0(amt); }
for (const pr of PROJ) {
  const [id, , , , bud, s, pe, ae, cf] = pr;
  if (id === 'CP-11') {
    for (let i = 0; i <= 59; i++) {
      const m = 45000 * Math.pow(1.03, i / 12);
      if (isAct(i)) addCapex(i, 'Actual', id, m * N(i, 61, 0.35));
      if (i >= BUD_FROM && i <= BUD_TO) addCapex(i, 'Budget', id, m);
      if (i >= FC_FROM) addCapex(i, 'Forecast', id, m);
    }
    continue;
  }
  const n = pe - s + 1;
  // budget: spread evenly over the planned months, in the budget years
  for (let i = s; i <= pe; i++) if (i >= BUD_FROM && i <= BUD_TO) addCapex(i, 'Budget', id, bud / n);
  // actual and forecast: the real cost, over the real duration
  const total = bud * cf, end = ae !== null ? ae : (id === 'CP-05' ? 49 : id === 'CP-07' ? 47 : pe);
  const m = end - s + 1;
  for (let i = s; i <= end; i++) {
    const amt = total / m * (id === 'CP-10' ? 1 : N(i * 13 + s, 62, 0.15));
    if (isAct(i)) addCapex(i, 'Actual', id, amt);
    else if (i >= FC_FROM) addCapex(i, 'Forecast', id, amt);
  }
}

/* ---------- P&L by location (general ledger) ---------- */
// account: [key, account, P&L line, section, sign, sort]
const ACCTS = [
  [4010, 'Store Product Sales', 'Gross Sales', 'Revenue', 1], [4020, 'E-commerce Sales', 'Gross Sales', 'Revenue', 1], [4030, 'Commercial Sales', 'Gross Sales', 'Revenue', 1],
  [4040, 'Services Revenue', 'Gross Sales', 'Revenue', 1], [4090, 'Discounts & Markdowns', 'Discounts & Markdowns', 'Revenue', -1],
  [5010, 'Product Cost', 'Cost of Sales', 'Cost of Sales', -1], [5020, 'Freight & Fulfillment', 'Cost of Sales', 'Cost of Sales', -1],
  [5030, 'Shrink & Obsolescence', 'Cost of Sales', 'Cost of Sales', -1], [5040, 'Service Delivery Cost', 'Cost of Sales', 'Cost of Sales', -1],
  [6010, 'Store & Fulfillment Labor', 'Labor', 'Operating Expenses', -1], [6020, 'Fitting & Instruction Labor', 'Labor', 'Operating Expenses', -1],
  [6030, 'Corporate & Account Salaries', 'Labor', 'Operating Expenses', -1], [6040, 'Benefits & Payroll Taxes', 'Labor', 'Operating Expenses', -1],
  [6100, 'Rent & Occupancy', 'Occupancy', 'Operating Expenses', -1], [6110, 'Utilities', 'Occupancy', 'Operating Expenses', -1],
  [6200, 'Marketing', 'Marketing', 'Operating Expenses', -1], [6300, 'Technology', 'Technology & Admin', 'Operating Expenses', -1],
  [6400, 'Card & Payment Fees', 'Technology & Admin', 'Operating Expenses', -1], [6500, 'Other G&A', 'Technology & Admin', 'Operating Expenses', -1],
  [7010, 'Depreciation & Amortization', 'Depreciation & Amortization', 'Below EBITDA', -1],
  [8010, 'Interest Expense', 'Interest', 'Below EBITDA', -1], [8020, 'Income Tax', 'Income Tax', 'Below EBITDA', -1]
];
const BS_ACCTS = [
  [1010, 'Cash', 'Cash', 'Current Assets', 1], [1100, 'Accounts Receivable', 'Accounts Receivable', 'Current Assets', 1], [1200, 'Inventory', 'Inventory', 'Current Assets', 1],
  [1300, 'Prepaid & Other', 'Prepaid & Other', 'Current Assets', 1], [1500, 'Property & Equipment', 'Property & Equipment, Net', 'Long-Term Assets', 1],
  [1510, 'Accumulated Depreciation', 'Property & Equipment, Net', 'Long-Term Assets', -1],
  [2010, 'Accounts Payable', 'Accounts Payable', 'Current Liabilities', 1], [2100, 'Accrued Liabilities', 'Accrued Liabilities', 'Current Liabilities', 1],
  [2200, 'Gift Cards & Deferred Revenue', 'Gift Cards & Deferred Revenue', 'Current Liabilities', 1], [2300, 'Revolving Credit Facility', 'Revolving Credit Facility', 'Debt', 1],
  [2400, 'Term Loan', 'Term Loan', 'Debt', 1], [3010, 'Paid-In Capital', 'Paid-In Capital', 'Equity', 1], [3020, 'Retained Earnings', 'Retained Earnings', 'Equity', 1]
];
const GL = [];      // { i, scen, loc, acct, amount }  P&L: positive natural amounts; BS: month-end balances
const pl = {};      // `${scen}|${i}` -> { acct: amount } company totals
function post(i, scen, loc, acct, amt) {
  if (!amt) return; amt = r2(amt);
  GL.push({ i, scen, loc, acct, amount: amt });
  const k = scen + '|' + i; const o = pl[k] || (pl[k] = {}); o[acct] = (o[acct] || 0) + amt;
}
// sales detail into revenue and cost lines
const agg = {};
SALES.forEach(s => {
  const p = PRODUCTS[s.prod - 1], k = s.i + '|' + s.scen + '|' + s.loc;
  const o = agg[k] || (agg[k] = { g4010: 0, g4020: 0, g4030: 0, g4040: 0, disc: 0, c5010: 0, c5040: 0, net: 0, netProdStore: 0, apparelNet: 0 });
  const acct = p.cat === 'Services' ? 'g4040' : s.loc === 13 ? 'g4020' : s.loc === 14 ? 'g4030' : 'g4010';
  o[acct] += s.gross; o.disc += s.disc; o.net += s.net;
  if (p.cat === 'Services') o.c5040 += s.cogs; else o.c5010 += s.cogs;
  if (s.loc <= 12 && p.cat !== 'Services') o.netProdStore += s.net;
});
const laborAgg = {};
LABOR.forEach(l => { const k = l.i + '|' + l.scen + '|' + l.loc; const o = laborAgg[k] || (laborAgg[k] = { store: 0, fit: 0, corp: 0, ben: 0 });
  if (l.dept === 'Fitting & Instruction') o.fit += l.wages; else if (l.dept === 'Corporate' || l.dept === 'Account Management') o.corp += l.wages; else o.store += l.wages; o.ben += l.benefits; });

const scenMonths = { Actual: [0, LAST_ACTUAL], Budget: [BUD_FROM, BUD_TO], Forecast: [FC_FROM, FC_TO] };
for (const scen of ['Actual', 'Budget', 'Forecast']) {
  const [a, b] = scenMonths[scen];
  const act = scen !== 'Budget', fc = scen === 'Forecast';
  for (let i = a; i <= b; i++) {
    let companyNet = 0;
    for (const loc of LOC) {
      const s = agg[i + '|' + scen + '|' + loc.key], L = laborAgg[i + '|' + scen + '|' + loc.key];
      if (s) {
        companyNet += s.net;
        post(i, scen, loc.key, 4010, s.g4010); post(i, scen, loc.key, 4020, s.g4020); post(i, scen, loc.key, 4030, s.g4030); post(i, scen, loc.key, 4040, s.g4040);
        post(i, scen, loc.key, 4090, s.disc); post(i, scen, loc.key, 5010, s.c5010); post(i, scen, loc.key, 5040, s.c5040);
        // freight: e-commerce shipping (carrier rates up in 2026), commercial freight
        if (loc.type === 'E-commerce') post(i, scen, loc.key, 5020, s.net * (act && i >= 36 ? 0.104 : 0.092));
        if (loc.type === 'Commercial') post(i, scen, loc.key, 5020, s.net * 0.03);
        if (loc.type === 'Store') post(i, scen, loc.key, 5030, s.netProdStore * 0.009 * (act && !fc ? N(i * 3 + loc.key, 71, 0.3) : 1));
        // card fees on consumer sales
        if (loc.type === 'Store' || loc.type === 'E-commerce') post(i, scen, loc.key, 6400, s.net * 0.024);
      }
      if (L) { post(i, scen, loc.key, 6010, L.store); post(i, scen, loc.key, 6020, L.fit); post(i, scen, loc.key, 6030, L.corp); post(i, scen, loc.key, 6040, L.ben); }
      if (loc.rent) post(i, scen, loc.key, 6100, loc.rent * Math.pow(1.03, Math.floor(i / 12)) * (loc.key === 4 && i >= 43 ? 1.06 : 1));
      if (loc.type === 'Store' || loc.type === 'E-commerce' || loc.type === 'Corporate') {
        const util = (loc.sqft || 10000) * 0.19 * (1 + 0.25 * Math.cos((i % 12) / 12 * 2 * Math.PI)) * Math.pow(1.035, i / 12);
        post(i, scen, loc.key, 6110, util * (act && !fc ? N(i * 5 + loc.key, 72, 0.08) : 1));
      }
    }
    // obsolescence: reserve for aged apparel taken in Sep and Oct 2026
    if (act && (i === 44 || i === 45)) post(i, scen, 15, 5030, i === 44 ? 210000 : 165000);
    // corporate costs
    const y = 2023 + Math.floor(i / 12), mo = (i % 12) + 1;
    let mkt = companyNet * 0.034;
    if (act && y === 2026 && mo >= 3 && mo <= 6) mkt *= 1.38;                 // spring campaign over plan
    post(i, scen, 15, 6200, mkt * (act && !fc ? N(i, 73, 0.06) : 1));
    let tech = 118000 * Math.pow(1.05, i / 12);
    if (act && i >= 36) tech += 42000 + (i <= 49 ? 26000 : 0);                 // POS & ERP running costs and overrun
    if (!act && i >= 36) tech += 30000;
    post(i, scen, 15, 6300, tech);
    post(i, scen, 15, 6500, (52000 + companyNet * 0.006) * (act && !fc ? N(i, 74, 0.10) : 1));
  }
}

/* ---------- balance sheet and cash flow ---------- */
const CF = [];      // { i, scen, line, amount }
const AR = [];      // { i, scen, cust, bucket, amount }
const INV = [];     // { i, scen, prod, value, aged }
const BAL = {};     // `${scen}|${i}` -> balances
const DSO_TERMS = c => c.terms;
// how many days each commercial account takes to pay (beyond its terms), by month
function payDays(c, i, scen) {
  let d = c.terms + 4 + (scen === 'Budget' ? 0 : R(c.key * 7 + i, 81) * 8);
  if (scen !== 'Budget' && SLOW.includes(c) && i >= 38) d += c === SLOW[0] ? 34 + (i - 38) * 3 : c === SLOW[1] ? 48 : 26;
  if (scen === 'Forecast' && SLOW.includes(c)) d -= Math.min(20, (i - 45) * 3);   // collections plan assumed to work slowly
  return d;
}
const salesByCust = {};
SALES.forEach(s => { if (s.loc !== 14) return; const k = s.scen + '|' + s.i + '|' + s.cust; salesByCust[k] = (salesByCust[k] || 0) + s.net; });
const cogsByProd = {};
SALES.forEach(s => { const k = s.scen + '|' + s.i + '|' + s.prod; cogsByProd[k] = (cogsByProd[k] || 0) + s.cogs; });
const netBy = (scen, i, f) => { const o = pl[scen + '|' + i] || {}; return f(o); };
const revOf = o => (o[4010] || 0) + (o[4020] || 0) + (o[4030] || 0) + (o[4040] || 0) - (o[4090] || 0);
const consumerRev = o => (o[4010] || 0) + (o[4020] || 0) + (o[4040] || 0) - (o[4090] || 0) * 0.85;

function arFor(scen, i) {
  // commercial receivables: each account's sales for as many days back as it takes to pay
  let total = 0; const rows = [];
  for (const c of COMMS) {
    const d = payDays(c, i, scen);
    let left = d, back = 0, bal = 0; const buckets = { 'Current': 0, '1-30 Days': 0, '31-60 Days': 0, '61-90 Days': 0, '90+ Days': 0 };
    while (left > 0 && back < 6) {
      const ii = i - back; const s = salesByCust[(ii > LAST_ACTUAL && scen === 'Actual' ? 'Forecast' : (scen === 'Budget' && (ii < BUD_FROM) ? 'Actual' : (scen === 'Forecast' && ii <= LAST_ACTUAL ? 'Actual' : scen))) + '|' + ii + '|' + c.key] || 0;
      const take = Math.min(30, left) / 30; const amt = s * take; bal += amt;
      // age of this slice: invoices from `back` months ago, days past terms
      const ageDays = back * 30 + 15 - c.terms;
      const b = ageDays <= 0 ? 'Current' : ageDays <= 30 ? '1-30 Days' : ageDays <= 60 ? '31-60 Days' : ageDays <= 90 ? '61-90 Days' : '90+ Days';
      buckets[b] += amt; left -= 30; back++;
    }
    total += bal;
    for (const b in buckets) if (buckets[b] > 1) rows.push({ i, scen, cust: c.key, bucket: b, amount: r2(buckets[b]) });
  }
  return { total, rows };
}
function invFor(scen, i, opts) {
  // inventory by product: days of forward cost on hand, with the 2026 apparel over-buy
  let total = 0; const rows = [];
  for (const p of PRODUCTS) {
    if (p.cat === 'Services') continue;
    const look = k => { const ii = i + k; let sc = scen; if (scen === 'Actual' && ii > LAST_ACTUAL) sc = 'Forecast'; if (scen === 'Budget' && ii > BUD_TO) return null; if (scen === 'Forecast' && ii > FC_TO) return null;
      return cogsByProd[sc + '|' + ii + '|' + p.key]; };
    const f = [1, 2, 3].map(look).filter(x => x != null); const fwd = f.length ? f.reduce((a, b) => a + b, 0) / f.length : (cogsByProd[scen + '|' + i + '|' + p.key] || 0);
    let days = p.cat === 'Clubs' ? 100 : p.cat === 'Balls' ? 70 : p.cat === 'Accessories & Tech' ? 95 : 110;
    let aged = p.cat === 'Clubs' ? 0.09 : 0.06;
    if (scen !== 'Budget') {
      if (APPAREL.has(p.name) && i >= 39) { const k = Math.min(i, 46) - 38; days *= 1 + Math.min(0.65, 0.11 * k) - (i > 46 ? Math.min(0.55, (i - 46) * 0.07) : 0); aged = 0.06 + Math.min(0.22, 0.03 * (i - 38)) - (i > 46 ? Math.min(0.18, (i - 46) * 0.03) : 0); }
      if (p.name === 'Rangefinders & GPS' && i >= 40) days *= 1.25;
      if (scen === 'Actual') days *= N(i * 11 + p.key, 91, 0.04);
    }
    const v = fwd / 30 * days; total += v;
    rows.push({ i, scen, prod: p.key, value: r2(v), aged: r2(v * aged) });
  }
  return { total, rows };
}

function runBS(scen, from, to, open) {
  let b = Object.assign({}, open);
  for (let i = from; i <= to; i++) {
    const o = pl[scen + '|' + i] || {};
    const rev = revOf(o);
    const ar = arFor(scen, i), inv = invFor(scen, i);
    // card settlements: two days of consumer sales
    const arTot = ar.total + consumerRev(o) * 2 / 30;
    const cogs = (o[5010] || 0) + (o[5040] || 0);
    const purchases = cogs + (inv.total - b.inv);
    const dpo = 47 + (scen === 'Actual' ? R(i, 92) * 4 : 0);
    const purchAvg = (Math.max(0, purchases) + (b.purch === undefined ? Math.max(0, purchases) : b.purch)) / 2;
    const ap = purchAvg * dpo / 30;
    const opex = [6010, 6020, 6030, 6040, 6100, 6110, 6200, 6300, 6400, 6500].reduce((a, k) => a + (o[k] || 0), 0);
    const accrued = ((o[6010] || 0) + (o[6020] || 0) + (o[6030] || 0) + (o[6040] || 0)) * 0.55 + opex * 0.08;
    const mo = (i % 12) + 1;
    const gift = rev * [0.020, 0.018, 0.016, 0.014, 0.013, 0.012, 0.012, 0.012, 0.013, 0.015, 0.024, 0.036][mo - 1] * 12 / 12 * 1.0;
    const prepaid = 980000 * Math.pow(1.04, i / 12) * (mo === 1 ? 1.25 : 1);
    const capex = capexBy[scen + '|' + i] || 0;
    // depreciation: the opening base plus each month's capex over 7 years from the month after
    const dep = 205000 + b.ppeAdds / 84;
    post(i, scen, 15, 7010, dep);
    const ebitda = rev - [5010, 5020, 5030, 5040].reduce((a, k) => a + (o[k] || 0), 0) - opex;
    const interest = b.term * 0.07 / 12 + b.rev * 0.0825 / 12;
    post(i, scen, 15, 8010, interest);
    const pretax = ebitda - dep - interest, tax = Math.max(0, pretax) * 0.25 - (pretax < 0 ? -pretax * 0.25 : 0);
    post(i, scen, 15, 8020, tax);
    const ni = pretax - tax;
    // financing: term loan amortizes; distributions each quarter end (paused in the forecast from Q4 2026)
    const termPay = b.term > 0 ? Math.min(b.term, 125000) : 0;
    const dist = (mo % 3 === 0) ? (scen === 'Forecast' ? 0 : (scen === 'Budget' ? 300000 : (i >= 44 ? 0 : 250000 + (i >= 24 ? 50000 : 0)))) : 0;
    const dAR = arTot - b.ar, dInv = inv.total - b.inv, dPre = prepaid - b.pre, dAP = ap - b.ap, dAcc = accrued - b.acc, dGift = gift - b.gift;
    const cfo = ni + dep - dAR - dInv - dPre + dAP + dAcc + dGift;
    let cash = b.cash + cfo - capex - termPay - dist;
    // revolver: draw to keep $3.0M of cash, repay down to $4.5M
    let draw = 0;
    if (cash < 2.5e6) draw = Math.ceil((2.5e6 - cash) / 250000) * 250000;
    else if (cash > 4.0e6 && b.rev > 0) draw = -Math.min(b.rev, Math.floor((cash - 4.0e6) / 250000) * 250000);
    cash += draw;
    const lines = [['Net Income', ni], ['Depreciation & Amortization', dep], ['Change in Receivables', -dAR], ['Change in Inventory', -dInv], ['Change in Prepaid & Other', -dPre],
      ['Change in Payables', dAP], ['Change in Accrued Liabilities', dAcc], ['Change in Gift Cards & Deferred Revenue', dGift], ['Capital Expenditures', -capex],
      ['Revolver Draws (Repayments)', draw], ['Term Loan Repayments', -termPay], ['Distributions to Owners', -dist]];
    lines.forEach(([l, a]) => CF.push({ i, scen, line: l, amount: r2(a) }));
    if (scen !== 'Budget' || true) { ar.rows.forEach(r => AR.push(r)); inv.rows.forEach(r => INV.push(r)); }
    b = { cash, ar: arTot, inv: inv.total, pre: prepaid, ppe: b.ppe + capex, ppeAdds: b.ppeAdds + capex, accdep: b.accdep + dep, ap, acc: accrued, gift, rev: b.rev + draw, term: b.term - termPay, pic: b.pic, re: b.re + ni - dist, purch: Math.max(0, purchases) };
    const assets = b.cash + b.ar + b.inv + b.pre + b.ppe - b.accdep, le = b.ap + b.acc + b.gift + b.rev + b.term + b.pic + b.re;
    if (Math.abs(assets - le) > 1) throw new Error('BS does not balance ' + scen + ' ' + i + ': ' + (assets - le));
    BAL[scen + '|' + i] = b;
    const put = (k, v) => GL.push({ i, scen, loc: 15, acct: k, amount: r2(v) });
    put(1010, b.cash); put(1100, b.ar); put(1200, b.inv); put(1300, b.pre); put(1500, b.ppe); put(1510, b.accdep); put(2010, b.ap); put(2100, b.acc); put(2200, b.gift);
    put(2300, b.rev); put(2400, b.term); put(3010, b.pic); put(3020, b.re);
  }
  return b;
}
// opening balance sheet at Dec 31, 2022, built so it balances
const open = { cash: 4.6e6, ar: 2.9e6, inv: 0, pre: 0.98e6, ppe: 26.5e6, ppeAdds: 0, accdep: 11.2e6, ap: 0, acc: 0, gift: 0, rev: 0, term: 12.0e6, pic: 10.0e6, re: 0 };
// work out December 2022 working capital from the January 2023 run-rate (so January isn't a jump)
{ const inv = invFor('Actual', 0); open.inv = inv.total * 0.97; const o = pl['Actual|0']; open.ap = ((o[5010] || 0) + (o[5040] || 0)) * 1.55; open.acc = 1.25e6; open.gift = 2.1e6; open.ar = arFor('Actual', 0).total * 1.25 + 120000;
  open.re = open.cash + open.ar + open.inv + open.pre + open.ppe - open.accdep - (open.ap + open.acc + open.gift + open.rev + open.term + open.pic); }
// two passes: run 2023 once, then take Dec 2023 working capital back one year of growth as the Dec 2022 opening
{ const save = { GL: GL.length, CF: CF.length, AR: AR.length, INV: INV.length };
  const t = runBS('Actual', 0, 11, open);
  GL.length = save.GL; CF.length = save.CF; AR.length = save.AR; INV.length = save.INV;
  ['ar', 'inv', 'pre', 'ap', 'acc', 'gift'].forEach(k => { open[k] = t[k] / 1.075; }); open.purch = t.purch / 1.075;
  open.re = 0; open.re = open.cash + open.ar + open.inv + open.pre + open.ppe - open.accdep - (open.ap + open.acc + open.gift + open.rev + open.term + open.pic);
  Object.keys(pl).forEach(k => { if (k.startsWith('Actual|')) { const o = pl[k]; delete o[7010]; delete o[8010]; delete o[8020]; } }); }
const endAct = runBS('Actual', 0, LAST_ACTUAL, open);
runBS('Forecast', FC_FROM, FC_TO, endAct);
// budget balance sheet for FY2026 only, from the actual Dec 2025 balances (the plan's starting point)
runBS('Budget', 36, BUD_TO, BAL['Actual|35']);
// AR/inventory rows for budget months outside FY2026 aren't needed; drop budget P&L-derived duplicates? (none)

/* ---------- write ---------- */
const out = path.join(__dirname, 'csv'); fs.mkdirSync(out, { recursive: true });
const esc = v => v === null || v === undefined ? '' : typeof v === 'string' && /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : String(v);
function csv(name, cols, rows) { fs.writeFileSync(path.join(out, name + '.csv'), [cols.join(',')].concat(rows.map(r => r.map(esc).join(','))).join('\n') + '\n'); return rows.length; }
const D = i => MONTHS[i].date;
const counts = {};
counts.Locations = csv('Locations', ['LocationKey', 'Location', 'Location Type', 'Channel', 'City', 'Region', 'Format', 'Square Feet', 'Has Simulator Bays', 'Year Opened'],
  LOC.map(l => [l.key, l.name, l.type, l.channel, l.city, l.region, l.format, l.sqft, l.sim ? 'Yes' : 'No', l.opened]));
counts.Products = csv('Products', ['ProductKey', 'Product Line', 'Category', 'Product Group', 'List Price'],
  PRODUCTS.map(p => [p.key, p.name, p.cat, p.group, p.price]));
counts.Customers = csv('Customers', ['CustomerKey', 'Customer', 'Customer Type', 'Segment', 'Region', 'Payment Terms Days', 'Customer Since'],
  CUST.map(c => [c.key, c.name, c.type, c.segment, c.region, c.terms, c.since]));
counts.Accounts = csv('Accounts', ['AccountKey', 'Account', 'Line', 'Section', 'Statement', 'Sign'],
  ACCTS.map(a => [a[0], a[1], a[2], a[3], 'Income Statement', a[4]]).concat(BS_ACCTS.map(a => [a[0], a[1], a[2], a[3], 'Balance Sheet', a[4]])));
counts.Sales = csv('Sales', ['Date', 'Scenario', 'LocationKey', 'ProductKey', 'CustomerKey', 'Units', 'Gross Sales', 'Discounts', 'Net Sales', 'Cost of Sales'],
  SALES.map(s => [D(s.i), s.scen, s.loc, s.prod, s.cust, s.units, s.gross, s.disc, s.net, s.cogs]));
counts.Labor = csv('Labor', ['Date', 'Scenario', 'LocationKey', 'Department', 'Hours', 'Overtime Hours', 'Wages', 'Benefits', 'FTE'],
  LABOR.map(l => [D(l.i), l.scen, l.loc, l.dept, l.hours, l.ot, l.wages, l.benefits, l.fte]));
counts['General Ledger'] = csv('General Ledger', ['Date', 'Scenario', 'LocationKey', 'AccountKey', 'Amount'], GL.map(g => [D(g.i), g.scen, g.loc, g.acct, g.amount]));
counts['Cash Flow'] = csv('Cash Flow', ['Date', 'Scenario', 'Cash Flow Line', 'Amount'], CF.map(c => [D(c.i), c.scen, c.line, c.amount]));
counts['AR Aging'] = csv('AR Aging', ['Date', 'Scenario', 'CustomerKey', 'Aging Bucket', 'Amount'], AR.map(a => [D(a.i), a.scen, a.cust, a.bucket, a.amount]));
counts.Inventory = csv('Inventory', ['Date', 'Scenario', 'ProductKey', 'Inventory Value', 'Aged 180+ Days'], INV.map(v => [D(v.i), v.scen, v.prod, v.value, v.aged]));
counts['CapEx Projects'] = csv('CapEx Projects', ['ProjectKey', 'Project', 'Project Type', 'LocationKey', 'Approved Budget', 'Start Date', 'Planned Completion', 'Actual Completion', 'Annual Benefit'],
  PROJ.map(p => [p[0], p[1], p[2], p[3], p[4], D(p[5]).slice(0, 8) + '01', D(p[6]), p[7] === null ? '' : D(p[7]), p[9]]));
counts['CapEx Spend'] = csv('CapEx Spend', ['Date', 'Scenario', 'ProjectKey', 'Amount'], CAPEX.map(c => [D(c.i), c.scen, c.proj, c.amount]));

/* ---------- checks: the numbers the README and report text quote ---------- */
const yr = (scen, y, upto, acctF) => { let t = 0; for (let i = (y - 2023) * 12; i <= (y - 2023) * 12 + upto - 1; i++) { const o = pl[scen + '|' + i]; if (o) t += acctF(o); } return t; };
const ebitdaOf = o => revOf(o) - [5010, 5020, 5030, 5040, 6010, 6020, 6030, 6040, 6100, 6110, 6200, 6300, 6400, 6500].reduce((a, k) => a + (o[k] || 0), 0);
const gmOf = o => revOf(o) - [5010, 5020, 5030, 5040].reduce((a, k) => a + (o[k] || 0), 0);
const fy = (y, f) => { let t = 0; for (let m = 1; m <= 12; m++) { const i = (y - 2023) * 12 + m - 1; const sc = i <= LAST_ACTUAL ? 'Actual' : 'Forecast'; const o = pl[sc + '|' + i]; if (o) t += f(o); } return t; };
const checks = {
  rows: counts,
  revenue: { FY2023: fy(2023, revOf), FY2024: fy(2024, revOf), FY2025: fy(2025, revOf), YTD26: yr('Actual', 2026, 10, revOf), YTD26_Bud: yr('Budget', 2026, 10, revOf), YTD25: yr('Actual', 2025, 10, revOf), FY26_LE: fy(2026, revOf), FY26_Bud: yr('Budget', 2026, 12, revOf), FY27_FC: fy(2027, revOf) },
  gm: { YTD26: yr('Actual', 2026, 10, gmOf) / yr('Actual', 2026, 10, revOf), YTD26_Bud: yr('Budget', 2026, 10, gmOf) / yr('Budget', 2026, 10, revOf), YTD25: yr('Actual', 2025, 10, gmOf) / yr('Actual', 2025, 10, revOf) },
  ebitda: { FY2024: fy(2024, ebitdaOf), FY2025: fy(2025, ebitdaOf), YTD26: yr('Actual', 2026, 10, ebitdaOf), YTD26_Bud: yr('Budget', 2026, 10, ebitdaOf), YTD25: yr('Actual', 2025, 10, ebitdaOf), FY26_LE: fy(2026, ebitdaOf), FY26_Bud: yr('Budget', 2026, 12, ebitdaOf) },
  cash: Object.fromEntries([11, 23, 35, 44, 45, 49, 50, 51, 59].map(i => [MONTHS[i].date, { cash: r0(BAL[(i <= 45 ? 'Actual' : 'Forecast') + '|' + i].cash), revolver: r0(BAL[(i <= 45 ? 'Actual' : 'Forecast') + '|' + i].rev), ar: r0(BAL[(i <= 45 ? 'Actual' : 'Forecast') + '|' + i].ar), inv: r0(BAL[(i <= 45 ? 'Actual' : 'Forecast') + '|' + i].inv) }]))
};
fs.writeFileSync(path.join(out, '_checks.json'), JSON.stringify(checks, null, 1));
console.log(JSON.stringify(checks, (k, v) => typeof v === 'number' ? Math.round(v * 1000) / 1000 : v, 1));
