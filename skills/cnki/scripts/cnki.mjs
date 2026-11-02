#!/usr/bin/env node
// 知网检索 / 核对 / 导出（乔淼PhD · AI学术训练营）。只用 Node 自带的东西（Node 18 以上），不装 npm 包。
//
// 做法：开一个单独资料的 Chrome（没有就用 Edge），学员在这个窗口里用自己的身份上知网；
// 脚本通过浏览器调试口，在知网页面里调用知网自己的检索 / 导出接口，拿回 JSON。不破解验证码、不绕登录。
//
//   node cnki.mjs open                                   打开知网（第一次用、要登录、要拖验证码时）
//   node cnki.mjs search "词" [--field 主题] [--years 2015-2025] [--core CSSCI,北大核心] [--type 期刊] [--page 1] [--size 20]
//   node cnki.mjs verify "篇名" [--author 第一作者] [--year 2024] [--journal 刊名]
//   node cnki.mjs detail <行号|条目编号|知网链接>...      行号指上一次 search 的第几条
//   node cnki.mjs export <行号|条目编号>... --to ris [--out 文件.ris] | --to zotero
//   node cnki.mjs check                                  自检：每个字段还取不取得到
//
// 输出一律是一段 JSON（UTF-8），status 只有这几种：
//   ok 成功 / not_found 没查到 / captcha 要拖验证码 / blocked 被知网拦了 / limit 本小时查太多了 /
//   layout_changed 知网页面改了、脚本要更新 / unreachable 知网打不开 / no_browser 没找到 Chrome 或 Edge / error 其他
import { spawn } from 'node:child_process';
import http from 'node:http';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const HOME = path.join(os.homedir(), '.cnki-skill');
const PROFILE = path.join(HOME, 'browser');
const STATE = path.join(HOME, 'state.json');
const LAST = path.join(HOME, 'last-search.json');
const PORT = Number(process.env.CNKI_PORT) || 19333;
const HOURLY_LIMIT = 150; // 一小时内最多发给知网的请求数，防止被当成机器人
const HOSTS = [ // 先国内站；证书错 / 打不开就换海外版
  { name: '国内站', base: 'https://kns.cnki.net', extra: '' },
  { name: '海外版', base: 'https://oversea.cnki.net', extra: '&language=CHS&uniplatform=OVERSEA' },
];
const FIELDS = { 主题: 'SU', 篇名: 'TI', 关键词: 'KY', 作者: 'AU', 来源: 'LY', 篇关摘: 'TKA', 摘要: 'AB', 全文: 'FT' };
const CORE = { 北大核心: 'P01', CSSCI: 'P0209', CSCD: 'P0210', EI: 'P0202', AMI: 'P13', WJCI: 'P12' };

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
  const target = pages.find(t => /cnki\.net/.test(t.url)) || pages[0] || await devtools('/json/new?about:blank', 'PUT');
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

// ---------- 节流：每次请求随机隔 2–5 秒，一小时有上限 ----------

async function pace(n = 1) {
  const st = readJson(STATE, {}), now = Date.now();
  st.hits = (st.hits || []).filter(t => now - t < 3600e3);
  if (st.hits.length + n > HOURLY_LIMIT) throw new Stop('limit', `这一小时已经查了 ${st.hits.length} 次知网，再查容易被当成机器人。过一会儿再接着查`);
  const gap = 2000 + Math.random() * 3000 - (now - (st.last || 0));
  if (gap > 0) await sleep(gap);
  st.last = Date.now(); st.hits.push(...Array(n).fill(st.last));
  writeJson(STATE, st);
}

// ---------- 页面里跑的函数 ----------

// 进结果页前装上：记下页面自己发的第一个检索请求，当模板用（这样国内站、海外版各自的参数都不用写死）
const HOOK = `(() => { const o = XMLHttpRequest.prototype.open, s = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.open = function (m, u) { this.__u = String(u); return o.apply(this, arguments); };
  XMLHttpRequest.prototype.send = function (b) { if (/brief\\/grid/.test(this.__u) && !window.__cnkiTpl && typeof b === 'string') { window.__cnkiTpl = b; window.__cnkiGrid = new URL(this.__u, location.href).href; } return s.apply(this, arguments); }; })()`;

