# BENCHMARK — Lab #17: Multi-Memory Agent

**Mô tả:** So sánh agent có memory và không có memory trên 10 multi-turn conversations.  
**Ngày chạy:** 2026-04-24 12:22  
**Model:** gpt-4o-mini  
**Tổng số conversations:** 10  

---

## Summary Table

| # | Scenario | Category | No-memory | With-memory | Pass? |
|---|----------|----------|-----------|-------------|-------|
| 1 | Recall user name after 6 turns | profile_recall | ❌ | ✅ | ✅ |
| 2 | Allergy conflict update (sữa bò → đậu nành) | conflict_update | ❌ | ✅ | ✅ |
| 3 | Recall previous debug lesson (Docker service name) | episodic_recall | ✅ | ✅ | ✅ |
| 4 | Semantic retrieval — FAQ on Docker debug | semantic_retrieval | ❌ | ✅ | ✅ |
| 5 | Context window management — trim older turns | trim_budget | ❌ | ✅ | ✅ |
| 6 | Recall user age | profile_recall | ❌ | ✅ | ✅ |
| 7 | Recall learning outcome from previous session | episodic_recall | ❌ | ✅ | ✅ |
| 8 | Semantic retrieval — venv setup guide | semantic_retrieval | ✅ | ✅ | ✅ |
| 9 | Recall city and job | profile_recall | ❌ | ✅ | ✅ |
| 10 | Name conflict update (Minh → Tuấn) | conflict_update | ❌ | ✅ | ✅ |

**Pass rate (with-memory):** 100%  
**Pass rate (no-memory):** 20%  

---

## Detailed Results

### Scenario 1: Recall user name after 6 turns
**Category:** profile_recall  
**Expected keyword:** `linh`  

**Turn 1:** Xin chào! Tôi tên Linh.
- *No-memory:* Xin chào Linh! Rất vui được gặp bạn. Bạn có điều gì muốn chia sẻ hoặc hỏi không?
- *With-memory:* Xin chào Linh! Rất vui được gặp bạn. Bạn cần giúp gì hôm nay?

**Turn 2:** Tôi đang học lập trình Python.
- *No-memory:* Thật tuyệt vời! Python là một ngôn ngữ lập trình rất mạnh mẽ và dễ học. Bạn đang tìm hiểu về chủ đề nào trong Python? Có cần giúp đỡ về một vấn đề cụ thể nào không?
- *With-memory:* Thật tuyệt vời! Python là một ngôn ngữ lập trình rất mạnh mẽ và dễ học. Bạn đang học về chủ đề nào trong Python?

