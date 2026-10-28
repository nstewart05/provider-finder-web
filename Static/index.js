/**async function fetchData(){ (framework/example from youtube)

    try{

        const pokemonName = document.getElementById("pokemonName").value.toLowerCase();
        const response = await fetch(`https://pokeapi.co/api/v2/pokemon/${pokemonName}`);

        if(!response.ok){
            throw new Error("Could not fetch resource");
        }

        const data = await response.json();
        const pokemonSprite = data.sprites.front_default;
        const imgElement = document.getElementById("pokemonSprite");

        imgElement.src = pokemonSprite;
        imgElement.style.display = "block";
    }
    catch(error){
        console.error(error);
    }
} */

//IDS from html
/*
search box id = "search-box"
label for country input is "country"
label for the input is "input-box"
search button is "search-button"
*/

const region_input = document.querySelector("#country");
const movie_input = document.querySelector("#input-box");
const search_result = document.querySelector("#results");
const select_button = document.querySelector("#search-button");

const availabilityLabels = {
    flatrate : "Subscription",
    free: "Available For Free",
    ads : "Available For Free With Ads",
    rent : "Available To Rent",
    buy : "Available For Purchase",
};

select_button.addEventListener("click", searchTitles);
movie_input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        searchTitles();
    }
});4


async function searchTitles() {
    try{
    
        const searchedMovie = movie_input.value.trim();
        if(!searchedMovie){ //checks if the movie string is empty
            return;
        }
        const response = await fetch(`/search?q=${encodeURIComponent(searchedMovie)}`);
        

        if(!response.ok){
            throw new Error("Could not fetch response");
        }

        const results = await response.json();

        search_result.replaceChildren(); //wipes old results
        
        if(results.length === 0){ //checks if results have anything in the array
            const card = document.createElement("div");   // 1. make an empty element
            card.textContent = "No results found :(";                   // 2. put text in it
            search_result.append(card);                   // 3. attach it to the page
            return;
        }

        for (const item of results.slice(0, 10)) {
            const card = document.createElement("div");
            card.className = "result-card";
            const title = document.createElement("span");           // new
            title.className = "result-title";                       // new
            title.textContent = `${item.title} (${item.year})`;     // new
            card.append(title);                                     // new

            card.dataset.id = item.id;
            card.dataset.mediaType = item.media_type;
            card.addEventListener("click", () => showAvailability(card));
            search_result.append(card);
            

            const watchlistButt = document.createElement("button");
            watchlistButt.textContent = "+ Watchlist";
            watchlistButt.className = "button add-watchlist-button";
            card.append(watchlistButt);
            
            watchlistButt.addEventListener("click", async (clickEvent) =>{
                try{
                    clickEvent.stopPropagation();
                    const response = await fetch("/watchlist", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            tmdb_id: item.id,
                            media_type: item.media_type,
                            title: item.title,
                            year: item.year,
                        }),
                    });
                    if(response.status === 201){
                        watchlistButt.disabled = true;
                        watchlistButt.textContent = "Saved";
                    }
                    else if(response.status === 409){
                        watchlistButt.textContent = "Already Saved";
                    }
                    else{
                        throw new Error("Something went wrong");
                    }
                }
                catch (error) {
                    console.error(error);
                    watchlistButt.textContent = "Error";
                }


            });
        }
    }
        catch(error){
            console.error(error);
            search_result.textContent = "Something went wrong, please try again."
        }
    


}

async function showAvailability(card){
    try{
        const oldBlock = card.querySelector(".availability");
        if (oldBlock) {
            oldBlock.remove();
            return;
        }
        const params = new URLSearchParams({
            media_type: card.dataset.mediaType,
            tmdb_id: card.dataset.id,
            country: region_input.value,
        });
        const response = await fetch(`/availability?${params}`);
        
        if(!response.ok){
            throw new Error("Could not find availability");
        }
        const results = await response.json();

        console.log(results);

        const block = document.createElement("div");
        block.className = "availability";

        for(const [category, names] of Object.entries(results.providers)){
            if(names.length === 0){
                continue;
            }
            const line = document.createElement("div");
            line.className = "availability-line";
            line.textContent = `${availabilityLabels[category]}: ${names.join(", ")}`;
            block.append(line);
        }

        if (block.children.length === 0) {
            block.textContent = "Not available to stream in this region.";
        }

        card.append(block);
    } catch (error) {
        console.error(error);
    }
}