function pageState() {
  const cap = document.querySelector('#tcaptcha_transform_dy, #tcaptcha_iframe, .tencent-captcha');
  const captcha = !!(cap && cap.getBoundingClientRect().top >= 0 && cap.getBoundingClientRect().height > 0) || /拖动下方拼图|完成验证|安全验证/.test(document.body?.innerText.slice(0, 3000) || '');
  return { url: location.href, title: document.title, ready: document.readyState, tpl: !!window.__cnkiTpl, captcha };
}

async function gridSearch(o) {
  const clean = s => (s || '').replace(/[­​-‏‪-‮⁠-⁯﻿]/g, '').replace(/\s+/g, ' ').trim();
  const P = new URLSearchParams(window.__cnkiTpl), Q = JSON.parse(P.get('QueryJson'));
  const subject = Q.QNode.QGroup.find(g => g.Key === 'Subject') || Q.QNode.QGroup[0];
  subject.Items = [{ Field: o.field, Value: o.query, Operator: o.field === 'SU' ? 'TOPRANK' : 'DEFAULT', Logic: 0, Vector: '', Title: o.fieldName }];
  subject.ChildItems = [];
  Q.QNode.QGroup = [subject];
  if (o.years) Q.QNode.QGroup.push({ Key: 'ControlGroup', Title: '', Logic: 0, Items: [], ChildItems: [{ Key: '.tit-startend-yearbox', Title: '', Logic: 0,
    Items: [{ Key: '.tit-startend-yearbox', Title: '出版年度', Logic: 0, Field: 'YE', Operator: 7, Value: String(o.years[0]), Value2: String(o.years[1]) }], ChildItems: [] }] });
  if (o.core.length) Q.QNode.QGroup.push({ Key: 'SCDBGroup', Title: '', Logic: 0, Items: [], ChildItems: [{ Key: 'LYBSM', Title: '', Logic: 0,
    Items: o.core.map(([name, code]) => ({ Key: code, Title: name, Logic: 1, Field: 'LYBSM', Operator: 'DEFAULT', Value: code, Value2: '', options: {}, Name: 'LYBSM', ExtendType: 0 })), ChildItems: [] }] });
  if (o.journal) {
    const tab = document.querySelector('a[name=classify][resource=JOURNAL]');
    if (!tab) return { status: 'layout_changed', msg: '结果页上找不到「学术期刊」分类' };
    Object.assign(Q, { Resource: 'JOURNAL', Classid: tab.getAttribute('classid'), KuaKuCode: '', Products: '' });
  }
  const post = async (pageNum, turnpage) => {
    const b = new URLSearchParams(P);
    b.set('QueryJson', JSON.stringify(Q)); b.set('aside', ''); b.set('pageSize', String(o.size));
    b.set('boolSearch', turnpage ? 'false' : 'true'); b.set('pageNum', String(pageNum)); b.set('CurPage', String(pageNum));
    if (turnpage) b.set('turnpage', turnpage);
    const r = await fetch(window.__cnkiGrid, { method: 'POST', credentials: 'include', body: b,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest' } });
    const text = await r.text();
    return { code: r.status, text, doc: new DOMParser().parseFromString(text, 'text/html') };
  };
  const check = res => {
    if (res.code === 418 || res.code === 403 || res.code === 429) return { status: 'blocked', msg: `知网拒绝了请求（HTTP ${res.code}），多半是被当成了机器人` };
    if (/tcaptcha|拖动下方拼图|安全验证/.test(res.text) && !res.doc.querySelector('#briefBox')) return { status: 'captcha', msg: '知网要拖验证码' };
    if (res.code !== 200) return { status: 'error', msg: `知网回了 HTTP ${res.code}` };
    if (!res.doc.querySelector('#briefBox')) return { status: 'layout_changed', msg: '检索结果的页面结构变了', sample: clean(res.doc.body?.textContent).slice(0, 200) };
    return null;
  };
  let res = await post(1);
  let bad = check(res); if (bad) return bad;
  if (o.page > 1) {
    const tp = res.doc.querySelector('#hidTurnPage')?.value;
    if (!tp) return { status: 'layout_changed', msg: '找不到翻页需要的 hidTurnPage' };
    res = await post(o.page, tp); bad = check(res); if (bad) return bad;
  }
  const d = res.doc;
  const total = Number(d.querySelector('#totalCnt')?.value || (d.querySelector('.pagerTitleCell')?.textContent.match(/[\d,]+/) || ['0'])[0].replace(/,/g, ''));
  const rows = [...d.querySelectorAll('.result-table-list tbody tr')].map(tr => {
    const a = tr.querySelector('td.name a.fz14');
    a?.querySelectorAll('.hrc').forEach(x => x.remove()); // 知网往标题里塞的「版权」「知网」字样
    const cell = c => clean(tr.querySelector('td.' + c)?.textContent);
    return { title: clean(a?.textContent), authors: cell('author'), source: cell('source'), date: cell('date'), type: cell('data'),
      cited: cell('quote'), downloads: cell('download'), id: tr.querySelector('input.cbItem')?.value || '', link: a?.href || '' };
  });
  if (total > 0 && (!rows.length || !rows[0].title || !rows[0].id)) return { status: 'layout_changed', msg: '结果行里取不到篇名或条目编号' };
  return { status: rows.length ? 'ok' : 'not_found', total, page: o.page, pages: Math.ceil(total / o.size), rows };
}

async function exportMeta(ids, uniplatform) {
  const out = [];
  for (const [i, id] of ids.entries()) {
    if (i) await new Promise(r => setTimeout(r, 800 + Math.random() * 700));
    const r = await fetch(new URL('/dm8/API/GetExport', location.href), { method: 'POST', credentials: 'include',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ filename: id, displaymode: 'GBTREFER,elearning,EndNote', uniplatform }) });
    if (r.status === 418 || r.status === 403 || r.status === 429) return { status: 'blocked', msg: `导出被知网拒绝（HTTP ${r.status}）`, done: out };
    let j; try { j = await r.json(); } catch { return { status: 'layout_changed', msg: '导出接口回的不是 JSON', done: out }; }
    const modes = {}; for (const m of j.data || []) modes[m.mode] = String(m.value?.[0] || '');
    out.push(j.code === 1 ? { id, ...modes } : { id, error: j.msg || '导出失败' });
  }
  return { status: 'ok', items: out };
}

