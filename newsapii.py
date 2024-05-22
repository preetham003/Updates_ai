import requests
import json
from newsapi import NewsApiClient
from datetime import datetime, timedelta
# api = NewsApiClient(api_key='891c4e88914246a39615834e6697a955')

def newsapi1(query):
    # Get today's date
    today = datetime.today()
    yesterday = today - timedelta(days=1) 
    # Format the date as YYYY-MM-DD
    from_date = yesterday.strftime('%Y-%m-%d')
    to_date=today.strftime('%Y-%m-%d')
    # print(formatted_date)
    # query='python'
    print('query',query)
    # url=f'https://newsapi.org/v2/top-headlines?q={query}&apiKey=891c4e88914246a39615834e6697a955'
    url=f'https://newsapi.org/v2/everything?q={query}&from={from_date}&to={to_date}&sortBy=popularity&apiKey=891c4e88914246a39615834e6697a955'
    # url=str(url)
    r=requests.get(url)
    news=json.loads(r.text)
    # print("news",news)
    articles=news['articles']
    # print('articles:',articles)
    main_article=''
    for article in articles[:5]:
        # print(article)
        print(article['title'])
        print(article['description'])
        print(article['url'])
        print("******************")
        if article['content'] != None and article['title']!='null' :
            main_article+='title:'+article['title']+'description:'+article['content']+'url'+article['url']
    print(main_article)
    return main_article

def newsapi2(query):
    # query=input("what type of news are you intrested in?")
    # url=f'GET https://newsapi.org/v2/everything?q={query}&from=2024-05-20&to=2024-05-20&sortBy=popularity&apiKey=891c4e88914246a39615834e6697a955'
    url=f'https://eventregistry.org/api/v1/article/getArticles?action=getArticles&lang=eng&keyword={query}&articlesPage=1&articlesCount=5&articlesSortBy=date&articlesSortByAsc=false&articlesArticleBodyLen=-1&resultType=articles&dataType%5B%5D=news&dataType%5B%5D=pr&apiKey=c895dab9-8938-475d-8a5a-42cbfcb6c94d&forceMaxDataTimeWindow=31'
    r=requests.get(url)
    news=json.loads(r.text)
    articles=news['articles']
    articles_results=articles['results']
    # print('articles_results',articles_results)
    main_article=''
    for article in articles_results:
        print(article['title'])
        print(article['body'].replace('\n',' '))
        print(article['url'])
        print("********************************")
        main_article+='title:'+article['title']+'body:'+article['body'].replace('\n',' ')+'url:'+article['url']
    return main_article

# newsapi1('openai')
# print(articles_results['title'])

# result=api.get_everything(q='bitcoin')

# print(result)