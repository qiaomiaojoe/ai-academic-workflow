---
name: openalex
description: 英文文献公开接口（乔淼PhD · AI学术训练营 · AI学术工作流）。不开浏览器、不用账号，直接查 OpenAlex（用不了时退到 Crossref、Semantic Scholar）：按主题检索英文文献（带摘要）；按 DOI 或篇名核对一篇英文文献是否真实存在、作者 / 年份 / 刊名对不对、有没有撤稿；取被引数；查「谁引了这篇」和「这篇引了谁」。随 skill 附 scripts/openalex.mjs（要 Node.js 18 以上）；OpenAlex key 可填可不填。中文文献用 cnki。Trigger on："核对这篇英文文献是不是真的"、"查这个 DOI"、"这篇的被引数是多少"、"这篇论文的参考文献和施引文献"、"verify this paper exists"、"get citation count for this DOI"。
---

# OpenAlex · 英文文献公开接口

**必须用本 skill 目录下的 `scripts/openalex.mjs`，不要自己拼接口请求**。脚本会按 OpenAlex → Crossref（引用链是 Semantic Scholar）的顺序试，回一段 JSON。

```
node <skill>/scripts/openalex.mjs <命令> [参数]
```

| 要做的事 | 命令 |
|---|---|
| 检索（篇名 + 摘要） | `search "检索词" [--years 2020-2025] [--size 25] [--page 1]` |
| 核对一篇 | `verify "篇名" [--doi 10.x/y] [--author 第一作者姓] [--year 2024] [--journal 刊名]` |
| 一次核对多条 | `verify --file 清单.json`，内容是 `[{"title":…,"doi":…,"author":…,"year":…,"journal":…}]` |

- 要给一篇文献补 DOI、完整篇名、完整刊名，用 `verify`，**不要用 `search` 搜篇名再取第一条**（第一条常常是别的文献）。
- 谷歌学术截断的篇名、刊名（带 `…`）原样传进去就行，`verify` 认得出来，完整的写在 `match` 里，不算「有出入」。
| 谁引了这篇 | `cited-by <DOI> [--size 25]`（按被引数从高到低） |
| 这篇引了谁 | `refs <DOI> [--size 50]` |
| 自检 | `check` |

## 返回

先看 `status`：`ok` 成功；`not_found` 没查到；`limit` 接口都限流了，告诉用户过一会儿再查（填 OpenAlex key 额度会多很多，在 POPPER 的「AI学术环境配置」里填，别让用户把 key 贴进对话）；`unreachable` 连不上，请用户检查网络；`layout_changed` 接口变了，把 `msg` 转给用户；`error` 看 `msg`。

`verify` 的 `verdict` 只有三种（批量时还有 `没查成`，表示接口没回，**不是查无此文**，过一会儿重查）：
- `对上`：DOI 或篇名对得上，你给的作者、年份、刊名也都一致。
- `有出入`：`diff` 里逐条写着哪里不一样，`match` 是查到的那篇；撤稿也写在 `diff` 里。
- `没找到`：`nearest` 列出最接近的几条，**不要拿它们顶替原文献**。

每条记录：`title`、`authors`、`year`、`journal`、`doi`、`cited`、`type`、`abstract`（`search` 才有，付费文章多半是空的）、`retracted`、`open_access`、`source`（这条来自哪个接口）。

## 规矩

- 被引数各家不同：OpenAlex、Crossref、谷歌学术的数字对不上是正常的，写进表格时注明来源，不要换算。
- OpenAlex 里付费文章大多**没有摘要**，所以 `search` 只作谷歌学术上不去时的兜底和补充；用它检索的，报告里写明。
- 结果**不等于 Web of Science / Scopus 的检索结果**。
- key 不打印、不写进文件，也不要让用户贴进对话。