// ---------- 打开结果页、拿模板 ----------

async function openResults(b, query) {
  const st = readJson(STATE, {});
  const order = st.host && Date.now() - (st.hostAt || 0) < 86400e3 ? [...HOSTS].sort((x, y) => (y.name === st.host) - (x.name === st.host)) : HOSTS;
  const tried = [];
  await b.cmd('Page.enable');
  const { identifier } = await b.cmd('Page.addScriptToEvaluateOnNewDocument', { source: HOOK });
  try {
    for (const h of order) {
      await pace();
      try { await b.cmd('Page.navigate', { url: `${h.base}/kns8s/defaultresult/index?kw=${encodeURIComponent(query)}&korder=SU${h.extra}` }); }
      catch (e) { tried.push(`${h.name}：${e.message}`); continue; }
      let s;
      for (let i = 0; i < 60; i++) {
        await sleep(500);
        try { s = await b.run(pageState); } catch { continue; }
        if (s.tpl || s.captcha || /^chrome-error:/.test(s.url) || (s.ready === 'complete' && i > 30)) break;
      }
      if (s?.captcha) { await waitCaptcha(b); s = await b.run(pageState); }
      if (s?.tpl) { writeJson(STATE, { ...readJson(STATE, {}), host: h.name, hostAt: Date.now() }); return h; }
      tried.push(`${h.name}：${/^chrome-error:/.test(s?.url || '') ? '打不开（' + (s.title || '网络或证书错误') + '）' : '页面加载了但没发出检索请求'}`);
    }
  } finally { await b.cmd('Page.removeScriptToEvaluateOnNewDocument', { identifier }).catch(() => {}); }
  throw new Stop(tried.some(t => /没发出/.test(t)) ? 'layout_changed' : 'unreachable', `知网检索页用不了：${tried.join('；')}`);
}

