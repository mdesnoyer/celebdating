import numpy as np
from numpy.linalg import norm
from sets import Set

#_log = logging.getLogger(__name__)

# Data structure for celebrities and their dates.
#
class GraphRanking(object):
    def __init__(self, celebrities):
        self.celebrities = celebrities
        self.celeb_id_array = []
        self.dated_id_array = []
        self.celeb_gender_array = []
        all_face_array = []
        for celeb in self.celebrities:
            celeb_id = celeb["id"]
            celeb_gender = celeb["gender"]
            distance_dated = {}
            for dated in celeb["dated"]:
                dated_id = dated["id"]
                self.celeb_id_array.append(celeb_id)
                self.dated_id_array.append(dated_id)
                self.celeb_gender_array.append(celeb_gender)

                all_face_array.append(dated['data'])
        self.all_face_matrix = np.array(all_face_array)


    def get_distance(vector_1, vector_2):
        return norm(vector_1 - vector_2)

    def find_dating(self, user_face_data, user_prefer_gender):
        '''
        The user_face is a vector, we will search in the celebrities
        data and find the closest matching people group. We also want to
        make sure that we only consider the pairs where the distances are
        close enough.
        '''

        all_scores = np.inner(user_face_data, self.all_face_matrix)
        # Find which dated person is the most similar.

        # Get the sort indices in descending order
        sorted_score_indices = np.argsort(-all_scores)

        # Pick the highest maybe 20 stores, also the genders match
        num_picked = 20
        # Save the results into a set.
        top_dated_id_set = Set()
        count = 0
        for i in sorted_score_indices:
            if self.celeb_gender_array[i] != user_prefer_gender:
                continue
            count += 1
            top_dated_id_set.add(self.dated_id_array[i])
            if count == num_picked:
                break

        # Now we have the top num_picked of similar faces selected.
        # Note it can be duplicated faces, that's why we use a set.
        # For each of them, we want to get the average of similarity.
        max_similarity = 0
        for dated_id in top_dated_id_set:
            is_dated_id_array = np.array([x == dated_id for x in self.dated_id_array])
            avg_score = np.mean(all_scores[is_dated_id_array])
            print dated_id, is_dated_id_array, avg_score, all_scores[is_dated_id_array]
            if avg_score > max_similarity:
                max_similarity = avg_score
                max_dated_id = dated_id
        return max_dated_id


        # Initialize the data
        distance_measures = {}
        for celeb in self.celebrities:
            if celeb["gender"] != user_prefer_gender:
                continue
            celeb_id = celeb["id"]
            distance_dated = {}
            for dated in celeb["dated"]:
                dated_id = dated["id"]
                dated_face_vector = dated["vector"]
                distance_to_dated = get_distance(user_face_vector,
                                                 dated_face_vector)

                distance_dated[dated_id] = distance_to_dated

        # Calculate the ranking
        # The idea is to give it higher ratings for the closest matches.
        # So for the faces or people who don't look alike, they are not
        # to affect the matching results.
