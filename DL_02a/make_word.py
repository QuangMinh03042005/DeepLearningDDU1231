"""Sinh file Word tu ban LaTeX: reference.docx tuy chinh + hau xu ly page break/bia.

Chay: .\\.venv\\Scripts\\python DL_02a/make_word.py
"""

import re
import subprocess
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEX = HERE / "bai_tap_dl02a.tex"
DOCX = HERE / "bai_tap_dl02a.docx"
REF = HERE / "reference.docx"

# ---------------------------------------------------------------- style XML
NORMAL = """<w:style w:type="paragraph" w:default="1" w:styleId="Normal">
  <w:name w:val="Normal"/><w:qFormat/>
  <w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
</w:style>"""

HEADING1 = """<w:style w:type="paragraph" w:styleId="Heading1">
  <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="BodyText"/>
  <w:link w:val="Heading1Char"/><w:uiPriority w:val="9"/><w:qFormat/>
  <w:pPr><w:keepNext/><w:keepLines/><w:pageBreakBefore/><w:spacing w:before="240" w:after="240"/><w:jc w:val="center"/><w:outlineLvl w:val="0"/></w:pPr>
  <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"/><w:b/><w:color w:val="1F3864"/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr>
</w:style>"""

HEADING2 = """<w:style w:type="paragraph" w:styleId="Heading2">
  <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="BodyText"/>
  <w:link w:val="Heading2Char"/><w:uiPriority w:val="9"/><w:qFormat/>
  <w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/><w:outlineLvl w:val="1"/></w:pPr>
  <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"/><w:b/><w:color w:val="2E5496"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
</w:style>"""

TABLE = """<w:style w:type="table" w:default="1" w:styleId="Table">
  <w:name w:val="Table"/><w:basedOn w:val="TableNormal"/><w:semiHidden/><w:unhideWhenUsed/><w:qFormat/>
  <w:tblPr>
    <w:tblBorders>
      <w:top w:val="single" w:sz="4" w:space="0" w:color="808080"/>
      <w:left w:val="single" w:sz="4" w:space="0" w:color="808080"/>
      <w:bottom w:val="single" w:sz="4" w:space="0" w:color="808080"/>
      <w:right w:val="single" w:sz="4" w:space="0" w:color="808080"/>
      <w:insideH w:val="single" w:sz="4" w:space="0" w:color="808080"/>
      <w:insideV w:val="single" w:sz="4" w:space="0" w:color="808080"/>
    </w:tblBorders>
    <w:tblInd w:w="0" w:type="dxa"/>
    <w:tblCellMar>
      <w:top w:w="20" w:type="dxa"/><w:left w:w="100" w:type="dxa"/>
      <w:bottom w:w="20" w:type="dxa"/><w:right w:w="100" w:type="dxa"/>
    </w:tblCellMar>
  </w:tblPr>
  <w:tblStylePr w:type="firstRow"><w:rPr><w:b/></w:rPr></w:tblStylePr>
</w:style>"""

BODYTEXT = """<w:style w:type="paragraph" w:styleId="BodyText">
  <w:name w:val="Body Text"/><w:basedOn w:val="Normal"/><w:link w:val="BodyTextChar"/><w:qFormat/>
  <w:pPr><w:spacing w:before="80" w:after="80"/><w:jc w:val="both"/></w:pPr>
</w:style>"""

COMPACT = """<w:style w:type="paragraph" w:customStyle="1" w:styleId="Compact">
  <w:name w:val="Compact"/><w:basedOn w:val="BodyText"/><w:qFormat/>
  <w:pPr><w:spacing w:before="20" w:after="20"/><w:jc w:val="left"/></w:pPr>
</w:style>"""


