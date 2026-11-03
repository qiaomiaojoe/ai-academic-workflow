#!/usr/bin/env node
// 查期刊：收录（SCIE / SSCI / AHCI / ESCI）、影响因子、JCR 分区、分区、年发文量（乔淼PhD · AI学术训练营）。只用 Node 自带的东西（Node 18 以上）。
//
// 数据来自 iJournal（ijournal.topeditsci.com，投必得学术），不用登录。网站把数据加密后再在页面里解开，
// 所以脚本不直接请求接口：在单独资料的 Chrome（没有就用 Edge）里打开它的查询页，读页面已经显示出来的结果。
// 浏览器和 cnki skill 共用一个（~/.cnki-skill/browser），各用各的标签页。
//
//   node journal-rank.mjs lookup <刊名或 ISSN>...     一次可以查几本；刊名有空格要加引号
//   node journal-rank.mjs check                        自检：用一本固定的期刊看各项还取不取得到
//
// 输出一律是一段 JSON（UTF-8），status 只有这几种：
//   ok 成功（个别没查到的在 items 里标 not_found）/ not_found 一本都没查到 / limit 本小时查太多了 /
//   layout_changed 网站改了、脚本要更新 / unreachable 网站打不开 / no_browser 没找到 Chrome 或 Edge / error 其他
import { spawn } from 'node:child_process';
import http from 'node:http';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const HOME = path.join(os.homedir(), '.cnki-skill');
const PROFILE = path.join(HOME, 'browser');
const STATE = path.join(HOME, 'journal-rank-state.json');
const PORT = Number(process.env.CNKI_PORT) || 19333;
const HOURLY_LIMIT = 120; // 一小时内最多打开的查询页，查得太勤容易被网站限制
const BASE = 'https://ijournal.topeditsci.com';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const readJson = (f, d) => { try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch { return d; } };
const writeJson = (f, v) => { fs.mkdirSync(HOME, { recursive: true }); fs.writeFileSync(f, JSON.stringify(v, null, 1)); };
class Stop extends Error { constructor(status, msg, extra = {}) { super(msg); Object.assign(this, { status, extra }); } }

// ---------- 浏览器 ----------

function findBrowser() {
  if (process.env.CNKI_BROWSER) return process.env.CNKI_BROWSER;
  const env = process.env, list = process.platform === 'darwin' ? [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    path.join(os.homedir(), 'Applications/Google Chrome.app/Contents/MacOS/Google Chrome'),
  ] : process.platform === 'win32' ? [
    ...[env.PROGRAMFILES, env['PROGRAMFILES(X86)'], env.LOCALAPPDATA].filter(Boolean).map(d => path.join(d, 'Google', 'Chrome', 'Application', 'chrome.exe')),
    ...[env['PROGRAMFILES(X86)'], env.PROGRAMFILES].filter(Boolean).map(d => path.join(d, 'Microsoft', 'Edge', 'Application', 'msedge.exe')),
  ] : ['/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/microsoft-edge'];
  return list.find(p => fs.existsSync(p));
}

const devtools = (p, method = 'GET') => new Promise((res, rej) => {
  const r = http.request({ host: '127.0.0.1', port: PORT, path: p, method }, s => {
    let d = ''; s.setEncoding('utf8'); s.on('data', c => d += c);
    s.on('end', () => { try { res(JSON.parse(d)); } catch { rej(Error('调试口回的不是 JSON')); } });
  });
  r.on('error', rej); r.setTimeout(3000, () => r.destroy(Error('调试口没响应'))); r.end();
});

async function ensureBrowser() {
  try { await devtools('/json/version'); return; } catch {}
  const exe = findBrowser();
  if (!exe) throw new Stop('no_browser', '没找到 Chrome 或 Edge。装一个 Chrome，或者设环境变量 CNKI_BROWSER 指向浏览器程序');
  fs.mkdirSync(PROFILE, { recursive: true });
  // 单独一份资料：不碰学员日常浏览器；新版 Chrome 也只许在非默认资料上开调试口
  spawn(exe, [`--user-data-dir=${PROFILE}`, `--remote-debugging-port=${PORT}`, '--no-first-run', '--no-default-browser-check', 'about:blank'],
    { detached: true, stdio: 'ignore' }).unref();
  for (let i = 0; i < 60; i++) { await sleep(250); try { await devtools('/json/version'); return; } catch {} }
  throw new Stop('no_browser', `浏览器开了但连不上调试口（端口 ${PORT}）。关掉这个浏览器窗口再试；端口被占用的话设环境变量 CNKI_PORT 换一个`);
}

