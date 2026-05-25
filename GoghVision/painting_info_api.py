import requests

def fetch_summary_from_wikipedia(query):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "redirects": 1,
        "titles": query
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        pages = data.get("query", {}).get("pages", {})

        for page in pages.values():
            if "extract" in page and page["extract"].strip():
                return page["extract"].strip()
    except requests.RequestException:
        pass

    return None

def get_painting_summary(title, artist):
    # Normalize input
    title = title.strip()
    artist = artist.strip()
    title_words = title.split()
    partial_title = " ".join(title_words[:3]) if len(title_words) >= 3 else title

    queries = [
        f"{title} {artist}",
        f"{partial_title} {artist}",
        title,
        partial_title,
        artist
    ]

    for q in queries:
        summary = fetch_summary_from_wikipedia(q)
        if summary:
            return summary

    return "No reliable information found for this painting."
