import subprocess
import json
import requests
import pandas as pd

# 從 location_code.py 獲得地區代碼dict
def get_location_codes():
    try:
        # 執行location_code.py 腳本並獲取output
        result = subprocess.run(['python', 'location_code.py'], capture_output=True, text=True)
        
        # 將輸出轉換為 json 格式
        location_codes = json.loads(result.stdout)
        return location_codes
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        raise

# 使用104人力銀行api根據keyword, locaiton code 搜尋職缺
def get_jobs_from_api(keyword, location_code, pages=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
        "Referer": "https://www.104.com.tw/"
    }
    
    all_jobs = []
    for page in range(1, pages + 1):
        url = f'https://www.104.com.tw/jobs/search/list?ro=1&keyword={keyword}&area={location_code}&order=11&asc=0&page={page}&mode=s&jobsource=2018indexpoc'
        
        # 進用請求警告
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            jobs = data['data']['list']
            if jobs:
                for job in jobs[:10]:
                    
                    # 簡化職缺資訊   
                    simplified_job = {
                        "jobName": job.get("jobName"),
                        "companyName": job.get("custName"),
                        "location": job.get("jobAddrNoDesc"),
                        "salary": job.get("salaryDesc"),
                        "link": job["link"].get("job"),
                        "description": job.get("description")
                    }
                    all_jobs.append(simplified_job)
            else:
                break
        else:
            print(f"Error occurred: {response.status_code}")
            break

    return all_jobs

# 將職缺資訊保存為csv file
def save_jobs_to_csv(jobs, filename='jobs.csv'):
    if jobs:
        df = pd.DataFrame(jobs)
        df.to_csv(filename, index=False)
    else:
        print("無法存取為csv file")

if __name__ == "__main__":
    keyword = '軟體工程師'
    location_name = '台北市'
    location_codes = get_location_codes()
    location_code = location_codes.get(location_name)
    
    if location_code:
        pages = 5
        jobs = get_jobs_from_api(keyword, location_code, pages)
        save_jobs_to_csv(jobs)
    else:
        print(f"無法取得 {location_name} 的地區代碼")
