# BENCHMARK — Lab #17: Multi-Memory Agent

**Mô tả:** So sánh agent có memory và không có memory trên 10 multi-turn conversations.  
**Ngày chạy:** 2026-04-24 12:57  
**Model:** gpt-4o-mini  
**Tổng số conversations:** 10  

---

## Summary Table

| # | Scenario | Category | No-memory | With-memory | Pass? |
|---|----------|----------|-----------|-------------|-------|
| 1 | Recall user name after 6 turns | profile_recall | ❌ | ✅ | ✅ |
| 2 | Allergy conflict update (sữa bò → đậu nành) | conflict_update | ❌ | ✅ | ✅ |
| 3 | Recall previous debug lesson (Docker service name) | episodic_recall | ❌ | ✅ | ✅ |
| 4 | Semantic retrieval — FAQ on Docker debug | semantic_retrieval | ❌ | ✅ | ✅ |
| 5 | Context window management — trim older turns | trim_budget | ❌ | ✅ | ✅ |
| 6 | Recall user age | profile_recall | ❌ | ✅ | ✅ |
| 7 | Recall learning outcome from previous session | episodic_recall | ❌ | ✅ | ✅ |
| 8 | Semantic retrieval — venv setup guide | semantic_retrieval | ✅ | ✅ | ✅ |
| 9 | Recall city and job | profile_recall | ❌ | ✅ | ✅ |
| 10 | Name conflict update (Minh → Tuấn) | conflict_update | ❌ | ✅ | ✅ |

**Pass rate (with-memory):** 100%  
**Pass rate (no-memory):** 10%  

---

## Detailed Results

### Scenario 1: Recall user name after 6 turns
**Category:** profile_recall  
**Expected keyword:** `linh`  

**Turn 1:** Xin chào! Tôi tên Linh.
- *No-memory:* Xin chào Linh! Rất vui được gặp bạn. Bạn có điều gì muốn chia sẻ hoặc hỏi không?
- *With-memory:* Xin chào Linh! Rất vui được gặp bạn. Bạn cần giúp gì hôm nay?

**Turn 2:** Tôi đang học lập trình Python.
- *No-memory:* Thật tuyệt vời! Python là một ngôn ngữ lập trình rất mạnh mẽ và dễ học. Bạn đang tìm hiểu về khía cạnh nào của Python? Có cần giúp đỡ về cú pháp, thư viện hay dự án cụ thể nào không?
- *With-memory:* Thật tuyệt vời! Python là một ngôn ngữ lập trình rất linh hoạt và dễ học. Bạn đang tìm hiểu về phần nào của Python?

**Turn 3:** Bạn có thể giải thích list comprehension không?
- *No-memory:* Tất nhiên! List comprehension là một cách ngắn gọn và hiệu quả để tạo ra danh sách (list) trong Python. Nó cho phép bạn tạo ra một danh sách mới bằng cách áp dụng một biểu thức cho từng phần tử trong ...
- *With-memory:* List comprehension trong Python là một cách ngắn gọn và hiệu quả để tạo ra danh sách mới từ một iterable (như danh sách, tuple, hoặc chuỗi). Cú pháp cơ bản của list comprehension là:

