---
name: scholar
description: 谷歌学术检索（乔淼PhD · AI学术训练营 · AI学术工作流）。在单独的浏览器窗口里查 Google Scholar：按关键词、作者、刊名、年份、精确短语、只搜篇名检索，付费文章也能搜到题录和摘要片段，带被引数；查「谁引了这篇」滚雪球；导出 BibTeX 或直接进 Zotero。不用账号、不用 key，随 skill 附 scripts/scholar.mjs（要 Node.js 18 以上和 Chrome 或 Edge；国内要能上谷歌）。Trigger on："在谷歌学术搜一下"、"查 Google Scholar"、"谁引用了这篇论文"、"按被引滚雪球找文献"、"search Google Scholar"、"find papers citing this one"。
---

# Scholar · 谷歌学术检索

**必须用本 skill 目录下的 `scripts/scholar.mjs`，不要自己写抓网页的代码，也不要改用别的谷歌学术 skill**。脚本会自己打开浏览器、控制查询速度，最后回一段 JSON。

```
node <skill>/scripts/scholar.mjs <命令> [参数]
```

## 命令

| 要做的事 | 命令 |
|---|---|
| 检索 | `search "检索词" [--author 作者] [--journal 刊名] [--years 2020-2025] [--title-only] [--exact "精确短语"] [--exclude "不要的词"] [--sort date] [--page 1] [--size 20]` |
| 谁引了这篇 | `cited-by <行号或 cites_id> [--years 2020-2025] [--page 1] [--size 20]` |
| 导出 | `export <行号或 cid>... --to bib [--out 文件.bib]`，或 `--to zotero` |
| 打开谷歌学术窗口 | `open`（点验证码时用） |
| 自检 | `check`（怀疑谷歌改版时跑，要开 7 页） |

- 检索词里可以用谷歌的写法：`"精确短语"`、`OR`、`-不要的词`。
- `--sort date` 是「最近一年新收录的，按时间排」，这时 `--years` 不起作用。
- `--size` 最大 20。行号是**上一次 `search` 或 `cited-by`** 结果里的第几条（`n` 字段）。
- 每开一页要隔 5–10 秒，一小时最多 60 页；导出每条要开两页，一次最多 20 条。所以一次多取几条，少翻页；导出只导真正要的。

## 返回

先看 `status`：

| status | 意思 | 你怎么做 |
|---|---|---|
| `ok` | 成功 | 往下做 |
| `not_found` | 没查到 | 换词再试 |
| `captcha` | 要点验证码 | 脚本已经把浏览器窗口提到前面，并等了 3 分钟。请用户在那个窗口里点一下，点完再跑同一条命令 |
| `blocked` | 被谷歌拦了 | 停下，告诉用户至少过半小时再查或换网络，**不要连续重试**；这一库标「没搜成」 |
| `limit` | 这一小时查太多了 | 同上 |
| `unreachable` | 打不开谷歌学术 | 告诉用户国内要先开代理；这一库标「没搜成」，英文检索改用 `openalex` 的 `search` |
| `layout_changed` | 谷歌页面改了 | 告诉用户「谷歌学术改版了，scholar skill 要更新」，把 `msg` 原样转给用户 |
| `no_browser` | 没找到 Chrome 或 Edge；或浏览器开不起来 | 没装就请用户装 Chrome。开不起来：照 msg 原样告诉用户，**不要自己想办法开浏览器、改端口、杀进程** |
| `error` | 参数错了或其他问题 | 看 `msg` |

每条结果：`title`、`authors`（可能被谷歌截断，以 `…` 结尾）、`venue`（刊名，也可能截断）、`year`、`publisher`、`snippet`、`cited`、`cites_id`、`cid`、`link`、`fulltext`（谷歌给的全文链接，可能没有）、`type`（`PDF`、`HTML`、`BOOK`，`CITATION` 表示谷歌只见过别人引用它、没收录原文）。

## 规矩

- **`snippet` 不是摘要**，是谷歌截的片段，不要当摘要写进报告。要摘要、完整作者、完整刊名和 DOI，用 `openalex` 的 `verify`。
- 谷歌学术的结果**不是 Web of Science / Scopus 的检索结果**，覆盖面和收录标准都不同。要按期刊级别筛，用 `journal-rank` 查刊名（先拿到完整刊名），报告里写明筛选方式。
- `CITATION` 条目多半信息不全、可能是错误引用，用之前先验真。
- **不自动破解验证码**。遇到验证码只能请用户自己点。
- 脚本用**单独的一份浏览器资料**（和 `cnki`、`journal-rank` 共用，放在用户目录下的 `.cnki-skill/browser`），不碰用户平时用的浏览器，不用登录谷歌账号。
- `export --to zotero` 进 Zotero **当前选中的分类**。谷歌给的 BibTeX 没有 DOI，要连 PDF 入库用 `lit-pdf-zotero`。
- 不下载 PDF，下载 PDF 用 `scansci-pdf`。
