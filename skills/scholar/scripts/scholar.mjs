#!/usr/bin/env node
// 谷歌学术检索、被引追踪、导出（乔淼PhD · AI学术训练营）。只用 Node 自带的东西（Node 18 以上）。
//
// 在单独资料的 Chrome（没有就用 Edge）里打开谷歌学术的结果页，读页面已经显示出来的结果。
// 浏览器和 cnki、journal-rank 共用一个（~/.cnki-skill/browser），各用各的标签页。不用账号。
//
//   node scholar.mjs search "检索词" [--author 作者] [--journal 刊名] [--years 2020-2025] [--title-only] [--exact "精确短语"] [--exclude "不要的词"] [--sort date] [--page 1] [--size 20]
//   node scholar.mjs cited-by <行号或 cites 编号> [--years 2020-2025] [--page 1] [--size 20]     谁引了这篇
//   node scholar.mjs export <行号或 cid>... --to bib|zotero [--out 文件]                         行号是上一次 search / cited-by 的第几条
//   node scholar.mjs open                                                                         打开谷歌学术窗口（点验证码时用）
//   node scholar.mjs check                                                                        自检
//   以上都可以加 --new-network：被拦以后换了网络（比如手机热点），用它跳过 3 小时冷却
//
// 30 分钟内同样的 search / cited-by（同样的词、参数、页码）直接回上次的结果（cached: true），不再打开谷歌。
// 被拦（blocked）以后 3 小时内不再打开谷歌，直接回 blocked：每次再去都可能让封锁更久。
//
// 输出一律是一段 JSON（UTF-8），status 只有这几种：
//   ok 成功 / not_found 没查到 / captcha 要点验证码、等了 3 分钟没点完 / blocked 被谷歌拦了（或还在冷却）/ limit 这一小时查太多了 /
//   unreachable 打不开（国内没开代理多半是这个）/ layout_changed 页面改了、脚本要更新 / no_browser 没找到 Chrome 或 Edge / error 其他
import { spawn } from 'node:child_process';
import http from 'node:http';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const HOME = path.join(os.homedir(), '.cnki-skill');
const PROFILE = path.join(HOME, 'browser');
// 记录放 ~/.cnki-skill；写不了就放临时文件夹
const DATA = (() => {
  for (const d of [HOME, path.join(os.tmpdir(), 'cnki-skill')]) {
    try { fs.mkdirSync(d, { recursive: true }); fs.writeFileSync(path.join(d, '.w'), ''); return d; } catch {}
  }
  return HOME;
})();
const STATE = path.join(DATA, 'scholar-state.json'), LAST = path.join(DATA, 'scholar-last.json'), CACHE = path.join(DATA, 'scholar-cache.json');
const PORT = Number(process.env.CNKI_PORT) || 19333;
const HOURLY_LIMIT = 60; // 谷歌比知网敏感得多：一小时最多打开这么多页，每页隔 5–10 秒
const CACHE_MIN = 30;    // 同样的检索 30 分钟内不重开：AI 截断了输出又跑一遍时，不多开一页、不多弹一次验证码（11-10 实测出现过）
const COOLDOWN_H = 3;    // 被拦以后这么久不再去：乔淼家里网络被拦了一天以上，期间每次去都是白撞（11-09、11-10 实测）
const BASE = 'https://scholar.google.com';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const readJson = (f, d) => { try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch { return d; } };
const writeJson = (f, v) => { fs.mkdirSync(DATA, { recursive: true }); fs.writeFileSync(f, JSON.stringify(v, null, 1)); };
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

