# Nhật ký kiểm thử - Nice Fold Saigon Premium

Danh sách các lỗi phát hiện được trong quá trình kiểm thử và cách khắc phục.

## Nhật ký lỗi

### Lỗi 1: Chatbot trả lời sai khi khách hỏi giá ("giá bao nhiêu")
* **Triệu chứng:** Khi người dùng nhập "giá bao nhiêu", chatbot nhận diện sai từ khóa và phản hồi bằng tin nhắn Chào mừng (Greeting) thay vì hiển thị Bảng giá.
* **Nguyên nhân:** Thuật toán cũ sử dụng hàm `.includes()` tìm kiếm chuỗi con. Từ "nhiêu" khi bỏ dấu thành "nhieu" chứa chuỗi con "hi", từ đó khớp với từ khóa "hi" của phần Chào mừng (Greeting) nằm ở đầu danh sách câu hỏi. Ngoài ra, việc thay thế từ đồng nghĩa (synonyms) cũng sử dụng `.includes()` dẫn đến việc thay thế nhầm các chuỗi con trong từ (ví dụ: thay thế "hi" trong "nhieu" thành "xin chào", biến "nhiêu" thành "nxinchàoeu").
* **Cách khắc phục:** 
  * Định nghĩa hàm trợ giúp `matchKeyword(sourceText, keyword)` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) sử dụng biểu thức chính quy (RegEx) để kiểm tra khớp từ khóa theo ranh giới từ (word boundaries) kết hợp hỗ trợ tiếng Việt có dấu.
  * Cập nhật các vòng lặp kiểm tra từ khóa chatbot trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) để sử dụng `matchKeyword` thay vì `.includes()`, đảm bảo chỉ khớp khi là từ độc lập (ví dụ: khớp từ "hi" riêng lẻ chứ không khớp "hi" trong "nhieu").
  * Sửa logic thay thế từ đồng nghĩa (synonym replacement) trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) để sử dụng biểu thức chính quy với ranh giới từ (word boundaries), tránh việc dán đè nhầm cụm từ nằm trong từ khác.

### Lỗi 2: Chatbot trả lời sai hoặc không hiểu các câu hỏi về đồ lụa, áo dài, đồ da, spa hàng hiệu
* **Triệu chứng:** 
  * Khi khách hỏi *"Dịch vụ giặt ủi của mình có hợp với quần áo lụa không?"*, chatbot trả lời sai (khớp nhầm sang giá giặt áo sơ mi).
  * Khi khách hỏi *"Mình có áo lụa, gửi được không?"*, *"bên bạn có giặt áo dài không"*, *"bên bạn có phục hồi đồ da không"*, *"bên bạn có spa hàng hiệu không"*, chatbot phản hồi tin nhắn lỗi không hiểu câu hỏi (fallback message).
  * Khi khách hỏi *"có giặt giày da không"*, chatbot trả lời cảnh báo không nhận đồ da (vì tiệm có nhận vệ sinh giày da bằng tay, nhưng hệ thống bị nhận diện nhầm là áo da/quần da).
* **Nguyên nhân:** 
  * Trong bộ câu hỏi FAQ của chatbot chưa có kịch bản xử lý cho các loại đồ nhạy cảm, đồ không nhận giặt hoặc các dịch vụ phục chế/spa hàng hiệu cao cấp (Nice Fold chỉ nhận wash & fold thông thường).
  * Lỗi nhận nhầm "giày da" thành đồ không nhận giặt là do từ khóa `"da"` và `"leather"` đứng độc lập được thêm vào danh sách từ chối, khiến cụm từ *"giày da"* bị khớp nhầm.
* **Cách khắc phục:** 
  * Tạo một câu hỏi FAQ mới có ID `unsupported_query` chuyên để cảnh báo và từ chối các loại đồ nhạy cảm/không hỗ trợ trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js).
  * Đặt câu hỏi `unsupported_query` này lên vị trí thứ 3 (độ ưu tiên cao, ngay sau tin nhắn chào mừng) để đảm bảo nếu khách đề cập đến lụa, da, áo dài, hàng hiệu thì hệ thống sẽ lập tức nhận diện và phản hồi cảnh báo.
  * Tinh chỉnh lại bộ từ khóa của `unsupported_query`: **Loại bỏ từ khóa `"da"` và `"leather"` đứng một mình**, thay bằng các cụm từ chỉ quần áo da cụ thể như: `"đồ da"`, `"do da"`, `"áo da"`, `"ao da"`, `"quần da"`, `"quan da"`, `"leather jacket"`, `"leather clothes"`. Điều này đảm bảo khi khách hỏi *"giày da"* thì hệ thống sẽ khớp đúng vào dịch vụ giặt giày (`shoes_query`), còn khi hỏi *"áo da"* hoặc *"đồ da"* thì hệ thống sẽ cảnh báo không nhận giặt.
  * Cập nhật văn phong phản hồi của `unsupported_query` theo đúng luật CSKH: trả lời trực diện từ chối nhận giặt đồ lụa/nhạy cảm trước, giải thích lý do do tiệm chuyên giặt sấy tự động thông thường không hỗ trợ giặt hấp/thủ công, và kết thúc bằng câu xin lỗi lịch sự mong khách thông cảm.

