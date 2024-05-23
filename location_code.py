import json
import requests

# 從104人力銀行獲取地區代碼並解析為dict
def generate_location_codes():
    url = 'https://static.104.com.tw/category-tool/json/Area.json'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    
    try:
        # 禁用請求警告並發送GET請求
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, headers=headers, verify=False)
        
        # 如果請求失敗則引發異常
        response.raise_for_status()
        
        # 將response轉換為 json 格式
        data = response.json()
    except requests.exceptions.RequestException as e:
        # 如果請求失敗返回空的dict
        return {}

    # 解析json 數據以獲取location code
    def parse_location_codes(json_data):
        location_codes = {}
        if json_data:
            for item in json_data[0]['n']:
                # 添加市級地區代碼
                location_codes[item['des']] = item['no']  # 市
                for sub_item in item['n']:
                    # 添加區級地區代碼
                    location_codes[f"{item['des']}{sub_item['des']}"] = sub_item['no']  # 區
        return location_codes

    location_codes = parse_location_codes(data)
    
    return location_codes

if __name__ == "__main__":
    location_codes = generate_location_codes()
    print(json.dumps(location_codes, ensure_ascii=False))
