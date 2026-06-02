# Phân Tích Dữ Liệu Trò Chơi Steam & Mô Hình Dự Báo

Đồ án môn DS108:  phân tích dữ liệu trò chơi Steam (2022-Q2 2026) với phân tích khám phá, kiểm định thống kê và các mô hình máy học dự báo.

## Tổng Quan Dự Án

Dự án này nhằm mục đích:
- **Thu thập & Làm sạch** dữ liệu trò chơi Steam từ nhiều nguồn (SteamSpy API + Steam Store)
- **Phân tích** xu hướng, mẫu hình và mối quan hệ trong dữ liệu trò chơi
- **Xây dựng các mô hình dự báo** để dự báo các chỉ số thành công của trò chơi
- **Cung cấp thông tin chi tiết** về cảnh quan ngành công nghiệp game

## Tóm Tắt Dataset

| Thuộc Tính | Chi Tiết |
|---|---|
| **Tên Dataset** | Steam Games with Genres |
| **Số Lượng Bản Ghi** | 3,868 trò chơi |
| **Số Lượng Tính Năng** | 52 cột |
| **Khoảng Thời Gian** | 01/01/2022 đến 19/06/2026 |
| **Nguồn Dữ Liệu** | SteamSpy API + Steam Store (web scraping) |
| **Phân Bố Năm** | 2022: 861 | 2023: 1,101 | 2024: 1,269 | 2025: 579 | 2026: 58 |

### Các Tính Năng Chính

Dataset bao gồm:
- **Thông Tin Định Danh**: App ID, tên trò chơi, tên cửa hàng, ngày phát hành
- **Giá Cả**: Giá cơ sở, thông tin giảm giá
- **Nhà Phát Triển/Nhà Xuất Bản**: Nhiều nguồn (SteamSpy + Steam Store)
- **Đánh Giá & Xếp Hạng**: Đánh giá người dùng, số lượng đánh giá, điểm xếp hạng
- **Hoạt Động Người Chơi**: Người chơi cao điểm, tổng số người chơi, dữ liệu lượng người chơi
- **Thể Loại**: Các danh mục trò chơi được mã hóa one-hot (32 cột thể loại)
- **Metadata**: Nền tảng, ngôn ngữ, và nhiều hơn nữa

Xem [steam_games_data_dictionary.md](steam_games_data_dictionary.md) để có tài liệu chi tiết về các trường dữ liệu.

## Cấu Trúc Dự Án

```
d:\FINAL_DS108\
├── README.md                          # File này
├── steam_games_data_dictionary.md     # Tài liệu chi tiết về các trường dữ liệu
├── requirements.txt                   # Các dependencies của Python
│
├── data/
│   ├── raw/
│   │   └── steam_games_raw.csv        # Dữ liệu thô từ API/web scraping
│   └── processed/
│       └── steam_games_with_genres.csv # Dataset đã làm sạch và xử lý
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb         # Làm sạch dữ liệu & tiền xử lý
│   ├── 02_eda_statistical_tests.ipynb # Phân tích khám phá & kiểm định thống kê
│   └── 03_predictive_modeling.ipynb   # Các mô hình máy học
│
└── scripts/
    └── collect_steam_data.py          # Script thu thập dữ liệu (SteamSpy API)
```

## Cài Đặt & Thiết Lập

### Yêu Cầu Tiên Quyết
- Python 3.8+
- pip hoặc conda

### Bước 1: Clone/Tải Xuống Dự Án
```bash
cd d:\FINAL_DS108
```

### Bước 2: Tạo Môi Trường Ảo (Tùy Chọn nhưng Khuyến Nghị)
```bash
# Sử dụng venv
python -m venv venv
venv\Scripts\activate

# Hoặc sử dụng conda
conda create -n steam-analysis python=3.10
conda activate steam-analysis
```

### Bước 3: Cài Đặt Các Phụ Thuộc
```bash
pip install -r requirements.txt
```

### Bước 4: Khởi Chạy Jupyter Lab/Notebook
```bash
jupyter lab
# or
jupyter notebook
```

