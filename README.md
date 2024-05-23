# job-search-chatgpt

## 工作搜尋與推薦系統

此專案使用 Flask 架設了一個 API，允許使用者根據其技能和地區搜尋工作並獲得工作推薦。我們使用了 OpenAI 的 GPT-3.5 模型進行自然語言處理和推薦工作。此專案結合了 Retrieval-Augmented Generation (RAG) 技術來提升推薦的準確性和相關性。RAG 技術結合了基於檢索的模型和生成式模型，能夠根據使用者的技能和輸入內容生成更加合適的工作推薦。

## 專案目錄結構
```
job-search-chatgpt/
├── app.py
├── location_code.py
├── jobs.py
├── recommendation.py
├── requirements.txt
├── Procfile
├── README.md
├── openai_schema.json
└── demonstration
```

### 功能簡介

- **app.py**: 主應用程式，使用 Flask 架設 API。
- **location_code.py**: 爬取 104 人力銀行的地區代碼並生成地區代碼字典。
- **jobs.py**: 包含搜尋工作和保存工作的功能。
  ```python
  def get_location_codes():
      # 獲取地區代碼字典。
  ```

  ```python
  def get_jobs_from_api(keyword, location):
      # 根據關鍵字和地區搜尋職缺。
  ```

  ```python
  def save_jobs_to_csv(jobs):
      # 將職缺結果保存為 CSV 文件。
  ```
- **recommendation.py**: 根據使用者輸入的職位、技能和地區推薦工作。
  ```python
  def recommend_jobs(position, skills, location_name):
      # 根據提供的職位(position)和地區(location_name)搜尋相關工作，再利用RAG的方式推薦與技能(skills)相關的工作。
  ```
- **requirements.txt**: 專案依賴的 Python 套件。
- **Procfile**: Heroku 部署配置文件。
- **openai_schema.json**: 定義 OpenAI Function Calling Schema 的 JSON 文件。

## 安裝與使用

### 本地開發

1. clone此專案:
   ```bash
   git clone https://github.com/yourusername/occupation-chatgpt-api.git
   cd occupation-chatgpt-api
   ```
2. 建立並啟用虛擬環境：
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # 對於 Windows 使用 `venv\Scripts\activate`
   ```

3. 安裝依賴項：
   ```bash
   pip install -r requirements.txt
   ```

4. 修改recommendation.py中的OPEN_AI_KEY
5. 啟動應用程式
   ```bash
   flask run
   ```

## 部署到 Heroku
1. 登入Heroku:
   ```bash
   heroku login
   ```
2. 初始化git並提交
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. 創建Heroku應用並推送
   ```bash
   heroku create your-app-name
   git push heroku master
   ```
4. 監控應用程式
   ```bash
   heroku logs --tail -a your-app-name
   ```

## 部署到 ChatGPT
要將此專案部署到 ChatGPT 上，可以前往 ChatGPT GPTs Editor 使用 openai_schema.json 文件建立自己的 GPT。並將文件中servers的url換成heroku的url。這將允許你利用 OpenAI 的 function calling 特性來使用你部署的 API。

## API端點

### 搜尋工作
- **URL**: `/search_jobs`
- **方法**: `POST`
- **描述**: 根據關鍵字和地區搜尋工作。這個端點會先調用 jobs.py 中的 `get_location_codes` ，並將地區轉換為地區代碼。之後，再調用jobs.py中的 `get_jobs_from_api` 函數，並返回一個符合搜尋條件的工作列表。
- **請求範例**:
  ```json
  {
    "keyword": "軟體工程師",
    "location": "台北市",
    "pages": 1
  }
  ```
- **回應範例**:
  ```json
  [
    {
      "jobName": "軟體工程師",
      "companyName": "ABC 公司",
      "location": "台北市",
      "salary": "60000-80000",
      "link": "http://www.example.com/job/123",
      "description": "工作描述"
    }
  ]
  ```

### 獲得工作推薦
- **URL**: `/recommend_jobs`
- **方法**: `POST`
- **描述**: 根據職位、技能和地區獲得工作推薦。這個端點會調用 recommendation.py 中的 `recommend_jobs` 函數，並返回一個根據提供條件生成的非結構化推薦結果。
- **請求範例**:
  ```json
  {
    "position": "軟體工程師",
    "skills": ["Python", "SQL"],
    "location": "台北市"
  }
  ```
- **回應範例**:
  ```json
  {
    "result": "根據您的技能和地區，我們推薦以下工作：1. 軟體工程師 - ABC 公司 - 台北市 - 60000-80000..."
  }
  ```

## 技術內容

### 搜尋功能
- **HTTP 請求**: 使用 HTTP 請求訪問 104 人力銀行 API，根據關鍵字和地區搜尋工作。。
- **Flask**: 使用 Flask 構建 API，並在 `/search_jobs` 端點處理工作搜尋請求。

### 推薦功能
- **OpenAI GPT-3.5**: 使用 OpenAI GPT-3.5 模型進行自然語言處理和生成推薦結果。
- **LangChain**: 使用 LangChain 實現 Retrieval-Augmented Generation (RAG) 的推薦系統。RAG 結合了基於檢索的模型和生成式模型，用於生成更準確的推薦結果。
- **向量資料庫**: 使用 ChromaDB 作為向量資料庫，儲存和檢索文本向量化後的數據。

### 部署
- **Heroku**: 使用 Heroku 部署和託管應用程式，並使用 gunicorn 作為 WSGI 伺服器。
- **ChatGPT Function Calling**

## 貢獻
歡迎提出問題和提交 pull requests。

## 授權
此專案採用 MIT 授權條款。詳情請參閱 LICENSE 文件。