// 有验证码：把窗口提到前面，等学员拖完（最多 3 分钟）
async function waitCaptcha(b) {
  await b.cmd('Page.bringToFront').catch(() => {});
  process.stderr.write('知网要拖验证码：请在弹出的浏览器窗口里拖一下拼图，拖完脚本会自己接着做（最多等 3 分钟）\n');
  for (let i = 0; i < 90; i++) {
    await sleep(2000);
    const s = await b.run(pageState).catch(() => null);
    if (s && !s.captcha) return;
  }
  throw new Stop('captcha', '知网要拖验证码，3 分钟内没拖完。请在浏览器窗口里拖完后再运行一次');
}

async function ready(b, query) {
  const s = await b.run(pageState).catch(() => ({}));
  if (s.tpl && /cnki\.net/.test(s.url) && !s.captcha) return HOSTS.find(h => s.url.startsWith(h.base)) || HOSTS[0];
  return openResults(b, query);
}

async function search(b, o) {
  await ready(b, o.query);
  for (let attempt = 0; attempt < 2; attempt++) {
    await pace(o.page > 1 ? 2 : 1);
    const r = await b.run(gridSearch, o);
    if (r.status !== 'captcha') return r;
    if (attempt) break;
    await openResults(b, o.query); // 让验证码在页面上露出来，等学员拖完再查一次
  }
  throw new Stop('captcha', '知网要拖验证码，拖完了还是不让查。过一会儿再试');
}

async function exportIds(b, ids) {
  await ready(b, '知网');
  const uni = await b.run(() => new URLSearchParams(window.__cnkiTpl).get('uniplatform') || 'NZKPT');
  await pace(ids.length);
  const r = await b.run(exportMeta, ids, uni);
  if (r.status !== 'ok') throw new Stop(r.status, r.msg);
  return r.items.map(parseExport);
}

// 导出接口给的 EndNote / 题录文本 → 结构化字段
function parseExport(x) {
  if (x.error) return { id: x.id, error: x.error };
  const lines = s => (s || '').split(/<br\s*\/?>/i).map(l => l.trim()).filter(Boolean);
  const en = {}; for (const l of lines(x.ENDNOTE)) { const m = l.match(/^%(\S)\s?(.*)$/); if (m) (en[m[1]] ||= []).push(m[2].trim()); }
  const el = {}; for (const l of lines(x.ELEARNING)) { const m = l.match(/^([A-Za-z]+)-[^:：]*[:：]\s*(.*)$/); if (m) el[m[1]] = m[2].trim(); }
  const one = k => (en[k] || [])[0] || '';
  const pub = el.PubTime || ''; // 上网 / 出版时间；年份要用刊期年（%D、Year），网络首发的两者常差一年
  return {
    id: x.id, type: one('0') || el.SrcDatabase || '', title: one('T') || el.Title || '',
    authors: (en.A || []).length ? en.A : (el.Author || '').split(/[;；]/).map(s => s.trim()).filter(Boolean),
    journal: one('J') || el.Source || '', year: one('D') || el.Year || (pub.match(/\d{4}/) || [''])[0], online: pub,
    volume: one('V') || el.Roll || '', issue: one('N') || el.Period || '', pages: one('P') || el.Page || '',
    keywords: (one('K') || el.Keyword || '').split(/[;；]/).map(s => s.trim()).filter(Boolean),
    abstract: one('X') || el.Summary || '', affiliations: one('+') || el.Organ || '',
    doi: one('R'), issn: one('@'), cn: one('L'), publisher: one('I'), link: one('U') || el.Link || '',
    citation: (x.GBTREFER || '').replace(/<br\s*\/?>/gi, '').trim(),
  };
}

