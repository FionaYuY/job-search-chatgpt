import jobs
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
import os
import json
import warnings
import csv
from location_code import generate_location_codes

# 設置 OpenAI API KEY
os.environ["OPENAI_API_KEY"] = 'YOUR API KEY'

# 忽略棄用警告
warnings.filterwarnings("ignore", category=DeprecationWarning)

# 根據position, location name 獲取職缺並保存為csv file
def get_and_save_jobs(position, location_name):
    location_codes = generate_location_codes()
    location_code = location_codes.get(location_name)
    
    if not location_code:
        return f"地區 {location_name} 的地區碼未找到。"
    
    jobs_list = jobs.get_jobs_from_api(position, location_code)
    
    if not jobs_list:
        return f"在 {location_name} 沒有找到與 {position} 相關的職缺。"
    
    # Save jobs to a CSV file
    with open('jobs.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["jobName", "companyName", "location", "salary", "link", "description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs_list)
        
    return "jobs.csv"

# 根據職位、技能、地區推薦工作
def recommend_jobs(position, skills, location_name):
    csv_filename = get_and_save_jobs(position, location_name)
    
    # 檢查是否成功生成csv file
    if isinstance(csv_filename, str) and csv_filename.endswith(".csv"):
        # load csv file
        loader = CSVLoader(file_path=csv_filename)
        documents = loader.load()
        
        # 分割文本
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_docs = text_splitter.split_documents(documents)
        
        # 創建向量資料庫
        embedder = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(split_docs, embedder)
        
        # 創建retriever
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        
        # 創建檢索問答鏈
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever
        )
        
        # combine所有技能
        combined_skills = " ".join(skills)
        query = f"推薦給具備 {combined_skills} 技能的工作"
        result = qa_chain({"query": query})
        
        return result["result"]
    else:
        return csv_filename

if __name__ == "__main__":
    position = "軟體工程師"
    skills = ["Python", "SQL"]
    location_name = "台北市"
    recommendations = recommend_jobs(position, skills, location_name)
    if isinstance(recommendations, str):
        print(recommendations)
    else:
        print(json.dumps(recommendations, ensure_ascii=False, indent=4))
