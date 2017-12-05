"""This module will generate an HTML file of a movie list.
"""
import urllib2
import re
from media import Movie
from fresh_tomatoes import open_movies_page

# URL of the most played movies list of youku.
YOUKU_MOVIE_LIST_URL = "http://list.youku.com/category/show/c_96_s_1_d_2.html?spm=a2h1n.8251845.selectID.5!3~5~5!2~1~3!2~A"


class YoukuMovieExtractor(object):
    """Instances of this class can extract youku movies information from youku site.

    Parameters
    ---
    movies_count : int
        The max count of movies this `YoukuMovieExtractor` should process.
    """

    def __init__(self, movies_count):
        self.movies_count = movies_count

    def extract_most_played_movies(self):
        """Load and extract most played movies information from youku site.

        Returns
        ---
        [Movie]
            A list of `Movie` objects.
        """
        try:
            response = urllib2.urlopen(YOUKU_MOVIE_LIST_URL)
            html_content = response.read()
            return self._extract_movies(html_content)
        finally:
            response.close()

    def _extract_movies(self, html_content):
        """Extract movies information from the html content.

        Parameters
        ---
        html_content : string
            The HTML content fetched from the Internet.

        Returns
        ---
        [Movie]
            A list of `Movie` objects.
        """
        matched_html_contents = re.compile(
            '<div class="yk-pack pack-film"(.+?)</ul></div>',
            re.DOTALL).findall(html_content)
        if len(matched_html_contents) > self.movies_count:
            matched_html_contents = matched_html_contents[:self.movies_count]

        return [
            self._extract_movie(matched_html_content)
            for matched_html_content in matched_html_contents
        ]

    def _extract_movie(self, html_content):
        """Extract single movie information.

        Parameters
        ---
        html_content : string
            The HTML content fragment of one single movie information.

        Returns
        ---
        Movie
            A single `Movie` object.
        """
        # get title and trailer_url through regexp
        match = re.compile('<a href="([^"]+)" title="([^"]+)"',
                           re.DOTALL).search(html_content)
        if match:
            title = match.group(2)
            trailer_url = 'http:' + match.group(1)

        # get poster_image_url through regexp
        match = re.compile('<img.+?src="([^"]+)"',
                           re.DOTALL).search(html_content)
        if match:
            poster_image_url = match.group(1)

        movie = Movie(title, poster_image_url, trailer_url)
        return movie


def main():
    """Module main function.
    """
    extractor = YoukuMovieExtractor(12)
    open_movies_page(extractor.extract_most_played_movies())


if __name__ == "__main__":
    main()