function toRis(m) {
  const TY = { 'Journal Article': 'JOUR', Thesis: 'THES', 'Conference Proceedings': 'CONF', 'Newspaper Article': 'NEWS', Book: 'BOOK', 'Book Section': 'CHAP', Patent: 'PAT', Report: 'RPRT' };
  const L = [['TY', TY[m.type] || 'JOUR'], ['TI', m.title], ...m.authors.map(a => ['AU', a]), ['T2', m.journal], ['PY', m.year],
    ['VL', m.volume], ['IS', m.issue], ['SP', m.pages.split(/[-–~]/)[0]], ['EP', m.pages.split(/[-–~]/)[1]], ...m.keywords.map(k => ['KW', k]), ['AB', m.abstract], ['AD', m.affiliations],
    ['DO', m.doi], ['SN', m.issn], ['PB', m.publisher], ['UR', m.link], ['DB', 'CNKI'], ['LA', 'chi']];
  return L.filter(([, v]) => v).map(([k, v]) => `${k}  - ${String(v).replace(/\s+/g, ' ')}`).join('\r\n') + '\r\nER  - \r\n';
}

// ---------- 命令 ----------

function parseArgs(argv) {
  const pos = [], opt = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) { const k = argv[i].slice(2); opt[k] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true; }
    else pos.push(argv[i]);
  }
  return { pos, opt };
}

function searchOptions(query, opt) {
  const fieldName = opt.field || '主题', field = FIELDS[fieldName] || (Object.values(FIELDS).includes(String(fieldName).toUpperCase()) ? String(fieldName).toUpperCase() : null);
  if (!field) throw new Stop('error', `--field 只能是：${Object.keys(FIELDS).join(' / ')}`);
  let years = null;
  if (opt.years) { const m = String(opt.years).match(/^(\d{4})\s*[-–~至到]\s*(\d{4})?$|^(\d{4})$/); if (!m) throw new Stop('error', '--years 写成 2015-2025 或 2024'); years = m[3] ? [m[3], m[3]] : [m[1], m[2] || String(new Date().getFullYear())]; }
  const core = opt.core ? String(opt.core).split(/[,，、\s]+/).filter(Boolean).map(n => { const k = Object.keys(CORE).find(c => c.toLowerCase() === n.toLowerCase()); if (!k) throw new Stop('error', `--core 只能是：${Object.keys(CORE).join(' / ')}`); return [k, CORE[k]]; }) : [];
  const size = Math.min(50, Math.max(1, Number(opt.size) || 20)), page = Math.max(1, Number(opt.page) || 1);
  return { query, field, fieldName, years, core, journal: opt.type === '期刊' || opt.type === 'journal', size, page };
}

// 行号（上一次 search 的第几条）→ 条目编号
function resolveIds(refs) {
  const last = readJson(LAST, null);
  return refs.flatMap(r => String(r).split(/[,，\s]+/)).filter(Boolean).map(r => {
    if (/^\d{1,3}$/.test(r)) {
      const row = last?.rows?.[Number(r) - 1];
      if (!row) throw new Stop('error', `上一次搜索结果里没有第 ${r} 条（先 search，再用行号；或者直接给条目编号）`);
      return row.id;
    }
    return r;
  });
}

const norm = s => (s || '').replace(/[­​-‏‪-‮⁠-⁯﻿]/g, '').normalize('NFKC').toLowerCase().replace(/[\s\p{P}\p{S}]/gu, '');