**Turn 3:** Bạn có thể giải thích list comprehension không?
- *No-memory:* List comprehension là một cú pháp trong Python cho phép bạn tạo ra danh sách mới một cách ngắn gọn và dễ đọc từ một iterable (như danh sách, tuple, hoặc chuỗi) bằng cách sử dụng một biểu thức và một h...
- *With-memory:* List comprehension là một cách ngắn gọn và hiệu quả để tạo ra danh sách trong Python. Nó cho phép bạn tạo danh sách mới bằng cách áp dụng một biểu thức cho từng phần tử trong một iterable (như danh sá...

**Turn 4:** Cảm ơn! Tiếp tục nào.
- *No-memory:* Không có gì! Bạn cần giúp gì tiếp theo?
- *With-memory:* Bạn muốn tìm hiểu thêm về chủ đề gì trong Python hoặc có câu hỏi nào khác không?

**Turn 5:** Tôi muốn học về decorators.
- *No-memory:* Decorators trong Python là một tính năng mạnh mẽ cho phép bạn mở rộng hoặc thay đổi hành vi của các hàm hoặc phương thức mà không cần thay đổi mã nguồn của chúng. Decorators thường được sử dụng để thê...
- *With-memory:* Decorators trong Python là một cách để thay đổi hoặc mở rộng hành vi của một hàm hoặc phương thức mà không cần thay đổi mã nguồn của nó. Decorators thường được sử dụng để thêm các tính năng như ghi lo...

**Turn 6:** Bạn nhớ tên tôi không?
- *No-memory:* Xin lỗi, nhưng tôi không thể nhớ tên của bạn hoặc bất kỳ thông tin cá nhân nào. Mỗi lần trò chuyện với tôi đều là một lần mới. Bạn có muốn chia sẻ tên của mình không?
- *With-memory:* Có, tên bạn là Linh.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 2: Allergy conflict update (sữa bò → đậu nành)
**Category:** conflict_update  
**Expected keyword:** `đậu nành`  

**Turn 1:** Tôi dị ứng sữa bò.
- *No-memory:* Nếu bạn bị dị ứng sữa bò, bạn nên tránh hoàn toàn các sản phẩm từ sữa bò, bao gồm sữa, phô mai, bơ và các sản phẩm chế biến từ sữa khác. Bạn cũng nên đọc kỹ nhãn sản phẩm để đảm bảo không có thành phầ...
- *With-memory:* Tôi đã lưu thông tin bạn dị ứng sữa bò. Nếu có thêm dị ứng nào khác, hãy cho tôi biết nhé!

**Turn 2:** Hmm, tôi nhớ nhầm. À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò.
- *No-memory:* Không sao đâu! Nếu bạn dị ứng với đậu nành, hãy chắc chắn kiểm tra kỹ thành phần của các sản phẩm thực phẩm trước khi tiêu thụ. Nếu cần, tôi có thể giúp bạn tìm hiểu thêm về các loại thực phẩm thay th...
- *With-memory:* Tôi đã cập nhật thông tin của bạn. Hiện tại, bạn dị ứng đậu nành. Nếu có thêm dị ứng nào khác, hãy cho tôi biết nhé!

**Turn 3:** Tôi dị ứng gì vậy bạn?
- *No-memory:* Tôi không thể chẩn đoán tình trạng sức khỏe của bạn. Tuy nhiên, nếu bạn có triệu chứng như ngứa, phát ban, sưng tấy, hoặc khó thở sau khi tiếp xúc với một số thực phẩm, phấn hoa, bụi bẩn, hoặc vật nuô...
- *With-memory:* Bạn dị ứng đậu nành.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 3: Recall previous debug lesson (Docker service name)
**Category:** episodic_recall  
**Expected keyword:** `service`  

**Turn 1:** Tôi vừa fix lỗi Docker: dùng service name thay vì localhost. Xong rồi!
- *No-memory:* Tuyệt vời! Việc sử dụng service name thay vì localhost trong Docker là một bước quan trọng để đảm bảo các container có thể giao tiếp với nhau một cách chính xác. Khi bạn sử dụng service name, Docker s...
- *With-memory:* Tuyệt vời! Rất vui khi bạn đã khắc phục được lỗi Docker. Bạn có cần hỗ trợ gì thêm không?

**Turn 2:** Tốt. Cho tôi hỏi về Python threading.
- *No-memory:* Chắc chắn rồi! Python threading là một thư viện trong Python cho phép bạn thực hiện đa luồng (multithreading), tức là chạy nhiều luồng (thread) song song trong một chương trình. Điều này có thể giúp c...
- *With-memory:* Python threading cho phép bạn thực hiện nhiều luồng (threads) trong cùng một chương trình, giúp tối ưu hóa hiệu suất khi xử lý các tác vụ I/O hoặc khi cần thực hiện nhiều công việc đồng thời. Dưới đây...

**Turn 3:** Cảm ơn. Còn lỗi kết nối Docker thì sao?
- *No-memory:* Nếu bạn gặp lỗi kết nối với Docker, có một số bước bạn có thể thực hiện để khắc phục:

1. **Kiểm tra trạng thái Docker**: Đảm bảo rằng Docker daemon đang chạy. Bạn có thể kiểm tra bằng lệnh:
   ```bas...
- *With-memory:* Lỗi kết nối Docker thường xảy ra khi container không thể giao tiếp với nhau hoặc với máy chủ. Dưới đây là một số nguyên nhân phổ biến và cách khắc phục:

1. **Sử dụng service name**: Như bạn đã làm, h...

**Result:** No-memory ✅ | With-memory ✅

---
### Scenario 4: Semantic retrieval — FAQ on Docker debug
**Category:** semantic_retrieval  
**Expected keyword:** `service name`  

**Turn 1:** Làm sao debug lỗi kết nối giữa các container Docker?
- *No-memory:* Để debug lỗi kết nối giữa các container Docker, bạn có thể thực hiện theo các bước sau:

1. **Kiểm tra trạng thái của container**:
   - Sử dụng lệnh `docker ps` để xem danh sách các container đang chạ...
- *With-memory:* Để debug lỗi kết nối giữa các container Docker, bạn có thể thực hiện các bước sau:

1. **Kiểm tra Network**: Đảm bảo rằng các container đang chạy trên cùng một mạng Docker. Sử dụng lệnh `docker networ...

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 5: Context window management — trim older turns
**Category:** trim_budget  
**Expected keyword:** `an`  

**Turn 1:** Turn 1: Tôi tên An, làm kỹ sư phần mềm.
- *No-memory:* Chào An! Rất vui được gặp bạn. Bạn làm kỹ sư phần mềm ở lĩnh vực nào?
- *With-memory:* Chào An! Rất vui được biết bạn. Bạn có dị ứng thực phẩm nào không?

**Turn 2:** Turn 2: Tôi thích Python và machine learning.
- *No-memory:* Thật tuyệt! Python là một ngôn ngữ lập trình rất phổ biến trong lĩnh vực machine learning nhờ vào cú pháp dễ hiểu và nhiều thư viện mạnh mẽ như TensorFlow, Keras, và scikit-learn. Bạn đang học về mach...
- *With-memory:* Thật tuyệt! Python là ngôn ngữ rất phổ biến trong lĩnh vực machine learning. Bạn đã làm việc với thư viện nào trong Python chưa?

**Turn 3:** Turn 3: Bạn có thể giới thiệu về LangChain không?
- *No-memory:* LangChain là một framework mạnh mẽ được thiết kế để phát triển các ứng dụng sử dụng mô hình ngôn ngữ (language models) một cách dễ dàng và hiệu quả. Nó cung cấp các công cụ và thành phần để xây dựng c...
- *With-memory:* LangChain là một framework giúp xây dựng ứng dụng AI bằng cách kết hợp các mô hình ngôn ngữ với các nguồn dữ liệu bên ngoài. Nó cho phép bạn dễ dàng tích hợp các API, cơ sở dữ liệu và các công cụ khác...

**Turn 4:** Turn 4: Tôi muốn biết thêm về vector database.
- *No-memory:* Vector database (cơ sở dữ liệu vector) là một loại cơ sở dữ liệu được thiết kế để lưu trữ và truy vấn các vector, thường là các vector đặc trưng cho dữ liệu phi cấu trúc như văn bản, hình ảnh, âm than...
- *With-memory:* Vector database là một loại cơ sở dữ liệu được tối ưu hóa để lưu trữ và truy vấn các vector, thường được sử dụng trong các ứng dụng machine learning và tìm kiếm ngữ nghĩa. Chúng cho phép bạn thực hiện...

**Turn 5:** Turn 5: Chromadb có ưu điểm gì?
- *No-memory:* Chromadb là một cơ sở dữ liệu được thiết kế để lưu trữ và truy vấn các vector, thường được sử dụng trong các ứng dụng học máy và trí tuệ nhân tạo. Dưới đây là một số ưu điểm của Chromadb:

1. **Tối ưu...
- *With-memory:* ChromaDB có một số ưu điểm nổi bật như sau:

1. **In-process**: Chạy trong cùng một tiến trình với ứng dụng, giúp giảm độ trễ và tăng hiệu suất.
2. **Dễ sử dụng**: Cung cấp API đơn giản, dễ dàng tích ...

**Turn 6:** Turn 6: So sánh Chroma và FAISS đi.
- *No-memory:* Chroma và FAISS là hai công cụ phổ biến được sử dụng trong lĩnh vực tìm kiếm và truy xuất thông tin, đặc biệt là trong các ứng dụng liên quan đến học máy và trí tuệ nhân tạo. Dưới đây là một số điểm s...
- *With-memory:* ChromaDB và FAISS đều là các công cụ hỗ trợ tìm kiếm ngữ nghĩa dựa trên vector, nhưng có một số điểm khác biệt chính:

1. **Kiến trúc**:
   - **ChromaDB**: Là một vector database in-process, chạy tron...

**Turn 7:** Turn 7: Tôi đang xây agent hỏi đáp.
- *No-memory:* Rất tuyệt! Bạn đang xây dựng một agent hỏi đáp. Bạn cần hỗ trợ gì trong quá trình phát triển? Có thể là về kiến trúc, công nghệ, hay cách triển khai? Hãy cho tôi biết chi tiết hơn để tôi có thể giúp b...
- *With-memory:* Tuyệt vời! Bạn đang xây dựng một agent hỏi đáp bằng công nghệ nào? Bạn có cần hỗ trợ về kiến thức hoặc công cụ cụ thể nào không?

**Turn 8:** Turn 8: Tôi muốn thêm bộ nhớ dài hạn.
- *No-memory:* Hiện tại, tôi không có khả năng lưu trữ thông tin dài hạn hoặc ghi nhớ các cuộc trò chuyện trước đó. Mỗi lần bạn bắt đầu một cuộc trò chuyện mới, tôi không có thông tin từ các lần trước. Tuy nhiên, tô...
- *With-memory:* Bạn muốn thêm thông tin gì vào bộ nhớ dài hạn? Hãy cho tôi biết để tôi có thể cập nhật!

**Turn 9:** Turn 9: Còn bộ nhớ ngắn hạn thì sao?
- *No-memory:* Bộ nhớ ngắn hạn, hay còn gọi là bộ nhớ làm việc, là khả năng lưu trữ và xử lý thông tin trong một khoảng thời gian ngắn, thường chỉ từ vài giây đến vài phút. Nó cho phép chúng ta giữ lại thông tin tạm...
- *With-memory:* Bộ nhớ ngắn hạn là nơi lưu trữ các cuộc trò chuyện gần đây và thông tin tạm thời mà chúng ta đang thảo luận. Nó giúp tôi theo dõi và phản hồi nhanh chóng trong các cuộc trò chuyện hiện tại. Khi cuộc t...

**Turn 10:** Turn 10: Bạn có biết tên và nghề nghiệp của tôi không?
- *No-memory:* Xin lỗi, nhưng tôi không biết tên và nghề nghiệp của bạn. Tôi không có khả năng truy cập thông tin cá nhân của người dùng. Nếu bạn muốn chia sẻ, tôi rất vui lòng lắng nghe!
- *With-memory:* Có, tên bạn là An và bạn là kỹ sư.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 6: Recall user age
**Category:** profile_recall  
**Expected keyword:** `25`  

**Turn 1:** Tôi 25 tuổi và đang học AI.
- *No-memory:* Thật tuyệt vời! Học về trí tuệ nhân tạo (AI) là một lĩnh vực rất thú vị và có tiềm năng lớn trong tương lai. Bạn đang học về những khía cạnh nào của AI? Machine learning, deep learning hay một lĩnh vự...
- *With-memory:* Rất tốt! Học AI là một lĩnh vực thú vị và đầy tiềm năng. Nếu bạn cần hỗ trợ hay có câu hỏi nào về AI, hãy cho tôi biết nhé!

**Turn 2:** Bạn nhớ tôi bao nhiêu tuổi không?
- *No-memory:* Xin lỗi, tôi không có thông tin về tuổi của bạn. Nếu bạn muốn, bạn có thể chia sẻ với tôi!
- *With-memory:* Bạn 25 tuổi.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 7: Recall learning outcome from previous session
**Category:** episodic_recall  
**Expected keyword:** `transformer`  

**Turn 1:** Tôi vừa học xong bài về transformer architecture. Thành công!
- *No-memory:* Chúc mừng bạn đã hoàn thành bài học về kiến trúc transformer! Đây là một chủ đề rất thú vị và quan trọng trong lĩnh vực học máy, đặc biệt là trong xử lý ngôn ngữ tự nhiên. Nếu bạn có bất kỳ câu hỏi nà...
- *With-memory:* Tuyệt vời! Transformer architecture là một chủ đề rất thú vị và quan trọng trong học máy. Bạn có cần thảo luận thêm về nó không?

**Turn 2:** Bạn nhớ tôi học gì gần đây không?
- *No-memory:* Xin lỗi, nhưng tôi không có khả năng nhớ thông tin cá nhân hoặc theo dõi hoạt động của bạn. Tuy nhiên, tôi có thể giúp bạn với bất kỳ câu hỏi nào hoặc thông tin mà bạn cần. Bạn đã học gì gần đây?
- *With-memory:* Bạn vừa học xong bài về transformer architecture.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 8: Semantic retrieval — venv setup guide
**Category:** semantic_retrieval  
**Expected keyword:** `venv`  

**Turn 1:** Cách tạo môi trường ảo Python là gì?
- *No-memory:* Để tạo môi trường ảo trong Python, bạn có thể sử dụng công cụ `venv`, đây là một công cụ tích hợp sẵn trong Python từ phiên bản 3.3 trở đi. Dưới đây là các bước để tạo và sử dụng môi trường ảo:

### B...
- *With-memory:* Để tạo môi trường ảo trong Python, bạn có thể sử dụng `venv`. Dưới đây là các bước thực hiện:

1. **Mở terminal** (Command Prompt hoặc PowerShell trên Windows, Terminal trên macOS/Linux).
2. **Chuyển ...

**Result:** No-memory ✅ | With-memory ✅

---
### Scenario 9: Recall city and job
**Category:** profile_recall  
**Expected keyword:** `hà nội`  

**Turn 1:** Tôi sống ở Hà Nội và làm developer.
- *No-memory:* Rất vui được biết bạn sống ở Hà Nội và làm developer! Hà Nội là một thành phố tuyệt đẹp với nhiều cơ hội cho các lập trình viên. Bạn đang làm việc với công nghệ nào? Hay bạn có dự án nào thú vị đang t...
- *With-memory:* Tôi đã cập nhật thông tin của bạn. Bạn sống ở Hà Nội và làm developer.

**Turn 2:** Bạn biết gì về tôi không?
- *No-memory:* Tôi không biết gì về bạn, vì tôi không có khả năng truy cập thông tin cá nhân hoặc dữ liệu của người dùng. Tôi chỉ có thể trả lời dựa trên những gì bạn chia sẻ trong cuộc trò chuyện này. Nếu bạn có câ...
- *With-memory:* Bạn 25 tuổi, sống ở Hà Nội và làm developer. Gần đây, bạn đã học xong bài về transformer architecture. Bạn không có dị ứng thực phẩm nào.

**Result:** No-memory ❌ | With-memory ✅

---
### Scenario 10: Name conflict update (Minh → Tuấn)
**Category:** conflict_update  
**Expected keyword:** `tuấn`  

**Turn 1:** Tôi tên Minh.
- *No-memory:* Chào Minh! Bạn có điều gì muốn chia sẻ hoặc hỏi không?
- *With-memory:* Chào Minh! Rất vui được biết bạn. Bạn có muốn chia sẻ thêm thông tin gì không?

**Turn 2:** Thực ra tên tôi là Tuấn, không phải Minh.
- *No-memory:* Rất vui được biết tên thật của bạn, Tuấn! Có điều gì bạn muốn chia sẻ hoặc hỏi không?
- *With-memory:* Cảm ơn bạn đã thông báo! Tôi sẽ cập nhật lại tên của bạn thành Tuấn. Bạn có muốn chia sẻ thêm thông tin gì không?

**Turn 3:** Bạn nhớ tên tôi là gì?
- *No-memory:* Xin lỗi, nhưng tôi không có khả năng nhớ thông tin cá nhân của bạn. Bạn có thể cho tôi biết tên của bạn được không?
- *With-memory:* Tên của bạn là Tuấn.

**Result:** No-memory ❌ | With-memory ✅


---

## Analysis

### Memory Hit Rate
- Scenarios where with-memory agent passed: **10/10**
- Scenarios where no-memory agent passed: **2/10** (expected low for context-dependent queries)

### Token / Word Budget Breakdown

| # | No-memory words | With-memory words | Delta |
|---|-----------------|-------------------|-------|
| 1 | 678 | 450 | -228 |
| 2 | 248 | 54 | -194 |
| 3 | 690 | 385 | -305 |
| 4 | 426 | 196 | -230 |
| 5 | 1670 | 756 | -914 |
| 6 | 65 | 34 | -31 |
| 7 | 105 | 34 | -71 |
| 8 | 320 | 116 | -204 |
| 9 | 106 | 44 | -62 |
| 10 | 57 | 48 | -9 |

**Average word count per scenario — No-memory:** 436.5  
**Average word count per scenario — With-memory:** 211.7  

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
