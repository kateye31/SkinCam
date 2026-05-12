# 🌿 SkinCam — AI Skincare Analysis App

SkinCam is a full-stack web application that uses AI-powered image analysis to evaluate a user's skin and provide personalized skincare recommendations. Built with Python, Flask, the Anthropic API (Claude), and Supabase.

---

## Features

- 📸 **Skin scan analysis** — Upload a photo and receive an AI-generated breakdown of your skin's condition
- 🧴 **Personalized recommendations** — Get product and routine suggestions tailored to your skin type and concerns
- 🗂️ **Scan history tracking** — All past scans are saved per user via Supabase so you can track changes over time
- 🤖 **Consistent AI output** — Structured JSON prompts ensure reliable, parseable responses from the Claude Vision API

---

## Tech Stack


Backend | Python, Flask 
AI / Vision | Anthropic API (Claude) 
Database | Supabase (PostgreSQL) 
Auth | Supabase Auth 
Frontend | HTML, CSS, JavaScript 

---

## Getting Started

### Prerequisites

- Python 3.9+
- A [Supabase](https://supabase.com) project
- An [Anthropic API key](https://console.anthropic.com)

### Installation

```bash
# Clone the repo
git clone https://github.com/jahmee06/skincam.git
cd skincam

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### Run the App

```bash
flask run
```

Visit `http://localhost:5000` in your browser.

---

## Project Structure

```
skincam/
├── app.py              # Flask app entry point
├── routes/             # Route handlers
├── templates/          # HTML templates
├── static/             # CSS, JS, assets
├── .env                # Environment variables (not committed)
└── requirements.txt
```

---

## How It Works

1. User uploads a photo of their skin
2. The image is sent to the Claude Vision API with a structured JSON prompt
3. Claude returns a categorized analysis (skin type, concerns, severity)
4. Results and recommendations are displayed to the user
5. The scan is saved to Supabase and added to the user's history

---

## Status

🚧 **In Progress** — Core analysis and necessary features are functional. Additional features (progress tracking, product database, comparison view) are actively being developed.

---

## Author

**Jahmeelay Germinal**
[GitHub](https://github.com/jahmee06) · [LinkedIn](https://linkedin.com/in/jahmeelay-germinal-176220387)