```python
new_li...

**Turn 4:** Cảm ơn! Tiếp tục nào.
- *No-memory:* Không có gì! Bạn cần giúp gì tiếp theo?
- *With-memory:* Bạn muốn tìm hiểu thêm về điều gì trong Python? Hoặc có câu hỏi nào khác không?

**Turn 5:** Tôi muốn học về decorators.
- *No-memory:* Decorators trong Python là một công cụ mạnh mẽ cho phép bạn mở rộng hoặc thay đổi hành vi của các hàm hoặc phương thức mà không cần thay đổi mã nguồn của chúng. Decorators thường được sử dụng để thêm ...
- *With-memory:* Decorators trong Python là một cách để thay đổi hoặc mở rộng hành vi của một hàm hoặc phương thức mà không cần thay đổi mã nguồn của nó. Decorators thường được sử dụng để thêm tính năng như logging, k...

**Turn 6:** Bạn nhớ tên tôi không?
- *No-memory:* Xin lỗi, tôi không thể nhớ tên của bạn vì tôi không có khả năng lưu trữ thông tin cá nhân. Nhưng tôi rất vui được giúp đỡ bạn với bất kỳ câu hỏi nào!
- *With-memory:* Có, tên bạn là Linh.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 2: Allergy conflict update (sữa bò → đậu nành)
**Category:** conflict_update  
**Expected keyword:** `đậu nành`  

**Turn 1:** Tôi dị ứng sữa bò.
- *No-memory:* Nếu bạn dị ứng với sữa bò, bạn nên tránh tất cả các sản phẩm từ sữa bò, bao gồm sữa, phô mai, bơ và các sản phẩm chế biến từ sữa khác. Bạn cũng nên đọc kỹ nhãn mác thực phẩm để tránh các thành phần có...
- *With-memory:* Tôi đã lưu thông tin bạn dị ứng với sữa bò. Nếu có thêm dị ứng nào khác, hãy cho tôi biết nhé!

**Turn 2:** Hmm, tôi nhớ nhầm. À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò.
- *No-memory:* Nếu bạn dị ứng với đậu nành, hãy cẩn thận khi tiêu thụ các sản phẩm có chứa đậu nành hoặc các thành phần liên quan. Đậu nành thường có trong nhiều loại thực phẩm như đậu phụ, nước tương, và một số loạ...
- *With-memory:* Tôi đã cập nhật thông tin của bạn. Hiện tại, bạn dị ứng với đậu nành. Nếu có thêm dị ứng nào khác, hãy cho tôi biết nhé!

**Turn 3:** Tôi dị ứng gì vậy bạn?
- *No-memory:* Để xác định bạn bị dị ứng với gì, bạn cần tham khảo ý kiến của bác sĩ hoặc chuyên gia y tế. Họ có thể thực hiện các xét nghiệm dị ứng để xác định nguyên nhân gây dị ứng cho bạn. Một số triệu chứng phổ...
- *With-memory:* Bạn dị ứng với đậu nành.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 3: Recall previous debug lesson (Docker service name)
**Category:** episodic_recall  
**Expected keyword:** `service|dịch vụ`  

**Turn 1:** Tôi vừa fix lỗi Docker: dùng service name thay vì localhost. Xong rồi!
- *No-memory:* Tuyệt vời! Việc sử dụng service name thay vì localhost trong Docker là một cách tiếp cận đúng đắn, đặc biệt khi bạn làm việc với nhiều container. Điều này giúp các container có thể giao tiếp với nhau ...
- *With-memory:* Tuyệt vời! Rất mừng khi bạn đã fix được lỗi Docker. Bạn có cần hỗ trợ gì thêm không?

**Turn 2:** Tốt. Cho tôi hỏi về Python threading.
- *No-memory:* Chắc chắn rồi! Python threading là một thư viện cho phép bạn thực hiện đa luồng (multithreading) trong ứng dụng Python của mình. Điều này có nghĩa là bạn có thể chạy nhiều luồng (threads) cùng một lúc...
- *With-memory:* Python threading cho phép bạn chạy nhiều luồng (threads) cùng một lúc, giúp tối ưu hóa hiệu suất cho các tác vụ I/O-bound. Thư viện `threading` trong Python cung cấp các công cụ để tạo và quản lý luồn...

**Turn 3:** Cảm ơn. Còn lỗi kết nối Docker thì sao?
- *No-memory:* Lỗi kết nối Docker có thể xuất phát từ nhiều nguyên nhân khác nhau. Dưới đây là một số nguyên nhân phổ biến và cách khắc phục:

1. **Docker Daemon không chạy**: Kiểm tra xem Docker Daemon có đang chạy...
- *With-memory:* Lỗi kết nối Docker thường xảy ra khi container không thể giao tiếp với nhau hoặc với máy chủ. Dưới đây là một số nguyên nhân và cách khắc phục:

1. **Sử dụng service name**: Như bạn đã biết, hãy sử dụ...

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 4: Semantic retrieval — FAQ on Docker debug
**Category:** semantic_retrieval  
**Expected keyword:** `service name`  

**Turn 1:** Làm sao debug lỗi kết nối giữa các container Docker?
- *No-memory:* Để debug lỗi kết nối giữa các container Docker, bạn có thể thực hiện các bước sau:

1. **Kiểm tra trạng thái của các container**:
   Sử dụng lệnh `docker ps` để xem danh sách các container đang chạy. ...
- *With-memory:* Để debug lỗi kết nối giữa các container Docker, bạn có thể thực hiện các bước sau:

1. **Kiểm tra Network**: Đảm bảo rằng các container đang chạy trên cùng một network. Bạn có thể sử dụng lệnh `docker...

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 5: Context window management — trim older turns
**Category:** trim_budget  
**Expected keyword:** `an`  

