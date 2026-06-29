# QUY TẮC FORMAT .DOCX & CÁCH DÙNG md_to_docx.py

## QUY TẮC FORMAT MẶC ĐỊNH (script tự áp; chỉnh theo brand khách)
- **Font:** Times New Roman, size 12 (Normal).
- **Header bảng:** nền `#176bb4` (màu mặc định — đổi theo brand khách qua hằng `HEADER_FILL` trong `md_to_docx.py`), chữ trắng `#ffffff`, in đậm.
- **Lề trang:** Left 3cm · Right 2cm · Top 3cm · Bottom 2.5cm.
- **Footer:** số trang góc dưới bên phải.
- **Heading:** map theo cấp `#`→Heading1 ... `#####`→Heading5. Số/chữ mục (A, 1.1...) tự viết trong text tiêu đề.

## TRANG BÌA (cover) — bật bằng khối `<!-- COVER -->` ở ĐẦU file .md
Script tự dựng trang bìa chuyên nghiệp: **hàng 2 logo căn giữa → tên công ty (navy, đậm) → tên tài liệu → ngày cập nhật GHIM Ở CHÂN trang bìa** → ngắt sang trang nội dung. Khai báo:
```
<!-- COVER
company: Công ty Cổ phần Mondelez Kinh Đô Việt Nam
title: TÀI LIỆU GIẢI PHÁP (TO-BE) | MODULE THEO DÕI TIẾN ĐỘ CHUYỂN KHO
date: 23/06/2026
logo-left: logo-smartlog.png      # đường dẫn TƯƠNG ĐỐI so với file .md
logo-right: logo-khach.png        # logo thiếu file -> tự để ô placeholder
drop-title: true                  # bỏ tiêu đề H1 + metadata lặp ở đầu nội dung
-->
```
- **Một lệnh duy nhất:** cover dựng ngay trong `md_to_docx.py` khi convert; convert lại bao nhiêu lần vẫn có bìa.
- **`title` dùng `|` để xuống dòng;** dòng đầu nhỏ hơn (16pt), dòng sau lớn (19pt).
- **Ngày ghim ở footer-trang-đầu** → LUÔN nằm đáy trang bìa, không bị dòng trống đẩy tràn trang 2 (đừng dùng dòng trống để "đẩy" ngày xuống).
- **Logo:** PNG/JPG dùng trực tiếp; `.webp` tự convert PNG nếu có Pillow (`pip install pillow`); rộng 4.5cm; thiếu file → ô placeholder gạch nét đứt.
- **`drop-title: true`** bỏ tiêu đề/metadata lặp đầu nội dung; .md vẫn giữ H1 để đọc dạng markdown.
- Khuyến nghị bật bìa cho **bản giao/trình khách** (kể cả gói TO-BE+PRD inhouse khi xuất bản giao khách).

## CÁCH DÙNG
```
# Bash
export PYTHONIOENCODING=utf-8 PYTHONUTF8=1
python scripts/md_to_docx.py "_TOBE-BLUEPRINT.md"            # ra _TOBE-BLUEPRINT.docx
python scripts/md_to_docx.py "_TOBE-TICH-HOP.md" -o "Tich hop.docx"
```
```
# PowerShell
$env:PYTHONIOENCODING="utf-8"; $env:PYTHONUTF8="1"
python scripts/md_to_docx.py "_TOBE-BLUEPRINT.md"
```

## SCRIPT XỬ LÝ GÌ
- Heading markdown (`#`..`#####`) → Heading styles.
- Pipe table → bảng Word có header tô #176bb4 (mặc định) chữ trắng đậm (dòng phân cách `|---|` được bỏ). **KHÔNG tự canh độ rộng cột** — để Word chia đều, người dùng tự chỉnh tay trong Word (đã thử auto-size và GỠ theo yêu cầu).
- Đoạn văn, bullet `- ` / `* `, đánh số `1.` → paragraph/list.
- **Strip truy vết:** tự BỎ `_(Truy vết …)_`, `_(Ghi chú …)_`, `(Truy vết … )` cuối câu khỏi .docx (giữ trong .md để tracking nội bộ). → bản giao khách không lộ mã BR/PP/OBJ/BRULE.
- **Blockquote `>`** → đoạn **thụt lề 1cm, KHÔNG in nghiêng** (gom block liên tiếp, bỏ dòng trống thừa, `space_after` nhỏ; bullet trong blockquote có hanging indent). Dùng để thụt nội dung chi tiết bên trong mỗi "Bước N —".
- **Tiêu đề bước "Bước N —"** (dòng in đậm bắt đầu `**Bước \d`) → `space_before=12pt` (tách bước) + `space_after=2pt` (sát nội dung bên dưới).
- Fence ```mermaid → **ưu tiên chèn PNG swimlane** (xem `swimlane-guide.md`): tìm `luu-do/<ten>.png` qua comment `# src: <ten>` đầu block (hoặc file JSON cùng tên) → chèn ảnh `width=15.5cm`. Nếu không có PNG → fallback `mmdc` (mermaid-cli) → fallback placeholder.
- Placeholder ảnh màn hình `[[MH-...]]` → đoạn placeholder in nghiêng, xám (để chèn ảnh sau).
- Heading **"MỤC LỤC KẾ HOẠCH"** → script TỰ BỎ khỏi .docx (cùng phần dưới tới heading cùng/cao cấp hơn). 🐞 *Bug đã sửa: trước đây match cả chữ "TRACKING" chung → tiêu đề/section có "THEO DÕI TIẾN ĐỘ/TRACKING" bị cắt sạch. Nay chỉ match đúng cụm "MỤC LỤC KẾ HOẠCH".*
- `**đậm**`, `*nghiêng*` inline cơ bản được giữ.

> ⚠️ **Đóng file Word trước khi convert lại**, nếu không sẽ `PermissionError [Errno 13]` (file đang bị khóa). Khi đó xuất tạm `-o "<tên>-vN.docx"` rồi dọn sau, hoặc nhắc người dùng đóng Word.

## WORKAROUND LỖI ĐÃ BIẾT (python-docx)
- **Không có style "Heading n":** một số template thiếu; script fallback tạo paragraph in đậm cỡ phù hợp.
- **Bảng lệch khi cell nhiều dòng:** dùng `\n` trong cell markdown bằng `<br>`; script đổi `<br>`→xuống dòng trong cell.
- **Màu header không ăn:** script set shading bằng XML `w:shd` (đã xử lý), không dùng API màu cell (không có).
- **Footer page number:** script chèn field `PAGE` bằng XML.
- Nếu thiếu `python-docx`: `pip install python-docx`.
