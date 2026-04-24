# BENCHMARK — Lab #17: Multi-Memory Agent

**Mô tả:** So sánh agent có memory và không có memory trên 10 multi-turn conversations.  
**Ngày chạy:** 2026-04-24 12:46  
**Model:** gpt-4o-mini  
**Tổng số conversations:** 10  

---

## Summary Table

| # | Scenario | Category | No-memory | With-memory | Pass? |
|---|----------|----------|-----------|-------------|-------|
| 1 | Recall user name after 6 turns | profile_recall | ❌ | ✅ | ✅ |
| 2 | Allergy conflict update (sữa bò → đậu nành) | conflict_update | ❌ | ✅ | ✅ |
| 3 | Recall previous debug lesson (Docker service name) | episodic_recall | ❌ | ❌ | ❌ |
| 4 | Semantic retrieval — FAQ on Docker debug | semantic_retrieval | ❌ | ✅ | ✅ |
| 5 | Context window management — trim older turns | trim_budget | ❌ | ✅ | ✅ |
| 6 | Recall user age | profile_recall | ❌ | ✅ | ✅ |
| 7 | Recall learning outcome from previous session | episodic_recall | ❌ | ✅ | ✅ |
| 8 | Semantic retrieval — venv setup guide | semantic_retrieval | ✅ | ✅ | ✅ |
| 9 | Recall city and job | profile_recall | ❌ | ✅ | ✅ |
| 10 | Name conflict update (Minh → Tuấn) | conflict_update | ❌ | ✅ | ✅ |

**Pass rate (with-memory):** 90%  
**Pass rate (no-memory):** 10%  

---

## Detailed Results

### Scenario 1: Recall user name after 6 turns
**Category:** profile_recall  
**Expected keyword:** `linh`  

**Turn 1:** Xin chào! Tôi tên Linh.
- *No-memory:* Xin chào Linh! Rất vui được gặp bạn. Bạn có điều gì muốn chia sẻ hoặc hỏi không?
- *With-memory:* Chào Linh! Tuy nhiên, tôi đã ghi nhớ tên bạn là Tuấn. Bạn có muốn cập nhật thêm thông tin nào không?

**Turn 2:** Tôi đang học lập trình Python.
- *No-memory:* Thật tuyệt vời! Python là một ngôn ngữ lập trình rất mạnh mẽ và dễ học. Bạn đang học về chủ đề nào trong Python? Có cần giúp đỡ gì không?
- *With-memory:* Tuyệt vời! Python là một ngôn ngữ lập trình rất mạnh mẽ và dễ học. Bạn đang học về chủ đề gì trong Python?

