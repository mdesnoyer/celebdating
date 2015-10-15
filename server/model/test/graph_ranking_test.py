import numpy as np
import os.path
import sys
__base_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if sys.path[0] != __base_path__:
    sys.path.insert(0, __base_path__)
import unittest
import graph_ranking

class TestGraphRanking(unittest.TestCase):
    def setup(self):
        self.celebrities = [
            {
                'id' : 'c1',
                'gender' : 'M',
                'dated' : [
                    {
                        'id' : 'd1',
                        'data' : [0.1, 0.0, 0.2, 0.3, 0.4,
                                  0.5, 0.6, 0.7, 0.8, 0.9]
                    }
                ]
            },
            {
                'id' : 'c2',
                'gender' : 'M',
                'dated' : [
                    {
                        'id' : 'd2',
                        'data' : [0.2, 0.1, 0.0, 0.3, 0.4,
                                  0.5, 0.6, 0.7, 0.8, 0.9]
                    },
                    {
                        'id' : 'd3',
                        'data' : [0.3, 0.1, 0.2, 0.0, 0.4,
                                  0.5, 0.6, 0.7, 0.8, 0.9]
                    }
                ]
            },
            {
                'id' : 'c3',
                'gender' : 'M',
                'dated' : [
                    {
                        'id' : 'd4',
                        'data' : [0.4, 0.1, 0.2, 0.3, 0.0,
                                  0.5, 0.6, 0.7, 0.8, 0.9]
                    },
                    {
                        'id' : 'd5',
                        'data' : [0.5, 0.1, 0.2, 0.3, 0.4,
                                  0.0, 0.6, 0.7, 0.8, 0.9]
                    }
                ]
            }
        ]

    def test_load_data(self):
        self.setup()
        gr = graph_ranking.GraphRanking(self.celebrities)
        np.testing.assert_array_equal(gr.all_face_matrix,
            np.array([
                [0.1, 0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                [0.2, 0.1, 0.0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                [0.3, 0.1, 0.2, 0.0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                [0.4, 0.1, 0.2, 0.3, 0.0, 0.5, 0.6, 0.7, 0.8, 0.9],
                [0.5, 0.1, 0.2, 0.3, 0.4, 0.0, 0.6, 0.7, 0.8, 0.9],
            ]))

    def test_find_dating(self):
        self.setup()
        gr = graph_ranking.GraphRanking(self.celebrities)
        user_face_data = np.array([0.3, 0.1, 0.2, 0.0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        (celeb_id, dated_id) = gr.find_dating(user_face_data, 'M')
        self.assertEqual(celeb_id, 'c2')
        self.assertEqual(dated_id, 'd3')

def main():
    unittest.main()