## Các Thư Viện Phụ Thuộc

- **pandas** (≥1.5.0) - Thao tác và phân tích dữ liệu
- **numpy** (≥1.24.0) - Tính toán số học
- **scikit-learn** (≥1.2.0) - Các mô hình máy học
- **matplotlib** (≥3.6.0) - Trực quan hóa tĩnh
- **seaborn** (≥0.12.0) - Trực quan hóa thống kê
- **plotly** (≥5.15.0) - Trực quan hóa tương tác
- **scipy** (≥1.10.0) - Các hàm thống kê
- **steamspypi** (≥1.0.0) - Wrapper API Steam Spy
- **streamlit** (≥1.28.0) - Dashboard ứng dụng web (tùy chọn)
- **jupyterlab** (≥3.6.0) - Môi trường notebook tương tác

## Bắt Đầu Nhanh

### Chạy Phân Tích

1. **Làm Sạch Dữ Liệu**: Bắt đầu với `01_data_cleaning.ipynb`
   - Tải dữ liệu thô
   - Xử lý các giá trị bị thiếu
   - Chuyển đổi kiểu dữ liệu
   - Kỹ thuật hóa tính năng (mã hóa one-hot thể loại)
   - Xuất dataset đã làm sạch

2. **Phân Tích Khám Phá Dữ Liệu**: Chạy `02_eda_statistical_tests.ipynb`
   - Phân tích một biến (phân bố, giá trị ngoại lệ)
   - Phân tích hai biến (tương quan, mối quan hệ)
   - Kiểm định giả thuyết thống kê
   - Phân tích thể loại
   - Xu hướng theo thời gian

3. **Mô Hình Dự Báo**: Thực hiện `03_predictive_modeling.ipynb`
   - Lựa chọn tính năng và tiền xử lý
   - Huấn luyện mô hình (nhiều thuật toán)
   - Điều chỉnh siêu tham số
   - Đánh giá và so sánh mô hình
   - Phân tích tầm quan trọng tính năng

### Thu Thập Dữ Liệu (Tùy Chọn)

Để thu thập dữ liệu mới từ Steam:
```bash
python scripts/collect_steam_data.py
```

**Ghi Chú**: Yêu cầu quyền truy cập API SteamSpy hợp lệ và tuân thủ giới hạn tỉ lệ API.

## Các Thành Phần Phân Tích

### 1. Làm Sạch Dữ Liệu (`01_data_cleaning.ipynb`)
- Tải dữ liệu thô và kiểm tra cấu trúc
- Xử lý các giá trị bị thiếu và trùng lặp
- Chuyển đổi kiểu dữ liệu thích hợp
- Kỹ thuật hóa tính năng (trích xuất năm, mã hóa thể loại)
- Xác thực dữ liệu và kiểm tra chất lượng
- Xuất dataset đã xử lý

### 2. Phân Tích Khám Phá Dữ Liệu (`02_eda_statistical_tests.ipynb`)
- **Thống Kê Mô Tả**: Thống kê tóm tắt cho tất cả các tính năng
- **Phân Tích Phân Bố**: Biểu đồ, đồ thị KDE cho các tính năng số
- **Phân Tích Tương Quan**: Heatmaps hiển thị mối quan hệ tính năng
- **Phân Tích Thể Loại**: Thể loại phổ biến, kết hợp thể loại
- **Phân Tích Theo Thời Gian**: Phát hành trò chơi theo thời gian, xu hướng
- **Kiểm Định Thống Kê**: Kiểm định giả thuyết trên các mối quan hệ chính

### 3. Mô Hình Dự Báo (`03_predictive_modeling.ipynb`)
- **Biến Mục Tiêu**: Chỉ số thành công trò chơi (ví dụ: lượng người chơi, điểm đánh giá)
- **Các Mô Hình Được Triển Khai**:
  - Linear Regression (Hồi Quy Tuyến Tính)
  - Random Forest (Rừng Ngẫu Nhiên)
  - Gradient Boosting (Tăng Cường Gradient)
  - Các thuật toán ML khác
