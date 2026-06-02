# Data Dictionary — Steam Games with Genres

| Thuộc tính | Giá trị |
|---|---|
| **Tên dataset** | Steam Games with Genres |
| **Số dòng dữ liệu** | 3,868 |
| **Số cột** | 52 |
| **Nguồn dữ liệu** | SteamSpy API + Steam Store (web scrape) |
| **Phạm vi thời gian** | Phát hành từ 2022 đến Q2/2026 |
| **Phân phối năm** | 2022: 861 | 2023: 1,101 | 2024: 1,269 | 2025: 579 | 2026: 58 |
| **Ghi chú chung** | Tập dữ liệu chủ yếu gồm game phổ biến nhất trên Steam. Một số trường null tương ứng game miễn phí hoặc thiếu dữ liệu từ nguồn. |

---

## Mục lục

1. [Thông tin định danh & cơ bản](#1-thông-tin-định-danh--cơ-bản)
2. [Nhà phát triển & Nhà xuất bản (2 nguồn)](#2-nhà-phát-triển--nhà-xuất-bản-2-nguồn)
3. [Giá bán](#3-giá-bán)
4. [Đánh giá & Xếp hạng](#4-đánh-giá--xếp-hạng)
5. [Người chơi & Độ phổ biến](#5-người-chơi--độ-phổ-biến)
6. [Thể loại game (One-hot Encoding)](#6-thể-loại-game-one-hot-encoding)
7. [Tham chiếu: Giá trị định danh](#7-tham-chiếu-giá-trị-định-danh)

---

## 1. Thông tin định danh & cơ bản

### 1.1 `appid` — ID ứng dụng Steam

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Integer (số nguyên dương) |
| **Miền giá trị** | 1,501,610 – 3,597,690 |
| **Null** | 0 |
| **Ý nghĩa** | Mã định danh duy nhất (primary key) mà Steam gán cho mỗi ứng dụng/game trên nền tảng. Dùng để truy vấn API Steam, mở trang store. Mỗi appid là duy nhất toàn cầu trên Steam. |
| **Ví dụ** | `1623730` = Palworld, `1943950` = Escape the Backrooms |

---

### 1.2 `name` — Tên game

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | String (text) |
| **Miền giá trị** | Bất kỳ chuỗi ký tự nào (Unicode) — tối đa vài trăm ký tự |
| **Null** | 0 |
| **Unique** | 3,868 / 3,868 (tất cả đều duy nhất) |
| **Ý nghĩa** | Tên hiển thị chính thức của game trên Steam Store. Đây là tên do nhà phát triển đăng ký và hiển thị cho người dùng. Có chứa ký tự đặc biệt, dấu nhãn hiệu ™/®, dấu câu, ký tự Unicode (tiếng Nhật, v.v.). |
| **Ví dụ** | `"Call of Duty: Modern Warfare II"`, `"Black Myth: Wukong"`, `"ELDEN RING NIGHTREIGN"` |

---

### 1.3 `store_name` — Tên hiển thị trên Steam Store

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | String (text) |
| **Miền giá trị** | Chuỗi ký tự Unicode |
| **Null** | 0 |
| **Unique** | 3,868 / 3,868 |
| **Ý nghĩa** | Tên game phiên bản "URL-friendly" hoặc tên rút gọn hiển thị trên Steam Store. Có thể khác `name` vì: (a) xóa ký tự đặc biệt cho URL, (b) tên rút gọn, (c) mã hóa khác. Dùng để đối chiếu và truy vấn chính xác trên store. |
| **Ví dụ** | `name="Call of Duty®"` → `store_name="Call of Duty®"`; `name="EA SPORTS™ FIFA 23"` → `store_name="EA SPORTS™ FIFA 23"` |

---

### 1.4 `release_date` — Ngày phát hành

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Date (lưu dạng string YYYY-MM-DD) |
| **Miền giá trị** | Khoảng 2022-01-01 đến 2026-06-1 |
| **Null** | 0 |
| **Unique** | 1,123 giá trị duy nhất |
| **Ý nghĩa** | Ngày phát hành chính thức (global release date) của game trên Steam. Định dạng chuẩn ISO 8601 (YYYY-MM-DD). Được dùng để tính tuổi game, lọc theo thời gian, phân tích xu hướng. |
| **Ví dụ** | `2024-01-18` (Palworld), `2025-02-27` (Monster Hunter Wilds) |

---

### 1.5 `year` — Năm phát hành

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Float (số thực) — thực chất là số nguyên |
| **Miền giá trị** | 2022.0 – 2026.0 |
| **Null** | 0 |
| **Ý nghĩa** | Năm được trích xuất từ `release_date`. Dùng để phân nhóm, lọc theo năm, phân tích xu hướng theo thời gian. Lưu dạng float do cách xử lý dữ liệu gốc (có thể từ Pandas). |
| **Phân phối** | 2022: 861 | 2023: 1,101 | 2024: 1,269 | 2025: 579 | 2026: 58 |

---

## 2. Nhà phát triển & Nhà xuất bản (2 nguồn)

Tập dữ liệu có **2 cặp cột** cho developer/publisher, đến từ **2 nguồn khác nhau**:

| Nguồn | Developer | Publisher | Đặc điểm |
|---|---|---|---|
| **SteamSpy** | `developer_spy` | `publisher_spy` | Nhiều tên (có thể không đầy đủ), 5 null ở publisher |
| **Steam Store** | `developer_store` | `publisher_store` | Tên chính xác trên store, 7 null ở publisher |

> **Lưu ý quan trọng:** Hai nguồn thường khác nhau. SteamSpy liệt kê tất cả studio tham gia (có thể nhiều tên cách nhau bằng dấu phẩy), còn Steam Store chỉ hiển thị tên chính. Có **344/3,868 (8.9%)** game có `developer_spy ≠ developer_store` và **442/3,868 (11.4%)** có `publisher_spy ≠ publisher_store`.

### 2.1 `developer_spy` — Nhà phát triển (SteamSpy)

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | String (text, multi-value) |
| **Miền giá trị** | Chuỗi ký tự, nhiều tên phân cách bằng dấu phẩy (`,`) |
| **Null** | 0 |
| **Unique** | 3,290 giá trị duy nhất |
| **Ý nghĩa** | Tên các studio/nhà phát triển tham gia làm game, theo dữ liệu từ SteamSpy API. Có thể chứa nhiều tên (cùng phát triển) cách nhau bởi dấu phẩy. Đây là danh sách đầy đủ hơn so với Steam Store. |
| **Ví dụ** | `"Pocketpair"`; `"Treyarch, Raven Software, Beenox, High Moon Studios, ..."`; `"CAPCOM Co., Ltd."` |

---

### 2.2 `publisher_spy` — Nhà xuất bản (SteamSpy)

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | String (text, multi-value) |
| **Miền giá trị** | Chuỗi ký tự, nhiều tên phân cách bằng dấu phẩy |
| **Null** | 5 |
| **Unique** | 2,575 giá trị duy nhất |
| **Ý nghĩa** | Tên các công ty xuất bản game, theo SteamSpy. Có thể có nhiều nhà xuất bản (multi-region publishing) được liệt kê. |
| **Các game có null** | *Marauders*, *Knights of Pen and Paper 3*, *Black & White*, *Clicker Arena*, *Trash of the Titans* — các game này có thể đã bị xóa khỏi Steam hoặc SteamSpy không thu thập được dữ liệu. |

---

### 2.3 `developer_store` — Nhà phát triển (Steam Store)

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | String (text, single-value) |
| **Miền giá trị** | Chuỗi ký tự Unicode |
| **Null** | 0 |
| **Unique** | 3,216 giá trị duy nhất |
| **Ý nghĩa** | Tên nhà phát triển chính thức hiển thị trên trang Steam Store của game. Thường chỉ có 1 tên (studio chính), khác với `developer_spy` có thể liệt kê nhiều studio. Đây là nguồn chính xác nhất để xác định developer. |

---

### 2.4 `publisher_store` — Nhà xuất bản (Steam Store)

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | String (text, single-value) |
| **Miền giá trị** | Chuỗi ký tự Unicode |
| **Null** | 7 |
| **Unique** | 2,436 giá trị duy nhất |
| **Ý nghĩa** | Tên nhà xuất bản chính thức trên Steam Store. |
| **Ví dụ** | `"Electronic Arts"`, `"PlayStation Publishing LLC"`, `"CAPCOM Co., Ltd."` |

---

## 3. Giá bán

### 3.1 `price` — Giá bán cuối cùng (USD)

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Float |
| **Đơn vị** | USD (đô la Mỹ) |
| **Miền giá trị** | 0.00 – 99.99 |
| **Null** | 0 |
| **Ý nghĩa** | Giá bán cuối cùng mà người chơi phải trả sau khi áp dụng mọi giảm giá. Game miễn phí có `price = 0.00`. Giá này được hiển thị trực tiếp trên trang Steam Store. |
| **Ví dụ** | `29.99` (Palworld), `69.99` (Call of Duty), `0.00` (Free to Play) |

---

### 3.2 `is_free` — Cờ game miễn phí

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Binary (nhị phân: 0 hoặc 1, lưu dạng Float) |
| **Miền giá trị** | `0` hoặc `1` |
| **Null** | 0 |
| **Ý nghĩa** | Biến chỉ báo (flag): `1` = game hoàn toàn miễn phí, `0` = game trả phí. Khi `is_free = 1` thì `price = 0.00` và `price_group = "Free"`. Ngược lại, `is_free = 0` có thể có giá từ `< $10` đến `> $30`. |
| **Phân phối** | `0` (trả phí): 3,612 games (93.4%) | `1` (miễn phí): 256 games (6.6%) |

---

### 3.3 `price_group` — Nhóm giá phân loại

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Categorical (chuỗi) |
| **Miền giá trị** | `"<$10"`, `"$10-30"`, `">$30"`, `"Free"` |
| **Null** | 0 |
| **Ý nghĩa** | Nhóm giá được phân loại thủ công dựa trên `price`. Dùng để phân tích theo phân khúc giá mà không cần xử lý giá trị liên tục. |
| **Phân phối** | `"<$10"`: 1,568 (40.5%) | `"$10-30"`: 1,679 (43.4%) | `">$30"`: 365 (9.4%) | `"Free"`: 256 (6.6%) |

---

### 3.4 `price_spy` — Giá gốc theo SteamSpy (đơn vị cents)

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Integer |
| **Đơn vị** | **Cents** (1 USD = 100 cents) |
| **Miền giá trị** | 0 – 99,900,000 (có outliers lớn) |
| **Null** | 0 |
| **Ý nghĩa** | Giá gốc của game theo dữ liệu từ SteamSpy API, lưu dưới dạng cents (cần chia 100 để ra USD). Tuy nhiên trường này chứa nhiều giá trị bất thường: ví dụ Palworld có `price_spy = 38,500,000` (= $385,000), trong khi giá thực tế là $29.99. Nguyên nhân có thể do cách SteamSpy mã hóa/aggregate giá. **Không nên dùng trực tiếp mà cần hiệu chỉnh.** |
| **Lưu ý** | Có 3,365/3,868 game (87.0%) có `price_spy > 999,000` cents, cho thấy hầu hết giá trị này đều là outliers. |

---

### 3.5 `price_store` — Giá trên Steam Store (USD)

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Float |
| **Đơn vị** | USD |
| **Miền giá trị** | 2.99 – 999.00 |
| **Null** | 346 |
| **Ý nghĩa** | Giá gốc lấy trực tiếp từ Steam Store. Đây là nguồn chính xác hơn `price_spy`. Giá trị null xảy ra cho: (a) **256 game miễn phí** (`is_free = 1`), và (b) **90 game trả phí** nhưng Steam Store không trả về giá (có thể game đã bị gỡ, giới hạn region, hoặc lỗi scrape). |
| **Phân phối null** | Game miễn phí: 256 | Game trả phí nhưng null: 90 |

---

### 3.6 `initialprice` — Giá khởi điểm (SteamSpy, cents)

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Integer |
| **Đơn vị** | Cents (chia 100 → USD) |
| **Miền giá trị** | 0 – 9,999 |
| **Null** | 0 |
| **Ý nghĩa** | Giá ban đầu khi game ra mắt trên Steam (theo SteamSpy), trước mọi đợt giảm giá. Dùng để tính tổng mức giảm giá lịch sử. Khác với `initialprice` là giá đã điều chỉnh (giá Steam hiện tại). |
| **Ví dụ** | Palworld: `initialprice = 2999` cents = $29.99 (giá ra mắt = giá hiện tại, chưa giảm). Call of Duty MW2: `initialprice = 6999` cents = $69.99, `discount = 45%` → giá hiện tại $38.49. |

---

### 3.7 `discount` — Phần trăm giảm giá

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Integer |
| **Đơn vị** | Phần trăm (%) |
| **Miền giá trị** | 0 – 95 |
| **Null** | 0 |
| **Ý nghĩa** | Tỷ lệ giảm giá hiện tại trên Steam Store (theo SteamSpy). `0` = không giảm giá (bán giá gốc). Giá trị cao (50-95%) thường là sale sự kiện (Steam Summer/Winter Sale). |
| **Phân phối** | 0%: phần lớn game | Có game lên đến 95% giảm (cũ/sale sâu) |

---

## 4. Đánh giá & Xếp hạng

### 4.1 `positive_ratings` — Số đánh giá tích cực

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Integer |
| **Miền giá trị** | 11 – 1,111,720 |
| **Null** | 0 |
| **Ý nghĩa** | Số lượng review "Recommended" (thích/thỏa mãn) từ cộng đồng Steam, theo SteamSpy. Đây là số đánh giá tích cực thu thập được (có thể là toàn bộ lịch sử). Số càng cao cho thấy game càng phổ biến và được đánh giá nhiều. |
| **Ví dụ** | Palworld: 358,266 | Black Myth: Wukong: 1,111,720 (cao nhất) |

---

### 4.2 `negative_ratings` — Số đánh giá tiêu cực

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Integer |
| **Miền giá trị** | 0 – 294,520 |
| **Null** | 0 |
| **Ý ngh�a** | Số lượng review "Not Recommended" (không thích/không hài lòng) từ cộng đồng Steam. |
| **Ví dụ** | Black Myth: Wukong: 38,378 | Call of Duty MW2: 294,520 (cao nhất do nhiều người chơi) |

---

### 4.3 `total_ratings` — Tổng số đánh giá

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Integer |
| **Miền giá trị** | 101 – 1,150,098 |
| **Null** | 0 |
| **Ý nghĩa** | Tổng số đánh giá đã xử lý = `positive_ratings + negative_ratings`. Là proxy cho độ phổ biến và mức độ tương tác của game. Giá trị tối thiểu 101 là ngưỡng SteamSpy dùng để lọc game có đủ dữ liệu đánh giá. |
| **Ví dụ** | Black Myth: Wukong: 1,150,098 = 1,111,720 + 38,378 |

---

### 4.4 `rating_ratio` — Tỷ lệ đánh giá tích cực

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Float |
| **Miền giá trị** | 0.093 – 1.0 (9.3% – 100%) |
| **Null** | 0 |
| **Công thức** | `rating_ratio = positive_ratings / total_ratings` |
| **Ý nghĩa** | Tỷ lệ phần trăm đánh giá tích cực. Giá trị cao (> 0.8) cho thấy game được đánh giá tốt bởi người chơi. Giá trị thấp (< 0.5) cho thấy game gây tranh cãi hoặc có vấn đề lớn. Tuy nhiên cần kết hợp với `wilson_score` vì `rating_ratio` không tính đến số lượng đánh giá. |
| **Ví dụ** | Mirror 2: rating_ratio = 0.246 (rất thấp, ~25% tích cực) |

---

### 4.5 `wilson_score` — Điểm Wilson Score

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Float |
| **Miền giá trị** | 0.053 – 0.995 |
| **Null** | 0 |
| **Ý nghĩa** | Điểm xếp hạng có độ tin cậy thống kê (Wilson Score Interval). Khác với `rating_ratio` đơn thuần, Wilson Score cân bằng giữa **tỷ lệ tích cực** và **số lượng đánh giá**. Game có nhiều đánh giá và tỷ lệ cao sẽ có điểm cao. Game có ít đánh giá dù tỷ lệ 100% cũng chỉ có điểm vừa phải. Dùng để xếp hạng game một cách công bằng hơn. |
| **Công thức** | Dựa trên Wilson Score Interval với confidence level 95% |
| **Ví dụ** | Balatro: wilson_score = 0.979 (rất cao, nhiều đánh giá + tỷ lệ gần 100%) |

---

### 4.6 `temp_total` — Tổng đánh giá thô (proxy)

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Integer |
| **Miền giá trị** | 101 – 1,150,098 |
| **Null** | 0 |
| **Ý nghĩa** | Cột trung gian trong quá trình xử lý dữ liệu, có giá trị bằng `total_ratings`. Được tạo ra từ `positive_ratings + negative_ratings`. Trong hầu hết các trường hợp, `temp_total = total_ratings`. Có thể dùng để kiểm tra tính nhất quán. |

---

## 5. Người chơi & Độ phổ biến

### 5.1 `ccu` — Concurrent Users (người chơi đồng thời)

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Integer |
| **Miền giá trị** | 0 – 163,599 |
| **Null** | 0 |
| **Ý nghĩa** | Số người chơi đồng thời (concurrent users) tối đa trong 24 giờ qua, theo SteamSpy. Là chỉ số "hotness" — game nào đang có nhiều người chơi cùng lúc. Khác với `owners` (tổng số người sở hữu), `ccu` phản ánh hoạt động thời gian thực. |
| **Ví dụ** | ELDEN RING NIGHTREIGN: 163,599 CCU (cao nhất, vừa ra mắt) |

---

### 5.2 `owners` — Khoảng số chủ sở hữu (SteamSpy)

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | String (categorical range) |
| **Miền giá trị** | 12 khoảng cố định (xem bảng dưới) |
| **Null** | 0 |
| **Unique** | 12 giá trị |
| **Ý nghĩa** | Ước tính khoảng số người sở hữu game trên Steam, theo SteamSpy. Đây là ước tính không chính xác 100% (Steam không công bố số liệu này). SteamSpy dùng phương pháp thống kê để ước tính và phân vào 12 khoảng. Khoảng lớn hơn = game càng phổ biến. |

**12 giá trị khoảng (từ thấp đến cao):**

| `owners` | Khoảng số chủ sở hữu |
|---|---|
| `0 .. 20,000` | Ít phổ biến / mới ra mắt |
| `20,000 .. 50,000` | Rất ít |
| `50,000 .. 100,000` | Ít |
| `100,000 .. 200,000` | Hơi ít |
| `200,000 .. 500,000` | Trung bình thấp |
| `500,000 .. 1,000,000` | Trung bình |
| `1,000,000 .. 2,000,000` | Trung bình cao |
| `2,000,000 .. 5,000,000` | Phổ biến |
| `5,000,000 .. 10,000,000` | Rất phổ biến |
| `10,000,000 .. 20,000,000` | Cực phổ biến |
| `20,000,000 .. 50,000,000` | Đình đám |
| `50,000,000 .. 100,000,000` | Huyền thoại |

---

### 5.3 `owners_min` — Cận dưới khoảng owners

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Integer |
| **Miền giá trị** | 0 – 50,000,000 |
| **Null** | 0 |
| **Ý nghĩa** | Giá trị nhỏ nhất của khoảng `owners`. Dùng để tính toán thống kê mô tả (ví dụ: xác định rõ phạm vi). Kết hợp với `owners_max` và `owners_midpoint` để làm phân tích về độ phổ biến. |

---

### 5.4 `owners_max` — Cận trên khoảng owners

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Integer |
| **Miền giá trị** | 20,000 – 100,000,000 |
| **Null** | 0 |
| **Ý nghĩa** | Giá trị lớn nhất của khoảng `owners`. Game có `owners_max = 100,000,000` thuộc nhóm phổ biến nhất (≥50 triệu chủ sở hữu). |

---

### 5.5 `owners_midpoint` — Điểm giữa khoảng owners

| Thuộc tính | Giá trị |
|---|---|
| **Kiểu dữ liệu** | Integer |
| **Miền giá trị** | 10,000 – 75,000,000 |
| **Null** | 0 |
| **Công thức** | `(owners_min + owners_max) / 2` |
| **Ý nghĩa** | Giá trị đại diện ước tính số chủ sở hữu của game, dùng để phân tích thống kê, vẽ biểu đồ, so sánh độ phổ biến. Là giá trị liên tục có thể dùng trong tính toán, thay vì dùng `owners` dạng categorical. |

---

## 6. Thể loại game (One-hot Encoding)

Có **23 cột** mã hóa nhị phân (0/1), mỗi cột tương ứng một thể loại Steam. Giá trị `1` = game thuộc thể loại đó, `0` = không thuộc. Một game có thể thuộc nhiều thể loại đồng thời.

### Định nghĩa từng thể loại

| # | Cột | Thể loại | Số game | % | Ý nghĩa |
|---|---|---|---|---|---|
| 1 | `genre_Accounting` | Accounting | 1 | 0.0% | Phần mềm kế toán, quản lý tài chính cá nhân/doanh nghiệp |
| 2 | `genre_Action` | Action | 1,598 | 41.3% | Hành động: yêu cầu phản xạ, tốc độ, thể loại phổ biến nhất |
| 3 | `genre_Adventure` | Adventure | 1,776 | 45.9% | Phiêu lưu: khám phá, cốt truyện, giải đố — phổ biến nhất |
| 4 | `genre_Animation & Modeling` | Animation & Modeling | 10 | 0.3% | Công cụ tạo/hiệu chỉnh animation, 3D modeling |
| 5 | `genre_Audio Production` | Audio Production | 1 | 0.0% | Phần mềm sản xuất âm thanh, DAW |
| 6 | `genre_Casual` | Casual | 1,272 | 32.9% | Game thư giãn, dễ chơi, không yêu cầu kỹ năng cao |
| 7 | `genre_Design & Illustration` | Design & Illustration | 7 | 0.2% | Công cụ thiết kế đồ họa, vẽ minh họa |
| 8 | `genre_Early Access` | Early Access | 391 | 10.1% | Game đang trong giai đoạn phát triển mở, người chơi mua trước |
| 9 | `genre_Education` | Education | 1 | 0.0% | Game giáo dục, học tập |
| 10 | `genre_Free To Play` | Free To Play | 178 | 4.6% | Miễn phí chơi, có thể có microtransactions |
| 11 | `genre_Game Development` | Game Development | 4 | 0.1% | Công cụ phát triển game (engine, editor) |
| 12 | `genre_Indie` | Indie | 2,501 | 64.7% | Game từ studio độc lập nhỏ — phổ biến nhất |
| 13 | `genre_Massively Multiplayer` | Massively Multiplayer | 97 | 2.5% | Game nhiều người chơi trực tuyến hàng loạt (MMO/MMORPG) |
| 14 | `genre_Photo Editing` | Photo Editing | 1 | 0.0% | Phần mềm chỉnh sửa ảnh |
| 15 | `genre_RPG` | RPG | 1,232 | 31.9% | Nhập vai: phát triển nhân vật, cốt truyện |
| 16 | `genre_Racing` | Racing | 95 | 2.5% | Đua xe, đua động cơ |
| 17 | `genre_Simulation` | Simulation | 1,107 | 28.6% | Mô phỏng: quản lý, xây dựng, phiêu lưu thực tế |
| 18 | `genre_Sports` | Sports | 133 | 3.4% | Thể thao: bóng đá, bóng rổ, đua, v.v. |
| 19 | `genre_Strategy` | Strategy | 970 | 25.1% | Chiến thuật: quản lý tài nguyên, xây dựng, chiến đấu có kế hoạch |
| 20 | `genre_Utilities` | Utilities | 15 | 0.4% | Công cụ tiện ích (benchmark, mod manager, ...) |
| 21 | `genre_Video Production` | Video Production | 2 | 0.1% | Phần mềm sản xuất video |
| 22 | `genre_Web Publishing` | Web Publishing | 1 | 0.0% | Công cụ xuất bản nội dung web |

> **Ghi chú:** 8 thể loại đầu tiên trong danh sách Steam (Accounting → Game Development) thường ít gặp trong game phổ biến, trong khi Indie, Action, Adventure, Casual, RPG, Simulation, Strategy chiếm đa số. Thể loại "Early Access" là nhãn trạng thái phát triển, không phải thể loại chính, nhưng được encode như một cột riêng.

---

## 7. Tham chiếu: Giá trị định danh

### Cột không có trong dataset nhưng quan trọng hiểu

| Tên cột (không tồn tại) | Giá trị thay thế trong dataset |
|---|---|
| `developer` | Dùng `developer_spy` hoặc `developer_store` |
| `publisher` | Dùng `publisher_spy` hoặc `publisher_store` |
| `initialprice` (USD) | `initialprice` hiện lưu cents — chia 100 để ra USD |

### Quan hệ giữa các cột giá

```
price (USD, cuối cùng)
  ├── is_free (0/1) → price = 0 nếu 1
  ├── price_group ("Free"/"<$10"/"$10-30"/">$30")
  ├── initialprice (cents) → giá ra mắt ban đầu
  ├── discount (%) → mức giảm giá hiện tại
  ├── price_store (USD, từ Steam Store, có thể null)
  └── price_spy (cents, từ SteamSpy, thường là outliers)
```

### Quan hệ giữa các cột đánh giá

```
total_ratings = positive_ratings + negative_ratings = temp_total
rating_ratio = positive_ratings / total_ratings
wilson_score = Wilson(positive_ratings, total_ratings)  ← công thức thống kê
```

### Quan hệ giữa các cột owners

```
owners (categorical range)
  ├── owners_min (integer, cận dưới)
  ├── owners_max (integer, cận trên)
  └── owners_midpoint = (owners_min + owners_max) / 2
```

---

## Tổng quan kiểu dữ liệu

| Kiểu | Số cột | Các cột |
|---|---|---|
| Integer (số nguyên) | 13 | `appid`, `positive_ratings`, `negative_ratings`, `price_spy`, `initialprice`, `discount`, `ccu`, `owners_min`, `owners_max`, `owners_midpoint`, `temp_total`, `total_ratings` + 23 genre_* |
| Float (số thực) | 8 | `price_store`, `is_free`, `year`, `rating_ratio`, `wilson_score`, `price`, `owners_midpoint` + genre_* |
| String (văn bản) | 7 | `name`, `developer_spy`, `publisher_spy`, `developer_store`, `publisher_store`, `store_name`, `release_date`, `owners`, `price_group` + genre labels |
| Binary (0/1) | 23 | Tất cả `genre_*` + `is_free` |
