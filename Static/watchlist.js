const watchlistDiv = document.querySelector("#watchlist-list");

function showEmpty() {
    const message = document.createElement("div");
    message.className = "empty-message";
    message.textContent = "Your Watchlist Is Empty";
    watchlistDiv.append(message);
}

async function loadWatchList() {
    try {
        const response = await fetch("/watchlist");

        if (!response.ok) {
            throw new Error("Something went wrong");
        }

        const results = await response.json();

        if (results.length === 0) {
            showEmpty();
            return;
        }

        for (const item of results) {
            const card = document.createElement("div");
            card.className = "result-card";

            const title = document.createElement("span");
            title.className = "result-title";
            title.textContent = `${item.title} (${item.year})`;
            card.append(title);

            card.dataset.id = item.id;
            card.dataset.mediaType = item.media_type;
            card.dataset.tmdbId = item.tmdb_id;

            watchlistDiv.append(card);

            const removeButton = document.createElement("button");
            removeButton.textContent = "Remove";
            removeButton.className = "button remove-button";
            card.append(removeButton);

            removeButton.addEventListener("click", async () => {
                try {
                    const response = await fetch(`/watchlist/${item.id}`, {
                        method: "DELETE",
                    });

                    if (response.ok || response.status === 404) {
                        card.remove();
                        if (watchlistDiv.children.length === 0) {
                            showEmpty();
                        }
                    } else {
                        throw new Error("Could not remove item");
                    }
                } catch (error) {
                    console.error(error);
                    removeButton.textContent = "Error";
                }
            });
        }
    } catch (error) {
        console.error(error);
        watchlistDiv.textContent = "Could not load your watchlist.";
    }
}

loadWatchList();