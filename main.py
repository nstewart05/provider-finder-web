from fastapi import FastAPI, HTTPException

from tmdbsearch import search, get_providers

from pydantic import BaseModel

from database import create_tables, add_to_watchlist, get_watchlist, remove_from_watchlist

app = FastAPI()

create_tables() #makes sure the tables exist


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

class WatchlistItem(BaseModel):
    tmdb_id: int
    media_type: str
    title: str
    year: str = ""


@app.post("/watchlist", status_code=201)
def save_to_watchlist(item: WatchlistItem):
    if item.media_type not in ("movie", "tv"):
        raise HTTPException(status_code=400, detail="media_type must be 'movie' or 'tv'")

    added = add_to_watchlist(item.tmdb_id, item.media_type, item.title, item.year)
    if not added:
        raise HTTPException(status_code=409, detail="Already in your watchlist")
    return {"message": "Added to watchlist"}


@app.get("/watchlist")
def list_watchlist():
    return get_watchlist()

#POST vs GET
# GET asks for data and the details travel in the address
#POST sends data to the server to be stored
# the details travel in the body of the request which is hidden from the address
#Saving a title is a change, so it's a POST.

@app.delete("/watchlist/{item_id}")
def delete_watchlist_item(item_id: int):
    removed = remove_from_watchlist(item_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Removed from watchlist"}