// 最小的 WebSocket 客户端（Node 22 以前没有自带的）
function wsConnect(url) {
  return new Promise((res, rej) => {
    const u = new URL(url);
    const req = http.request({ host: u.hostname, port: u.port, path: u.pathname,
      headers: { Connection: 'Upgrade', Upgrade: 'websocket', 'Sec-WebSocket-Key': crypto.randomBytes(16).toString('base64'), 'Sec-WebSocket-Version': '13' } });
    req.on('upgrade', (_, sock) => {
      let buf = Buffer.alloc(0), parts = [];
      const listeners = new Set();
      const send = (data, op = 1) => {
        const p = Buffer.from(data), mask = crypto.randomBytes(4), n = p.length;
        const head = n < 126 ? Buffer.from([128 | op, 128 | n])
          : n < 65536 ? Buffer.from([128 | op, 254, n >> 8, n & 255])
          : Buffer.concat([Buffer.from([128 | op, 255]), (b => (b.writeBigUInt64BE(BigInt(n)), b))(Buffer.alloc(8))]);
        for (let i = 0; i < n; i++) p[i] ^= mask[i & 3];
        sock.write(Buffer.concat([head, mask, p]));
      };
      sock.on('data', d => {
        buf = Buffer.concat([buf, d]);
        for (;;) {
          if (buf.length < 2) return;
          let n = buf[1] & 127, off = 2;
          if (n === 126) { if (buf.length < 4) return; n = buf.readUInt16BE(2); off = 4; }
          else if (n === 127) { if (buf.length < 10) return; n = Number(buf.readBigUInt64BE(2)); off = 10; }
          if (buf.length < off + n) return;
          const fin = buf[0] & 128, op = buf[0] & 15, payload = buf.subarray(off, off + n);
          buf = buf.subarray(off + n);
          if (op === 8) { sock.end(); return; }
          if (op === 9) { send(payload, 10); continue; }
          if (op <= 2) { parts.push(payload); if (fin) { const t = Buffer.concat(parts).toString('utf8'); parts = []; listeners.forEach(f => f(t)); } }
        }
      });
      sock.on('error', () => {});
      res({ send: t => send(t), on: f => listeners.add(f), close: () => sock.destroy() });
    });
    req.on('response', r => rej(Error(`调试口拒绝连接（HTTP ${r.statusCode}）`)));
    req.on('error', rej); req.end();
  });
}