async function verify(b, title, opt) {
  const r = await search(b, searchOptions(title, { field: '篇名', size: 20 }));
  const want = norm(title);
  const cands = (r.rows || []).filter(x => { const t = norm(x.title); return t === want || (t.length && want.length && (t.includes(want) || want.includes(t)) && Math.min(t.length, want.length) / Math.max(t.length, want.length) > 0.85); })
    .sort((x, y) => (norm(y.title) === want) - (norm(x.title) === want)).slice(0, 3);
  if (!cands.length) return { status: 'not_found', verdict: '没找到', msg: `知网按篇名查「${title}」没有篇名对得上的（共 ${r.total || 0} 条相近结果）`, nearest: (r.rows || []).slice(0, 3).map(x => ({ title: x.title, authors: x.authors, source: x.source, date: x.date })) };
  const metas = await exportIds(b, cands.map(c => c.id));
  const checks = metas.map((m, i) => {
    const diff = [];
    if (norm(m.title) !== want) diff.push(`篇名有差别：知网是「${m.title}」`);
    if (opt.author && !m.authors.some(a => norm(a) === norm(opt.author))) diff.push(`作者里没有「${opt.author}」（知网：${m.authors.join('；')}）`);
    else if (opt.author && norm(m.authors[0]) !== norm(opt.author)) diff.push(`「${opt.author}」不是第一作者（知网第一作者：${m.authors[0]}）`);
    if (opt.year && m.year && String(opt.year) !== m.year) diff.push(`年份不同：知网是 ${m.year}`);
    if (opt.journal && norm(opt.journal) !== norm(m.journal)) diff.push(`刊名不同：知网是「${m.journal}」`);
    return { ...m, cited: cands[i].cited, downloads: cands[i].downloads, diff };
  }).sort((x, y) => x.diff.length - y.diff.length);
  const best = checks[0];
  const brief = ({ abstract, ...m }) => m; // 核对用不着摘要，省篇幅
  return { status: 'ok', verdict: best.diff.length ? '有出入' : '对上', diff: best.diff, match: brief(best), others: checks.slice(1).map(brief) };
}

async function check(b) {
  const items = [];
  const t = (name, ok, note = '') => items.push({ 项: name, 结果: ok ? '✓' : '✗', 说明: note });
  const r = await search(b, searchOptions('人工智能', { years: '2023-2024', core: 'CSSCI', type: '期刊', size: 5 }));
  t('检索', r.status === 'ok', `共 ${r.total} 条`);
  const row = r.rows?.[0] || {};
  for (const [k, n] of [['title', '篇名'], ['authors', '作者'], ['source', '来源'], ['date', '日期'], ['id', '条目编号'], ['link', '链接']]) t(`结果行·${n}`, !!row[k], String(row[k] || '').slice(0, 40));
  const p2 = await search(b, searchOptions('人工智能', { size: 5, page: 2 }));
  t('翻页', p2.status === 'ok' && p2.page === 2 && p2.rows[0]?.title !== row.title, `第 ${p2.page} 页`);
  if (row.id) {
    const [m] = await exportIds(b, [row.id]);
    for (const [k, n] of [['title', '篇名'], ['authors', '作者'], ['journal', '刊名'], ['year', '年份'], ['abstract', '摘要'], ['citation', 'GB/T 引文']]) t(`导出·${n}`, !!(Array.isArray(m[k]) ? m[k].length : m[k]), String(Array.isArray(m[k]) ? m[k].join('；') : m[k] || '').slice(0, 40));
    t('导出·篇名和结果行一致', norm(m.title) === norm(row.title));
    t('年份筛选（按刊期年）', /^202[34]$/.test(m.year), m.year);
  }
  const host = readJson(STATE, {}).host;
  return { status: items.every(i => i.结果 === '✓') ? 'ok' : 'layout_changed', host, items };
}