def build_reference() -> None:
    """Tao reference.docx tu ban mac dinh cua pandoc, thay style cho dep hon."""
    raw = subprocess.run(
        ["pandoc", "--print-default-data-file", "reference.docx"],
        capture_output=True,
        check=True,
    ).stdout
    tmp = HERE / "_ref_default.docx"
    tmp.write_bytes(raw)

    zin = zipfile.ZipFile(tmp)
    styles = zin.read("word/styles.xml").decode("utf-8")
    repl = {
        "Normal": NORMAL,
        "Heading1": HEADING1,
        "Heading2": HEADING2,
        "Table": TABLE,
        "BodyText": BODYTEXT,
        "Compact": COMPACT,
    }
    for sid, xml in repl.items():
        pat = r'<w:style [^>]*w:styleId="%s".*?</w:style>' % sid
        if re.search(pat, styles, re.S):
            styles = re.sub(pat, xml, styles, count=1, flags=re.S)

    with zipfile.ZipFile(REF, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                data = styles.encode("utf-8")
            zout.writestr(item, data)
    zin.close()
    tmp.unlink()


# ---------------------------------------------------------------- hau xu ly
def ensure_pPr(p: str) -> str:
    m = re.match(r"(<w:p(?: [^>]*)?>)(.*)(</w:p>)$", p, re.S)
    open_tag, body, close = m.groups()
    if body.lstrip().startswith("<w:pPr>"):
        return p
    return open_tag + "<w:pPr></w:pPr>" + body + close


def set_cover_ppr(p: str, space_before: int, space_after: int) -> str:
    p = ensure_pPr(p)
    ppr = (
        '<w:pPr><w:spacing w:before="%d" w:after="%d"/>'
        '<w:jc w:val="center"/></w:pPr>' % (space_before, space_after)
    )
    return re.sub(r"<w:pPr>.*?</w:pPr>", ppr, p, count=1, flags=re.S)


def set_heading1_ppr(p: str, page_break: bool = True) -> str:
    p = ensure_pPr(p)
    pb = "<w:pageBreakBefore/>" if page_break else ""
    ppr = (
        '<w:pPr><w:pStyle w:val="Heading1"/><w:keepNext/><w:keepLines/>'
        + pb
        + '<w:spacing w:before="240" w:after="240"/>'
        '<w:jc w:val="center"/><w:outlineLvl w:val="0"/></w:pPr>'
    )
    return re.sub(r"<w:pPr>.*?</w:pPr>", ppr, p, count=1, flags=re.S)


A4_SIZE = '<w:pgSz w:w="11906" w:h="16838"/>'
A4_MARGIN = (
    '<w:pgMar w:top="1418" w:right="1134" w:bottom="1418" w:left="1701" '
    'w:header="709" w:footer="709" w:gutter="0"/>'
)


def cover_section_break(doc: str) -> str:
    """Tao doan ket thuc section bia, kem vien trang (pgBorders)."""
    sides = "".join(
        '<w:%s w:val="double" w:sz="12" w:space="24" w:color="1F3864"/>' % s
        for s in ("top", "left", "bottom", "right")
    )
    sect = (
        "<w:sectPr>"
        + A4_SIZE
        + A4_MARGIN
        + '<w:pgBorders w:offsetFrom="page">'
        + sides
        + "</w:pgBorders>"
        + "</w:sectPr>"
    )
    return "<w:p><w:pPr>" + sect + "</w:pPr></w:p>"


def fix_final_sectpr(doc: str) -> str:
    """Bo sung kho giay A4 + le cho section cuoi (mac dinh pandoc thieu)."""
    m = re.search(r"<w:sectPr[^>]*>", doc)
    return doc[: m.end()] + A4_SIZE + A4_MARGIN + doc[m.end() :]


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
            '<w:r><w:rPr><w:b/><w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr>'
            % (size, size),
            1,
        )

    return re.sub(r"<w:r>.*?</w:r>", fix_run, p, flags=re.S)


def postprocess() -> None:
    zin = zipfile.ZipFile(DOCX)
    items = {it.filename: zin.read(it.filename) for it in zin.infolist()}
    order = [it.filename for it in zin.infolist()]
    zin.close()
    doc = items["word/document.xml"].decode("utf-8")

    paras = list(re.finditer(r"<w:p(?: [^>]*)?>.*?</w:p>", doc, re.S))
    # tim Heading1 dau tien -> doan truoc no la bia
    first_h1 = None
    for i, m in enumerate(paras):
        if '<w:pStyle w:val="Heading1"' in m.group(0):
            first_h1 = i
            break
    assert first_h1 is not None, "khong tim thay Heading1"

    new_paras = []
    for i, m in enumerate(paras):
        p = m.group(0)
        if i < first_h1:  # --- bia ---
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
            else:  # cac dong thong tin
                p = set_cover_ppr(p, 0, 40)
        elif '<w:pStyle w:val="Heading1"' in p:
            if i == first_h1:
                # section break ket thuc bia (co vien trang) + khong can page break rieng
                p = cover_section_break(doc) + set_heading1_ppr(p, page_break=False)
            else:
                p = set_heading1_ppr(p)
        new_paras.append(p)

    # ghep lai theo dung vi tri
    out, pos = [], 0
    for m, p in zip(paras, new_paras):
        out.append(doc[pos : m.start()])
        out.append(p)
        pos = m.end()
    out.append(doc[pos:])
    doc = "".join(out)
    doc = fix_final_sectpr(doc)

    with zipfile.ZipFile(DOCX, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in order:
            data = doc.encode("utf-8") if name == "word/document.xml" else items[name]
            zout.writestr(name, data)


def main() -> None:
    build_reference()
    subprocess.run(
        ["pandoc", str(TEX), "-o", str(DOCX), "--reference-doc", str(REF)],
        cwd=HERE,
        check=True,
    )
    postprocess()
    print("Da tao:", DOCX.name)


if __name__ == "__main__":
    main()