### Lỗi 3: Trùng khớp chuỗi không dấu gây nhận diện sai chủ đề (lên/len, tôi/tối, hí/hi) và độ ưu tiên kịch bản
* **Triệu chứng:**
  * Khách hỏi *"Bạn có lên tận phòng lấy đồ không..."* bị trả lời cảnh báo không nhận đồ len (vì từ `"lên"` bỏ dấu thành `"len"`, trùng với từ khóa len dạ).
  * Khách hỏi *"Địa chỉ tiệm ở đâu, tôi tự mang qua..."* bị nhảy vào kịch bản trả lời lấy đồ sau 5h chiều (vì từ `"tôi"` bỏ dấu thành `"toi"`, trùng với từ khóa `"tối"` của kịch bản late pickup).
  * Khách hỏi *"hí ship tính thế nào?"* (typo của phí ship) bị nhảy vào Chào mừng (vì `"hí"` bỏ dấu thành `"hi"`, trùng với `"hi"` của kịch bản chào mừng).
  * Khách hỏi giao đồ đêm *"Tối muộn 9-10h đêm..."* bị khớp nhầm vào kịch bản giao nhận thông thường (`pickup`) thay vì kịch bản lấy đồ sau 5h chiều (`after5`).
* **Nguyên nhân:**
  * Hệ thống so khớp không dấu bằng cách bỏ dấu của cả câu hỏi và từ khóa, dẫn đến các từ vô nghĩa hoặc khác nghĩa bị trùng nhau sau khi bỏ dấu.
  * Độ ưu tiên của các kịch bản bị lệch (kịch bản giao nhận `pickup` nằm trên kịch bản thời gian `after5`, nên khi câu hỏi chứa cả hai thông tin thì `pickup` luôn thắng).
  * Kịch bản giao nhận thiếu các từ khóa độc lập như `"ship"`, `"phí ship"`, `"giá ship"`, `"trời mưa"` vào kịch bản giao nhận `pickup`.
* **Cách khắc phục:**
  * Thay thế các từ khóa một từ dễ trùng trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) thành cụm từ ghép: `"len"` và `"dạ"` thành `"áo len"`, `"đồ len"`, `"áo dạ"`, `"đồ dạ"`.
  * Thay thế từ khóa `"tối"` của kịch bản lấy đồ sau 5h chiều (`after5`) thành cụm từ ghép `"buổi tối"`, `"sau 5h"`, `"sau 5 giờ"`, `"đêm"`, `"muộn"`.
  * Bổ sung các từ khóa `"ship"`, `"phí ship"`, `"giá ship"`, `"trời mưa"` vào kịch bản giao nhận `pickup`.
  * Thay đổi thứ tự trong mảng `questions` ở [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) đưa kịch bản lấy đồ muộn `after5` lên trước kịch bản giao nhận `pickup` để ưu tiên trả lời về thời gian giao nhận khi khách hỏi giờ muộn.

### Lỗi 4: Thiếu kịch bản trả lời các chủ đề về giặt riêng, sấy khô xếp vali và loại nước giặt
* **Triệu chứng:**
  * Khách hỏi *"Bên bạn có giặt chung đồ của tôi với người khác không?"* bị nhảy vào kịch bản trả lời lấy đồ sau 5h chiều (do từ `"tôi"` khớp `"tối"` ở file chưa cập nhật). Ngoài ra, tiệm chưa có kịch bản trả lời cụ thể để chứng minh cam kết giặt riêng.
  * Khách hỏi *"Đồ có được sấy khô hoàn toàn để xếp vào vali luôn không?"* bị rơi vào fallback không hiểu câu hỏi.
  * Khách hỏi *"Bên bạn dùng nước giặt gì? Có thơm không?"* bị rơi vào fallback không hiểu câu hỏi.
* **Nguyên nhân:** Chatbot chưa được cấu hình kịch bản dữ liệu cho các câu hỏi quan tâm sâu về vệ sinh (giặt riêng), độ khô (xếp vali) và hóa chất sử dụng (nước giặt/độ thơm).
* **Cách khắc phục:**
  * Bổ sung 3 kịch bản FAQ mới vào [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) bao gồm:
    1. `hygiene_query`: Khớp các từ khóa `"giặt chung"`, `"giat chung"`, `"giặt riêng"`, `"giat rieng"` $\rightarrow$ Trả lời cam kết giặt riêng từng máy độc lập 100%.
    2. `drying_query`: Khớp các từ khóa `"sấy khô"`, `"xếp vali"`, `"cất vali"` $\rightarrow$ Trả lời cam kết sấy khô hoàn toàn 100% bằng máy chuyên dụng.
    3. `detergent_query`: Khớp các từ khóa `"nước giặt"`, `"nước xả"`, `"thơm"`, `"mùi"` $\rightarrow$ Trả lời về các loại nước giặt/xả cao cấp, thơm dịu, lành tính.
  * Đặt 3 kịch bản này ở vị trí ưu tiên cao (sau `unsupported_query`) để bắt chính xác các câu hỏi này.

