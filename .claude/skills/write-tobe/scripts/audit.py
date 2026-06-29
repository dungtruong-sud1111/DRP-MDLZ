#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Self-audit cho TO-BE Blueprint (chạy ở Bước 9 trước khi convert .docx).
Kiểm tự động các lỗi thường gặp; in báo cáo và trả exit code != 0 nếu có lỗi.

Dùng:
    python audit.py "_TOBE-BLUEPRINT.md" ["_TOBE-TICH-HOP.md" ...]

Tự tìm trong CÙNG thư mục với file đầu:
    _DANH-SACH-MAN-HINH.md   (danh sách mô tả màn hình)
    luu-do/                  (thư mục chứa file .mmd)

Kiểm:
  1. Mọi placeholder [[MH-x.y]] trong blueprint đều có 1 khối mô tả khớp ID trong _DANH-SACH-MAN-HINH.md.
  2. Không có khối mô tả màn hình "mồ côi" (có mô tả nhưng không placeholder nào dùng).
  3. Số lưu đồ mermaid trong blueprint <= số file .mmd trong luu-do/ (mỗi lưu đồ nên có 1 .mmd).
  4. Marker [CẦN XÁC NHẬN ...]: CẢNH BÁO (draft cho phép). Nếu còn marker mà THIẾU mục "Câu hỏi còn mở" → LỖI (phải gom điểm treo vào mục cuối tài liệu trước khi giao khách).
  5. Cảnh báo nếu còn bảng "MỤC LỤC KẾ HOẠCH" (nên để md_to_docx tự bỏ, nhưng nhắc).