**Turn 1:** Turn 1: Tôi tên An, làm kỹ sư phần mềm.
- *No-memory:* Chào An! Rất vui được gặp bạn. Bạn đang làm việc trong lĩnh vực nào của kỹ sư phần mềm?
- *With-memory:* Tôi đã ghi nhớ thông tin mới của bạn. Bạn tên An và làm kỹ sư phần mềm.

**Turn 2:** Turn 2: Tôi thích Python và machine learning.
- *No-memory:* Rất tuyệt! Python là một ngôn ngữ lập trình rất phổ biến trong lĩnh vực machine learning. Bạn đã bắt đầu học về machine learning chưa? Nếu có, bạn đang tìm hiểu về những chủ đề nào?
- *With-memory:* Tôi đã ghi nhớ rằng bạn thích Python và machine learning.

**Turn 3:** Turn 3: Bạn có thể giới thiệu về LangChain không?
- *No-memory:* LangChain là một framework được thiết kế để xây dựng các ứng dụng sử dụng mô hình ngôn ngữ (language models) một cách dễ dàng và hiệu quả. Nó cung cấp các công cụ và thành phần để tích hợp các mô hình...
- *With-memory:* LangChain là một framework giúp xây dựng ứng dụng sử dụng mô hình ngôn ngữ (language model) một cách dễ dàng và hiệu quả. Nó cung cấp các công cụ để tích hợp mô hình ngôn ngữ với các nguồn dữ liệu khá...

**Turn 4:** Turn 4: Tôi muốn biết thêm về vector database.
- *No-memory:* Vector database (cơ sở dữ liệu vector) là một loại cơ sở dữ liệu được thiết kế để lưu trữ và truy vấn các vector (đặc trưng) trong không gian nhiều chiều. Các vector này thường được sử dụng trong các ...
- *With-memory:* Vector database là một loại cơ sở dữ liệu được thiết kế để lưu trữ và truy vấn các vector, thường được sử dụng trong các ứng dụng học máy và tìm kiếm ngữ nghĩa. Chúng cho phép bạn lưu trữ các vector đ...

**Turn 5:** Turn 5: Chromadb có ưu điểm gì?
- *No-memory:* Chromadb là một cơ sở dữ liệu chuyên dụng cho việc lưu trữ và truy vấn dữ liệu nhúng (embedding), thường được sử dụng trong các ứng dụng học máy và trí tuệ nhân tạo. Dưới đây là một số ưu điểm của Chr...
- *With-memory:* ChromaDB có một số ưu điểm như sau:

1. **In-process**: Chạy trong cùng một tiến trình, giúp giảm độ trễ và tăng hiệu suất.
2. **Dễ sử dụng**: Cung cấp API đơn giản, dễ dàng tích hợp vào các ứng dụng ...

