from fastapi import FastAPI, HTTPException

from tmdbsearch import search, get_providers

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Provider finder is running"}


@app.get("/search")
def search_titles(q: str):
    if not q.strip():
        return []

    results = search(q)

    shows = []
    for item in results:
        if item["media_type"] in ("movie", "tv"):
            year = item.get("release_date") or item.get("first_air_date") or ""
            shows.append({
                "id": item["id"],
                "media_type": item["media_type"],
                "title": item.get("title") or item.get("name"),
                "year": year[:4],
            })
    return shows


@app.get("/availability")
def availability(media_type: str, tmdb_id: int, country: str = "US"):
    if media_type not in ("movie", "tv"):
        raise HTTPException(status_code=400, detail="media_type must be 'movie' or 'tv'")

    country = country.strip().upper()
    providers = get_providers(media_type, tmdb_id, country)

    cleaned = {}
    for kind in ("flatrate", "free", "ads", "rent", "buy"):
        names = []
        for provider in providers.get(kind, []):
            names.append(provider["provider_name"])
        cleaned[kind] = names

    return {"country": country, "providers": cleaned}