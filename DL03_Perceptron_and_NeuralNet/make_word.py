"""Sinh file Word cho bai DL03 tu ban LaTeX (reference.docx + hau xu ly)."""

import re
import subprocess
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEX = HERE / "bai_tap_dl03.tex"
DOCX = HERE / "bai_tap_dl03.docx"

A4_SIZE = '<w:pgSz w:w="11906" w:h="16838"/>'
A4_MARGIN = ('<w:pgMar w:top="1418" w:right="1134" w:bottom="1418" w:left="1701" '
             'w:header="709" w:footer="709" w:gutter="0"/>')

COVER_LINES = {
    "TRƯỜNG ĐẠI HỌC": (160, 60),
    "KHOA TOÁN": (0, 60),
}


def ensure_pPr(p: str) -> str:
    m = re.match(r"(<w:p(?: [^>]*)?>)(.*)(</w:p>)$", p, re.S)
    open_tag, body, close = m.groups()
    if body.lstrip().startswith("<w:pPr>"):
        return p
    return open_tag + "<w:pPr></w:pPr>" + body + close


def set_cover_ppr(p: str, before: int, after: int) -> str:
    p = ensure_pPr(p)
    ppr = ('<w:pPr><w:spacing w:before="%d" w:after="%d"/>'
           '<w:jc w:val="center"/></w:pPr>' % (before, after))
    return re.sub(r"<w:pPr>.*?</w:pPr>", ppr, p, count=1, flags=re.S)


def set_heading1_ppr(p: str, page_break: bool = True) -> str:
    p = ensure_pPr(p)
    pb = "<w:pageBreakBefore/>" if page_break else ""
    ppr = ('<w:pPr><w:pStyle w:val="Heading1"/><w:keepNext/><w:keepLines/>'
           + pb +
           '<w:spacing w:before="240" w:after="240"/>'
           '<w:jc w:val="center"/><w:outlineLvl w:val="0"/></w:pPr>')
    return re.sub(r"<w:pPr>.*?</w:pPr>", ppr, p, count=1, flags=re.S)


def make_runs_big(p: str, size: int) -> str:
    def fix_rpr(m):
        rpr = m.group(1)
        rpr = re.sub(r"<w:sz[^/]*/>|<w:szCs[^/]*/>", "", rpr)
        rpr += '<w:b/><w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size)
        return "<w:rPr>" + rpr + "</w:rPr>"

    def fix_run(m):
        run = m.group(0)
        if "<w:t" not in run:
            return run
        if "<w:rPr>" in run:
            return re.sub(r"<w:rPr>(.*?)</w:rPr>", fix_rpr, run, count=1, flags=re.S)
        return run.replace(
            "<w:r>",
            '<w:r><w:rPr><w:b/><w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr>' % (size, size),
            1,
        )

    return re.sub(r"<w:r>.*?</w:r>", fix_run, p, flags=re.S)


def cover_section_break() -> str:
    sides = "".join(
        '<w:%s w:val="double" w:sz="12" w:space="24" w:color="1F3864"/>' % s
        for s in ("top", "left", "bottom", "right")
    )
    sect = ("<w:sectPr>" + A4_SIZE + A4_MARGIN
            + '<w:pgBorders w:offsetFrom="page">' + sides + "</w:pgBorders>"
            + "</w:sectPr>")
    return "<w:p><w:pPr>" + sect + "</w:pPr></w:p>"


def fix_final_sectpr(doc: str) -> str:
    m = re.search(r"<w:sectPr[^>]*>", doc)
    return doc[:m.end()] + A4_SIZE + A4_MARGIN + doc[m.end():]


def postprocess() -> None:
    zin = zipfile.ZipFile(DOCX)
    items = {it.filename: zin.read(it.filename) for it in zin.infolist()}
    order = [it.filename for it in zin.infolist()]
    zin.close()
    doc = items["word/document.xml"].decode("utf-8")

    paras = list(re.finditer(r"<w:p(?: [^>]*)?>.*?</w:p>", doc, re.S))
    first_h1 = next(
        i for i, m in enumerate(paras) if '<w:pStyle w:val="Heading1"' in m.group(0)
    )

    new_paras = []
    for i, m in enumerate(paras):
        p = m.group(0)
        if i < first_h1:
            txt = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S))
            if "<w:drawing>" in p:
                p = set_cover_ppr(p, 0, 240)
            elif txt.startswith("TRƯỜNG ĐẠI HỌC"):
                p = set_cover_ppr(p, 120, 60)
            elif txt.startswith("KHOA TOÁN"):
                p = set_cover_ppr(p, 0, 60)
            elif txt.startswith("BÀI TẬP"):
                p = set_cover_ppr(p, 480, 120)
                p = make_runs_big(p, 32)
            elif txt.startswith("Môn:"):
                p = set_cover_ppr(p, 0, 480)
            elif txt.startswith("TP. Hồ Chí Minh"):
                p = set_cover_ppr(p, 480, 0)
            else:
                p = set_cover_ppr(p, 0, 40)
        elif '<w:pStyle w:val="Heading1"' in p:
            if i == first_h1:
                p = cover_section_break() + set_heading1_ppr(p, page_break=False)
            else:
                p = set_heading1_ppr(p)
        new_paras.append(p)

    out, pos = [], 0
    for m, p in zip(paras, new_paras):
        out.append(doc[pos:m.start()])
        out.append(p)
        pos = m.end()
    out.append(doc[pos:])
    doc = fix_final_sectpr("".join(out))

    with zipfile.ZipFile(DOCX, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in order:
            data = doc.encode("utf-8") if name == "word/document.xml" else items[name]
            zout.writestr(name, data)


def main() -> None:
    subprocess.run(
        ["pandoc", str(TEX), "-o", str(DOCX), "--reference-doc", str(HERE / "reference.docx")],
        cwd=HERE, check=True,
    )
    postprocess()
    print("Da tao:", DOCX.name)


if __name__ == "__main__":
    main()