async function connect() {
  await ensureBrowser();
  const pages = (await devtools('/json/list')).filter(t => t.type === 'page');
  const target = pages.find(t => /ijournal\.topeditsci\.com/.test(t.url)) || await devtools('/json/new?about:blank', 'PUT'); // 自己开一个标签页，不占知网那个
  const ws = await wsConnect(target.webSocketDebuggerUrl);
  let seq = 0; const waiting = new Map();
  ws.on(m => { const j = JSON.parse(m); if (j.id && waiting.has(j.id)) { waiting.get(j.id)(j); waiting.delete(j.id); } });
  const cmd = (method, params = {}) => new Promise((res, rej) => {
    const id = ++seq; const t = setTimeout(() => { waiting.delete(id); rej(Error(`${method} 超时`)); }, 90e3);
    waiting.set(id, j => { clearTimeout(t); j.error ? rej(Error(j.error.message)) : res(j.result); });
    ws.send(JSON.stringify({ id, method, params }));
  });
  // 在页面里跑一个函数：fn 必须自给自足（不引用外面的变量），参数走 JSON
  const run = async (fn, ...args) => {
    const r = await cmd('Runtime.evaluate', { expression: `(${fn})(...${JSON.stringify(args)})`, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
    return r.result.value;
  };
  return { cmd, run, close: () => ws.close() };
}

// ---------- 节流：每页随机隔 2–4 秒，一小时有上限 ----------

async function pace() {
  const st = readJson(STATE, {}), now = Date.now();
  st.hits = (st.hits || []).filter(t => now - t < 3600e3);
  if (st.hits.length >= HOURLY_LIMIT) throw new Stop('limit', `这一小时已经查了 ${st.hits.length} 次，再查容易被网站限制。过一会儿再接着查`);
  const gap = 2000 + Math.random() * 2000 - (now - (st.last || 0));
  if (gap > 0) await sleep(gap);
  st.last = Date.now(); st.hits.push(st.last);
  writeJson(STATE, st);
}

// ---------- 页面里跑的函数 ----------

// 查询页是 Vue 写的：找到持有结果列表的那个组件，读它已经解开的数据
function readResults(keyword) {
  let vm = null;
  const walk = c => { if (!c || vm) return; if (c.$data && 'journalList' in c.$data) { vm = c; return; } (c.$children || []).forEach(walk); };
  walk(document.querySelector('#app')?.__vue__);
  if (!vm) return { ready: false, app: !!document.querySelector('#app') };
  if (vm.journalListLoading || vm.search.keyword !== keyword) return { ready: false, app: true, vm: true };
  return { ready: true, total: vm.pagination.total, list: JSON.parse(JSON.stringify(vm.journalList)) };
}

// ---------- 查一本 ----------

const ISSN = /^\d{4}-?\d{3}[\dXx]$/;
const norm = s => String(s || '').toUpperCase().replace(/&/g, ' AND ').replace(/^THE\s+/, '').replace(/[^A-Z0-9一-鿿]/g, '');
const pct = v => v === '' || v == null || isNaN(Number(v)) ? null : Math.round(Number(v) * (Number(v) <= 1 ? 1000 : 10)) / 10; // 0.1536 → 15.4；11.06 → 11.1
// EI 那几行的 ISSN 写法不一样（71013 = 0007-1013），统一成 0000-0000
const fixIssn = s => { const d = String(s || '').replace(/[^0-9Xx]/g, '').toUpperCase(); return d && d.length <= 8 ? d.padStart(8, '0').replace(/^(\d{4})/, '$1-') : ''; };
const parse = s => { try { return typeof s === 'string' ? JSON.parse(s) : s; } catch { return null; } };

async function fetchList(b, keyword, type) {
  await pace();
  const url = `${BASE}/search?keywordType=${type}&keyword=${encodeURIComponent(keyword)}&pageNum=1`;
  try { await b.cmd('Page.navigate', { url }); } catch (e) { throw new Stop('unreachable', `iJournal 打不开：${e.message}`); }
  let r = {}, settled = 0;
  for (let i = 0; i < 50; i++) { // 最多等 20 秒；连续两次都是「加载完」才算数
    await sleep(400);
    r = await b.run(readResults, keyword).catch(() => ({}));
    settled = r.ready ? settled + 1 : 0;
    if (settled >= 2) return r;
  }
  if (!r.app) throw new Stop('unreachable', 'iJournal 打不开（20 秒内页面没出来），检查网络');
  throw new Stop('layout_changed', 'iJournal 页面改了：找不到结果列表，journal-rank 要更新');
}

function toItem(rows) {
  // 同一本刊的几行（SSCI 一行、SCIE 一行）字段不一定全，每项取第一行有值的
  const has = v => v !== '' && v != null && !(Array.isArray(v) && !v.length) && v !== '[]';
  const r = {}; for (const x of rows) for (const [k, v] of Object.entries(x)) if (!has(r[k]) && has(v)) r[k] = v;
  const jcr = parse(r.jcrJson) || [], jci = parse(r.jci_json) || [];
  return {
    title: r.journalTitle || null, cn_title: r.journalCnTitle || undefined, abbr: r.abbrJournal || undefined, issn: r.issn,
    databases: [...new Set(rows.map(x => x.journalDb).filter(Boolean))],
    impact_factor: r.impactFactor || null,
    jci: r.quote_factor || null,
    jcr: jcr.map(x => ({ category: x.category, edition: x.edition, quartile: x.jrcZone,
      jci_rank: (jci.find(y => y.small_sub === x.category) || {}).rank || undefined })),
    zone: r.subZone ? `${r.subZone}区` : null, zone_subject: r.subjectDcac || null,
    annual_articles: r.annualPublication || null,
    review_ratio_pct: pct(r.totalReviewRatio), oa_ratio_pct: pct(r.open_ratio), self_cite_pct: pct(r.selfCites),
    open_access: !!r.openAccess, domestic: !!r.isDomestic,
    publisher: r.publisherName || null,
    link: r.issn ? `${BASE}/journal/${r.issn}` : `${BASE}/search?keywordType=title&keyword=${encodeURIComponent(r.journalTitle)}`,
  };
}

async function lookup(b, q) {
  const isIssn = ISSN.test(q.trim());
  const key = isIssn ? q.trim().toUpperCase().replace(/^(\d{4})-?/, '$1-') : q.trim();
  const r = await fetchList(b, key, isIssn ? 'issn' : 'title');
  let list = (r.list || []).map(x => ({ ...x, issn: fixIssn(x.issn) }));
  const same = x => norm(x.journalTitle) === norm(key) || norm(x.abbrJournal) === norm(key) || (x.journalCnTitle && norm(x.journalCnTitle) === norm(key));
  // 网站按字面查：「and」和「&」查出来不一样，没对上就换另一种写法再查一次
  const alt = !isIssn && (/\band\b/i.test(key) ? key.replace(/\s+and\s+/gi, ' & ') : /&/.test(key) ? key.replace(/\s*&\s*/g, ' and ') : '');
  if (alt && !list.some(same)) list = list.concat(((await fetchList(b, alt, 'title')).list || []).map(x => ({ ...x, issn: fixIssn(x.issn) })));
  const hit = isIssn ? list.filter(x => x.issn === key)
    : list.filter(same);
  if (!hit.length) return { query: q, status: 'not_found', candidates: list.slice(0, 5).map(x => ({ title: x.journalTitle, issn: x.issn, database: x.journalDb })) };
  // 同一本刊在 SSCI、SCIE 各有一行，按 ISSN 合并；刊名一样但 ISSN 不同的（极少）分开列
  // 按 ISSN 查回来的行常常缺 JCR 学科，也查不到 EI 那一行（EI 的 ISSN 写法不一样），再按刊名查一次补上
  if (isIssn && hit.length) {
    const more = await fetchList(b, hit[0].journalTitle, 'title').catch(() => ({}));
    hit.push(...(more.list || []).filter(x => fixIssn(x.issn) === key).map(x => ({ ...x, issn: key })));
  }
  // EI 那一行常常没有 ISSN：并到同名、有 ISSN 的那组里
  const byIssn = {};
  for (const x of hit.filter(x => x.issn)) (byIssn[x.issn] = byIssn[x.issn] || []).push(x);
  for (const x of hit.filter(x => !x.issn)) {
    const g = Object.values(byIssn).find(g => g.some(y => norm(y.journalTitle) === norm(x.journalTitle)));
    if (g) g.push(x); else (byIssn['?' + norm(x.journalTitle)] = byIssn['?' + norm(x.journalTitle)] || []).push(x);
  }
  const groups = Object.values(byIssn);
  return groups.length === 1 ? { query: q, status: 'ok', ...toItem(groups[0]) } : { query: q, status: 'ok', note: '同名的有几本，看 ISSN 区分', matches: groups.map(toItem) };
}

// ---------- 自检 ----------

async function check(b) {
  const items = [], t = (name, ok, got) => items.push({ 项: name, 结果: ok ? '✓' : '✗', ...(ok ? {} : { 实际: got }) });
  const a = await lookup(b, '0360-1315'), c = await lookup(b, 'Computers & Education');
  t('按 ISSN 查到', a.status === 'ok', a.status);
  t('按刊名查到同一本', c.status === 'ok' && c.issn === '0360-1315', c.issn || c.status);
  t('刊名', /COMPUTERS & EDUCATION/i.test(a.title || ''), a.title);
  t('收录库（SSCI）', (a.databases || []).includes('SSCI'), a.databases);
  t('影响因子是数字', !isNaN(parseFloat(a.impact_factor)), a.impact_factor);
  t('JCR 学科和分区', (a.jcr || []).length > 0 && a.jcr.every(x => /^Q[1-4]$/.test(x.quartile) && x.category), a.jcr);
  t('分区', /^[1-4]区$/.test(a.zone || ''), a.zone);
  t('年发文量', Number(a.annual_articles) > 0, a.annual_articles);
  const n = await lookup(b, 'Journal That Does Not Exist Xyzzy');
  t('查不到时回 not_found', n.status === 'not_found', n.status);
  return { status: items.every(i => i.结果 === '✓') ? 'ok' : 'layout_changed', items };
}

function parseArgs(argv) {
  const pos = [], opt = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) { const k = argv[i].slice(2); opt[k] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true; }
    else pos.push(argv[i]);
  }
  return { pos, opt };
}

