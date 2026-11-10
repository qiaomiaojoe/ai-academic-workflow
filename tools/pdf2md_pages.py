# pdf2md_pages.py · 用 MinerU 把 PDF 转成带页码的 Markdown（乔淼PhD · AI学术工作流）
#
# 每篇 PDF 旁边生成同名 .md：
#   - 每页前插一行 <!-- 第 N 页 -->；页面上印的页码不一样时写成 <!-- 第 N 页 · 印的页码 41 -->，引用时用它
#   - 图片换成 [图]，不把图片编码塞进文字稿
#
# 先装 MinerU 4.x（用 uv 装）：  uv tool install --python 3.12 "mineru>=4.0,<5"
# 用法（Mac；用 MinerU 自己的 Python 运行）：
#   ~/.local/share/uv/tools/mineru/bin/python pdf2md_pages.py 论文.pdf
#   ~/.local/share/uv/tools/mineru/bin/python pdf2md_pages.py *.pdf     # 一次转整个文件夹，模型只加载一次
# 模型第一次用时会自动下载（约 2 GB），默认从国内的 ModelScope 下载。
import os, re, sys, time
PRINTED = re.compile(r"^\s*(?:-\s*)?(\d{1,5}|[ivxlcdm]{1,8})(?:\s*-)?\s*$", re.I)

def printed_number(page):
    for b in page.blocks:
        if str(getattr(b, "type", "")).split(".")[-1].lower() not in ("page_number", "blocktype.page_number"):
            continue
        text = "".join(str(getattr(c, "content", "") or "") for c in (getattr(b, "content", None) or []))
        m = PRINTED.match(text)
        if m:
            return m.group(1)
    return ""

def main(pdfs):
    os.environ.setdefault("MINERU_MODEL_SOURCE", "modelscope")
    from mineru.parser import MinerUParser
    from mineru.render.markdown import render_markdown
    img = lambda b: "[公式（没认出来）]" if "equation" in str(getattr(b, "type", "") or "") else "[图]"
    parser = MinerUParser(tier="standard")
    for pdf in pdfs:
        t0 = time.time()
        mj = parser.parse(pdf).middle_json
        pages = sorted(mj.pages, key=lambda p: p.page_idx)
        found = {p.page_idx + 1: printed_number(p) for p in pages}
        offs = {int(v) - k for k, v in found.items() if v.isdigit()}
        if len(offs) == 1 and sum(1 for v in found.values() if v.isdigit()) >= 2:
            off = offs.pop()
            found = {k: (v or (str(k + off) if k + off > 0 else "")) for k, v in found.items()}
        parts = []
        for p in pages:
            n = p.page_idx + 1
            pr = found.get(n, "")
            mark = "第 %d 页" % n + (" · 印的页码 %s" % pr if pr and pr != str(n) else "")
            text = render_markdown(mj.model_copy(update={"pages": [p]}), image_renderer=img).strip()
            parts.append("<!-- %s -->\n\n%s" % (mark, text or "（这一页没有文字）"))
        out = os.path.splitext(pdf)[0] + ".md"
        with open(out, "w", encoding="utf-8") as f:
            f.write("\n\n".join(parts).strip() + "\n")
        print("转好了：%s（%d 页，%d 秒）" % (out, len(pages), round(time.time() - t0)))
    parser.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法：python pdf2md_pages.py 论文.pdf")
    main(sys.argv[1:])
