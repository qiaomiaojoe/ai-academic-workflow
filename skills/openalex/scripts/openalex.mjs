#!/usr/bin/env node
// 英文文献的公开接口：检索、核对真伪、被引数、引用链（乔淼PhD · AI学术训练营）。只用 Node 自带的东西（Node 18 以上），不开浏览器。
//
// 先查 OpenAlex；它用不了（没 key 额度用完、网络问题）退到 Crossref；引用链退到 Semantic Scholar。
// OpenAlex 的 key 依次读环境变量 OPENALEX_API_KEY → 文件 ~/.config/openalex/api_key，没有也能少量用。key 只放进请求，绝不打印。
//
//   node openalex.mjs search "检索词" [--years 2020-2025] [--size 25] [--page 1]   检索篇名和摘要
//   node openalex.mjs verify "篇名" [--doi 10.x/y] [--author 第一作者姓] [--year 2024] [--journal 刊名]
//   node openalex.mjs verify --file 清单.json     一次核对多条：[{"title":…,"doi":…,"author":…,"year":…,"journal":…}]
//   node openalex.mjs cited-by <DOI> [--size 25]   谁引了这篇（按被引数从高到低）
//   node openalex.mjs refs <DOI> [--size 50]       这篇引了谁
//   node openalex.mjs check                        自检
//
// 输出一律是一段 JSON（UTF-8），status 只有这几种：
//   ok 成功 / not_found 没查到 / limit 几个接口都限流了 / unreachable 都连不上 / layout_changed 接口返回的格式变了 / error 其他
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const OA = 'https://api.openalex.org', CR = 'https://api.crossref.org', S2 = 'https://api.semanticscholar.org/graph/v1';
const sleep = ms => new Promise(r => setTimeout(r, ms));
class Stop extends Error { constructor(status, msg, extra = {}) { super(msg); Object.assign(this, { status, extra }); } }
const readText = f => { try { return fs.readFileSync(f, 'utf8').trim(); } catch { return ''; } };
const KEY = process.env.OPENALEX_API_KEY || readText(path.join(os.homedir(), '.config', 'openalex', 'api_key'));
const norm = s => String(s || '').normalize('NFKC').toLowerCase().replace(/&/g, ' and ').replace(/[\s\p{P}\p{S}]/gu, '');
const fixDoi = s => String(s || '').trim().replace(/^https?:\/\/(dx\.)?doi\.org\//i, '').replace(/^doi:\s*/i, '');

// 请求：限流、服务器错误重试一次。报错里不带网址（网址里有 key）
async function get(base, p, params = {}, name = base) {
  const q = new URLSearchParams(params);
  if (base === OA && KEY) q.set('api_key', KEY);
  const url = `${base}${p}${q.size ? '?' + q : ''}`;
  for (let i = 0; i < 2; i++) {
    let r;
    try { r = await fetch(url, { headers: { 'User-Agent': 'ai-academic-workflow/openalex-skill' }, signal: AbortSignal.timeout(30000) }); }
    catch { if (i) return { fail: 'unreachable' }; await sleep(1000); continue; }
    if (r.status === 404) return { missing: true };
    if (r.status === 429 || r.status >= 500) { if (i) return { fail: r.status === 429 ? 'limit' : 'unreachable' }; await sleep(2500); continue; }
    if (r.status === 401 || r.status === 403) return { fail: 'limit' };
    if (!r.ok) return { fail: 'error', code: r.status };
    try { return { json: await r.json() }; } catch { return { fail: 'layout_changed' }; }
  }
}

// 两边的记录都变成同一个样子
function abstractOf(inv) { if (!inv) return ''; const w = []; for (const [t, ps] of Object.entries(inv)) for (const p of ps) w[p] = t; return w.join(' '); }
const fromOA = w => ({ title: w.title || w.display_name || '', authors: (w.authorships || []).map(a => a.author?.display_name).filter(Boolean), year: w.publication_year ? String(w.publication_year) : '',
  journal: w.primary_location?.source?.display_name || '', doi: fixDoi(w.doi), cited: w.cited_by_count ?? null, type: w.type || '', abstract: abstractOf(w.abstract_inverted_index),
  retracted: !!w.is_retracted, open_access: !!w.open_access?.is_oa, id: (w.id || '').split('/').pop(), source: 'OpenAlex' });
const fromCR = w => ({ title: (w.title || [])[0] || '', authors: (w.author || []).map(a => [a.given, a.family].filter(Boolean).join(' ') || a.name).filter(Boolean),
  year: String((w.issued?.['date-parts']?.[0]?.[0]) || ''), journal: (w['container-title'] || [])[0] || '', doi: fixDoi(w.DOI), cited: w['is-referenced-by-count'] ?? null, type: w.type || '',
  abstract: String(w.abstract || '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim(), retracted: false, open_access: null, id: '', source: 'Crossref' });
const fromS2 = w => ({ title: w.title || '', authors: (w.authors || []).map(a => a.name), year: w.year ? String(w.year) : '', journal: w.venue || '', doi: fixDoi(w.externalIds?.DOI), cited: w.citationCount ?? null, source: 'Semantic Scholar' });
const OA_FIELDS = 'id,doi,title,display_name,authorships,publication_year,primary_location,cited_by_count,type,is_retracted,open_access,abstract_inverted_index';

const worst = fails => fails.includes('layout_changed') ? 'layout_changed' : fails.includes('limit') ? 'limit' : fails.includes('unreachable') ? 'unreachable' : 'error';
const STOP_MSG = { limit: '几个公开接口都限流了，过一会儿再查（OpenAlex 填了 key 额度会多很多）', unreachable: '公开接口都连不上，检查网络', layout_changed: '接口返回的格式变了，这个 skill 要更新', error: '接口出错了' };
const giveUp = fails => { const s = worst(fails); throw new Stop(s, STOP_MSG[s]); };

async function byDoi(doi) {
  const fails = [];
  const a = await get(OA, `/works/doi:${encodeURIComponent(doi)}`, { select: OA_FIELDS });
  if (a.json) return fromOA(a.json); if (a.fail) fails.push(a.fail);
  const c = await get(CR, `/works/${encodeURIComponent(doi)}`);
  if (c.json?.message) return fromCR(c.json.message); if (c.fail) fails.push(c.fail);
  if (fails.length === 2) giveUp(fails);
  return null; // 至少一边明确说没有
}

async function byTitle(title) {
  const fails = [];
  const a = await get(OA, '/works', { filter: `title.search:${title.replace(/[,:|"]/g, ' ')}`, 'per-page': '10', select: OA_FIELDS });
  if (a.json?.results) { const rows = a.json.results.map(fromOA); if (rows.some(r => close(r.title, title))) return rows; } else if (a.fail) fails.push(a.fail);
  const c = await get(CR, '/works', { 'query.bibliographic': title, rows: '10' });
  if (c.json?.message?.items) return [...c.json.message.items.map(fromCR), ...(a.json?.results || []).map(fromOA)]; if (c.fail) fails.push(c.fail);
  if (fails.length === 2) giveUp(fails);
  return (a.json?.results || []).map(fromOA);
}

function close(x, y) { const a = norm(x), b = norm(y); return a === b || (a.length && b.length && (a.includes(b) || b.includes(a)) && Math.min(a.length, b.length) / Math.max(a.length, b.length) > 0.85); }
const brief = ({ abstract, ...m }) => m;

function compare(m, want) {
  const diff = [];
  if (want.title && norm(m.title) !== norm(want.title)) diff.push(`篇名有差别：实际是「${m.title}」`);
  if (want.author) { const w = norm(want.author), hit = m.authors.some(a => norm(a).includes(w)); if (m.authors.length && !hit) diff.push(`作者里没有「${want.author}」（实际：${m.authors.slice(0, 5).join('；')}）`); }
  if (want.year && m.year && String(want.year) !== m.year) diff.push(`年份不同：实际是 ${m.year}`);
  if (want.journal && m.journal && !norm(m.journal).includes(norm(want.journal)) && !norm(want.journal).includes(norm(m.journal))) diff.push(`刊名不同：实际是「${m.journal}」`);
  if (m.retracted) diff.push('这篇已被撤稿');
  return diff;
}

async function verify(want) {
  const doi = fixDoi(want.doi);
  if (doi) {
    const m = await byDoi(doi);
    if (m) { const diff = compare(m, want); return { status: 'ok', verdict: diff.length ? '有出入' : '对上', diff, match: brief(m) }; }
    if (!want.title) return { status: 'not_found', verdict: '没找到', msg: `DOI ${doi} 在 OpenAlex / Crossref 都解析不到` };
  }
  if (!want.title) throw new Stop('error', '要给篇名或 --doi');
  const rows = await byTitle(want.title), cands = rows.filter(r => close(r.title, want.title));
  const doiNote = doi ? [`你给的 DOI ${doi} 解析不到，下面是按篇名找到的`] : [];
  if (!cands.length) return { status: 'not_found', verdict: '没找到', msg: `按篇名查不到对得上的：${want.title}`, nearest: rows.slice(0, 3).map(r => ({ title: r.title, authors: r.authors.slice(0, 3), year: r.year, journal: r.journal, doi: r.doi })) };
  const scored = cands.map(m => ({ m, diff: [...doiNote, ...compare(m, want)] })).sort((x, y) => x.diff.length - y.diff.length);
  return { status: 'ok', verdict: scored[0].diff.length ? '有出入' : '对上', diff: scored[0].diff, match: brief(scored[0].m) };
}

function years(opt) {
  if (!opt.years) return null;
  const m = String(opt.years).match(/^(\d{4})\s*[-–~至到]\s*(\d{4})?$|^(\d{4})$/);
  if (!m) throw new Stop('error', '--years 写成 2015-2025 或 2024');
  return m[3] ? [m[3], m[3]] : [m[1], m[2] || String(new Date().getFullYear())];
}

async function search(query, opt) {
  const size = Math.min(50, Math.max(1, Number(opt.size) || 25)), page = Math.max(1, Number(opt.page) || 1), y = years(opt), fails = [];
  const a = await get(OA, '/works', { search: query, 'per-page': String(size), page: String(page), select: OA_FIELDS, ...(y ? { filter: `from_publication_date:${y[0]}-01-01,to_publication_date:${y[1]}-12-31` } : {}) });
  if (a.json?.results) return { status: a.json.results.length ? 'ok' : 'not_found', source: 'OpenAlex', total: a.json.meta?.count ?? null, page, rows: a.json.results.map((r, i) => ({ n: i + 1, ...fromOA(r) })) };
  if (a.fail) fails.push(a.fail);
  const c = await get(CR, '/works', { 'query.bibliographic': query, rows: String(size), offset: String((page - 1) * size), ...(y ? { filter: `from-pub-date:${y[0]},until-pub-date:${y[1]}` } : {}) });
  if (c.json?.message?.items) return { status: c.json.message.items.length ? 'ok' : 'not_found', source: 'Crossref', note: 'OpenAlex 用不了，这次用的 Crossref：只按题录匹配，多数没有摘要', total: c.json.message['total-results'] ?? null, page, rows: c.json.message.items.map((r, i) => ({ n: i + 1, ...fromCR(r) })) };
  if (c.fail) fails.push(c.fail);
  giveUp(fails);
}

// 引用链：OpenAlex → Semantic Scholar
async function chain(doi, dir, opt) {
  const size = Math.min(100, Math.max(1, Number(opt.size) || (dir === 'cited-by' ? 25 : 50))), fails = [];
  const a = await get(OA, `/works/doi:${encodeURIComponent(doi)}`, { select: 'id,title,cited_by_count' });
  if (a.json?.id) {
    const id = a.json.id.split('/').pop();
    const l = await get(OA, '/works', { filter: dir === 'cited-by' ? `cites:${id}` : `cited_by:${id}`, sort: 'cited_by_count:desc', 'per-page': String(size), select: OA_FIELDS.replace(',abstract_inverted_index', '') });
    if (l.json?.results) return { status: l.json.results.length ? 'ok' : 'not_found', source: 'OpenAlex', paper: a.json.title, total: l.json.meta?.count ?? null, rows: l.json.results.map((r, i) => { const { abstract, ...m } = fromOA(r); return { n: i + 1, ...m }; }) };
    if (l.fail) fails.push(l.fail);
  } else if (a.fail) fails.push(a.fail);
  const f = dir === 'cited-by' ? 'citingPaper' : 'citedPaper';
  const s = await get(S2, `/paper/DOI:${encodeURIComponent(doi)}/${dir === 'cited-by' ? 'citations' : 'references'}`, { fields: 'title,authors,year,venue,externalIds,citationCount', limit: String(size) });
  if (s.json?.data) { const rows = s.json.data.map(x => x[f]).filter(x => x?.title).map(fromS2).sort((x, y) => (y.cited || 0) - (x.cited || 0)); return { status: rows.length ? 'ok' : 'not_found', source: 'Semantic Scholar', rows: rows.map((r, i) => ({ n: i + 1, ...r })) }; }
  if (s.fail) fails.push(s.fail);
  if (s.missing && !fails.length) return { status: 'not_found', msg: `DOI ${doi} 查不到` };
  giveUp(fails.length ? fails : ['error']);
}

async function check() {
  const items = [], t = (name, ok, note = '') => items.push({ 项: name, 结果: ok ? '✓' : '✗', 说明: String(note).slice(0, 60) });
  t('OpenAlex key', true, KEY ? '有' : '没有（少量免费额度）');
  const r = await search('cognitive load theory', { years: '2015-2024', size: 5 });
  t('检索', r.status === 'ok', `${r.source} 共 ${r.total} 条`);
  const row = (r.rows || []).find(x => x.doi) || {};
  for (const [k, n] of [['title', '篇名'], ['year', '年份'], ['doi', 'DOI']]) t(`结果行·${n}`, !!row[k], row[k]);
  t('结果行·作者', !!row.authors?.length, row.authors?.[0]);
  if (row.doi) {
    const v = await verify({ doi: row.doi, title: row.title, year: row.year });
    t('按 DOI 核对', v.verdict === '对上', v.verdict);
    const w = await verify({ title: row.title });
    t('按篇名核对', w.status === 'ok', w.verdict);
    const c = await chain(row.doi, 'cited-by', { size: 3 });
    t('谁引了这篇', c.status === 'ok' || c.status === 'not_found', c.source);
    const f = await chain(row.doi, 'refs', { size: 3 });
    t('这篇引了谁', f.status === 'ok' || f.status === 'not_found', f.source);
  }
  const fake = await verify({ title: 'Quantum zebra pedagogy in sublunar kindergartens: a nonexistent paper zqxv' });
  t('假文献查无此文', fake.verdict === '没找到', fake.verdict);
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
  if (cmd === 'search') { if (!pos[0]) throw new Stop('error', '要给检索词'); return search(pos.join(' '), opt); }
  if (cmd === 'verify') {
    if (opt.file) {
      let list; try { list = JSON.parse(fs.readFileSync(String(opt.file), 'utf8')); } catch (e) { throw new Stop('error', `清单读不出来：${e.message}`); }
      if (!Array.isArray(list)) throw new Stop('error', '清单要是一个 JSON 数组');
      const items = [];
      for (const [i, w] of list.entries()) { if (i) await sleep(300); try { items.push({ n: i + 1, input: w.title || w.doi, ...(await verify(w)) }); } catch (e) { items.push({ n: i + 1, input: w.title || w.doi, status: e.status || 'error', verdict: '没查成', msg: e.message }); } }
      const count = v => items.filter(x => x.verdict === v).length;
      return { status: 'ok', summary: { 对上: count('对上'), 有出入: count('有出入'), 没找到: count('没找到'), 没查成: count('没查成') }, items };
    }
    return verify({ title: pos.join(' '), doi: opt.doi, author: opt.author, year: opt.year, journal: opt.journal });
  }
  if (cmd === 'cited-by' || cmd === 'refs') { const doi = fixDoi(pos[0]); if (!doi) throw new Stop('error', '要给 DOI'); return chain(doi, cmd, opt); }
  if (cmd === 'check') return check();
  throw new Stop('error', `不认识的命令 ${cmd}。用 node openalex.mjs help 看用法`);
}

main().then(r => { process.stdout.write(JSON.stringify(r, null, 1) + '\n'); if (!['ok', 'not_found'].includes(r.status)) process.exitCode = 1; }, e => {
  process.stdout.write(JSON.stringify({ status: e instanceof Stop ? e.status : 'error', msg: e.message, ...(e.extra || {}) }, null, 1) + '\n');
  process.exitCode = 1;
});
