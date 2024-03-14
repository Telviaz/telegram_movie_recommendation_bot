import os
import requests
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Import configuration from config.py
from . import config

# Dictionary to store user ratings
user_ratings = {}

# Function to handle /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to Movie/TV Show Recommendation Bot! You can ask for recommendations by genre, actors, directors, or titles. You can also search for a specific movie trailer using /trailer <movie_title>.")

# Function to handle /recommend command
def recommend(update: Update, context: CallbackContext) -> None:
    genre = context.args[0] if context.args else None
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={config.TMDB_API_KEY}&with_genres={genre}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        if results:
            # Select a random movie from the results
            selected_movie = results[0]
            title = selected_movie.get('title')
            movie_id = selected_movie.get('id')
            # Fetch additional details about the movie
            details_message = get_movie_details(movie_id)
            # Get trailer for the movie
            trailer_url = get_movie_trailer(title)
            update.message.reply_text(f"Recommendation for genre {genre}: \nTitle: {title}\n\n{details_message}\nTrailer: {trailer_url}", parse_mode=ParseMode.HTML)
        else:
            message = "Sorry, couldn't find any recommendations for the given genre."
            update.message.reply_text(message)
    else:
        message = "Failed to fetch recommendations. Please try again later."
        update.message.reply_text(message)

# Function to handle /search_actor command
def search_actor(update: Update, context: CallbackContext) -> None:
    actor_name = ' '.join(context.args)
    actor_id = search_person(actor_name)
    if actor_id:
        movies = get_movies_by_actor(actor_id)
        if movies:
            message = f"Movies featuring {actor_name}:\n"
            for movie in movies:
                message += f"- {movie}\n"
            update.message.reply_text(message)
        else:
            update.message.reply_text(f"No movies found featuring {actor_name}.")
    else:
        update.message.reply_text("Actor not found.")

# Function to handle /search_director command
def search_director(update: Update, context: CallbackContext) -> None:
    director_name = ' '.join(context.args)
    director_id = search_person(director_name)
    if director_id:
        movies = get_movies_by_director(director_id)
        if movies:
            message = f"Movies directed by {director_name}:\n"
            for movie in movies:
                message += f"- {movie}\n"
            update.message.reply_text(message)
        else:
            update.message.reply_text(f"No movies found directed by {director_name}.")
    else:
        update.message.reply_text("Director not found.")

# Function to search for person (actor/director)
def search_person(person_name):
    url = f"https://api.themoviedb.org/3/search/person?api_key={config.TMDB_API_KEY}&query={person_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        if results:
            return results[0].get('id')
    return None

# Function to get movies by actor
def get_movies_by_actor(actor_id):
    url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={config.TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        movies = [credit.get('title') for credit in data.get('cast', [])]
        return movies
    return []

# Function to get movies by director
def get_movies_by_director(director_id):
    url = f"https://api.themoviedb.org/3/person/{director_id}/movie_credits?api_key={config.TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        movies = [credit.get('title') for credit in data.get('crew', []) if credit.get('department') == 'Directing']
        return movies
    return []

# Function to get additional details about a movie
def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={config.TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        overview = data.get('overview')
        release_date = data.get('release_date')
        runtime = data.get('runtime')
        genres = ', '.join([genre.get('name') for genre in data.get('genres', [])])
        details_message = f"<b>Overview:</b> {overview}\n<b>Release Date:</b> {release_date}\n<b>Runtime:</b> {runtime} minutes\n<b>Genres:</b> {genres}"
        return details_message
    return ""

# Function to search for a movie trailer
def get_movie_trailer(movie_title):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={movie_title} trailer&key={config.YOUTUBE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        if items:
            video_id = items[0].get('id', {}).get('videoId')
            if video_id:
                return f"https://www.youtube.com/watch?v={video_id}"
    return None

# Function to handle /trailer command
def trailer(update: Update, context: CallbackContext) -> None:
    movie_title = ' '.join(context.args)
    trailer_url = get_movie_trailer(movie_title)
    if trailer_url:
        update.message.reply_text(f"Trailer for '{movie_title}': {trailer_url}")
    else:
        update.message.reply_text("Trailer not found.")

# Function to handle user ratings
def rate_movie(update: Update, context: CallbackContext) -> None:
    movie_title = ' '.join(context.args[:-1])
    rating = int(context.args[-1])
    user_id = update.message.from_user.id
    user_ratings.setdefault(user_id, {})
    user_ratings[user_id][movie_title] = rating
    update.message.reply_text(f"Thank you for rating {movie_title} as {rating} stars.")

# Function to handle /recommend_by_rating command
def recommend_by_rating(update: Update, context: CallbackContext) -> None:
    if user_ratings.get(update.message.from_user.id):
        rated_movies = user_ratings[update.message.from_user.id]
        top_rated_movie = max(rated_movies, key=rated_movies.get)
        update.message.reply_text(f"Based on your ratings, you might like: {top_rated_movie}")
    else:
        update.message.reply_text("You haven't rated any movies yet.")

# Function to handle text messages
def text_handler(update: Update, context: CallbackContext) -> None:
    message = update.message.text.lower()
    if message.startswith('/recommend'):
        # Extract genre from the message and recommend
        genre = message.split('recommend')[-1].strip()
        recommend(update, context)
    elif message.startswith('/search_actor'):
        # Extract actor name from the message and search for movies
        actor_name = message.split('search_actor')[-1].strip()
        search_actor(update, context)
    elif message.startswith('/search_director'):
        # Extract director name from the message and search for movies
        director_name = message.split('search_director')[-1].strip()
        search_director(update, context)
    elif message.startswith('/trailer'):
        # Extract movie title from the message and get trailer
        movie_title = message.split('trailer')[-1].strip()
        trailer(update, context)
    elif message.startswith('/rate'):
        # Extract movie title and rating from the message
        rate_movie(update, context)
    elif message.startswith('/recommend_by_rating'):
        # Recommend based on user ratings
        recommend_by_rating(update, context)
    else:
        update.message.reply_text("Sorry, I couldn't understand your request.")

# Main function
def main():
    updater = Updater(config.TELEGRAM_BOT_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    # Define handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("recommend", recommend))
    dispatcher.add_handler(CommandHandler("search_actor", search_actor))
    dispatcher.add_handler(CommandHandler("search_director", search_director))
    dispatcher.add_handler(CommandHandler("trailer", trailer))
    dispatcher.add_handler(CommandHandler("rate", rate_movie))
    dispatcher.add_handler(CommandHandler("recommend_by_rating", recommend_by_rating))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
