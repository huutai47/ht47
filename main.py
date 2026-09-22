import requests
from bs4 import BeautifulSoup
import datetime

# 1. Định nghĩa nguồn lấy dữ liệu (Ví dụ giả định cấu trúc web bóng đá)
SOURCE_URL = "https://example-sports-site.com" 
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def get_match_streams():
    matches = []
    try:
        response = requests.get(SOURCE_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm các phần tử chứa trận đấu dựa theo cấu trúc HTML của trang đó
        # (Bạn cần F12 trên trình duyệt để tìm class chính xác)
        match_elements = soup.find_all('div', class_='match-item') 
        
        for item in match_elements:
            title = item.find('span', class_='match-name').text.strip()
            time = item.find('span', class_='match-time').text.strip()
            stream_url = item.find('a', class_='btn-watch')['href'] # Link luồng phát hoặc link trang xem
            logo = item.find('img')['src'] if item.find('img') else ""
            
            # Chỉ lấy các trận sắp hoặc đang diễn ra trong ngày
            matches.append({
                "title": f"[{time}] {title}",
                "url": stream_url,
                "logo": logo
            })
    except Exception as e:
        print(f"Lỗi khi cào dữ liệu: {e}")
    return matches

def generate_m3u(matches):
    # Khởi tạo định dạng chuẩn M3U
    m3u_content = "#EXTM3U x-tvg-url=\"\"\n"
    
    for match in matches:
        # Nhóm các trận đấu vào thư mục "Bóng Đá Trực Tiếp"
        m3u_content += f'#EXTINF:-1 tvg-logo="{match["logo"]}" group-title="Bóng Đá Trực Tiếp", {match["title"]}\n'
        m3u_content += f'{match["url"]}\n'
        
    # Ghi ra file
    with open("live_football.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Đã cập nhật danh sách phát M3U thành công!")

if __name__ == "__main__":
    match_list = get_match_streams()
    generate_m3u(match_list)