- **Chỉ Số Đánh Giá**: R², MAE, RMSE, điểm xác nhận chéo
- **Tầm Quan Trọng Tính Năng**: Xác định các yếu tố dự báo chính
- **So Sánh Mô Hình**: Trực quan hóa hiệu suất

## Những Thông Tin Chính (Dự Kiến)

- Phân bố thể loại và xu hướng phổ biến
- Mối quan hệ giữa giá và sự tham gia của người chơi
- Ảnh hưởng của nhà phát triển/nhà xuất bản đối với thành công trò chơi
- Các mẫu hình theo thời gian trong phát hành trò chơi và hoạt động người chơi
- Các yếu tố dự báo sự phổ biến của trò chơi

## Ghi Chú Dữ Liệu

- **Giá Trị Bị Thiếu**: Một số trường null cho các trò chơi miễn phí hoặc do hạn chế của nguồn dữ liệu
- **Phạm Vi Thời Gian**: Chủ yếu là các trò chơi phổ biến trên Steam
- **Cập Nhật Dữ Liệu**: Dataset tính đến tháng 6 năm 2026 (Q2)
- **Nguồn**: SteamSpy API + web scraping Steam Store
- **Tính Nhất Quán**: Hai nguồn dữ liệu cho nhà phát triển/nhà xuất bản (SteamSpy vs. Steam Store) để xác thực

## Từ Điển Dữ Liệu

Để biết thông tin chi tiết về từng trường, vui lòng xem:
- [steam_games_data_dictionary.md](steam_games_data_dictionary.md)

## Mẹo Quy Trình Làm Việc

1. **Bắt Đầu Từ Đầu**: Luôn chạy notebooks theo thứ tự (01 → 02 → 03)
2. **Lưu Trữ Dữ Liệu**: Dữ liệu đã xử lý được lưu vào `data/processed/` để tái sử dụng
3. **Khả Năng Tái Tạo**: Đặt seed ngẫu nhiên trong notebook mô hình để có kết quả nhất quán
4. **Trực Quan Hóa**: Sử dụng cả matplotlib và plotly cho các phong cách khám phá khác nhau
5. **Hiệu Suất**: Các thao tác lớn có thể mất vài giây; hãy kiên nhẫn với các tác vụ nặng bộ nhớ

## Các Tác Vụ Thường Gặp

### Cập Nhật Dữ Liệu
```bash
python scripts/collect_steam_data.py
```

### Khởi Động Lại Kernel
Nếu bạn gặp vấn đề bộ nhớ:
1. Lưu công việc của bạn
2. Kernel → Restart Kernel trong JupyterLab
3. Chạy các ô từ trên xuống dưới

### Tạo Phân Tích Mới
1. Xóa hoặc lưu trữ các tệp đã xử lý
2. Chạy tất cả các notebooks theo thứ tự
3. Xem xét các kết quả đầu ra và trực quan hóa

## Đóng Góp

Để cải tiến hoặc sửa lỗi:
1. Tạo một nhánh mới
2. Thực hiện các thay đổi của bạn
3. Kiểm tra kỹ lưỡng
4. Ghi chép lại các sửa đổi của bạn

## Giấy Phép

Dự án này được sử dụng cho mục đích giáo dục và nghiên cứu.

## Tác Giả
- 24521961 - Nguyễn Thị Phương Tuyền
- 24521991 - Phùng Châu Đan Vi

Tạo: Tháng 6 năm 2026

## Hỗ Trợ  
- Liên hệ : 24521961@gm.uit.edu.vn.
- Đối với các câu hỏi hoặc vấn đề:
1. Kiểm tra từ điển dữ liệu để làm rõ trường
2. Xem xét các nhận xét trong notebook và các ô markdown
3. Xác minh tất cả các phụ thuộc được cài đặt đúng cách

---

**Cập Nhật Lần Cuối**: 2 tháng 6 năm 2026  
**Trạng Thái**: Đang phát triển
