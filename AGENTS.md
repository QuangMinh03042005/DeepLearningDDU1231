# AGENTS.md — Quy ước chung cho mọi lab (DeepLearning DDU1231)

File này là nguồn quy ước duy nhất cho agent khi làm việc trong repo,
áp dụng cho mọi lab hiện tại và sau này (Lab01, Lab02, EX-LT01, ...).

## 1. Tổng quan repo

- Môn: Học sâu (Deep Learning). Mỗi lab nằm trong 1 thư mục riêng:
  - Lab thực hành: `LabXX/` gồm đề PDF, `labXX.ipynb`, `bao_cao_labXX.tex` / `.pdf`.
  - Lab ML (Kaggle): thêm `data/` (CSV), `experiments/`, `submissions/` (1 file mỗi lần nộp).
  - Bài lý thuyết: `EX-XXX/` gồm PDF gốc + `tom_tat_*.tex` / `.pdf`.
  - Báo cáo để trong `report/` cùng lab (kèm logo trường `SGU-LOGO.png` trên bìa).
- Ngôn ngữ giao tiếp và comment code: **tiếng Việt**.

## 2. Thông tin sinh viên (dùng cho trang bìa báo cáo)

- Họ tên: Đinh Quang Minh — MSSV: 3123580024 (để chữ thường, không in đậm)
- Lớp: DDU1231 — Ngành: Khoa học dữ liệu — Khoa: Toán - Ứng dụng
- Trường: Trường Đại học Sài Gòn
- GVHD: TS. Đỗ Như Tài — Học kỳ I, năm học 2026

## 3. Môi trường

- `.venv` (Python 3.12) ở root; mọi lệnh chạy bằng `.\.venv\Scripts\python`.
- Gói mới (pandas, ruff, ...) cài vào `.venv` rồi cập nhật `requirements.txt`.
- Notebook dùng kernel `deeplearningddu1231` (`DeepLearningDDU1231 (.venv)`),
  interpreter mặc định đã ghim trong `.vscode/settings.json`.
- torch bản CPU (`torch --index-url https://download.pytorch.org/whl/cpu`).

## 4. Chuẩn code

- Comment **ngắn gọn, tiếng Việt có dấu** (cả comment code lẫn tiêu đề/nhãn biểu đồ),
  giải thích từng khối/import lạ.
- Mọi code sinh ra phải chạy `.\.venv\Scripts\ruff format` (và `ruff check` khi phù hợp).
- Cố định seed (`SEED = 42`) cho mọi thí nghiệm để tái lập kết quả.
- Giữ code ở mức sinh viên đang học môn Học sâu hiểu được: pipeline từng
  bước tường minh (pandas từng bước thay vì `ColumnTransformer`/`Pipeline`
  lồng nhau; vòng lặp đơn giản thay vì class Transformer tự viết hay hàm
  chung khó đọc). Không trừu tượng hóa sớm — viết lặp rõ ràng còn hơn
  gộp chung khó hiểu.
- Đường dẫn tương đối, chạy được cả từ root lẫn trong thư mục lab
  (vd: `Path('data') if Path('data').exists() else Path('Lab02/data')`).
- Không dùng `bash` cho thao tác file (đọc/viết/sửa) — dùng tool chuyên dụng.

## 5. Chuẩn notebook (`labXX.ipynb`)

- Chia Part rõ ràng theo yêu cầu đề bài (hoặc 6 bước CRISP-DM với lab ML).
- Mỗi cell code có 1 cell markdown giải thích đứng ngay trước
  (ý tưởng + vì sao làm + mong đợi gì), ngắn gọn 2–4 câu.
- Yêu cầu trong đề phải có đủ 3 phần: **code + kết quả chạy + nhận xét**.
- Verify bằng `jupyter nbconvert --execute` — **0 cell lỗi** mới coi là xong.
- Khi đơn giản hóa code cũ: đối chiếu kết quả (mảng/điểm số) khớp 100%
  trước khi thay, để nhật ký thí nghiệm không sai lệch.

## 6. Chuẩn báo cáo LaTeX → PDF

- Preamble mẫu: `babel` vietnamese (UTF-8/T5), `geometry`, `hyperref`
  (+ `listings` có syntax highlight, output đóng khung nền xám nếu có code).
- Trang 1 là **bìa đầy đủ** (mục 2) + `\newpage`; mỗi mục lớn sang trang mới.
- Biên dịch `pdflatex` **2 lần**, kiểm tra số trang trong log, dọn file
  `.aux/.log/.out/.toc` sau khi xong.

## 7. Chuẩn lab ML (CRISP-DM, PyTorch)

- Toàn bộ mô hình bằng PyTorch (sklearn chỉ hỗ trợ chia fold/tiền xử lý).
- Fine-tune 2 vòng/mô hình: screening nhanh → refine bằng K-fold CV → refit.
- Nhật ký bắt buộc trong `experiments/model_log.md` (+ `runs.csv`):
  `exp_id | mô hình | siêu tham số | CV metric | nhận xét | quyết định`.
- Bố cục: `experiments/{configs,models,oof,figures}` — ID thống nhất
  (`M5_mlp_d3_w128_do02`) xuyên suốt notebook, log và tên file.

## 8. Quy trình làm việc

- Làm **từng giai đoạn**, xong 1 giai đoạn dừng lại để user review,
  chỉ tiếp tục khi được đồng ý. Không làm gộp nhiều giai đoạn.
- Hỏi lại khi yêu cầu mờ (dùng tool question), không tự đoán việc quan trọng.
- Commit khi user yêu cầu, message tiếng Việt theo mẫu:
  `LabXX: ...` / `Lab02 GĐn: ...` / `EX-XXX: ...`.
- Không commit: `.venv/`, `.vscode/`, CSV dữ liệu, weights (`*.pt`),
  dự báo `*.npy`, ảnh sinh ra, file tạm (`*_check.ipynb`, `compile.log`).