### Lỗi 5: Nhận diện sai chủ đề thanh toán (cọc trước/giặt xong trả tiền) và thiếu kịch bản bồi thường, phai màu đồ
* **Triệu chứng:**
  * Khách hỏi *"tôi phải cọc trước hay giặt xong mới trả tiền?"* bị nhảy nhầm vào kịch bản Bảng giá (`pricing_query`) thay vì kịch bản Thanh toán (`payment`).
  * Khách hỏi *"Lỡ làm mất đồ hoặc hỏng đồ của tôi thì đền thế nào?"* bị nhảy vào kịch bản thời gian muộn (do chữ `"tôi"` khớp `"tối"` ở bản cũ trên host) hoặc rơi vào fallback.
  * Khách hỏi *"Đồ của tôi bị phai màu thì sao?"* bị nhảy nhầm sang kịch bản Giặt riêng đồ trắng (`whites`).
* **Nguyên nhân:**
  * Kịch bản thanh toán (`payment`) thiếu từ khóa liên quan đến việc *"đặt cọc"`, *"trả tiền"* dẫn đến việc từ *"tiền"* bị khớp nhầm vào kịch bản bảng giá.
  * Tiệm chưa có kịch bản bồi thường cụ thể khi xảy ra sự cố hư hỏng/mất đồ của khách du lịch.
  * Việc hỏi phai màu bị nhảy sang đồ trắng tuy có liên quan nhưng cần phản hồi giải thích rõ ràng hơn về giới hạn trách nhiệm của tiệm.
* **Cách khắc phục:**
  * Bổ sung các từ khóa `"trả tiền"`, `"cọc"`, `"đặt cọc"` vào kịch bản thanh toán (`payment`) để định tuyến chính xác.
  * Bổ sung kịch bản `compensation_query` vào [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) với từ khóa `"mất đồ"`, `"hỏng đồ"`, `"đền"`, `"đền bù"` $\rightarrow$ Trả lời rõ ràng chính sách đền bù tối đa lên tới 10 lần phí dịch vụ (tối đa 2.000.000đ).
  * Bổ sung kịch bản `color_bleed_query` vào [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) với từ khóa `"phai màu"`, `"lem màu"`, `"loang màu"` $\rightarrow$ Khuyên khách chọn dịch vụ giặt riêng đồ trắng và giải thích tiệm không chịu trách nhiệm trong trường hợp quần áo tự phai màu do thuốc nhuộm kém chất lượng.

### Lỗi 6: Câu trả lời giặt giày da quá dài dòng và chứa cả giá giày thể thao/canvas
* **Triệu chứng:** Khách hỏi *"có giặt giày da không"*, chatbot phản hồi cả bảng giá giặt giày (trong đó ghi cả giá giày thể thao, gói hỏa tốc,...), khiến câu trả lời bị dài và không tập trung vào đúng câu hỏi của khách.
* **Nguyên nhân:** Chưa có kịch bản riêng biệt dành riêng cho giày da/da lộn, nên câu hỏi về giày da phải dùng chung kịch bản giặt giày tổng quát (`shoes_query`).
* **Cách khắc phục:**
  * Tạo kịch bản FAQ mới chuyên biệt mang ID `leather_shoes_query` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js).
  * Từ khóa bao gồm: `"giày da"`, `"giay da"`, `"giặt giày da"`, `"vệ sinh giày da"`, `"giày da lộn"`, `"giay da lon"`.
  * Trả lời trực tiếp và ngắn gọn: Xác nhận có nhận giặt giày da & da lộn và nêu đúng giá **220.000đ / đôi** kèm phí ship khứ hồi 50.000đ.
  * Cấu hình điều hướng kịch bản để khi khách hỏi về giày da thì chatbot hiển thị các nút hành động (nút đặt lịch và menu chính) giống như kịch bản giặt giày thông thường.

### Lỗi 7: Hỏi gửi đồ ở lễ tân bị rơi vào tin nhắn không hiểu (fallback)
* **Triệu chứng:** Khách hỏi *"Tôi gửi đồ ở lễ tân rồi bạn qua lấy được không?"* bị rơi vào fallback không hiểu câu hỏi.
* **Nguyên nhân:** Cụm từ trên không chứa từ khóa ghép `"lấy đồ"`, chỉ chứa từ `"lấy"`. Đồng thời trong danh sách từ khóa của kịch bản giao nhận `pickup` bị thiếu các từ đặc trưng của khách sạn Việt Nam như `"lễ tân"`, `"gửi đồ"`, `"sảnh"`.
* **Cách khắc phục:**
  * Bổ sung các từ khóa tiếng Việt đặc thù của giao nhận khách sạn vào kịch bản `pickup` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js): `"lễ tân"`, `"le tan"`, `"gửi lễ tân"`, `"gui le tan"`, `"sảnh"`, `"sanh"`, `"gửi đồ"`, `"gui do"`, `"nhận đồ"`, `"nhan do"`.

### Lỗi 8: Câu trả lời về giao nhận lên phòng chưa làm rõ việc chỉ giao nhận tại sảnh lễ tân
* **Triệu chứng:** Khách hỏi *"Bạn có lên tận phòng lấy đồ không hay tôi phải xuống sảnh?"*, chatbot trả lời thông tin giao nhận chung chung nhưng chưa trả lời trực tiếp là phải xuống sảnh/lễ tân chứ tiệm không lên phòng do vấn đề an ninh.
* **Nguyên nhân:** Kịch bản phản hồi của `pickup` chưa nhấn mạnh rõ giới hạn địa điểm giao nhận tại sảnh khách sạn do vấn đề an ninh.
* **Cách khắc phục:**
  * Thay đổi nội dung phản hồi của kịch bản `pickup` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js): Khẳng định rõ để đảm bảo an ninh khách sạn, shipper của chúng tôi không thể lên phòng riêng. Yêu cầu khách vui lòng gặp shipper tại sảnh lễ tân, hoặc gửi đồ trước tại quầy lễ tân khách sạn để lấy/giao tiện lợi.

### Lỗi 9: Hỏi địa chỉ tự mang đồ bị rơi vào fallback hoặc nhận diện sai
* **Triệu chứng:** Khách hỏi *"Địa chỉ tiệm ở đâu, tôi tự mang qua được không?"*, chatbot phản hồi sai hoặc fallback.
* **Nguyên nhân:** Chưa có kịch bản riêng cho câu hỏi về địa điểm xưởng giặt và việc khách hàng tự đem đồ tới xưởng thay vì đặt giao nhận tận nơi.
* **Cách khắc phục:**
  * Tạo kịch bản FAQ mới mang ID `address_query` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js).
  * Từ khóa bao gồm: `"địa chỉ"`, `"dia chi"`, `"tự mang"`, `"tu mang"`, `"đến tiệm"`, `"xưởng"`, `"location"`, `"address"`.
  * Phản hồi trực tiếp: Nêu rõ địa chỉ **121/10 Lê Thị Riêng, Bến Thành, Quận 1, TP.HCM** kèm đường link Google Maps trực tiếp: https://maps.app.goo.gl/gJG1N3VRNuTYXMSy9. Giải thích chính sách giảm 25.000đ/lượt tự mang.

### Lỗi 10: Hỏi khu vực phục vụ (Quận 1, Quận 3, Quận 7...) bị phản hồi thông tin sảnh lễ tân chung chung
* **Triệu chứng:** Khách hỏi *"Có giao đồ ở Quận 1 / Quận 3 / Quận 7... không?"*, chatbot phản hồi kịch bản giao nhận sảnh lễ tân mà không nói rõ có giao nhận đến các quận đó hay không.
* **Nguyên nhân:** Thiếu kịch bản thông tin chi tiết về các quận huyện và khu vực phục vụ chính của tiệm giặt.
* **Cách khắc phục:**
  * Tạo kịch bản FAQ mới mang ID `coverage_query` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js).
  * Từ khóa bao gồm: `"quận 1"`, `"quan 1"`, `"quận 3"`, `"quan 3"`, `"thảo điền"`, `"thao dien"`, `"quận 2"`, `"quan 2"`, `"quận 7"`, `"quan 7"`, `"bình thạnh"`, `"binh thanh"`, `"khu vực"`, `"khu vuc"`, `"quận nào"`, `"quan nao"`, `"quận"`, `"quan"`, `"district"`.
  * Phản hồi chi tiết: Liệt kê các khu vực hỗ trợ freeship dưới 6km (Q1, Q3, Bình Thạnh, Thảo Điền Q2) và các quận xa hơn (Q7, Q4, Phú Nhuận,...) thì tiệm vẫn có thể phục vụ kèm mức phụ phí nhỏ từ 20.000đ - 50.000đ.

### Lỗi 11: Hỏi về giờ bay hoặc checkout gấp bị nhảy sang thông tin giao nhận chung chung
* **Triệu chứng:** Khách hỏi *"Tôi sắp bay/check-out lúc 6h tối, có kịp nhận đồ không"*, chatbot phản hồi kịch bản giao nhận sảnh lễ tân mà không giải đáp cụ thể cam kết giao đồ trước giờ bay/checkout.
* **Nguyên nhân:** Thiếu kịch bản căn chỉnh thời gian giặt sấy theo lịch trình chuyến bay hoặc trả phòng của khách du lịch.
* **Cách khắc phục:**
  * Tạo kịch bản FAQ mới mang ID `flight_checkout_query` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js).
  * Từ khóa bao gồm: `"bay"`, `"chuyến bay"`, `"chuyen bay"`, `"checkout"`, `"check-out"`, `"check out"`, `"trả phòng"`, `"tra phong"`, `"kịp không"`, `"kip khong"`, `"kịp nhận"`, `"flight"`, `"leave"`, `"leaving"`, `"airport"`.
  * Phản hồi chi tiết: Cam kết giao đồ trước giờ bay/checkout. Hướng dẫn khách sử dụng gói **Hỏa tốc 4H** (gửi trước 1h trưa để nhận trước 5h chiều nếu bay lúc 6h tối) hoặc gửi từ ngày hôm trước với gói **Tiêu chuẩn 24H**.

### Lỗi 12: Hỏi về thời điểm bắt đầu tính giờ gói Hỏa tốc bị rơi vào fallback không hiểu
* **Triệu chứng:** Khách hỏi *"Giặt hỏa tốc 4 tiếng là tính từ lúc nào?"*, chatbot phản hồi tin nhắn lỗi không hiểu câu hỏi (fallback message).
* **Nguyên nhân:** Thiếu kịch bản giải thích thời điểm tính giờ của dịch vụ Hỏa tốc (bắt đầu tính từ khi shipper lấy đồ thành công).
* **Cách khắc phục:**
  * Tạo kịch bản FAQ mới mang ID `express_start_query` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js).
  * Từ khóa bao gồm: `"tính từ lúc nào"`, `"tinh tu luc nao"`, `"từ lúc nào"`, `"4 tiếng"`, `"4 tieng"`, `"from when"`.
  * Phản hồi chi tiết: Giải thích rõ ràng 4 tiếng được tính kể từ lúc shipper nhận đồ từ khách/lễ tân đến lúc giao đồ lại sảnh lễ tân.

### Lỗi 13: Hỏi về giao đồ khi trời mưa bị trả lời theo kịch bản giao nhận chung sảnh lễ tân
* **Triệu chứng:** Khách hỏi *"Hôm nay trời mưa có giao đồ đúng hẹn không?"*, chatbot trả lời kịch bản giao nhận sảnh lễ tân mà không giải đáp cụ thể cách bảo vệ đồ và cam kết đúng giờ khi trời mưa.
* **Nguyên nhân:** Thiếu kịch bản trấn an về phương án giao nhận chống nước và cam kết thời gian khi thời tiết xấu.
* **Cách khắc phục:**
  * Tạo kịch bản FAQ mới mang ID `rainy_day_query` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js).
  * Từ khóa bao gồm: `"trời mưa"`, `"troi mua"`, `"mưa"`, `"ngập"`, `"rain"`.
  * Phản hồi chi tiết: Cam kết giao đúng hẹn ngày mưa. Giải thích phương án bọc kín đồ sạch bằng **2 lớp túi chống nước chuyên dụng** và chính sách xin phép hẹn giao lại khi bớt mưa nếu mưa lớn (trừ khi khách cần gấp).

### Lỗi 14: Hỏi tách riêng đồ trắng bị nhảy nhầm sang kịch bản giặt riêng từng khách hàng
* **Triệu chứng:** Khách hỏi *"Có tách riêng đồ trắng giặt riêng không?"*, chatbot phản hồi kịch bản cam kết giặt riêng từng máy độc lập cho mỗi khách hàng (`hygiene_query`) thay vì kịch bản phụ phí giặt riêng đồ trắng (`whites`).
* **Nguyên nhân:** Do kịch bản `hygiene_query` nằm trước kịch bản `whites` nên từ khóa "giặt riêng" bị khớp nhầm trước.
* **Cách khắc phục:**
  * Thay đổi thứ tự ưu tiên trong mảng `questions` ở [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js). Đưa kịch bản giặt đồ trắng (`whites`) lên trước kịch bản giặt riêng mỗi khách (`hygiene_query`). Khi khách hỏi có chứa từ khóa đồ trắng, đồ màu thì sẽ lập tức ưu tiên trả lời kịch bản giặt đồ trắng.

### Lỗi 15: Hỏi gửi ít đồ (1-2kg) bị trả về bảng giá chung chung mà không làm rõ mức tính giá tối thiểu
* **Triệu chứng:** Khách hỏi *"Đồ của tôi chỉ có 1-2kg thì tính giá thế nào?"*, chatbot trả về toàn bộ bảng giá các gói mà không giải thích cụ thể rằng giá sẽ tính theo mức tối thiểu của gói giặt khách chọn.
* **Nguyên nhân:** Thiếu kịch bản giải thích cơ chế tính phí tối thiểu (minimum charge) cho các đơn hàng ít quần áo (dưới 3kg hoặc 4kg).
* **Cách khắc phục:**
  * Tạo kịch bản FAQ mới mang ID `low_weight_query` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js).
  * Từ khóa bao gồm: `"1-2kg"`, `"1kg"`, `"2kg"`, `"ít đồ"`, `"ít kg"`, `"dưới 3kg"`, `"ít quần áo"`.
  * Phản hồi chi tiết: Xác nhận giá sẽ tùy theo gói giặt bạn chọn, giải thích tiệm có mức tính giá tối thiểu (ví dụ: Standard tính tối thiểu từ 3kg giá 170k, các gói khác tính tối thiểu từ 4kg) và liệt kê chi tiết giá tối thiểu của từng gói giặt chính.

### Lỗi 16: Hỏi làm sao biết số ký để tính tiền bị nhảy nhầm sang bảng giá chung chung
* **Triệu chứng:** Khách hỏi *"Làm sao biết đồ của tôi nặng bao nhiêu kg để tính tiền"*, chatbot trả về toàn bộ bảng giá các gói mà chưa hướng dẫn cụ thể quy trình tiệm sẽ nhận đồ và cân chính xác để báo lại cho khách.
* **Nguyên nhân:** Thiếu kịch bản giải thích quy trình cân đồ và gửi hóa đơn xác nhận sau khi shipper lấy đồ về tiệm.
* **Cách khắc phục:**
  * Tạo kịch bản FAQ mới mang ID `weghing_process_query` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js).
  * Từ khóa bao gồm: `"nặng bao nhiêu"`, `"biết kg"`, `"cân thế nào"`, `"cân đồ"`, `"sao biết cân"`, `"cân như thế nào"`.
  * Phản hồi chi tiết: Khẳng định khách không cần tự cân trước. Giải thích sau khi shipper mang đồ về tiệm cân có số ký cụ thể, tiệm sẽ tính tiền chính xác theo số ký thực tế và gửi thông báo xác nhận kèm hóa đơn chi tiết cho khách.

### Lỗi 17: Hỏi so sánh khác biệt giữa các gói giặt bị nhảy nhầm sang thời điểm tính giờ Hỏa tốc
* **Triệu chứng:** Khách hỏi *"Giá gói 4 tiếng khác gì gói trong ngày?"*, chatbot trả lời kịch bản thời điểm bắt đầu tính giờ gói Hỏa tốc (`express_start_query`) thay vì bảng so sánh các gói giặt chính.
* **Nguyên nhân:** Do kịch bản `express_start_query` chứa từ khóa "4 tiếng" và nằm trước kịch bản so sánh nên bị khớp nhầm trước.
* **Cách khắc phục:**
  * Tạo kịch bản FAQ mới mang ID `comparison_query` chuyên để so sánh sự khác biệt giữa các gói giặt chính (Tiêu chuẩn, Lấy trong ngày, Hỏa tốc) về thời gian và giá cả.
  * Từ khóa bao gồm: `"khác gì"`, `"khác biệt"`, `"so sánh"`, `"khác nhau"`, `"gói nào"`, `"lựa chọn"`.
  * Đưa kịch bản này lên trên `express_start_query` in mảng `questions` ở [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) để ưu tiên so sánh khi khách hỏi khác biệt.

### Lỗi 18: Hỏi phương thức thanh toán tiền mặt bị nhảy sang kịch bản giao nhận tại sảnh lễ tân
* **Triệu chứng:** Khách hỏi *"Tôi trả bằng tiền mặt lúc nhận đồ được không?"*, chatbot trả lời kịch bản giao nhận sảnh lễ tân (`pickup`) thay vì kịch bản phương thức thanh toán (`payment`).
* **Nguyên nhân:** Do kịch bản `pickup` chứa từ khóa "nhận đồ" và nằm trước kịch bản `payment` nên bị khớp nhầm trước.
* **Cách khắc phục:**
  * Thay đổi thứ tự ưu tiên trong mảng `questions` ở [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js). Đưa kịch bản thanh toán (`payment`) lên trước kịch bản giao nhận sảnh lễ tân (`pickup`). Khi khách hỏi có các từ khóa như "tiền mặt", "thanh toán", "chuyển khoản" thì hệ thống sẽ lập tức ưu tiên trả lời kịch bản thanh toán.

### Lỗi 19: Chính sách bồi thường chưa cập nhật theo mức đền bù thực tế hoặc tối đa 500.000đ và liên kết đồ không hỗ trợ
* **Triệu chứng:** Khách hỏi về chính sách bồi thường khi mất/hỏng đồ, chatbot trả lời đền gấp 10 lần giá dịch vụ (tối đa 2.000.000đ), không đúng với chính sách đền bù thực tế mới của tiệm.
* **Nguyên nhân:** Nội dung phản hồi trong `compensation_query` chưa cập nhật theo yêu cầu đền bù tối đa 500.000đ/món và chưa nhắc khách tham khảo danh sách đồ không hỗ trợ.
* **Cách khắc phục:**
  * Cập nhật phản hồi của `compensation_query` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) để:
    1. Nhắc nhở khách kiểm tra kỹ danh sách **⚠️ Đồ không hỗ trợ** (không gửi lụa, đồ da, len, blazer, đồ luxury).
    2. Khẳng định mức đền bù đối với đồ giặt sấy bị hư hỏng/mất mát là đền theo đúng giá trị thực tế của món đồ đó hoặc tối đa là 500.000đ/món.

### Lỗi 20: Chính sách phai màu & lem màu chưa nêu rõ yêu cầu sấy đặc biệt và giới hạn hỗ trợ đồ phai màu
* **Triệu chứng:** Khách hỏi *"Đồ của tôi bị phai màu thì sao?"*, chatbot phản hồi kịch bản phai màu cũ mà không nhắc nhở khách báo trước đồ không được sấy nhiệt để tiệm phơi khô tự nhiên, đồng thời chưa nêu rõ giới hạn không thể hỗ trợ thêm cho đồ tự phai màu.
* **Nguyên nhân:** Chưa cập nhật nội dung mới về yêu cầu sấy đặc biệt và miễn trách nhiệm đối với đồ tự phai màu do chất lượng vải kém.
* **Cách khắc phục:**
  * Cập nhật phản hồi của `color_bleed_query` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) để:
    1. Yêu cầu khách vui lòng báo trước những món đồ không được sấy nhiệt, tiệm sẽ hỗ trợ phơi khô tự nhiên thay vì sấy.
    2. Khẳng định tiệm không chịu trách nhiệm và không thể hỗ trợ thêm trong trường hợp quần áo tự phai màu/lem màu do thuốc nhuộm vải kém chất lượng.

### Lỗi 21: Khách hỏi quần áo công sở bị trả lời giá sơ mi gập chung chung mà chưa làm rõ giới hạn dịch vụ sấy gập (không ủi)
* **Triệu chứng:** Khách hỏi *"Dịch vụ giặt ủi của bạn có phù hợp với quần áo công sở không"*, chatbot trả lời thông tin giặt sấy áo sơ mi (`shirt_query`) mà chưa làm rõ bản chất quần áo công sở là đồ cần giữ form, cần ủi phẳng, trong khi tiệm chỉ có dịch vụ giặt sấy gập thông thường chứ không có dịch vụ ủi phẳng.
* **Nguyên nhân:** Do chưa có kịch bản riêng phân tích giới hạn của giặt sấy gập đối với quần áo công sở cần ủi là phẳng phiu.
* **Cách khắc phục:**
  * Tạo kịch bản FAQ mới mang ID `office_clothes_query` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js).
  * Từ khóa bao gồm: `"công sở"`, `"quần tây"`, `"sơ mi công sở"`, `"sơ mi đi làm"`, `"office wear"`.
  * Phản hồi chi tiết: Giải thích rõ Nice Fold chuyên dịch vụ **Giặt sấy gập (Wash & Fold)**, tiệm **KHÔNG có dịch vụ ủi (là) đồ** và không nhận giặt khô/giặt hấp ạ. Khuyên khách cân nhắc vì quần áo công sở cần giữ form, nếu gửi giặt sấy gập thì đồ sẽ bị nhăn, không giữ được form phẳng phiu đứng dáng.

### Lỗi 22: Rà soát toàn diện văn phong CSKH của chatbot đảm bảo bắt đầu trực diện và thân thiện, có đầu có đuôi
* **Triệu chứng:** Một số câu trả lời cũ của chatbot có văn phong hơi ngắn hoặc thiếu cấu trúc (ví dụ: giặt riêng đồ trắng chỉ trả lời "Có.", phơi gió tự nhiên trả lời quá cộc lốc, sấy nhiệt thấp/thanh toán/nhận đồ muộn chưa đủ dịu dàng).
* **Nguyên nhân:** Chưa được tối ưu hóa đồng bộ theo bộ quy tắc CSKH chuyên nghiệp.
* **Cách khắc phục:**
  * Cập nhật đồng loạt **17 phản hồi** trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) và [nice-fold-saigon-frontend/app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/nice-fold-saigon-frontend/app.js) để:
    1. Bắt đầu bằng câu trả lời trực diện kèm từ xưng hô lịch thiệp ("Dạ có ạ!", "Dạ tiệm xin lỗi vì chưa hỗ trợ...", "Dạ đối với...").
    2. Giải thích chi tiết, thấu đáo và thân thiện ở phần thân.
    3. Kết thúc bằng lời chúc, lời mời đặt lịch hoặc lời mong khách thông cảm ấm áp.

### Lỗi 23: Trùng lặp từ khóa "muốn" (muon) và "đêm" (dem) gây nhận diện sai sang kịch bản lấy đồ muộn (after5)
* **Triệu chứng:** Khách gõ câu hỏi chứa từ `"muốn"` hoặc `"đem"` (Ví dụ: *"tôi muốn giặt áo dài"*, *"tự đem đồ qua"*) bị chatbot nhận diện nhầm và phản hồi kịch bản thông tin giao nhận muộn sau 5h chiều (`after5`).
* **Nguyên nhân:**
  * Từ khóa `"muốn"` khi bỏ dấu thành `"muon"`, trùng khớp hoàn hảo với từ khóa `"muộn"` (đã được bỏ dấu thành `"muon"` trong cơ sở dữ liệu của chatbot).
  * Từ khóa `"đem"` (mang đồ đi) khi bỏ dấu thành `"dem"`, trùng khớp hoàn hảo với từ khóa `"đêm"` (đã được bỏ dấu thành `"dem"`).
* **Cách khắc phục:**
  * Loại bỏ hoàn toàn các từ đơn dễ gây trùng dấu như `"muộn"`, `"muon"`, `"đêm"`, `"dem"`, và cụm từ dễ trùng `"toi muon"` (xung đột với "tôi muốn") ra khỏi danh sách từ khóa của kịch bản `after5` trong cả hai file [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) và [nice-fold-saigon-frontend/app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/nice-fold-saigon-frontend/app.js).
  * Thay thế bằng các cụm từ ghép an toàn không lo xung đột: `"tối muộn"`, `"toi muon"`, `"đêm muộn"`, `"dem muon"`, `"lấy muộn"`, `"lay muon"`, `"giao muộn"`, `"giao muon"`, `"buổi đêm"`, `"buoi dem"`. Điều này giải quyết triệt để lỗi và không gây match nhầm khi khách gõ các câu hỏi thông dụng chứa *"muốn"* hoặc *"đem"*.

### Lỗi 24: Khách hỏi giặt áo cưới bị rơi vào tin nhắn không hiểu (fallback) thay vì báo từ chối giặt chất liệu nhạy cảm
* **Triệu chứng:** Khách hỏi *"có giặt áo cưới không"*, chatbot phản hồi tin nhắn không hiểu câu hỏi (fallback message).
* **Nguyên nhân:** Chưa bổ sung từ khóa nhận diện cho váy cưới/áo cưới vào nhóm đồ nhạy cảm, đồ không nhận giặt (`unsupported_query`). Áo cưới là loại đồ cực kỳ đặc biệt, đính đá, ren và tơ/voan mỏng dễ hỏng khi giặt máy sấy công nghiệp.
* **Cách khắc phục:**
  * Bổ sung thêm các từ khóa liên quan đến áo cưới vào kịch bản `unsupported_query` của cả hai file [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) và [nice-fold-saigon-frontend/app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/nice-fold-saigon-frontend/app.js):
    * Tiếng Việt: `"áo cưới"`, `"ao cuoi"`, `"váy cưới"`, `"vay cuoi"`.
    * Tiếng Anh: `"wedding dress"`, `"wedding gown"`, `"wedding dresses"`.
  * Nhờ đó khi khách hỏi về áo cưới, chatbot sẽ lập tức từ chối nhận giặt một cách lịch sự, dịu dàng, tránh gây hiểu lầm hoặc hư hỏng đồ của khách.

### Lỗi 25: Khách hỏi dịch vụ tẩy đồ/tẩy vết bẩn bị rơi vào tin nhắn không hiểu (fallback)
* **Triệu chứng:** Khách hỏi *"đồ của tôi bị dơ, có tẩy đồ không"*, chatbot phản hồi tin nhắn không hiểu câu hỏi (fallback message).
* **Nguyên nhân:** Tiệm giặt Nice Fold chuyên về giặt sấy tự động thông thường (Wash & Fold), **không nhận dịch vụ tẩy đồ hoặc xử lý các vết ố vàng/vết bẩn chuyên sâu**. Chatbot chưa được cấu hình kịch bản từ chối tẩy đồ nên rơi vào fallback.
* **Cách khắc phục:**
  * Tạo kịch bản FAQ mới mang ID `bleach_query` trong cả hai file [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) và [nice-fold-saigon-frontend/app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/nice-fold-saigon-frontend/app.js).
  * Từ khóa bao gồm:
    * Tiếng Việt: `"tẩy đồ"`, `"tay do"`, `"tẩy ố"`, `"tay o"`, `"tẩy trắng"`, `"tay trang"`, `"tẩy vết bẩn"`, `"tay vet ban"`, `"vết bẩn cứng đầu"`, `"vet ban cung dau"`, `"bị dơ"`, `"bi do"`, `"bleach"`, `"stain removal"`.
    * Tiếng Anh: `"bleach"`, `"bleaching"`, `"stain"`, `"stains"`, `"stain removal"`, `"stubborn stain"`.
  * Phản hồi chi tiết: Giải thích rõ tiệm không có dịch vụ tẩy ố/vết bẩn chuyên biệt do chỉ làm dịch vụ giặt sấy máy tự động, hướng dẫn khách thông cảm vì giặt thường chỉ sạch bụi bẩn và mồ hôi thông thường.

### Lỗi 26: Khách hỏi giặt áo phao được trả lời đồng ý giặt thường trong khi áo phao lông vũ là đồ cần giặt khô
* **Triệu chứng:** Khách hỏi *"có giặt áo phao không"*, chatbot phản hồi xác nhận nhận giặt và tính cước theo kg thông thường, không đúng với thực tế hoạt động của tiệm (Nice Fold chỉ chuyên giặt sấy gập máy thông thường, áo phao lông vũ/áo khoác phao dày cần được giặt khô/giặt hấp chuyên sâu để tránh làm hỏng và xẹp lớp lông vũ bên trong).
* **Nguyên nhân:** Định cấu hình nhầm áo phao thuộc nhóm đồ giặt sấy gập thông thường.
* **Cách khắc phục:**
  * Xóa bỏ hoàn toàn kịch bản `jacket_query` ở cả hai file [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) và [nice-fold-saigon-frontend/app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/nice-fold-saigon-frontend/app.js).
  * Chuyển các từ khóa của áo phao vào nhóm đồ không nhận giặt (`unsupported_query`) bao gồm: `"áo phao"`, `"ao phao"`, `"áo khoác phao"`, `"ao khoac phao"` (cho tiếng Việt) và `"puffer jacket"`, `"puffer jackets"`, `"down jacket"`, `"down jackets"` (cho tiếng Anh).
  * Cập nhật nội dung phản hồi của `unsupported_query` để chỉ rõ áo phao lông vũ nằm trong danh sách chất liệu nhạy cảm/cần giặt khô chuyên biệt mà tiệm chưa thể hỗ trợ.

### Lỗi 27: Phân tách kịch bản giặt khô và đồ nhạy cảm không cần thiết, cần hợp nhất các kịch bản đồ không nhận giặt/chỉ giặt khô
* **Triệu chứng:** Khách hỏi các câu hỏi về dịch vụ giặt khô, giặt hấp, ủi đồ hoặc gửi các món đồ cần giặt khô (như vest, suit, lụa, da, len, dạ, áo cưới, áo phao) bị phản hồi bởi 2 kịch bản khác nhau (`dryclean_query` và `unsupported_query`). Điều này làm tản mát từ khóa và nội dung phản hồi không được đồng bộ toàn diện.
* **Nguyên nhân:** Chưa hợp nhất các từ khóa và nội dung của dịch vụ giặt khô và đồ không hỗ trợ.
* **Cách khắc phục:**
  * Hợp nhất toàn bộ từ khóa của dịch vụ giặt khô/ủi đồ và tất cả các món đồ nhạy cảm cần giặt khô vào danh sách từ khóa của cả `unsupported_query` và `dryclean_query` trong [app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/app.js) và [nice-fold-saigon-frontend/app.js](file:///Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/nice-fold-saigon-frontend/app.js).
  * Cấu hình nội dung phản hồi chung vô cùng chuyên nghiệp và dịu dàng, nêu rõ lý do tiệm chỉ chuyên giặt sấy gập tự động (Wash & Fold), liệt kê rõ ràng toàn bộ các món đồ tiệm từ chối nhận (vest, blazer, lụa, áo dài lụa, đồ da, len, dạ, áo cưới/váy cưới, áo phao lông vũ, đồ đính đá/cườm...) và từ chối cung cấp dịch vụ giặt khô/giặt hấp/ủi phẳng riêng lẻ.