// 沙箱里开不起浏览器（建不了资料文件夹、Chrome 起来就退，11-07 实测）：POPPER 在沙箱外替它开（内容 1.5.2）
const IN_POPPER = '如果是在 AI学术工作站（POPPER）里让 AI 跑的：AI 的沙箱里开不了浏览器，请到 POPPER 左下角「AI学术环境配置」→「大家共用的」→「检索浏览器」点「打开」，再让 AI 重试（AI 别自己想办法开）。';
async function ensureBrowser() {
  // POPPER 交任务时可能刚替它开了浏览器，多等两三秒
  for (let i = 0; i < 6; i++) { try { await devtools('/json/version'); return; } catch {} if (i < 5) await sleep(500); }
  const exe = findBrowser();
  if (!exe) throw new Stop('no_browser', '没找到 Chrome 或 Edge。装一个 Chrome，或者设环境变量 CNKI_BROWSER 指向浏览器程序');
  try { fs.mkdirSync(PROFILE, { recursive: true }); } catch (e) { throw new Stop('no_browser', `建不了浏览器资料文件夹 ${PROFILE}（${e.code || e.message}）。` + IN_POPPER); }
  // 单独一份资料：不碰学员日常浏览器；新版 Chrome 也只许在非默认资料上开调试口
  spawn(exe, [`--user-data-dir=${PROFILE}`, `--remote-debugging-port=${PORT}`, '--no-first-run', '--no-default-browser-check', 'about:blank'],
    { detached: true, stdio: 'ignore' }).on('error', () => {}).unref();
  for (let i = 0; i < 60; i++) { await sleep(250); try { await devtools('/json/version'); return; } catch {} }
  throw new Stop('no_browser', `浏览器开了但连不上调试口（端口 ${PORT}）。` + IN_POPPER + `自己在终端里跑的：关掉这个浏览器窗口再试；端口被占用的话设环境变量 CNKI_PORT 换一个`);
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
  const target = pages.find(t => /scholar\.google|\/sorry\//.test(t.url)) || await devtools('/json/new?about:blank', 'PUT'); // 自己开一个标签页，不占知网、查期刊的
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

// ---------- 节流 ----------

async function pace() {
  const st = readJson(STATE, {}), now = Date.now();
  st.hits = (st.hits || []).filter(t => now - t < 3600e3);
  if (st.hits.length >= HOURLY_LIMIT) throw new Stop('limit', `这一小时已经开了 ${st.hits.length} 页谷歌学术，再查容易被拦。过一会儿再接着查`);
  const gap = 5000 + Math.random() * 5000 - (now - (st.last || 0));
  if (gap > 0) await sleep(gap);
  st.last = Date.now(); st.hits.push(st.last);
  writeJson(STATE, st);
}

// 被拦后的冷却：换了网络就加 --new-network
function coolDown(newNetwork) {
  const st = readJson(STATE, {});
  if (!st.blocked) return;
  if (newNetwork) { delete st.blocked; writeJson(STATE, st); return; }
  const until = st.blocked + COOLDOWN_H * 3600e3;
  if (Date.now() >= until) return;
  const hm = t => new Date(t).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', hour12: false });
  throw new Stop('blocked', `谷歌 ${hm(st.blocked)} 拦过这个网络，${hm(until)} 以前不再去查（每次再去都可能让封锁更久），这次没有打开谷歌。换了网络（比如手机热点）的话，加 --new-network 再跑`, { cooldown_until: new Date(until).toISOString() });
}
function markBlocked(on) {
  const st = readJson(STATE, {});
  if (on) st.blocked = Date.now(); else if (st.blocked) delete st.blocked; else return;
  writeJson(STATE, st);
}

// 同样的检索 30 分钟内直接回上次的结果
const cacheKey = (kind, params) => kind + ' ' + JSON.stringify(Object.keys(params).sort().map(k => [k, params[k]]));
function cacheGet(key) {
  const e = readJson(CACHE, {})[key];
  return e && Date.now() - e.at < CACHE_MIN * 60e3 ? e : null;
}
function cachePut(key, result, meta) {
  const c = readJson(CACHE, {}), now = Date.now();
  for (const k of Object.keys(c)) if (now - c[k].at >= CACHE_MIN * 60e3) delete c[k];
  c[key] = { at: now, meta, result };
  writeJson(CACHE, c);
}

// ---------- 页面里跑的函数 ----------

function pageState() {
  const text = document.body?.innerText.slice(0, 3000) || '';
  const form = !!document.querySelector('#gs_captcha_f, #gs_captcha_ccl, #captcha-form, iframe[src*="recaptcha"], .g-recaptcha');
  const robot = /unusual traffic|not a robot|automated queries|异常流量|不是自动程序/i.test(text);
  return { url: location.href, title: document.title, ready: document.readyState, captcha: form, robot: robot || /\/sorry\//.test(location.href),
    results: !!document.querySelector('#gs_res_ccl_mid'), plain: document.contentType === 'text/plain' };
}

function readRows() {
  const clean = s => (s || '').replace(/\s+/g, ' ').trim();
  const rows = [...document.querySelectorAll('#gs_res_ccl_mid .gs_r.gs_or.gs_scl')].map(r => {
    const h = r.querySelector('.gs_rt'), a = h?.querySelector('a'), tag = h?.querySelector('.gs_ct1')?.textContent;
    const box = h?.cloneNode(true); box?.querySelectorAll('.gs_ctc, .gs_ct1, .gs_ct2, .gs_ctu').forEach(x => x.remove());
    const meta = clean(r.querySelector('.gs_a')?.textContent).replace(/ /g, ' '), parts = meta.split(/\s+-\s+/);
    const venueYear = parts.length >= 3 ? parts.slice(1, -1).join(' - ') : (parts[1] || '');
    const year = (venueYear.match(/\b(19|20)\d{2}\b(?!.*\b(19|20)\d{2}\b)/) || [''])[0];
    const cite = [...r.querySelectorAll('.gs_fl a')].find(x => /[?&]cites=\d+/.test(x.href));
    return { title: clean(box?.textContent), type: clean(tag).replace(/[\[\]]/g, ''), authors: clean(parts[0]), venue: clean(venueYear.replace(/,?\s*(19|20)\d{2}\s*$/, '')), year,
      publisher: parts.length >= 3 ? clean(parts[parts.length - 1]) : '', snippet: clean(r.querySelector('.gs_rs')?.textContent),
      cited: cite ? Number((cite.textContent.match(/\d+/) || ['0'])[0]) : 0, cites_id: cite ? cite.href.match(/[?&]cites=(\d+)/)[1] : '',
      cid: r.getAttribute('data-cid') || '', link: a?.href || '', fulltext: r.querySelector('.gs_or_ggsm a')?.href || '' };
  });
  const m = clean(document.querySelector('#gs_ab_md')?.textContent).match(/([\d,]+)\s+results?/i);
  return { rows, total: m ? Number(m[1].replace(/,/g, '')) : rows.length, empty: /did not match any articles/i.test(document.body?.innerText || '') };
}

// ---------- 打开一页 ----------

async function open_(b, url) {
  await pace();
  try { await b.cmd('Page.navigate', { url }); } catch (e) { throw new Stop('unreachable', `谷歌学术打不开：${e.message}`); }
  let s;
  for (let i = 0; i < 60; i++) {
    await sleep(500);
    s = await b.run(pageState).catch(() => null);
    if (s && (s.captcha || s.robot || /^chrome-error:/.test(s.url) || (s.ready === 'complete' && (s.results || s.plain || i > 12)))) break;
  }
  if (!s || /^chrome-error:/.test(s.url)) throw new Stop('unreachable', '谷歌学术打不开。国内网络要先开代理；代理开着的话，看这个浏览器窗口里能不能打开 scholar.google.com');
  if (s.captcha) s = await waitCaptcha(b);
  else if (s.robot) {
    markBlocked(true);
    throw new Stop('blocked', `谷歌把这个网络当成了自动程序，这次没给验证码。这种封锁常常要几小时到一天以上，接下来 ${COOLDOWN_H} 小时脚本不再去查；换个网络（比如手机热点）通常就能用，换了以后加 --new-network。不要连续重试`);
  }
  markBlocked(false);
  return s;
}

async function waitCaptcha(b) {
  await b.cmd('Page.bringToFront').catch(() => {});
  process.stderr.write('谷歌学术要点验证码：请在弹出的浏览器窗口里点一下，点完脚本会自己接着做（最多等 3 分钟）\n');
  for (let i = 0; i < 90; i++) {
    await sleep(2000);
    const s = await b.run(pageState).catch(() => null);
    if (s && !s.captcha && !s.robot && s.ready === 'complete') return s;
  }
  throw new Stop('captcha', '谷歌学术要点验证码，3 分钟内没点完。请在浏览器窗口里点完后再运行一次');
}

// B 是按需打开的浏览器：命中缓存时不用开
async function list(B, params, meta, { useCache = true } = {}) {
  const key = cacheKey('list', params), hit = useCache && cacheGet(key);
  if (hit) {
    if (hit.result.rows.length) writeJson(LAST, { ...hit.meta, at: new Date(hit.at).toISOString(), rows: hit.result.rows }); // 行号照样能接着用
    return { ...hit.result, cached: true, msg: `${CACHE_MIN} 分钟内查过同样的，直接用的上次结果（${new Date(hit.at).toLocaleTimeString('zh-CN', { hour12: false })}），没有再打开谷歌` };
  }
  const b = await B.get();
  const q = new URLSearchParams({ hl: 'en', ...params });
  const s = await open_(b, `${BASE}/scholar?${q}`);
  const r = await b.run(readRows);
  if (r.rows.length && !r.rows[0].title) throw new Stop('layout_changed', '结果行里取不到篇名');
  if (!r.rows.length && !r.empty && !s.results) throw new Stop('layout_changed', `结果页的结构变了（标题：${s.title}）`);
  const rows = r.rows.map((x, i) => ({ n: i + 1, ...x }));
  if (rows.length) writeJson(LAST, { ...meta, at: new Date().toISOString(), rows });
  const result = { status: rows.length ? 'ok' : 'not_found', total: r.total, page: meta.page, rows };
  if (useCache) cachePut(key, result, meta);
  return result;
}

// ---------- 导出 ----------

// 只取 BibTeX：RefMan（RIS）那个链接是下载，会往下载文件夹里丢文件、页面上读不到（11-09 实测）
async function exportOne(b, cid) {
  await open_(b, `${BASE}/scholar?${new URLSearchParams({ q: `info:${cid}:scholar.google.com/`, output: 'cite', scirp: '0', hl: 'en' })}`);
  const href = await b.run(() => [...document.querySelectorAll('#gs_citi a, a.gs_citi')].find(a => a.textContent.trim() === 'BibTeX')?.href || '');
  if (!href) throw new Stop('layout_changed', '引用框里找不到 BibTeX 链接');
  await open_(b, href);
  const text = await b.run(() => document.body?.innerText || '');
  if (!/^\s*@\w+\s*\{/.test(text)) throw new Stop('layout_changed', `BibTeX 内容不对：${text.slice(0, 80)}`);
  return text.trim();
}

// ---------- 命令 ----------

function parseArgs(argv) {
  const pos = [], opt = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) { const k = argv[i].slice(2); opt[k] = !['title-only', 'new-network'].includes(k) && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true; } // 这两个不带值
    else pos.push(argv[i]);
  }
  return { pos, opt };
}

function paging(opt) {
  const size = Math.min(20, Math.max(1, Number(opt.size) || 20)), page = Math.max(1, Number(opt.page) || 1);
  const out = { num: String(size), ...(page > 1 ? { start: String((page - 1) * size) } : {}) };
  if (opt.years) {
    const m = String(opt.years).match(/^(\d{4})\s*[-–~至到]\s*(\d{4})?$|^(\d{4})$/);
    if (!m) throw new Stop('error', '--years 写成 2015-2025 或 2024');
    out.as_ylo = m[3] || m[1]; out.as_yhi = m[3] || m[2] || String(new Date().getFullYear());
  }
  return { out, page };
}

function searchParams(query, opt) {
  const { out, page } = paging(opt);
  // 检索词写进 q（和在搜索框里打的一样）：高级检索的 as_epq、as_occt 在没有 as_q 时会被忽略，回一堆不相干的；
  // 作者、刊名单独放参数：写进 q 的 author: / source: 会让 allintitle 失效（都是 11-09 实测）
  const has = v => typeof v === 'string' && v.trim();
  const words = [query, has(opt.exact) && `"${opt.exact.replace(/"/g, '')}"`, ...(has(opt.exclude) ? opt.exclude.trim().split(/\s+/).map(w => '-' + w) : [])].filter(Boolean).join(' ');
  if (has(opt.author)) out.as_sauthors = opt.author.trim();
  if (has(opt.journal)) out.as_publication = opt.journal.trim();
  if (!words && !out.as_sauthors && !out.as_publication) throw new Stop('error', '要给检索词：search "词"');
  const q = words && opt['title-only'] ? 'allintitle: ' + words : words;
  out.q = q || [out.as_sauthors && `author:"${out.as_sauthors}"`, out.as_publication && `source:"${out.as_publication}"`].filter(Boolean).join(' '); // 只给作者或刊名、没有检索词时，单放参数查不出东西
  if (!q) { delete out.as_sauthors; delete out.as_publication; }
  if (opt.sort === 'date') { out.scisbd = '1'; delete out.as_ylo; delete out.as_yhi; }
  else if (opt.sort && opt.sort !== 'relevance') throw new Stop('error', '--sort 只能是 relevance 或 date');
  return { params: out, page };
}

function fromLast(ref, field) {
  if (!/^\d{1,3}$/.test(ref)) return ref;
  const row = readJson(LAST, null)?.rows?.[Number(ref) - 1];
  if (!row) throw new Stop('error', `上一次结果里没有第 ${ref} 条（先 search，再用行号）`);
  if (!row[field]) throw new Stop('error', field === 'cites_id' ? `第 ${ref} 条还没有人引用` : `第 ${ref} 条取不到编号`);
  return row[field];
}

async function check(B) {
  const items = [], t = (name, ok, note = '') => items.push({ 项: name, 结果: ok ? '✓' : '✗', 说明: String(note).slice(0, 60) });
  const s = searchParams('cognitive load theory', { years: '2015-2024', size: '10' });
  const nc = { useCache: false }, b = await B.get();
  const r = await list(B, s.params, { query: 'check', page: 1 }, nc);
  t('检索', r.status === 'ok', `共 ${r.total} 条`);
  const row = r.rows[0] || {};
  for (const [k, n] of [['title', '篇名'], ['authors', '作者'], ['year', '年份'], ['cid', '编号'], ['link', '链接'], ['snippet', '摘要片段']]) t(`结果行·${n}`, !!row[k], row[k]);
  const yrs = r.rows.filter(x => x.year).every(x => x.year >= '2015' && x.year <= '2024'); t('年份筛选', yrs, r.rows.map(x => x.year).join(' '));
  const c = r.rows.find(x => x.cites_id); t('被引数', !!c, c ? c.cited : '');
  const p2 = await list(B, searchParams('cognitive load theory', { years: '2015-2024', size: '10', page: '2' }).params, { query: 'check', page: 2 }, nc);
  t('翻页', p2.status === 'ok' && p2.rows[0]?.cid !== row.cid);
  if (c) { const cb = await list(B, { ...paging({ size: '10' }).out, cites: c.cites_id }, { query: 'check', page: 1 }, nc); t('谁引了这篇', cb.status === 'ok', `共 ${cb.total} 条`); }
  if (row.cid) { const bib = await exportOne(b, row.cid); t('导出 BibTeX', /^@\w+\{/.test(bib), bib.slice(0, 40)); }
  return { status: items.every(i => i.结果 === '✓') ? 'ok' : 'layout_changed', items };
}

async function main() {
  const [cmd, ...rest] = process.argv.slice(2);
  const { pos, opt } = parseArgs(rest);
  if (!cmd || cmd === 'help' || opt.help) return { status: 'ok', usage: fs.readFileSync(new URL(import.meta.url), 'utf8').split('\n').slice(1).filter((l, i, all) => all.slice(0, i + 1).every(x => x.startsWith('//'))).map(l => l.replace(/^\/\/ ?/, '')).join('\n') };
  const so = cmd === 'search' ? searchParams(pos.join(' '), opt) : null; // 参数先检查，错了不用开浏览器
  // 浏览器用到才开；开之前先看冷却（open 是用户自己要看窗口，不拦）
  let conn = null;
  const B = { get: () => conn ||= (async () => {
    if (cmd !== 'open') coolDown(!!opt['new-network']);
    const b = await connect(); await b.cmd('Page.enable'); return b;
  })() };
  if (opt['new-network']) coolDown(true);
  try {
    if (cmd === 'open') { const b = await B.get(); await open_(b, `${BASE}/?hl=en`); await b.cmd('Page.bringToFront').catch(() => {}); return { status: 'ok', msg: '谷歌学术已在浏览器窗口里打开' }; }
    if (cmd === 'search') return await list(B, so.params, { query: pos.join(' '), page: so.page });
    if (cmd === 'cited-by') {
      if (!pos[0]) throw new Stop('error', '要给行号或 cites 编号：cited-by 3');
      const id = fromLast(pos[0], 'cites_id'), { out, page } = paging(opt);
      return { ...(await list(B, { ...out, cites: id }, { query: `cited-by ${id}`, page })), cites_id: id };
    }
    if (cmd === 'export') {
      const refs = pos.flatMap(r => r.split(/[,，\s]+/)).filter(Boolean);
      if (!refs.length) throw new Stop('error', '要给行号或 cid');
      if (!['bib', 'zotero'].includes(opt.to)) throw new Stop('error', '--to 只能是 bib / zotero');
      if (refs.length > 20) throw new Stop('error', '一次最多导出 20 条（每条要开两页，查多了谷歌会拦）');
      const got = [], ids = refs.map(ref => fromLast(ref, 'cid')), b = await B.get();
      for (const id of ids) got.push(await exportOne(b, id));
      const text = got.join('\n\n') + '\n';
      if (opt.to === 'zotero') {
        const r = await fetch('http://127.0.0.1:23119/connector/import', { method: 'POST', headers: { 'Content-Type': 'application/x-bibtex' }, body: text })
          .catch(() => { throw new Stop('error', 'Zotero 没开（连不上 127.0.0.1:23119）。打开 Zotero 桌面版再试，或者改用 --to bib'); });
        if (r.status !== 201 && r.status !== 200) throw new Stop('error', `Zotero 没收下（HTTP ${r.status}）：${(await r.text()).slice(0, 200)}`);
        return { status: 'ok', to: 'zotero', count: got.length, msg: '已导入 Zotero 当前选中的分类' };
      }
      const out = path.resolve(typeof opt.out === 'string' ? opt.out : `谷歌学术导出-${new Date().toISOString().slice(0, 10)}.bib`);
      fs.writeFileSync(out, text);
      return { status: 'ok', to: 'bib', file: out, count: got.length };
    }
    if (cmd === 'check') return await check(B);
    throw new Stop('error', `不认识的命令 ${cmd}。用 node scholar.mjs help 看用法`);
  } finally { if (conn) await conn.then(b => b.close(), () => {}); }
}

main().then(r => { process.stdout.write(JSON.stringify(r, null, 1) + '\n'); if (!['ok', 'not_found'].includes(r.status)) process.exitCode = 1; }, e => {
  process.stdout.write(JSON.stringify({ status: e instanceof Stop ? e.status : 'error', msg: e.message, ...(e.extra || {}) }, null, 1) + '\n');
  process.exitCode = 1;
});