async function main() {
  const [cmd, ...rest] = process.argv.slice(2);
  const { pos, opt } = parseArgs(rest);
  if (!cmd || cmd === 'help' || opt.help) return { status: 'ok', usage: fs.readFileSync(new URL(import.meta.url), 'utf8').split('\n').slice(1).filter((l, i, all) => all.slice(0, i + 1).every(x => x.startsWith('//'))).map(l => l.replace(/^\/\/ ?/, '')).join('\n') };
  if (cmd === 'lookup' && !pos.length) throw new Stop('error', '要给刊名或 ISSN：lookup "Computers & Education" 0360-1315');
  if (!['lookup', 'check'].includes(cmd)) throw new Stop('error', `不认识的命令 ${cmd}。用 node journal-rank.mjs help 看用法`);
  const b = await connect();
  try {
    if (cmd === 'check') return await check(b);
    const items = [];
    for (const q of pos) items.push(await lookup(b, q));
    return { status: items.some(i => i.status === 'ok') ? 'ok' : 'not_found', source: 'iJournal（ijournal.topeditsci.com）', items };
  } finally { b.close(); }
}

main().then(r => { process.stdout.write(JSON.stringify(r, null, 1) + '\n'); if (!['ok', 'not_found'].includes(r.status)) process.exitCode = 1; }, e => {
  process.stdout.write(JSON.stringify({ status: e instanceof Stop ? e.status : 'error', msg: e.message, ...(e.extra || {}) }, null, 1) + '\n');
  process.exitCode = 1;
});
