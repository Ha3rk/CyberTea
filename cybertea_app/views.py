from django.shortcuts import render, redirect,  get_object_or_404
from .models import User, Author, Category, Post, Comment, Reply
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from bs4 import BeautifulSoup
from .models import Category
from django.http import JsonResponse
import requests
import os
import openai
import logging
from django.contrib import messages
from .forms import LoginForm, RegistrationForm, PostForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from .utils import update_views


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
def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        author = Author.objects.get(user=request.user)
    
    if "comment-form" in request.POST:
        comment = request.POST.get("comment")
        new_comment, created = Comment.objects.get_or_create(user=author, content=comment)
        post.comments.add(new_comment.id)

    if "reply-form" in request.POST:
        reply = request.POST.get("reply")
        commenr_id = request.POST.get("comment-id")
        comment_obj = Comment.objects.get(id=commenr_id)
        new_reply, created = Reply.objects.get_or_create(user=author, content=reply)
        comment_obj.replies.add(new_reply.id)


    context = {
        "post":post,
        "title": "OZONE: "+post.title,
    }
    update_views(request, post)
    return render(request, "cyberevents/detail.html", context)



def forums(request):
    forums = Category.objects.all()
    num_posts = Post.objects.all().count()
    num_users = User.objects.all().count()
    num_categories = forums.count()
    try:
        last_post = Post.objects.latest("date")
    except:
        last_post = []

    context = {
        "forums":forums,
        "num_posts":num_posts,
        "num_users":num_users,
        "num_categories":num_categories,
        "last_post":last_post,
        "title": "OZONE forum app"
    }
    return render(request, "cyberevents/forums.html", context)

def posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved=True, categories=category)
    paginator = Paginator(posts, 5)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) 

    context = {
        "posts":posts,
        "forum": category,
        "title": "OZONE: Posts"
    }

    return render(request, "cyberevents/posts.html", context)

def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print("\n\n its valid")
            author = Author.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.save()
            form.save_m2m()
            return redirect("home")
    context.update({
        "form": form,
        "title": "OZONE: Create New Post"
    })
    return render(request, "cyberevents/create_post.html", context)
def latest_posts(request):
    posts = Post.objects.all().filter(approved=True)[:10]
    context = {
        "posts":posts,
        "title": "OZONE: Latest 10 Posts"
    }

    return render(request, "cyberevents/latest-posts.html", context)


def search_result(request):

    return render(request, "cyberevents/search.html")

def about(request):
    return render(request, 'cyberevents/about.html', {'about': about})

def contact(request):
    return render(request, 'cyberevents/about.html', {'about': about})

def resource(request):
    return render(request, 'cyberevents/about.html', {'about': about})

def trending(request):
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
                return redirect('forums')
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



def logout_view(request):
    logout(request)
    return redirect('index') 


api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API Key not found. Make sure to set the OPENAI_API_KEY environment variable.")


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

def summarize_with_gpt(article_text):
    try:
        logger.debug("Starting summarization with GPT for provided article text.")
        logger.debug(f"Article text: {article_text[:200]}...")  # Log the first 200 characters to avoid verbosity

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "highlight all key points in an ordered list of 3 short concise sentences. If there is professional level technical term, explain after the highlights in glossary format"},
                {"role": "user", "content": article_text}
            ],
            max_tokens=3000
        )

        summary = response['choices'][0]['message']['content'].strip()
        logger.debug(f"Summarization response: {summary}")
        return summary

    except Exception as e:
        logger.error(f"Error during summarization: {str(e)}")
        return f"Error during summarization: {str(e)}"
