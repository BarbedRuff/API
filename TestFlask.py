import unittest
import requests as r
from main import app

class TestCase(unittest.TestCase):
    def testAddMovie(self):
        MovieAdded = {
            "movie": {
                "id": 1,
                "title": "Врата Штейна",
                "year": 2011,
                "director": "Ханада, Дзюкки, Масахиро Ёкотани",
                "length": "10:25:00",
                "rating": 10
            }
        }
        resp = r.post(
            url='http://127.0.0.1:5000/api/movies',
            json=MovieAdded 
        )
        self.assertEqual(resp.status_code, 200)
        
    def testGetAllMovies(self):
        resp = r.get(url='http://127.0.0.1:5000/api/movies')
        self.assertEqual(resp.status_code, 200)
        
    def testGetMovieById(self):
        resp = r.get('http://127.0.0.1:5000/api/movies/96001425261386344404583071092676138855')
        self.assertEqual(resp.status_code, 200)
        
    def testPatchMovieById(self):
        MoviePatched = {
            "movie": {
                "id": 1,
                "title": "Врата Штейна 0",
                "year": 2011,
                "director": "Ханада, Дзюкки, Масахиро Ёкотани",
                "length": "10:25:00",
                "rating": 10
            }
        }
        resp = r.patch(
            'http://127.0.0.1:5000/api/movies/96001425261386344404583071092676138855',
            json=MoviePatched 
        )
        self.assertEqual(resp.status_code, 200)
        
    def testDeleteMovieById(self):
        resp = r.delete(
            'http://127.0.0.1:5000/api/movies/188615737011347594891100218072374438236',
        )
        self.assertEqual(resp.status_code, 200)
        
            
if __name__ == '__main__':
    unittest.main()