#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chuyển lưu đồ mermaid (subset chuẩn) -> file .drawio để mở/tinh chỉnh trong draw.io.

Dùng:
    python mermaid_to_drawio.py "luu-do/nhap-hang.mmd" [-o nhap-hang.drawio]

Hỗ trợ subset (xem flowchart-guide.md):
    flowchart TD|LR
    ID([text])    -> Bắt đầu/Kết thúc (stadium)
    ID[text]      -> Bước thủ công (rectangle)
    ID[[text]]    -> Bước hệ thống (process)
    ID{text}      -> Quyết định (rhombus)
    ID[/text/]    -> Chứng từ/Dữ liệu (parallelogram)
    A --> B            cạnh
    A -->|nhãn| B      cạnh có nhãn

Không cần thư viện ngoài. Layout đơn giản (xếp thẳng), bạn tự kéo lại trong draw.io.
"""
import sys, os, re, html

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BRAND_BLUE = "#176BB4"  # màu mặc định — đổi theo brand khách
STYLE = {
    "stadium":  "rounded=1;whiteSpace=wrap;html=1;arcSize=50;fillColor=#DAE8FC;strokeColor=#176BB4;",
    "rect":     "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#176BB4;",
    "process":  "shape=process;whiteSpace=wrap;html=1;fillColor=#D5E8D4;strokeColor=#176BB4;",
    "decision": "rhombus;whiteSpace=wrap;html=1;fillColor=#FFF2CC;strokeColor=#176BB4;",
    "document": "shape=parallelogram;whiteSpace=wrap;html=1;fillColor=#FCE4D6;strokeColor=#176BB4;",
}

NODE_RE = re.compile(r"^([A-Za-z0-9_]+)\s*(\(\[.*?\]\)|\[\[.*?\]\]|\[/.*?/\]|\{.*?\}|\[.*?\])?\s*$")


def parse_node_token(tok):
    """-> (id, label_or_None, shape_or_None)"""
    tok = tok.strip()
    m = NODE_RE.match(tok)
    if not m:
        # có thể là id trần
        if re.match(r"^[A-Za-z0-9_]+$", tok):
            return tok, None, None
        return None, None, None
    nid, body = m.group(1), m.group(2)
    if not body:
        return nid, None, None
    if body.startswith("([") and body.endswith("])"):
        return nid, body[2:-2], "stadium"
    if body.startswith("[[") and body.endswith("]]"):
        return nid, body[2:-2], "process"
    if body.startswith("[/") and body.endswith("/]"):
        return nid, body[2:-2], "document"
    if body.startswith("{") and body.endswith("}"):
        return nid, body[1:-1], "decision"
    if body.startswith("[") and body.endswith("]"):
        return nid, body[1:-1], "rect"
    return nid, body, "rect"


def main():
    args = sys.argv[1:]
    if not args:
        print('Dùng: python mermaid_to_drawio.py "file.mmd" [-o out.drawio]')
        sys.exit(1)
    path = args[0]
    out = args[args.index("-o") + 1] if "-o" in args else os.path.splitext(path)[0] + ".drawio"
    if not os.path.isfile(path):
        print(f"[LỖI] Không thấy file: {path}")
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    direction = "TD"
    nodes = {}   # id -> (label, shape)
    order = []   # thứ tự xuất hiện
    edges = []   # (src, dst, label)

    def reg(nid, label, shape):
        if nid is None:
            return
        if nid not in nodes:
            nodes[nid] = [label or nid, shape or "rect"]
            order.append(nid)
        else:
            if label:
                nodes[nid][0] = label
            if shape:
                nodes[nid][1] = shape

    for ln in lines:
        low = ln.lower()
        if low.startswith("flowchart") or low.startswith("graph"):
            mdir = re.search(r"(TD|TB|LR|RL|BT)", ln.upper())
            if mdir:
                direction = mdir.group(1)
            continue
        if "%%" in ln or ln.startswith("classDef") or ln.startswith("class "):
            continue
        if "-->" in ln:
            # tách cạnh (có thể nhiều cạnh nối tiếp A-->B-->C)
            m = re.match(r"^(.*?)\s*-->\s*(?:\|([^|]*)\|)?\s*(.*)$", ln)
            if not m:
                continue
            left, label, right = m.group(1), m.group(2), m.group(3)
            lid, llab, lsh = parse_node_token(left)
            rid, rlab, rsh = parse_node_token(right)
            reg(lid, llab, lsh)
            reg(rid, rlab, rsh)
            if lid and rid:
                edges.append((lid, rid, label or ""))
        else:
            nid, lab, sh = parse_node_token(ln)
            reg(nid, lab, sh)

    # layout đơn giản
    cells = []
    idmap = {}
    cid = 2
    for idx, nid in enumerate(order):
        label, shape = nodes[nid]
        style = STYLE.get(shape, STYLE["rect"])
        if direction in ("LR", "RL"):
            x, y = 40 + idx * 200, 200
        else:
            x, y = 240, 40 + idx * 100
        w, h = (160, 60) if shape != "decision" else (140, 80)
        idmap[nid] = str(cid)
        val = html.escape(label)
        cells.append(
            f'<mxCell id="{cid}" value="{val}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )
        cid += 1
    for src, dst, label in edges:
        if src not in idmap or dst not in idmap:
            continue
        val = html.escape(label)
        cells.append(
            f'<mxCell id="{cid}" value="{val}" '
            f'style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#176BB4;" '
            f'edge="1" parent="1" source="{idmap[src]}" target="{idmap[dst]}">'
            f'<mxGeometry relative="1" as="geometry"/></mxCell>'
        )
        cid += 1

    name = html.escape(os.path.splitext(os.path.basename(path))[0])
    xml = (
        '<mxfile host="app.diagrams.net">'
        f'<diagram name="{name}">'
        '<mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" '
        'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageWidth="827" '
        'pageHeight="1169" math="0" shadow="0"><root>'
        '<mxCell id="0"/><mxCell id="1" parent="0"/>'
        + "".join(cells) +
        '</root></mxGraphModel></diagram></mxfile>'
    )
    with open(out, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"[OK] Đã tạo: {out}  ({len(order)} node, {len(edges)} cạnh)")
    print("[i] Mở bằng draw.io / diagrams.net để tinh chỉnh stencil & màu theo brand khách.")


if __name__ == "__main__":
    main()
