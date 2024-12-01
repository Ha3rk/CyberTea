<<<<<<< HEAD
🛡☕  CyberTea

An AI-powered community platform providing:

    📰 Cybersecurity news aggregation
    🎙️ Narration
    📊 Real-time incident display dashboard

👨🏾‍💻 Author: Akeem Ajibare
💻 Language: Python
🌐 Framework: Django
=======
🛡☕ CyberTea

An AI-powered community platform providing:

📰 Cybersecurity news aggregation
🎙️ Narration
📊 Real-time incident display dashboard

👨🏾‍💻 Author: Akeem Ajibare 💻 Language: Python 🌐 Framework: Django
>>>>>>> 73248e7 ( css:chaged to royal purple, no ai, no community, no display, read me update)

🚀 How to Run

# Clone the Repository

git clone <repo>

# Navigate to the Project Directory

cd project-directory

# Create Virtual Environment

python -m venv projectenv

# Activate On macOS/Linux:

source projectenv/bin/activate  

# Activate On Windows: 

projectenv\Scripts\activate

# Install Dependencies
##Please Note Openai==0.28 alone works for the program, so do not upgrade

pip install -r requirements.txt 

(remove d-bus & tzdata in requirement.txt for windows and use pip instead of pip3 as in linux/mac oS)

# Configure Environment Variable

pip install python-dotenv
create .env file in root directory (where you have manage.py )
put your secret key there
import and load the secret key in settings.py


# Make and Run Migrations
python manage.py makemigrations cybertea_app
python manage.py migrate

# Start the Development Server

    python manage.py runserver

