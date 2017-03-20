# coding=UTF-8

import random
from common import utils, defines, path_define

class similar_class_crime:
    def __init__(self):
        crime_class = [utils.load_pyobj(path_define.CASE_INDIV_CLASS_DIR + criminal_name + '.pkl') for criminal_name in defines.crime_list]
        self.similar_crime_list = []
        for i in defines.confused_crime.keys():
            similar_crime_indiv_class = crime_class[i]
            for sim_class_index in defines.confused_crime[i]:
                similar_crime_indiv_class += crime_class[sim_class_index]
            self.similar_crime_list.append(similar_crime_indiv_class)

    def random_get_similar_cases(self, crime_index, cases_num):
        if crime_index not in defines.confused_crime.keys():
            return []
        if cases_num > len(self.similar_crime_list[crime_index]):
            return self.similar_crime_list[crime_index]
        slice = random.sample(self.similar_crime_list[crime_index], cases_num)
        return slice