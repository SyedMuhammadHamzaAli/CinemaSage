import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import ast
import string


def download_stopwords():
    """
    Downloads stopwords and tokenizer from NLTK if not already present.
    """

    try:
        nltk.data.find('corpora/stopwords')
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('stopwords')
        nltk.download('punkt')


def preprocessing(df):
    """
    Preprocesses a pandas dataframe containing movie data.
    Args:
        df (pandas.DataFrame): The dataframe to preprocess.
    Returns:
        pandas.DataFrame: The preprocessed dataframe.
    """

    download_stopwords()

    stop_words = stopwords.words('english')
    punc = string.punctuation

    def actors_characters(actors, characters):
        """
        Processes the 'Actors' and 'Characters' columns, ensuring consistent list lengths.
        Args:
            actors (str): A string containing comma-separated actor names (potentially with quotes).
            characters (str): A string containing comma-separated character names (potentially with quotes).
        Returns:
            tuple: A tuple containing two lists: processed actors and characters.
        """

        actors = ast.literal_eval(actors)  # Convert string to list in actors column
        characters = ast.literal_eval(characters)  # Convert string to list in characters column

        diff = len(actors) - len(characters)  # Calculate the difference in list lengths

        # Adjust the shorter list by adding "NotFound" entries
        if diff > 0:
            characters.extend(["NotFound"] * diff)
        elif diff < 0:
            actors.extend(["NotFound"] * abs(diff))

        return actors, characters

    def clean_summary(text):
        """
        Cleans a text summary.
        Args:
            text (str): The text summary to clean.
        Returns:
            str: The cleaned text summary.
        """

        text = text.lower()  # Convert to lowercase
        text = text.replace("{{plot}}", "")  # Remove {{plot}} keyword if it exists
        tokens = word_tokenize(text)  # Tokenization
        filtered = [word for word in tokens if word not in stop_words and word not in punc]  # Remove stopwords and punctuations
        return ' '.join(filtered)  # Join the filtered words back into a single string

    # Apply the above two functions
    df[["Actors", "Characters"]] = df.apply(lambda row: actors_characters(row["Actors"], row["Characters"]), axis=1, result_type="expand")
    df["Summary"] = df["Summary"].apply(clean_summary)
    return df


df = pd.read_csv('summaries.csv')
df = preprocessing(df)
df.to_csv('processed_summaries.csv', index=False, encoding='utf8')
