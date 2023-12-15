from bs4 import BeautifulSoup as bs
import requests
import lxml

def get_html(url):
    response = requests.get(url)
    return response.text


def get_data(html):
    soup = bs(html, 'lxml')
    all_news = soup.find_all('div', class_='ArticleItem--data ArticleItem--data--withImage')

    data_ls = []
    count = 0

    for news in all_news:
        try:
            title = news.find('a', class_='ArticleItem--name').text.strip()
            
            photo = news.find('a', class_='ArticleItem--image').find('img').get('src')

            desc_href = news.find('a', class_='ArticleItem--name').get('href')
            desc_html = get_html(desc_href)
            soup1 = bs(desc_html, 'lxml')
            desc = soup1.find('div', class_='Article--text').text.replace('\n', '').replace('\r', '').strip()

        except:
            title = ''
            photo = ''
            desc = ''

        data_ls.append([title, desc, photo])

        count += 1

        if count == 20:
            break

    return data_ls


def main():
    url = 'https://kaktus.media/?lable=8&date=2023-12-14&order=time'
    html = get_html(url)
    data1 = get_data(html)
    return data1

if __name__ == '__main__':
    main()
