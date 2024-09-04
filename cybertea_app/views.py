from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

# Function to get news from Krebs on Security
def get_krebs_news():
    krebs_news = []
    try:
        krebs_r = requests.get("https://krebsonsecurity.com/")
        krebs_r.raise_for_status()

        krebs_soup = BeautifulSoup(krebs_r.content, 'html5lib')
        krebs_headings = krebs_soup.find_all('h2', {"class": "entry-title"})
        
        for kh in krebs_headings:
            krebs_news.append(kh.text.strip())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Krebs on Security news: {e}")
    
    return krebs_news

# Function to get news from Dark Reading
def get_darkreading_news():
    darkreading_news = []
    try:
        dr_r = requests.get("https://www.darkreading.com/")
        dr_r.raise_for_status()

        dr_soup = BeautifulSoup(dr_r.content, 'html5lib')
        dr_headings = dr_soup.find_all('h3', {"class": "listing-title"})

        for drh in dr_headings:
            darkreading_news.append(drh.text.strip())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Dark Reading news: {e}")
    
    return darkreading_news

# Function to get news from The Hacker News
def get_hackernews_news():
    hackernews_news = []
    try:
        hn_r = requests.get("https://thehackernews.com/")
        hn_r.raise_for_status()

        hn_soup = BeautifulSoup(hn_r.content, 'html5lib')
        hn_headings = hn_soup.find_all('h2', {"class": "home-title"})

        for hnh in hn_headings:
            hackernews_news.append(hnh.text.strip())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching The Hacker News: {e}")
    
    return hackernews_news

# Function to get news from Bleeping Computer
def get_bleepingcomputer_news():
    bleepingcomputer_news = []
    try:
        bc_r = requests.get("https://www.bleepingcomputer.com/")
        bc_r.raise_for_status()

        bc_soup = BeautifulSoup(bc_r.content, 'html5lib')
        bc_headings = bc_soup.find_all('h2', {"class": "bc-title"})

        for bch in bc_headings:
            bleepingcomputer_news.append(bch.text.strip())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bleeping Computer news: {e}")
    
    return bleepingcomputer_news

# Function to get news from SecurityWeek
def get_securityweek_news():
    securityweek_news = []
    try:
        sw_r = requests.get("https://www.securityweek.com/")
        sw_r.raise_for_status()

        sw_soup = BeautifulSoup(sw_r.content, 'html5lib')
        sw_headings = sw_soup.find_all('h2', {"class": "title"})

        for swh in sw_headings:
            securityweek_news.append(swh.text.strip())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SecurityWeek news: {e}")
    
    return securityweek_news

# Function to get news from Threatpost
def get_threatpost_news():
    threatpost_news = []
    try:
        tp_r = requests.get("https://threatpost.com/")
        tp_r.raise_for_status()

        tp_soup = BeautifulSoup(tp_r.content, 'html5lib')
        tp_headings = tp_soup.find_all('h2', {"class": "c-title"})

        for tph in tp_headings:
            threatpost_news.append(tph.text.strip())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Threatpost news: {e}")
    
    return threatpost_news

def index(request):
    # Fetch news from all cybersecurity sources
    krebs_news = get_krebs_news()
    darkreading_news = get_darkreading_news()
    hackernews_news = get_hackernews_news()
    bleepingcomputer_news = get_bleepingcomputer_news()
    securityweek_news = get_securityweek_news()
    threatpost_news = get_threatpost_news()

    # Render the data in the template
    return render(request, 'cyberevents/index.html', {
        'krebs_news': krebs_news,
        'darkreading_news': darkreading_news,
        'hackernews_news': hackernews_news,
        'bleepingcomputer_news': bleepingcomputer_news,
        'securityweek_news': securityweek_news,
        'threatpost_news': threatpost_news,
    })