**Turn 6:** Turn 6: So sánh Chroma và FAISS đi.
- *No-memory:* Chroma và FAISS là hai công cụ phổ biến được sử dụng trong lĩnh vực tìm kiếm và quản lý dữ liệu, đặc biệt là trong các ứng dụng liên quan đến học máy và trí tuệ nhân tạo. Dưới đây là một số điểm so sá...
- *With-memory:* ChromaDB và FAISS đều là các giải pháp cho tìm kiếm ngữ nghĩa, nhưng có một số điểm khác biệt:

1. **Kiến trúc**:
   - **ChromaDB**: Là một vector database in-process, dễ tích hợp vào ứng dụng nhỏ và ...

**Turn 7:** Turn 7: Tôi đang xây agent hỏi đáp.
- *No-memory:* Rất tuyệt! Bạn đang xây dựng một agent hỏi đáp. Bạn cần hỗ trợ gì trong quá trình phát triển? Có phải bạn cần ý tưởng về cách thiết kế, công nghệ sử dụng hay cách xử lý dữ liệu không?
- *With-memory:* Tuyệt vời! Bạn có cần hỗ trợ gì về việc xây dựng agent hỏi đáp không? Ví dụ như lựa chọn công nghệ, thiết kế kiến trúc hay cách tích hợp với vector database?

**Turn 8:** Turn 8: Tôi muốn thêm bộ nhớ dài hạn.
- *No-memory:* Xin lỗi, nhưng tôi không thể thêm bộ nhớ dài hạn. Tuy nhiên, tôi có thể giúp bạn với thông tin và câu hỏi ngay trong phiên trò chuyện này. Bạn cần hỗ trợ gì?
- *With-memory:* Bạn muốn thêm thông tin gì vào bộ nhớ dài hạn? Hãy cho tôi biết để tôi có thể cập nhật nhé!

**Turn 9:** Turn 9: Còn bộ nhớ ngắn hạn thì sao?
- *No-memory:* Bộ nhớ ngắn hạn, hay còn gọi là bộ nhớ làm việc, là khả năng lưu trữ và xử lý thông tin trong một khoảng thời gian ngắn. Nó cho phép chúng ta giữ lại thông tin tạm thời để thực hiện các nhiệm vụ như g...
- *With-memory:* Bộ nhớ ngắn hạn là nơi lưu trữ thông tin tạm thời trong cuộc trò chuyện hiện tại. Nó giúp tôi theo dõi các câu hỏi và câu trả lời gần đây để có thể phản hồi một cách mạch lạc và liên tục. Khi cuộc trò...

**Turn 10:** Turn 10: Bạn có biết tên và nghề nghiệp của tôi không?
- *No-memory:* Xin lỗi, nhưng tôi không biết tên và nghề nghiệp của bạn. Tôi không có thông tin cá nhân về người dùng. Nếu bạn muốn chia sẻ, tôi rất vui lòng lắng nghe!
- *With-memory:* Có, tên bạn là An và bạn là kỹ sư.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 6: Recall user age
**Category:** profile_recall  
**Expected keyword:** `25`  

**Turn 1:** Tôi 25 tuổi và đang học AI.
- *No-memory:* Thật tuyệt vời! Học về trí tuệ nhân tạo (AI) là một lĩnh vực rất thú vị và có tiềm năng lớn trong tương lai. Bạn đang học về những khía cạnh nào của AI? Machine learning, deep learning hay là ứng dụng...
- *With-memory:* Rất tốt! Học AI là một lĩnh vực thú vị và đang phát triển mạnh mẽ. Bạn có dự định gì cụ thể trong việc học AI không?

**Turn 2:** Bạn nhớ tôi bao nhiêu tuổi không?
- *No-memory:* Xin lỗi, nhưng tôi không có thông tin về tuổi của bạn. Nếu bạn muốn chia sẻ, tôi có thể giúp bạn với thông tin liên quan!
- *With-memory:* Bạn 25 tuổi.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 7: Recall learning outcome from previous session
**Category:** episodic_recall  
**Expected keyword:** `transformer`  

