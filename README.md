# 🔴 Privacy Wrapped
### *Spotify Wrapped, but make it terrifying.*

> "You spend your days solving for x, but the algorithm already solved for **you**."

Privacy Wrapped is an open-source tool that takes your Instagram and Google data exports and generates a personalized, slightly savage AI report showing exactly what these platforms know about you.

**No server. No upload. Your data never leaves your machine.**
---
## 🔥 Live Demo

> Here's a real (slightly censored) report generated from actual Instagram + Google data:
> 
![Privacy Wrapped Demo](demo.png)
<img width="642" height="870" alt="Screenshot 2026-05-16 205257" src="https://github.com/user-attachments/assets/1c54f8e9-8298-462d-a96c-4b43a74c6327" />


---
### 👁️ PRIVACY WRAPPED: THE SEMI-SENTIENT EDITION

**📊 THE NUMBERS**
There are **5,881 companies** currently living inside your pocket. That is more than the entire student body of a major college — watching you brush your teeth. You can't even decide on a data plan without thousands of CEOs getting a notification about it. 🐜

**🧠 YOUR ALGORITHM PERSONALITY**
By day: a high-functioning logic machine sweating over Python tuples and complex algebraic expressions.
By night: the mask slips. The math stops. The thirst begins. 🎭

Instagram has you filed under:
- ✅ Engaged Shopper
- ✅ Relationship Status: Single
- ✅ Education: Associate/Bachelors Degree
- ✅ Potential mobile network change (they know before your bank does)

**🫧 THE INVISIBLE BUBBLE**
Because you're trapped in the feedback loop the algorithm built for you, here's what you're NOT being shown:
- Original thoughts outside your niche
- Content that might make you question your habits
- Silence. If we let you be bored, you might delete the app. We can't have that.

**🎯 THE PUNCHLINE**
The algorithm already solved for you — and it turns out you're just a predictable mix of algebra, cricket stats, and a very specific Bollywood crush. 💅

---

## ⚡ Get Your Own Report in 4 Steps

### Step 1 — Download Your Instagram Data
👉 [Click here to request your Instagram data](https://accountscenter.instagram.com/info_and_permissions/dyi/)
- Select: **Download to device**
- Format: **JSON**
- Takes: 1–48 hours to arrive in your email

### Step 2 — Download Your Google Data  
👉 [Click here to open Google Takeout](https://takeout.google.com)
- Deselect all → Select only **YouTube** and **My Activity**
- Format: **HTML**
- Takes: Usually under 1 hour

### Step 3 — Run the Tool
```bash
git clone https://github.com/YOUR_USERNAME/privacy-wrapped
cd privacy-wrapped
pip install -r requirements.txt
# Add your OpenRouter API key to .env
python parsers/instagram_parser.py
python parsers/google_parser.py
python parsers/combine.py
```

### Step 4 — See Your Report
Open `report/templates/report.html` in your browser and drag in `output/combined_data.json`

---

## 🛠️ How It Works

```
Your Instagram ZIP → BeautifulSoup Parser → Clean JSON
Your Google Takeout → Regex Line Parser  → Clean JSON
                                    ↓
                            Combined Profile
                                    ↓
                         OpenRouter AI (Free)
                                    ↓
                      Personalized Scary Report 🔥
```

---

## 📁 Project Structure

```
privacy-wrapped/
├── parsers/
│   ├── instagram_parser.py   # Parses Instagram HTML exports
│   ├── google_parser.py      # Parses Google Takeout data
│   └── combine.py            # Merges data + generates AI report
├── report/
│   └── templates/
│       └── report.html       # Dark UI, drag and drop
├── output/                   # Generated JSON and reports (gitignored)
├── data/                     # Your raw exports (gitignored)
├── .env.example              # Template for API key
├── requirements.txt
└── README.md
```

---

## 🔐 Privacy Note

This tool runs **entirely on your machine**. Your personal data files never leave your computer. The only external call is to OpenRouter's API to generate the report text — and even then, only anonymized insights (not raw data) are sent.

---

## 🧰 Tech Stack

- **Python** + **BeautifulSoup4** — HTML parsing
- **Regex** — Fast line-by-line parsing for large files (50MB+)
- **OpenRouter API** — Free AI report generation
- **python-dotenv** — Secret management
- **Pure HTML/CSS/JS** — Zero framework frontend

---

## 🗺️ Roadmap

- [x] Instagram parser
- [x] Google/YouTube parser
- [x] Industry categorizer (4,295+ advertisers)
- [x] AI report generator
- [x] Dark UI with drag and drop
- [ ] Spotify parser
- [ ] Twitter/X parser
- [ ] Flask web app for non-technical users
- [ ] One-click Vercel deploy
- [ ] Demo mode with sample data

---

## 🤝 Contributing

PRs welcome! Especially for:
- Adding more platform parsers (Spotify, Twitter, LinkedIn)
- Improving advertiser categorization for Indian brands
- UI improvements

---

## ⚠️ Disclaimer

This tool is for educational purposes to raise awareness about data privacy. All data processing happens locally on your machine.

---

*Built in one night out of curiosity and mild existential dread.* 🌙