async function main() {
  const [cmd, ...rest] = process.argv.slice(2);
  const { pos, opt } = parseArgs(rest);
  if (!cmd || cmd === 'help' || opt.help) return { status: 'ok', usage: fs.readFileSync(new URL(import.meta.url), 'utf8').split('\n').slice(1).filter((l, i, all) => all.slice(0, i + 1).every(x => x.startsWith('//'))).map(l => l.replace(/^\/\/ ?/, '')).join('\n') };
  const so = cmd === 'search' && pos[0] ? searchOptions(pos.join(' '), opt) : null; // 参数先检查，错了不用开浏览器
  const b = await connect();
  try {
    if (cmd === 'open') {
      await openResults(b, '人工智能');
      await b.cmd('Page.bringToFront').catch(() => {});
      return { status: 'ok', host: readJson(STATE, {}).host, msg: '知网已在浏览器窗口里打开。要登录的话在这个窗口里登录，以后会记住' };
    }
    if (cmd === 'search') {
      if (!pos[0]) throw new Stop('error', '要给检索词：search "词"');
      const r = await search(b, so);
      if (r.status === 'ok') writeJson(LAST, { query: pos.join(' '), at: new Date().toISOString(), rows: r.rows });
      return { ...r, host: readJson(STATE, {}).host, rows: (r.rows || []).map((x, i) => ({ n: i + 1, ...x })) };
    }
    if (cmd === 'verify') {
      if (!pos[0]) throw new Stop('error', '要给篇名：verify "篇名"');
      return { ...(await verify(b, pos.join(' '), opt)), host: readJson(STATE, {}).host };
    }
    if (cmd === 'detail' || cmd === 'export') {
      const links = pos.filter(p => /^https?:/.test(p)), ids = resolveIds(pos.filter(p => !/^https?:/.test(p)));
      for (const url of links) { // 知网详情页链接：打开页面读它的条目编号
        await pace(); await b.cmd('Page.navigate', { url });
        let id = '';
        for (let i = 0; i < 40 && !id; i++) { await sleep(500); id = await b.run(() => document.querySelector('#export-id')?.value || '').catch(() => ''); }
        if (!id) throw new Stop((await b.run(pageState).catch(() => ({}))).captcha ? 'captcha' : 'layout_changed', `详情页上取不到条目编号：${url}`);
        ids.push(id);
      }
      if (!ids.length) throw new Stop('error', '要给行号、条目编号或知网链接');
      const metas = await exportIds(b, ids);
      if (cmd === 'detail') return { status: 'ok', items: metas };
      const good = metas.filter(m => !m.error), ris = good.map(toRis).join('\r\n');
      if (opt.to === 'zotero') {
        const r = await fetch('http://127.0.0.1:23119/connector/import', { method: 'POST', headers: { 'Content-Type': 'application/x-research-info-systems' }, body: ris })
          .catch(() => { throw new Stop('error', 'Zotero 没开（连不上 127.0.0.1:23119）。打开 Zotero 桌面版再试，或者改用 --to ris'); });
        if (r.status !== 201 && r.status !== 200) throw new Stop('error', `Zotero 没收下（HTTP ${r.status}）：${(await r.text()).slice(0, 200)}`);
        return { status: 'ok', to: 'zotero', count: good.length, msg: '已导入 Zotero 当前选中的分类', failed: metas.filter(m => m.error) };
      }
      const out = path.resolve(typeof opt.out === 'string' ? opt.out : `知网导出-${new Date().toISOString().slice(0, 10)}.ris`);
      fs.writeFileSync(out, '﻿' + ris);
      return { status: 'ok', to: 'ris', file: out, count: good.length, failed: metas.filter(m => m.error) };
    }
    if (cmd === 'check') return await check(b);
    throw new Stop('error', `不认识的命令 ${cmd}。用 node cnki.mjs help 看用法`);
  } finally { b.close(); }
}

main().then(r => { process.stdout.write(JSON.stringify(r, null, 1) + '\n'); if (!['ok', 'not_found'].includes(r.status)) process.exitCode = 1; }, e => {
  process.stdout.write(JSON.stringify({ status: e instanceof Stop ? e.status : 'error', msg: e.message, ...(e.extra || {}) }, null, 1) + '\n');
  process.exitCode = 1;
});