Không cần thư viện ngoài. Luôn chạy với PYTHONIOENCODING=utf-8 PYTHONUTF8=1.
"""
import sys, os, re, glob

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

MH_USE_RE = re.compile(r"\[\[\s*(MH-[^\]\n]+?)\s*\]\]")
# định nghĩa khối mô tả: dòng heading "### [[MH-x.y: ...]]" trong file danh sách màn hình
MH_DEF_RE = re.compile(r"^#{1,6}\s*\[\[\s*(MH-[^\]\n]+?)\s*\]\]", re.M)
CONFIRM_RE = re.compile(r"\[CẦN XÁC NHẬN[^\]]*\]")


def norm_id(s):
    # chỉ lấy phần mã trước dấu ':' để khớp ID (bỏ phần tên cho linh hoạt)
    return s.split(":")[0].strip()


def main():
    args = [a for a in sys.argv[1:] if a]
    if not args:
        print('Dùng: python audit.py "_TOBE-BLUEPRINT.md" [file khác ...]')
        sys.exit(2)
    md_files = [a for a in args if os.path.isfile(a)]
    missing = [a for a in args if not os.path.isfile(a)]
    for m in missing:
        print(f"[LỖI] Không thấy file: {m}")
    if not md_files:
        sys.exit(2)

    base_dir = os.path.dirname(os.path.abspath(md_files[0]))
    screens_path = os.path.join(base_dir, "_DANH-SACH-MAN-HINH.md")
    luudo_dir = os.path.join(base_dir, "luu-do")

    errors, warnings = [], []

    # gom nội dung blueprint
    used_ids, confirm_hits, mermaid_count, has_tracking = {}, [], 0, False
    has_oq_section = False  # có mục "Câu hỏi còn mở" / Open Questions không
    bare_blocks = []  # heading đi thẳng vào bảng/lưu đồ, thiếu câu dẫn giải (cảnh báo mềm)
    HEAD_RE = re.compile(r"^#{2,6}\s+\S")
    for mf in md_files:
        txt = open(mf, encoding="utf-8").read()
        for m in MH_USE_RE.finditer(txt):
            used_ids.setdefault(norm_id(m.group(1)), mf)
        lines = txt.split("\n")
        for ln_no, line in enumerate(lines, 1):
            if CONFIRM_RE.search(line):
                confirm_hits.append(f"{os.path.basename(mf)}:{ln_no}: {line.strip()[:90]}")
        # văn phong: heading đi NGAY tới bảng/```mermaid``` mà không có đoạn văn xen giữa
        for i, line in enumerate(lines):
            if HEAD_RE.match(line):
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    nxt = lines[j].strip()
                    if nxt.startswith("|") or nxt.startswith("```mermaid"):
                        kind = "bảng" if nxt.startswith("|") else "lưu đồ"
                        bare_blocks.append(f"{os.path.basename(mf)}:{i+1}: '{line.strip()[:45]}' đi thẳng vào {kind} (thiếu câu dẫn giải?)")
        mermaid_count += len(re.findall(r"```mermaid", txt))
        if "MỤC LỤC KẾ HOẠCH" in txt.upper():
            has_tracking = True
        up = txt.upper()
        if "CÂU HỎI CÒN MỞ" in up or "OPEN QUESTION" in up:
            has_oq_section = True

    # 1 & 2: đối chiếu placeholder vs mô tả màn hình
    defined_ids = {}
    if os.path.isfile(screens_path):
        stxt = open(screens_path, encoding="utf-8").read()
        for m in MH_DEF_RE.finditer(stxt):
            defined_ids[norm_id(m.group(1))] = True
    else:
        if used_ids:
            warnings.append(f"Không thấy {os.path.basename(screens_path)} dù blueprint có {len(used_ids)} placeholder màn hình.")

    no_spec = sorted(set(used_ids) - set(defined_ids))
    orphan = sorted(set(defined_ids) - set(used_ids))
    if no_spec:
        errors.append("Placeholder THIẾU khối mô tả trong _DANH-SACH-MAN-HINH.md: " + ", ".join(no_spec))
    if orphan:
        warnings.append("Khối mô tả màn hình MỒ CÔI (không placeholder nào dùng): " + ", ".join(orphan))

    # 3: lưu đồ
    mmd_files = glob.glob(os.path.join(luudo_dir, "*.mmd")) if os.path.isdir(luudo_dir) else []
    if mermaid_count > len(mmd_files):
        warnings.append(f"Có {mermaid_count} lưu đồ mermaid trong blueprint nhưng chỉ {len(mmd_files)} file .mmd trong luu-do/ (nên lưu mỗi lưu đồ thành 1 .mmd).")

    # 4: marker CẦN XÁC NHẬN — CẢNH BÁO (không chặn). Draft cho phép; trước khi giao khách
    #    phải chuyển hết vào mục "Câu hỏi còn mở".
    if confirm_hits:
        warnings.append(f"Còn {len(confirm_hits)} marker [CẦN XÁC NHẬN] (draft OK — trước khi giao khách hãy chuyển vào mục 'Câu hỏi còn mở'):")
        for h in confirm_hits[:15]:
            warnings.append("   - " + h)
        if len(confirm_hits) > 15:
            warnings.append(f"   - … và {len(confirm_hits) - 15} chỗ khác.")
        if not has_oq_section:
            errors.append("Có điểm treo [CẦN XÁC NHẬN] nhưng CHƯA có mục 'Câu hỏi còn mở' ở cuối tài liệu — bổ sung mục này (gom đề xuất BA + điểm chờ khách xác nhận).")

    # 5: tracking
    if has_tracking:
        warnings.append("Còn 'MỤC LỤC KẾ HOẠCH' trong tài liệu (md_to_docx sẽ tự bỏ khi convert; xác nhận đây là chủ ý).")

    # 6: văn phong (cảnh báo mềm) — bảng/lưu đồ "trần", thiếu câu dẫn giải
    if bare_blocks:
        warnings.append(f"VĂN PHONG: {len(bare_blocks)} chỗ heading đi thẳng vào bảng/lưu đồ, có thể thiếu câu dẫn giải (xem writing-style.md):")
        for b in bare_blocks[:15]:
            warnings.append("   • " + b)
        if len(bare_blocks) > 15:
            warnings.append(f"   • … và {len(bare_blocks) - 15} chỗ khác.")

    # báo cáo
    print("="*70)
    print("SELF-AUDIT TO-BE BLUEPRINT")
    print("="*70)
    print(f"File kiểm: {', '.join(os.path.basename(f) for f in md_files)}")
    print(f"Placeholder màn hình: {len(used_ids)} | Khối mô tả: {len(defined_ids)} | "
          f"Lưu đồ mermaid: {mermaid_count} | File .mmd: {len(mmd_files)}")
    print()
    if errors:
        print(f"❌ LỖI ({len([e for e in errors if not e.startswith('   ')])} nhóm):")
        for e in errors:
            print("  " + e)
    if warnings:
        print(f"\n⚠️  CẢNH BÁO ({len(warnings)}):")
        for w in warnings:
            print("  - " + w)
    if not errors and not warnings:
        print("✅ Không phát hiện vấn đề. Sẵn sàng convert .docx.")
    elif not errors:
        print("\n✅ Không có lỗi chặn; xem cảnh báo ở trên.")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
