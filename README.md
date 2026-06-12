# AI News Summarizer

A Streamlit web application that get the latest news across multiple categories and uses Google's Gemini AI to generate synthesized overviews of current events.

## Features

- Browse news across multiple categories: Science, Finance, Politics, Sports, Technology, and more
- AI-generated topic overviews that synthesize themes across multiple articles
- Full-text article extraction using trafilatura for better summary quality
- Clean multipage Streamlit interface with one-click navigation

## Tech Stack

- **Frontend:** Streamlit
- **News data:** Currents News API
- **Article extraction:** trafilatura
- **AI summarization:** Google Gemini API
  (model gemini-2.5-flash-lite)

## Architecture

The app runs a simple linear pipeline that turns a topic click into a synthesized news briefing.

**Frontend (Streamlit)** — The user picks a category on the home page. Streamlit handles routing between pages, and the selected category is passed through `st.session_state`.

**Getting the news (Currents API)** — The category triggers a request to Currents API, which returns the 10 latest articles with their metadata and URLs.

**Content extraction (trafilatura)** — Each URL is fetched and cleaned by trafilatura, which strips ads, menus, and other boilerplate to leave only the article text. 

**AI synthesis (Gemini)** — All extracted texts are sent to Gemini in a single batched call. The prompt asks for cross-article themes rather than per-article summaries, producing a coherent 3-4 sentence overview.

**Presentation (Streamlit)** — The overview is rendered at the top of the page, with source links below for users who want to dig deeper.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A free Currents API key — https://currentsapi.services
- A free Google Gemini API key — https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-lite

### Installation

1. Clone the repository
```bash
git clone https://github.com/ivash12/news_with_ai.git
cd news_with_ai
```

2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
````

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API keys
CURRENTS_API_KEY=your_currents_key_here
GEMINI_API_KEY=your_gemini_key_here

5. Run the app
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## How it works
First, the user chooses the topic they want a news summary for.
Then trafilatura extracts the article texts from the URLs that the program received from the Currents API.
Finally, the Gemini model (gemini-2.5-flash-lite) summarizes all the texts into 3-4 sentences, and the summary along with the reference links is shown to the user via Streamlit.

## Author
https://github.com/ivash12