**Turn 1:** Tôi vừa học xong bài về transformer architecture. Thành công!
- *No-memory:* Chúc mừng bạn đã hoàn thành bài học về kiến trúc transformer! Đây là một chủ đề rất thú vị và quan trọng trong lĩnh vực học máy, đặc biệt là trong xử lý ngôn ngữ tự nhiên. Nếu bạn có bất kỳ câu hỏi nà...
- *With-memory:* Tuyệt vời! Transformer architecture là một khái niệm rất quan trọng trong học sâu và xử lý ngôn ngữ tự nhiên. Bạn có cần thảo luận thêm về nó không?

**Turn 2:** Bạn nhớ tôi học gì gần đây không?
- *No-memory:* Xin lỗi, nhưng tôi không có khả năng nhớ thông tin cá nhân hoặc theo dõi hoạt động của bạn. Tuy nhiên, tôi có thể giúp bạn với bất kỳ câu hỏi nào hoặc chủ đề nào bạn muốn thảo luận! Bạn đã học gì gần ...
- *With-memory:* Có, bạn vừa học xong bài về transformer architecture. Bạn có muốn thảo luận thêm về nó không?

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 8: Semantic retrieval — venv setup guide
**Category:** semantic_retrieval  
**Expected keyword:** `venv`  

**Turn 1:** Cách tạo môi trường ảo Python là gì?
- *No-memory:* Môi trường ảo trong Python là một cách để tạo ra một không gian riêng biệt cho các dự án Python, giúp quản lý các thư viện và phiên bản Python mà không ảnh hưởng đến hệ thống toàn cục. Dưới đây là các...
- *With-memory:* Để tạo môi trường ảo trong Python, bạn có thể sử dụng `venv`. Dưới đây là các bước cơ bản:

1. **Mở terminal** (Command Prompt hoặc Terminal).
2. **Chuyển đến thư mục dự án** của bạn.
3. **Chạy lệnh s...

**Result:** No-memory ✅ | With-memory ✅

---
### Scenario 9: Recall city and job
**Category:** profile_recall  
**Expected keyword:** `hà nội`  

**Turn 1:** Tôi sống ở Hà Nội và làm developer.
- *No-memory:* Rất vui được biết bạn! Hà Nội là một thành phố tuyệt đẹp với nhiều cơ hội phát triển trong lĩnh vực công nghệ. Bạn đang làm việc trong lĩnh vực nào của phát triển phần mềm? Frontend, backend hay full-...
- *With-memory:* Tôi đã cập nhật thông tin của bạn. Bạn sống ở Hà Nội và làm developer. Nếu có thông tin nào khác bạn muốn chia sẻ, hãy cho tôi biết nhé!

**Turn 2:** Bạn biết gì về tôi không?
- *No-memory:* Tôi không biết gì về bạn vì tôi không có khả năng truy cập thông tin cá nhân hoặc dữ liệu riêng tư. Tôi chỉ có thể cung cấp thông tin và trả lời câu hỏi dựa trên những gì bạn chia sẻ với tôi. Nếu bạn ...
- *With-memory:* Có, bạn 25 tuổi, sống ở Hà Nội và làm developer. Gần đây, bạn đã học về transformer architecture. Nếu có điều gì khác bạn muốn chia sẻ hoặc hỏi, hãy cho tôi biết!

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 10: Name conflict update (Minh → Tuấn)
**Category:** conflict_update  
**Expected keyword:** `tuấn`  

**Turn 1:** Tôi tên Minh.
- *No-memory:* Chào Minh! Rất vui được gặp bạn. Bạn cần giúp gì hôm nay?
- *With-memory:* Chào Minh! Rất vui được gặp bạn. Bạn có cần giúp gì không?

**Turn 2:** Thực ra tên tôi là Tuấn, không phải Minh.
- *No-memory:* Chào Tuấn! Rất vui được trò chuyện với bạn. Có điều gì bạn muốn chia sẻ hoặc hỏi không?
- *With-memory:* Xin lỗi về sự nhầm lẫn, Tuấn! Tôi đã cập nhật thông tin của bạn. Bạn cần giúp gì hôm nay?

