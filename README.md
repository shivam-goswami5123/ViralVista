# 🌟 ViralVista 🌟

ViralVista is a full-stack web application that uses **Python Selenium** to scrape trending topics from Twitter (X), saves the data into **MongoDB**, and displays the information using a **ReactJS frontend** powered by a **Node.js backend**. The project demonstrates web scraping, proxy handling, and full-stack development integration.

---

## ✨ Features

- 🔍 Scrapes trending topics from the **For You** page on Twitter (X).
- 🌐 Uses **ProxyMesh** for secure proxy-based web scraping.
- 🛢️ Saves trends to **MongoDB Atlas** for persistence.
- 💻 Provides a **ReactJS** frontend to display trends.
- ⚙️ Backend built with **Node.js and Express** to manage APIs.

---

## 📂 File Structure
```bash
ViralVista/
├── backend/                   # Backend API built with Node.js and Express
│   ├── server.js              # Main Node.js server file
│   ├── package.json           # Backend dependencies and npm scripts
│   └── README.md              # Backend-specific documentation (optional)
│
├── frontend/                  # ReactJS frontend for displaying trends
│   ├── public/
│   │   └── index.html         # Entry point HTML for React
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   ├── index.js           # React entry file for rendering
│   │   └── styles.css         # Stylesheet for the frontend
│   ├── package.json           # Frontend dependencies and npm scripts
│   └── README.md              # Frontend-specific documentation (optional)
│
├── scrapper/                  # Python scraper for Twitter (X) trends
│   ├── selenium_script.py     # Selenium script for scraping trending topics
│   ├── requirements.txt       # Python dependencies
│   ├── trends.html            # Saved HTML file of the "For You" page (generated)
│   └── README.md              # Scraper-specific documentation (optional)
│
├── README.md                  # Project documentation
└── .gitignore                 # Git ignored files (e.g., node_modules, sensitive files)
```

## 📦 Installation & Usage

```bash
#1.Clone the Repository
git clone https://github.com/yourusername/ViralVista.git
cd ViralVista
#2.Backend Setup ()
cd backend
npm install
#Create a .env file in backend folder and copy the contents from .env.sample with your credentials in this file
node server.js
#3.Frontend Setup (ReactJS) (in separate terminal other than backend)
cd ../frontend
npm install
npm start
#4. Scraper Setup (Python + Selenium)
cd ../scrapper
pip install -r requirements.txt
#Create a .env file in scrapper folder and copy the contents from .env.sample with your credentials in this file

```

## 🧰 Technologies Used

- **🐍 Python**: Web scraping using Selenium and BeautifulSoup.
- **🌐 ProxyMesh**: Proxy provider for secure web scraping.
- **🍃 MongoDB Atlas**: Cloud database for persistent data storage.
- **🟢 Node.js + Express**: Backend API management.
- **⚛️ ReactJS**: Frontend framework for displaying trends.


## 🌟 Future Improvements

- 🔐 Replace username/password login with OAuth for better security.
- 📊 Include data visualization for trending topics on the frontend.
- 🚀 Deploy the application to cloud platforms like AWS, Heroku, or Vercel.
