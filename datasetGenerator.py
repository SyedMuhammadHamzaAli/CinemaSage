"""
This code is responsible to extracting and combining data of movies from the 
CMU Movies Summary Corpus link: https://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz
into a single csv file 
"""

import csv

txt_file = "plot_summaries.txt"
movie_file = "movie.metadata.tsv"
cast_file = "character.metadata.tsv"
output = "summaries.csv"

names = {}  # Dictionary to store movie ID (key) and name of that movie (value)
actors = {}  # Dictionary to store movie ID (key) and list of actors (value)
characters = {}  # Dictionary to store movie ID (key) and list of characters (value)
genres = {}  # Dictionary to store movie ID (key) and list of genres (value)

# Read movie names and cast information
with open(movie_file, "r", encoding="utf-8") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    for row in tsvreader:
        movie_id = row[0]
        names[movie_id] = row[2]
        genre_dict = eval(row[8])
        genres[movie_id] = list(genre_dict.values())

with open(cast_file, "r", encoding="utf-8") as castfile:
    castreader = csv.reader(castfile, delimiter="\t")
    for row in castreader:
        movie_id = row[0]
        character = row[3].strip() if row[4] else "NotFound"  # Handle missing character names
        actor = row[8].strip() if row[8] else "NotFound"  # Handle missing actor names

        if movie_id not in actors:
            actors[movie_id] = []
        if movie_id not in characters:
            characters[movie_id] = []

        if actor:
            actors[movie_id].append(actor)
        if character:
            characters[movie_id].append(character)

# Process text file and write to CSV
with open(txt_file, "r", encoding="utf-8") as txtfile, open( output, "w", newline="", encoding="utf-8" ) as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header row
    csvwriter.writerow(["ID", "Name", "Genres", "Actors", "Characters", "Summary"])

    # Iterate through each line in the text file
    for line in txtfile:
        items = line.strip().split(None, 1)

        # Check if line can be split into at least two parts
        if len(items) > 1:
            id, data = items[0], items[1]
            name = names.get(id)  # Get movie name based on ID

            # Get actors and characters lists (empty lists if not found)
            actor_list = actors.get(id, [])  # Use get() with default [] for missing IDs
            character_list = characters.get(id, [])
            genres_string = ", ".join(genres.get(id, []))  # Use get() with default [] for missing IDs

            # Write data into output file
            csvwriter.writerow(
                [id, name, genres_string, actor_list, character_list, data]
            )

        else:
            print("Error: ID or Data are not separable")
            continue  # Skip to the next iteration if line is not separable