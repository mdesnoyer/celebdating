import numpy as np
from numpy.linalg import norm
from sets import Set
import _mysql

#_log = logging.getLogger(__name__)

# Data structure for celebrities and their dates.
#
class GraphRanking(object):
    def __init__(self, host, port, db_name, username, password, celebrity_model_file):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password
        self.celebrity_model_file = celebrity_model_file
        print "loading data..."
        self.celebrities = celebrities
        self.celeb_id_array = []
        self.dated_id_array = []
        self.celeb_gender_array = []
        all_face_array = []

        self.load_celebrity_model_file()

        try:
            # con = _mysql.connect('dateaceleb.cnvazyzlgq2v.us-east-1.rds.amazonaws.com',
            #                      'admin', 'admin123', 'celebs')
            con = mysql.connect(self.host, self.username, self.password, self.db_name)
            con.query('''SELECT celebrities.celebrity_id, celebrities.gender, dated.dated_id
                            FROM celebrities
                            INNER JOIN dated
                            ON celebrities.celebrity_id=dated.celebrity_id;''')
            result = con.user_result()

            all_face_array = []
            for (celeb_id, celeb_gender, dated_id) in result:
                self.celeb_id_array.append(celeb_id)
                self.dated_id_array.append(dated_id)
                self.celeb_gender_array.append(celeb_gender)
                all_face_array.append(self.dated_data[dated_id])

            # for celeb in self.celebrities:
            #     celeb_id = celeb["id"]
            #     celeb_gender = celeb["gender"]
            #     for dated in celeb["dated"]:
            #         dated_id = dated["id"]
            #         self.celeb_id_array.append(celeb_id)
            #         self.dated_id_array.append(dated_id)
            #         self.celeb_gender_array.append(celeb_gender)
            #
            #         all_face_array.append(dated['data'])

            self.all_face_matrix = np.array(all_face_array)

        except _mysql.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            if  con:
                con.close()
        print "Data loaded."

    def load_celebrity_model_file(self):
        face_data = np.load(self.celebrity_model_file)
        face_names = face.data.keys()
        self.dated_data = {}
        try:
            con = mysql.connect(self.host, self.username, self.password, self.db_name)
            q_string = '''SELECT dated_id
                            FROM dated
                            WHERE name IN {0};'''
            query_string = q_string.format(', '.join(face_names))
            con.query(query_string)
            result = con.user_result()

            for dated_id, face_name in zip(result, face_names):
                self.dated_data[dated_id] = face_data[face_name]
        except _mysql.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            if  con:
                con.close()



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
            is_dated_id_array = \
                np.array([x == dated_id for x in self.dated_id_array])
            avg_score = np.mean(all_scores[is_dated_id_array])
            if avg_score > max_similarity:
                max_similarity = avg_score
                max_dated_id = dated_id

        # Find the celebraty by dated_id
        for i, dated_id in enumerate(self.dated_id_array):
            if dated_id == max_dated_id:
                return self.celeb_id_array[i], max_dated_id
