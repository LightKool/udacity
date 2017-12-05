"""This module contains classes represents our movie data structure.
"""


class Movie(object):
    """Movie structure.

    Parameters
    ---
    title : string
        The title of the movie.
    poster_image_url : string
        The URL of the poster image of the movie.
    trailer_url : string
        The URL of the trailer page of the movie.
    """

    def __init__(self, title, poster_image_url, trailer_url):
        self.title = title
        self.poster_image_url = poster_image_url
        self.trailer_url = trailer_url
