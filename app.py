from flask import Flask, request, jsonify
from jobs import get_jobs_from_api, get_location_codes
from recommendation import recommend_jobs

# 建立flask應用
app = Flask(__name__)

# 定義 /search_jobs route
@app.route('/search_jobs', methods=['POST'])
def search_jobs():
    # 從需求中獲取 json 數據
    data = request.get_json()
    keyword = data.get('keyword')
    location_name = data.get('location')

    if not keyword or not location_name:
        return jsonify({'error': 'Keyword and location are required.'}), 400

    location_codes = get_location_codes()
    location_code = location_codes.get(location_name)
    
    # 檢查location code是否存在
    if not location_code:
        return jsonify({'error': f"Location code for {location_name} not found."}), 400

    # 使用keyword, location_code 搜尋工作
    jobs = get_jobs_from_api(keyword, location_code)
    return jsonify(jobs)

# 定義 /recommend_jobs route
@app.route('/recommend_jobs', methods=['POST'])
def recommend_jobs_route():
    # 從請求中獲取 json 數據
    data = request.get_json()
    position = data.get('position')
    skills = data.get('skills')
    location_name = data.get('location')

    # 檢查是否提供了position, skills, location_name
    if not position or not skills or not location_name:
        return jsonify({'error': 'Position, skills, and location are required.'}), 400

    # 使用position, skills, location_name 推薦工作
    recommendations = recommend_jobs(position, skills, location_name)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
