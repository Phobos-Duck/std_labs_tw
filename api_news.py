import requests
from bot_command import colect_news

def get_news(api_key, category):
        category_mapping = {
            'политика': 'politics',
            'спорт': 'sports',
            'технологии': 'technology',
            'бизнес' : 'business',
            'образование' : 'entertainment',
            'главные' : 'general',
            'здоровье' : 'health',
            'наука' : 'science'
        }
        category = category_mapping.get(category.lower(), category.lower())

        url = f'https://newsapi.org/v2/top-headlines?country=ru&category={category}&apiKey={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            articles = data['articles']
            for article in articles:
                title = article['title']
                url = article.get('url', 'No description available')
                colect_news(title, url)
        else:
            print('Ошибка при получении данных о новостях')