from django.shortcuts import render
from bs4 import BeautifulSoup
from .models import Category
import requests

# Function to get news from Krebs on Security
def get_krebs_news():
    krebs_news = []
    try:
        krebs_r = requests.get("https://krebsonsecurity.com/", timeout=10)  # Set a timeout
        krebs_r.raise_for_status()

        krebs_soup = BeautifulSoup(krebs_r.content, 'html5lib')
        krebs_headings = krebs_soup.find_all('h2', {"class": "entry-title"})
        for kh in krebs_headings:
            krebs_news.append(kh.text.strip())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Krebs on Security news: {e}")
    
    return krebs_news

# Function to get news from The Hacker News
def get_hackernews_news():
    hackernews_news = []
    try:
        hn_r = requests.get("https://thehackernews.com/", timeout=10)
        hn_r.raise_for_status()

        hn_soup = BeautifulSoup(hn_r.content, 'html5lib')
        hn_headings = hn_soup.find_all('h2', {"class": "home-title"})

        for hnh in hn_headings:
            hackernews_news.append(hnh.text.strip())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching The Hacker News: {e}")
    
    return hackernews_news


def index(request):
    # Fetch news from all cybersecurity sources
    krebs_news = get_krebs_news()
    hackernews_news = get_hackernews_news()


    # Render the data in the template
    return render(request, 'cyberevents/index.html', {
        'krebs_news': krebs_news,
        'hackernews_news': hackernews_news,
    })


def base(request):
    # Fetch news from all cybersecurity sources
    krebs_news = get_krebs_news()
    hackernews_news = get_hackernews_news()
   
    # Render the data in the template
    return render(request, 'cyberevents/base.html', {
        'krebs_news': krebs_news,
        'hackernews_news': hackernews_news,
    })
def category_list(request):
    categories = Category.objects.all() 
    return render(request, 'parts/category_list.html', {'categories': categories})

def about(request):
    return render(request, 'cyberevents/about.html', {'about': about})

def incident_stats(request):
    return render(request, 'cyberevents/incident_stats.html', {'incident_stats': incident_stats})

def login(request):
    return render(request, 'cyberevents/login.html', {'login': login})

def register(request):
    return render(request, 'cyberevents/register.html', {'register': register})