**Turn 3:** Bạn có thể giải thích list comprehension không?
- *No-memory:* Tất nhiên! List comprehension là một cách ngắn gọn và hiệu quả để tạo ra danh sách (list) trong Python. Nó cho phép bạn tạo ra một danh sách mới bằng cách áp dụng một biểu thức cho từng phần tử trong ...
- *With-memory:* List comprehension là một cách ngắn gọn và hiệu quả để tạo ra danh sách trong Python. Nó cho phép bạn tạo danh sách mới bằng cách áp dụng một biểu thức cho từng phần tử trong một iterable (như danh sá...

**Turn 4:** Cảm ơn! Tiếp tục nào.
- *No-memory:* Không có gì! Bạn cần giúp gì tiếp theo?
- *With-memory:* Bạn muốn tìm hiểu thêm về chủ đề gì trong Python hoặc có câu hỏi nào khác không?

**Turn 5:** Tôi muốn học về decorators.
- *No-memory:* Decorators trong Python là một công cụ mạnh mẽ cho phép bạn mở rộng hoặc thay đổi hành vi của các hàm hoặc lớp mà không cần phải thay đổi mã nguồn của chúng. Decorators thường được sử dụng để thêm các...
- *With-memory:* Decorators trong Python là một cách để thay đổi hoặc mở rộng hành vi của các hàm hoặc phương thức mà không cần thay đổi mã nguồn của chúng. Decorators thường được sử dụng để thêm chức năng như logging...

**Turn 6:** Bạn nhớ tên tôi không?
- *No-memory:* Xin lỗi, nhưng tôi không thể nhớ thông tin cá nhân của bạn. Tôi không lưu trữ dữ liệu từ các cuộc trò chuyện trước. Bạn có thể cho tôi biết tên của bạn không?
- *With-memory:* Tôi đã ghi nhớ tên bạn là Linh. Bạn có muốn cập nhật thêm thông tin gì không?

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 2: Allergy conflict update (sữa bò → đậu nành)
**Category:** conflict_update  
**Expected keyword:** `đậu nành`  

**Turn 1:** Tôi dị ứng sữa bò.
- *No-memory:* Nếu bạn dị ứng với sữa bò, bạn nên tránh hoàn toàn các sản phẩm từ sữa bò như sữa, phô mai, bơ và các sản phẩm chế biến từ sữa. Bạn cũng nên đọc kỹ nhãn mác thực phẩm để đảm bảo không có thành phần nà...
- *With-memory:* Bạn đã thông báo rằng bạn dị ứng đậu nành, vì vậy thông tin này đã được cập nhật. Bạn có muốn thay đổi lại thông tin dị ứng không?

**Turn 2:** Hmm, tôi nhớ nhầm. À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò.
- *No-memory:* Không sao đâu! Nếu bạn dị ứng đậu nành, hãy cẩn thận khi chọn thực phẩm, vì đậu nành thường có mặt trong nhiều sản phẩm chế biến sẵn. Nếu bạn cần tìm các lựa chọn thay thế hoặc thông tin về thực phẩm ...
- *With-memory:* Cảm ơn bạn đã thông báo! Tôi đã cập nhật thông tin dị ứng của bạn thành dị ứng đậu nành.

**Turn 3:** Tôi dị ứng gì vậy bạn?
- *No-memory:* Để xác định bạn có thể bị dị ứng với gì, cần có thêm thông tin về triệu chứng bạn gặp phải, thời gian xuất hiện triệu chứng, và các yếu tố môi trường hoặc thực phẩm bạn tiếp xúc. Một số dị ứng phổ biế...
- *With-memory:* Bạn dị ứng đậu nành.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 3: Recall previous debug lesson (Docker service name)
**Category:** episodic_recall  
**Expected keyword:** `service`  

**Turn 1:** Tôi vừa fix lỗi Docker: dùng service name thay vì localhost. Xong rồi!
- *No-memory:* Tuyệt vời! Việc sử dụng tên dịch vụ thay vì `localhost` trong Docker là một cách tiếp cận đúng đắn, đặc biệt khi bạn làm việc với các container khác nhau trong một mạng Docker. Điều này giúp các conta...
- *With-memory:* Tuyệt vời! Rất vui khi bạn đã khắc phục được lỗi Docker. Bạn có cần hỗ trợ gì thêm không?

**Turn 2:** Tốt. Cho tôi hỏi về Python threading.
- *No-memory:* Chắc chắn rồi! Python threading là một thư viện trong Python cho phép bạn thực hiện đa luồng (multithreading), giúp chạy nhiều luồng (thread) song song trong cùng một chương trình. Điều này rất hữu íc...
- *With-memory:* Python threading cho phép bạn thực hiện nhiều luồng (threads) trong cùng một chương trình, giúp tối ưu hóa việc sử dụng tài nguyên và cải thiện hiệu suất, đặc biệt trong các tác vụ I/O chậm. Bạn có mu...

**Turn 3:** Cảm ơn. Còn lỗi kết nối Docker thì sao?
- *No-memory:* Lỗi kết nối Docker có thể xuất phát từ nhiều nguyên nhân khác nhau. Dưới đây là một số nguyên nhân phổ biến và cách khắc phục:

1. **Docker Daemon không chạy**: Đảm bảo rằng Docker Daemon đang chạy. B...
- *With-memory:* Lỗi kết nối Docker thường xảy ra khi container không thể giao tiếp với nhau hoặc với máy chủ. Một số nguyên nhân phổ biến có thể bao gồm cấu hình mạng sai, firewall chặn kết nối, hoặc sử dụng `localho...

**Result:** No-memory ❌ | With-memory ❌

---
### Scenario 4: Semantic retrieval — FAQ on Docker debug
**Category:** semantic_retrieval  
**Expected keyword:** `service name`  

**Turn 1:** Làm sao debug lỗi kết nối giữa các container Docker?
- *No-memory:* Để debug lỗi kết nối giữa các container Docker, bạn có thể thực hiện các bước sau:

1. **Kiểm tra trạng thái container**: Sử dụng lệnh `docker ps` để kiểm tra xem các container của bạn có đang chạy ha...
- *With-memory:* Để debug lỗi kết nối giữa các container Docker, bạn có thể thực hiện các bước sau:

1. **Sử dụng Service Name**: Khi giao tiếp giữa các container, hãy sử dụng tên service thay vì `localhost`. Docker t...

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 5: Context window management — trim older turns
**Category:** trim_budget  
**Expected keyword:** `an`  

**Turn 1:** Turn 1: Tôi tên An, làm kỹ sư phần mềm.
- *No-memory:* Chào An! Rất vui được gặp bạn. Bạn làm kỹ sư phần mềm ở lĩnh vực nào?
- *With-memory:* Cảm ơn bạn đã chia sẻ! Tuy nhiên, tôi đã ghi nhớ tên bạn là "tôi không" và bạn là developer. Bạn có muốn cập nhật thông tin gì khác không?

**Turn 2:** Turn 2: Tôi thích Python và machine learning.
- *No-memory:* Thật tuyệt! Python là một ngôn ngữ lập trình rất phổ biến trong lĩnh vực machine learning nhờ vào cú pháp dễ đọc và nhiều thư viện mạnh mẽ như TensorFlow, Keras, và scikit-learn. Bạn đã bắt đầu học về...
- *With-memory:* Cảm ơn bạn đã chia sẻ! Tôi đã ghi nhớ rằng bạn thích Python và machine learning. Bạn có muốn nói thêm về sở thích này không?

**Turn 3:** Turn 3: Bạn có thể giới thiệu về LangChain không?
- *No-memory:* LangChain là một framework được thiết kế để phát triển các ứng dụng sử dụng mô hình ngôn ngữ (language models) một cách hiệu quả. Nó cung cấp các công cụ và thư viện giúp các nhà phát triển dễ dàng tí...
- *With-memory:* LangChain là một framework giúp xây dựng các ứng dụng AI bằng cách kết hợp các mô hình ngôn ngữ với các nguồn dữ liệu khác nhau. Nó cho phép bạn tạo ra các agent, chatbot, và nhiều ứng dụng khác bằng ...

**Turn 4:** Turn 4: Tôi muốn biết thêm về vector database.
- *No-memory:* Vector database (cơ sở dữ liệu vector) là một loại cơ sở dữ liệu được thiết kế để lưu trữ và truy vấn các vector, thường là các vector đặc trưng cho dữ liệu phi cấu trúc như hình ảnh, văn bản, âm than...
- *With-memory:* Vector database là loại cơ sở dữ liệu được thiết kế để lưu trữ và truy vấn dữ liệu dưới dạng vector, thường được sử dụng trong các ứng dụng machine learning và tìm kiếm ngữ nghĩa. ChromaDB là một ví d...

**Turn 5:** Turn 5: Chromadb có ưu điểm gì?
- *No-memory:* Chromadb là một cơ sở dữ liệu chuyên dụng cho việc lưu trữ và truy vấn dữ liệu vector, thường được sử dụng trong các ứng dụng trí tuệ nhân tạo và học máy. Dưới đây là một số ưu điểm của Chromadb:

1. ...
- *With-memory:* ChromaDB có một số ưu điểm như sau:

1. **Tìm kiếm ngữ nghĩa**: Hỗ trợ tìm kiếm dựa trên ngữ nghĩa, giúp cải thiện độ chính xác trong việc tìm kiếm thông tin.
2. **Hiệu suất cao**: Tối ưu hóa cho việc...

**Turn 6:** Turn 6: So sánh Chroma và FAISS đi.
- *No-memory:* Chroma và FAISS là hai công cụ phổ biến trong lĩnh vực tìm kiếm và truy xuất thông tin, đặc biệt là trong các ứng dụng liên quan đến học máy và trí tuệ nhân tạo. Dưới đây là một số điểm so sánh giữa c...
- *With-memory:* ChromaDB và FAISS đều là các công cụ hỗ trợ tìm kiếm vector, nhưng chúng có những điểm khác biệt:

1. **Mục đích sử dụng**:
   - **ChromaDB**: Tập trung vào việc lưu trữ và quản lý vector, đồng thời h...

**Turn 7:** Turn 7: Tôi đang xây agent hỏi đáp.
- *No-memory:* Chào bạn! Bạn đang xây dựng một agent hỏi đáp, thật thú vị! Bạn cần hỗ trợ gì trong quá trình phát triển? Có thể là về công nghệ, ngôn ngữ lập trình, hoặc cách thiết kế câu hỏi và câu trả lời? Hãy cho...
- *With-memory:* Cảm ơn bạn đã chia sẻ! Xây dựng một agent hỏi đáp là một dự án thú vị. Bạn đã có kế hoạch cụ thể nào cho dự án này chưa?

**Turn 8:** Turn 8: Tôi muốn thêm bộ nhớ dài hạn.
- *No-memory:* Hiện tại, tôi không có khả năng lưu trữ thông tin dài hạn. Mỗi phiên trò chuyện đều độc lập và không lưu lại dữ liệu từ các cuộc trò chuyện trước. Tuy nhiên, tôi có thể giúp bạn với bất kỳ câu hỏi hoặ...
- *With-memory:* Bạn muốn thêm thông tin gì vào bộ nhớ dài hạn? Hãy cho tôi biết để tôi có thể cập nhật!

**Turn 9:** Turn 9: Còn bộ nhớ ngắn hạn thì sao?
- *No-memory:* Bộ nhớ ngắn hạn, hay còn gọi là bộ nhớ làm việc, là khả năng lưu trữ và xử lý thông tin trong một khoảng thời gian ngắn, thường chỉ từ vài giây đến vài phút. Nó cho phép chúng ta giữ lại thông tin tạm...
- *With-memory:* Bộ nhớ ngắn hạn là nơi lưu trữ thông tin tạm thời trong cuộc trò chuyện hiện tại. Nó giúp tôi theo dõi các câu hỏi và câu trả lời gần đây để có thể phản hồi một cách mạch lạc và liên tục. Khi cuộc trò...

**Turn 10:** Turn 10: Bạn có biết tên và nghề nghiệp của tôi không?
- *No-memory:* Xin lỗi, nhưng tôi không biết tên và nghề nghiệp của bạn. Tôi không có thông tin cá nhân về người dùng. Nếu bạn muốn, bạn có thể chia sẻ với tôi!
- *With-memory:* Có, bạn tên là An và bạn là một kỹ sư.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 6: Recall user age
**Category:** profile_recall  
**Expected keyword:** `25`  

**Turn 1:** Tôi 25 tuổi và đang học AI.
- *No-memory:* Thật tuyệt vời! Học về trí tuệ nhân tạo (AI) là một lĩnh vực rất thú vị và có tiềm năng lớn trong tương lai. Bạn đang học ở đâu và bạn đang tìm hiểu về khía cạnh nào của AI?
- *With-memory:* Bạn 25 tuổi và đang học AI. Thật tuyệt! Bạn đang học về lĩnh vực nào trong AI?

**Turn 2:** Bạn nhớ tôi bao nhiêu tuổi không?
- *No-memory:* Xin lỗi, nhưng tôi không có thông tin về tuổi của bạn. Nếu bạn muốn, bạn có thể cho tôi biết tuổi của bạn!
- *With-memory:* Bạn 25 tuổi.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 7: Recall learning outcome from previous session
**Category:** episodic_recall  
**Expected keyword:** `transformer`  

**Turn 1:** Tôi vừa học xong bài về transformer architecture. Thành công!
- *No-memory:* Chúc mừng bạn đã hoàn thành bài học về kiến trúc transformer! Đây là một chủ đề rất thú vị và quan trọng trong lĩnh vực học máy, đặc biệt là trong xử lý ngôn ngữ tự nhiên. Nếu bạn có bất kỳ câu hỏi nà...
- *With-memory:* Tuyệt vời! Bạn đã học xong bài về transformer architecture. Đây là một chủ đề rất thú vị và quan trọng trong học máy. Bạn có cần thêm thông tin gì không?

**Turn 2:** Bạn nhớ tôi học gì gần đây không?
- *No-memory:* Xin lỗi, nhưng tôi không có khả năng nhớ thông tin cá nhân hoặc lịch sử học tập của bạn. Tuy nhiên, tôi có thể giúp bạn với bất kỳ câu hỏi nào hoặc chủ đề nào bạn đang quan tâm. Bạn đã học gì gần đây?
- *With-memory:* Bạn vừa học xong bài về transformer architecture.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 8: Semantic retrieval — venv setup guide
**Category:** semantic_retrieval  
**Expected keyword:** `venv`  

**Turn 1:** Cách tạo môi trường ảo Python là gì?
- *No-memory:* Để tạo môi trường ảo trong Python, bạn có thể sử dụng công cụ `venv`, đây là một công cụ tích hợp sẵn trong Python từ phiên bản 3.3 trở đi. Dưới đây là các bước để tạo và sử dụng môi trường ảo:

### B...
- *With-memory:* Để tạo môi trường ảo trong Python, bạn có thể sử dụng `venv`. Dưới đây là các bước cơ bản:

1. **Mở terminal** (Command Prompt hoặc PowerShell trên Windows, Terminal trên macOS/Linux).
2. **Chuyển đến...

**Result:** No-memory ✅ | With-memory ✅

---
### Scenario 9: Recall city and job
**Category:** profile_recall  
**Expected keyword:** `hà nội`  

**Turn 1:** Tôi sống ở Hà Nội và làm developer.
- *No-memory:* Rất vui được biết bạn sống ở Hà Nội và làm developer! Bạn đang làm việc với công nghệ nào? Có điều gì bạn muốn chia sẻ hoặc hỏi về lĩnh vực phát triển phần mềm không?
- *With-memory:* Cảm ơn bạn đã xác nhận! Tôi đã ghi nhớ rằng bạn sống ở Hà Nội và làm developer.

**Turn 2:** Bạn biết gì về tôi không?
- *No-memory:* Tôi không biết gì về bạn vì tôi không có khả năng truy cập thông tin cá nhân hoặc dữ liệu của người dùng. Tôi chỉ có thể trả lời dựa trên những gì bạn chia sẻ trong cuộc trò chuyện này. Nếu bạn có câu...
- *With-memory:* Bạn 25 tuổi, sống ở Hà Nội và làm developer. Gần đây, bạn đã học xong bài về transformer architecture.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 10: Name conflict update (Minh → Tuấn)
**Category:** conflict_update  
**Expected keyword:** `tuấn`  

**Turn 1:** Tôi tên Minh.
- *No-memory:* Chào Minh! Bạn có cần giúp đỡ gì không?
- *With-memory:* Cảm ơn bạn đã thông báo! Tuy nhiên, tôi đã ghi nhớ tên bạn là Tuấn. Bạn có muốn cập nhật thêm thông tin gì không?

**Turn 2:** Thực ra tên tôi là Tuấn, không phải Minh.
- *No-memory:* Chào Tuấn! Rất vui được trò chuyện với bạn. Có điều gì bạn muốn chia sẻ hoặc hỏi không?
- *With-memory:* Cảm ơn bạn đã thông báo! Tôi đã cập nhật lại tên của bạn thành Tuấn. Bạn có muốn chia sẻ thêm thông tin gì không?

**Turn 3:** Bạn nhớ tên tôi là gì?
- *No-memory:* Xin lỗi, nhưng tôi không có khả năng nhớ thông tin cá nhân của bạn. Bạn có thể cho tôi biết tên của bạn không?
- *With-memory:* Tên bạn là Tuấn.

**Result:** No-memory ❌ | With-memory ✅


---

## Analysis

### Memory Hit Rate
- Scenarios where with-memory agent passed: **9/10**
- Scenarios where no-memory agent passed: **1/10** (expected low for context-dependent queries)

### Token / Word Budget Breakdown

| # | No-memory words | With-memory words | Delta |
|---|-----------------|-------------------|-------|
| 1 | 702 | 472 | -230 |
| 2 | 250 | 56 | -194 |
| 3 | 675 | 133 | -542 |
| 4 | 356 | 190 | -166 |
| 5 | 1717 | 760 | -957 |
| 6 | 65 | 21 | -44 |
| 7 | 109 | 40 | -69 |
| 8 | 337 | 129 | -208 |
| 9 | 94 | 39 | -55 |
| 10 | 53 | 56 | +3 |

**Average word count per scenario — No-memory:** 435.8  
**Average word count per scenario — With-memory:** 189.6  

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
