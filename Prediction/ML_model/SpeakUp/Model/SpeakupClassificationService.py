
import numpy as np
import pickle

from .SpeakupImportGraph import ImportGraph

#Added by Meet Shah
import os
from django.conf import settings


class ClassificationService_speakup:
    def __init__(self):
        # '../dataset/speakup/speakup_category_index_dictionary_700_clean.pickle'
        print (settings.BASE_DIR)
        with open(settings.BASE_DIR+ "/Prediction/ML_model/SpeakUp/dataset/speakup/speakup_category_index_dictionary_700_clean.pickle",'rb') as f:
            self.index_complaint_title_map_r = pickle.load(f)

        self.index_complaint_title_map = {}

        for cat in self.index_complaint_title_map_r.keys():

            self.index_complaint_title_map[(self.index_complaint_title_map_r[cat])] = cat

        self.g0 = ImportGraph.get_instance()

    def get_probs_graph(self,model_id, data):
        if model_id == 0:
            model = self.g0


        data = model.process_query(data)
        return model.run(data)

    def get_top_3_cats_with_prob(self,data):
        prob1 = self.get_probs_graph(0, data)




        final_prob = prob1[0] #+ prob2 + prob3 + prob4 + prob5 + prob6 + prob7

        final_sorted = np.argsort(final_prob)

        final_categories = []
        final_probability = []
        # , float(final_prob[final_sorted[-3:][2-i]]/7)
        for i in range(3):
            final_categories.append(self.index_complaint_title_map[final_sorted[-3:][2 - i]])
            final_probability.append(float(final_prob[final_sorted[-3:][2 - i]]))

        result = {}

        for i in range(len(final_categories)):
            result[final_categories[i]] = final_probability[i]
        return result

'''
cs = ClassificationService()

while True:
    input = input('Enter Complaint Text:')
    # "DRAINAGE LINE COMING TO OUR PREMISES IS CHOCKED AND WATER HAS STARTED ACCUMULATING IN THE CHAMBER IN OUR NEIGHBOURS PLOT. THIS IS DUE TO THE BLOCKAGE"
    result = cs.get_top_3_cats_with_prob(input)
    print ("\n\n")

    print (result)

    print ("\n\n")
'''