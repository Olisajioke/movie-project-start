import requests

API_KEY = "8c98353eb7b5d60e810836a0735b7b80"
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4Yzk4MzUzZWI3YjVkNjBlODEwODM2YTA3MzViN2I4MCIsIm5iZiI6MTcyNzE3MzQxMC4xMjc4OTYsInN1YiI6IjY2ZjFjYTcxNmMzYjdhOGQ2NDhkZmI2OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.bKWtCAvUrvToWz2IJEsoVq2sfe6EqRyX_QIPYvyVaWc"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_TOKEN}",
}

class MovieApi:
    def __init__(self, movie):
        self.movie = movie
        self.data = self.get_movie()
        self.title = None
        self.overview = None
        self.release_date = None
        self.poster_path = None
        self.extract_movie_details()

    def get_movie(self):
        params = {
            'query': self.movie,
            'api_key': API_KEY
        }
        URL = 'https://api.themoviedb.org/3/search/movie'
        response = requests.get(URL, headers=headers, params=params)
        return response.json()

    def extract_movie_details(self):
        if 'results' in self.data and len(self.data['results']) > 0:
            movie_info = self.data['results'][0]
            self.title = movie_info.get('original_title')
            self.overview = movie_info.get('overview')
            self.release_date = movie_info.get('release_date')
            self.poster_path = movie_info.get('poster_path')
        else:
            print("No results found for the movie.")




class MovieList(MovieApi):
    def __init__(self, movie):
        super().__init__(movie)
        self.movie_list = []
        self.get_movie_list()

    def get_movie_list(self):
        if 'results' in self.data:
            for movie in self.data['results']:
                self.mov_list_date = (movie.get('original_title'), movie.get('release_date'), movie.get('id'))
                self.movie_list.append(self.mov_list_date)
        else:
            print("No results found for the movie.")

    def __str__(self):
        return f"Movies: {self.movie_list}"

    

class MovieId:
    def __init__(self, movie_id):
        self.movie_id = movie_id
        self.data = self.get_movie_id()

        try:
            self.title = self.data['original_title']
            self.overview = self.data['overview']
            self.release_date = self.data['release_date'].split('-')[0]
            self.poster_path = self.data['poster_path']
            self.myid = self.data['id']
        except Exception as e:
            print(e)

    def get_movie_id(self):
        url = f'https://api.themoviedb.org/3/movie/{self.movie_id}'
        headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json;charset=utf-8'
        }
        response = requests.get(url, headers=headers)
        return (response.json())
        



"""
    movie = MovieApi("Johnny English")
    print(movie.title)
    print(movie.overview)
    print(movie.release_date.split('-')[0])

"""