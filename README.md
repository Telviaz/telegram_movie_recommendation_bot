# Telegram Movie/TV Show Recommendation Bot

The Telegram Movie/TV Show Recommendation Bot is a chatbot designed to provide users with recommendations for movies and TV shows based on various criteria such as genre, actors, directors, or titles. It integrates with The Movie Database (TMDb) API to fetch movie data and YouTube API to fetch movie trailers.



## Features

- **Recommendations**: Get personalized movie and TV show recommendations based on genre.
- **Search by Actors and Directors**: Discover movies featuring your favorite actors and directors.
- **Movie Trailers**: Watch trailers for specific movies.
- **User Ratings**: Rate movies and receive recommendations based on your ratings.

## Setup Instructions

1. **Clone the Repository**: Clone this repository to your local machine using `git clone`.
2. **Install Dependencies**: Install the required Python dependencies using `pip install -r requirements.txt`.
3. **Set Up Configuration**: Open the `bot/config.py` file and replace the placeholder values for `TELEGRAM_BOT_TOKEN`, `TMDB_API_KEY`, and `YOUTUBE_API_KEY` with your actual API keys.
4. **Run the Bot**: Start the bot by running `python bot/bot.py`.
5. **Interact with the Bot**: Chat with the bot on Telegram by searching for its username or using its link.

## Commands

- `/start`: Start the bot and view welcome message.
- `/recommend <genre>`: Get movie recommendations based on the specified genre.
- `/search_actor <actor_name>`: Find movies featuring a specific actor.
- `/search_director <director_name>`: Find movies directed by a specific director.
- `/trailer <movie_title>`: Watch the trailer for a specific movie.
- `/rate <movie_title> <rating>`: Rate a movie (out of 5 stars).
- `/recommend_by_rating`: Get recommendations based on your ratings.

## Project Structure

telegram_movie_recommendation_bot/
│
├── bot/
│   ├── __init__.py
│   ├── bot.py
│   └── config.py
│
├── data/
│   └── ratings.json
│
├── requirements.txt
│
└── README.md

## Dependencies

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot): Python wrapper for the Telegram Bot API.
- [requests](https://pypi.org/project/requests/): HTTP library for making requests to APIs.
- [tmdbv3api](https://pypi.org/project/tmdbv3api/): Python wrapper for TMDb API v3.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request to suggest features, report bugs, or improve the code.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
