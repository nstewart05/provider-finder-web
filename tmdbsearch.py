import os #this is standard for python, you use it to read environmental variables (environmental variables being variables taht exist outside of the code, for example the TMDB search key)
#the actual code sits in the .env file that is not visible to the rest of the public github
#the environmental variables keep it so the actual address of the api key never actually appears in the code
import requests
#this is a python library that makes it so web requests arent clunky
from dotenv import load_dotenv
#from the dotenv library, bring in the function called load_dotenv
#this specific line looks for the .env file to read the specific key
#this line stays for every api database

load_dotenv()
#this loads the dotenv
#Looks for a file named .env in your project folder.
#Reads each line in the form NAME=value.
#Adds each one to the program's environment, so os.getenv("NAME") can find it.
KEY = os.getenv("TMDB_API_KEY")
#this one works in conjunction with load_dotenv()
#this line changes based on the key specific name
BASE = "https://api.themoviedb.org/3"
#this one also changes based on the api name given, but base = and key = will remain the same

def search(title): #declaring the function and passing title as a parameter
    response = requests.get(
        #requests.get( means "use the get function from the requests library." It sends an HTTP GET request over the internet, the same kind your browser sends when you visit a page. The parentheses hold the details of the request, which is why the call stays open until the ) on the last line.
        #this line above rarely changes in future projects
        f"{BASE}/search/multi",
        #f in front converts it to a f string so everything in the {} will get replaced by BASE (the url)
        #/search/multi is plain text that will get added to the end
        #this line will change based on the api's address
        params={"api_key": KEY, "query": title},
        #params is a dictionary that holds api key and the title that you are searching for and adds it to the end of the request
        timeout=10,
        #how long it will wait until it cuts off the server from replying
    )
    response.raise_for_status()
    #checks whether response works
    #wont really change or have to be updated
    return response.json()["results"]
    #"results" would be the only real thing to change in future projects

def get_providers(media_type, tmdb_id, country="US"):
    response = requests.get(
        f"{BASE}/{media_type}/{tmdb_id}/watch/providers",
        params={"api_key": KEY},
        timeout=10,
    )
    response.raise_for_status()
    all_countries = response.json()["results"]
    return all_countries.get(country, {})
#Write down what the user does, step by step.
#Read the API docs and find which endpoints give you each piece of data.
#Note what each step needs as input and produces as output. Where an output feeds the next step, that's a handoff point.
#Write one small function per step, and test each one on its own before connecting them.

if __name__ == "__main__":
    title = input("Enter a movie or show: ") #standard input for python
    results = search(title) #calls the function and stores it in results

    shows = [] #starts with an empty list
    for item in results: #loops through every result
        if item["media_type"] in ("movie", "tv"): #filters out the people result that is given
            #if the shows type is movie or tv than it adds to the list of shows
            shows.append(item) #adds to the list in index item

    if not shows:
        print("No results found.") #to handle no results
    else:
        top = shows[:5]
        for number, item in enumerate(top, start=1): #this numbers all the choices
            name = item.get("title") or item.get("name")
            print(number, "-", item["media_type"], "-", name)

        choice = int(input("Pick a number: "))
        #this will be changed to an option where user clicks on later this is just for testing
        picked = top[choice - 1]

        country = input("Country code (e.g. US, GB, CA): ").strip().upper()
        providers = get_providers(picked["media_type"], picked["id"], country)

        for kind in ("flatrate", "free", "ads", "rent", "buy"): #makes the prints look pretty
            for provider in providers.get(kind, []):
                print(kind, "-", provider["provider_name"])