**Turn 3:** Bạn nhớ tên tôi là gì?
- *No-memory:* Xin lỗi, nhưng tôi không thể nhớ thông tin cá nhân của bạn. Bạn có thể cho tôi biết tên của bạn không?
- *With-memory:* Tên bạn là Tuấn.

**Result:** No-memory ❌ | With-memory ✅


---

## Analysis

### Memory Hit Rate
- Scenarios where with-memory agent passed: **10/10**
- Scenarios where no-memory agent passed: **1/10** (expected low for context-dependent queries)

### Token / Word Budget Breakdown

| # | No-memory words | With-memory words | Delta |
|---|-----------------|-------------------|-------|
| 1 | 721 | 339 | -382 |
| 2 | 299 | 57 | -242 |
| 3 | 694 | 313 | -381 |
| 4 | 449 | 192 | -257 |
| 5 | 1595 | 692 | -903 |
| 6 | 74 | 31 | -43 |
| 7 | 107 | 48 | -59 |
| 8 | 325 | 111 | -214 |
| 9 | 99 | 65 | -34 |
| 10 | 55 | 38 | -17 |

**Average word count per scenario — No-memory:** 441.8  
**Average word count per scenario — With-memory:** 188.6  

### Context Utilization
- Short-term memory: sliding window (last 10 turns)
- Long-term profile: JSON KV store, conflict-safe (last-write-wins)
- Episodic log: JSON append log, keyword search retrieval
- Semantic store: ChromaDB / keyword fallback, top-3 chunks injected

---

## Reflection — Privacy & Limitations

### 1. Memory nào giúp agent nhất?
**Long-term profile** giúp nhất — lưu thông tin người dùng (tên, dị ứng, nghề nghiệp) và được inject vào mọi prompt, đảm bảo agent luôn biết context cơ bản.

### 2. Memory nào rủi ro nhất nếu retrieve sai?
**Episodic memory** rủi ro nhất — nếu retrieve nhầm episode (ví dụ: lẫn lộn giữa hai user), agent có thể đưa ra lời khuyên sai dựa trên bối cảnh không đúng. **Long-term profile** cũng rủi ro nếu fact bị ghi đè không đúng lúc.

### 3. PII / Privacy risks
- Profile store lưu **PII nhạy cảm**: tên, tuổi, dị ứng, thành phố. Đây là thông tin y tế có thể gây hại nếu bị lộ.
- Episodic log lưu context của từng cuộc hội thoại — tiềm ẩn rủi ro nếu nhiều user dùng chung instance.
- **Biện pháp cần thiết:**
  - TTL (time-to-live) cho từng profile key
  - Deletion API (right-to-be-forgotten — GDPR)
  - Consent flow khi lưu thông tin y tế
  - Mã hóa at-rest cho profile_store.json

### 4. Nếu user yêu cầu xóa memory, xóa ở backend nào?
1. **Long-term profile**: `LongTermProfile.delete(key)` — xóa ngay, ghi file
2. **Episodic log**: filter và rewrite `episodic_log.json` bỏ episodes của user đó
3. **Semantic store**: `collection.delete(ids=[doc_id])` trong Chroma
4. **Short-term**: `short_term.clear()` — đã in-memory, tự mất khi restart

### 5. Limitations kỹ thuật hiện tại
1. **No user isolation** — tất cả profile/episodic dùng chung một file → không dùng được multi-user.
2. **Keyword-based episodic search** — recall kém với paraphrase hoặc tiếng Việt có diacritics.
3. **Regex profile extraction** — dễ miss hoặc overextract; cần LLM-based extraction cho production.
4. **No TTL** — profile facts không tự expire, có thể stale sau nhiều tháng.
5. **Single-node Chroma** — không scale horizontally; cần managed vector DB cho production.
6. **Word-count token approximation** — không chính xác cho tokenizer (tiktoken) thật, có thể over/under-budget.
