from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from .models import Category
from django.http import JsonResponse
import requests
import os
import openai
import logging
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login as auth_login

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Set your OpenAI API key



def get_krebs_news():
    krebs_news = []
    try:
        krebs_r = requests.get("https://krebsonsecurity.com/", timeout=10)
        krebs_r.raise_for_status()
        krebs_soup = BeautifulSoup(krebs_r.content, 'html5lib')
        krebs_headings = krebs_soup.find_all('h2', {"class": "entry-title"})
        for kh in krebs_headings:
            title = kh.text.strip()
            url = kh.find('a')['href']
            krebs_news.append({'title': title, 'url': url})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Krebs on Security news: {e}")
    return krebs_news

def get_hackernews_news():
    hackernews_news = []
    try:
        hn_r = requests.get("https://thehackernews.com/", timeout=10)
        hn_r.raise_for_status()
        hn_soup = BeautifulSoup(hn_r.content, 'html5lib')
        hn_headings = hn_soup.find_all('h2', {"class": "home-title"})
        for hnh in hn_headings:
            title = hnh.text.strip()
            a_tag = hnh.find('a')
            if a_tag and 'href' in a_tag.attrs:
                url = a_tag['href']
                hackernews_news.append({'title': title, 'url': url})
            else:
                hackernews_news.append({'title': title, 'url': None})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching The Hacker News: {e}")
    return hackernews_news

def index(request):
    krebs_news = get_krebs_news()
    hackernews_news = get_hackernews_news()
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
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        login_form = LoginForm()

    return render(request, 'registration/login.html', {'login_form': login_form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Set the password
            user.save()
            messages.success(request, 'Registration successful.')
            return redirect('login')  # Redirect to a login page or any other page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


openai.api_key = os.environ.get("OPENAI_API_KEY") 

# Function to fetch article content and summarize it using GPT
def summarize_article(request):
    if request.method == 'POST':
        article_url = request.POST.get('url')
        try:
            response = requests.get(article_url, timeout=10)
            response.raise_for_status()
            article_html = response.content
            soup = BeautifulSoup(article_html, 'html.parser')
            article_text = " ".join([p.text for p in soup.find_all('p')])

            summary = summarize_with_gpt(article_text)
            return JsonResponse({'summary': summary})

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': 'Error fetching article: ' + str(e)}, status=500)

'''def summarize_with_gpt(article_text):
    try:
        logger.debug("Starting summarization with GPT for provided article text.")
        logger.debug(f"Article text: {article_text[:200]}...")  # Log the first 200 characters to avoid verbosity

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "narrate the article by highlighting all its key points in a list of five concise sentences."},
                {"role": "user", "content": article_text}
            ],
            max_tokens=10000
        )

        summary = response['choices'][0]['message']['content'].strip()
        logger.debug(f"Summarization response: {summary}")
        return summary

    except Exception as e:
        logger.error(f"Error during summarization: {str(e)}")
        return f"Error during summarization: {str(e)}"
        '''