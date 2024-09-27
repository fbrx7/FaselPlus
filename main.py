import requests
from bs4 import BeautifulSoup
import lxml
import re
import json
import os
from termcolor import cprint, colored
def sending_req(type:str):

    url_movies = 'https://www.faselplus.com/watchlist?type=movies'
    url_series = 'https://www.faselplus.com/watchlist?type=tv'
    
    with open ('cookies.json','r') as file:
        cookies = json.load(file)

    if type == 'movies':

        req = requests.session().get(url_movies, cookies=cookies)
        content = req.content
        return content
    
    elif type == 'series':

        req = requests.session().get(url_series, cookies=cookies)
        content = req.content
        return content

def soup_proc(content):

    image_urls = []

    soup = BeautifulSoup(content, 'lxml')
    find_all = soup.find_all('div', class_='category-item col_fix col-lg-2')
    
    for i in find_all:
        div = i.find("div", class_="image-background")

        if div:
            style = div.get("style")

    # استخدام تعبير عادي لاستخراج رابط الصورة من background-image
            match = re.search(r"url\('(.*?)'\)", style)
        if match:
            image_url = match.group(1)  # نحصل على الرابط داخل الـ url('')
            image_urls.append(image_url)

    
    return image_urls

def save(movies_urls, series_urls):
    # إنشاء المجلد الرئيسي
    main_folder = "downloaded_media"
    
    # إنشاء المجلدين الفرعيين للأفلام والمسلسلات
    movies_folder = os.path.join(main_folder, "movies")
    series_folder = os.path.join(main_folder, "series")
    
    # التأكد من وجود المجلدات، وإذا لم تكن موجودة يتم إنشاؤها
    for folder in [movies_folder, series_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # HTML الأساسي مع التبويبين
    html_content = '''
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>عرض الصور</title>
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #00aaff;
        }
        .tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .tabs button {
            background-color: #00aaff;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            font-size: 16px;
            margin: 0 5px;
        }
        .tabs button:hover {
            background-color: #0088cc;
        }
        .tab-content {
            display: none;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        .tab-content img {
            max-width: 300px;
            border: 2px solid #00aaff;
            border-radius: 8px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .tab-content img:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 20px rgba(0, 170, 255, 0.7);
        }
        .active {
            display: flex;
        }
    </style>
    <script>
        function openTab(tabName) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            document.getElementById(tabName).style.display = "flex";
        }
    </script>
</head>
<body>

    <h1>معرض الصور</h1>
    <div class="tabs">
        <button onclick="openTab('movies')">الأفلام</button>
        <button onclick="openTab('series')">المسلسلات</button>
    </div>
    
    <div id="movies" class="tab-content active">
'''

    # تنزيل وحفظ الصور للأفلام
    for url in movies_urls:
        # استخراج اسم الصورة
        image_name = url.split("/")[-1]
        image_path = os.path.join(movies_folder, image_name)

        # التحقق مما إذا كانت الصورة موجودة
        if not os.path.exists(image_path):
            try:
                # تنزيل الصورة
                response = requests.get(url)
                if response.status_code == 200:
                    with open(image_path, 'wb') as file:
                        file.write(response.content)
                    print(f"{colored('Image Downloaded: ','green')} {image_name}")
                else:
                    print(f"{colored('Failed to download image from link: ','red')} {url}")
            except Exception as e:
                print(f"{colored('Error: ')} {e}")
        else:
            print(f"{colored('image aleady exists','cyan')} {image_name}")

        # إضافة الصورة إلى تبويب الأفلام
        html_content += f'        <img src="{movies_folder}/{image_name}" alt="Movie Image">\n'

    html_content += '''
    </div>
    
    <div id="series" class="tab-content">
'''

    # تنزيل وحفظ الصور للمسلسلات
    for url in series_urls:
        # استخراج اسم الصورة
        image_name = url.split("/")[-1]
        image_path = os.path.join(series_folder, image_name)

        # التحقق مما إذا كانت الصورة موجودة
        if not os.path.exists(image_path):
            try:
                # تنزيل الصورة
                response = requests.get(url)
                if response.status_code == 200:
                    with open(image_path, 'wb') as file:
                        file.write(response.content)
                    print(f"{colored('Image Downloaded: ','green')} {image_name}")
                else:
                    print(f"{colored('Failed to download image from link: ','red')} {url}")
            except Exception as e:
                print(f"{colored('Error: ')} {e}")
        else:
            print(f"{colored('image aleady exists','blue')} {image_name}")

        # إضافة الصورة إلى تبويب المسلسلات
        html_content += f'        <img src="{series_folder}/{image_name}" alt="Series Image">\n'

    # إغلاق HTML
    html_content += '''
    </div>

</body>
</html>
'''

    # كتابة المحتوى إلى ملف HTML
    with open("gallery.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"{colored('Html File Created !','green')}")


def main():

    movies_content = sending_req('movies')
    series_content = sending_req('series')

    movies_urls = soup_proc(movies_content)
    series_urls = soup_proc(series_content)

    save(movies_urls, series_urls)

    
main()
