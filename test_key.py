import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("TMDB_API_KEY")

if key:
    print("Key loaded, length:", len(key))
else:
    print("Key not found")