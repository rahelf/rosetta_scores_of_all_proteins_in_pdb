import numpy as np
from operator import add
import sys
import cPickle

import matplotlib.pyplot as plt


class ResTypeAverageScores(object):


    def __init__( self, residue_type, score_term_list, pdb_identifier):
        self.res_type_all_score_dict = {}
        self.score_term_list = score_term_list
        st_counter = 1
        while st_counter < len( score_term_list):
            self.res_type_all_score_dict[score_term_list[st_counter]] = []
            st_counter += 1
        self.res_type = residue_type
        if( score_term_list == []):
            self.num_entries = 0
        else:
            self.num_entries = 1
        self.pdb_identifier_list = [pdb_identifier]
        #self.best_res = ResidueEnergies_instance.ResidueEnergies()(?)'''


    @classmethod
    def empty_init( cls, residue_type ):
        return cls( residue_type, [], [])


    def add_other_instance(self, other_instance):
        #1a. safety check whether other instance has same residue type
        if self.res_type != other_instance.res_type:
            sys.exit("ERROR in function add_other_instance: ResTypeAverageScores instance to be added has different residue_type!")
        #in case we got initialized empty we simply copy everything and return
        if self.num_entries == 0: #means we got initialized empty
            self.score_term_list = other_instance.score_term_list
            self.num_entries = other_instance.num_entries
            self.pdb_identifier_list = other_instance.pdb_identifier_list
            self.res_type_all_score_dict = other_instance.res_type_all_score_dict
            return
        #1b. safety check whether other instance has same score terms
        if self.score_term_list != other_instance.score_term_list:
            sys.exit("ERROR in function add_other_instance: ResTypeAverageScores_instance to be added has different score_term_list!")
        #2. add num_entries and append lists, also append pdb identifier 
        #= ResTypeAverageScores_instance
        self.num_entries += other_instance.num_entries
        #pdb-identifier should not be added more than once
        for i in range(len(other_instance.pdb_identifier_list)):
            if other_instance.pdb_identifier_list[i] in self.pdb_identifier_list:
                sys.exit('ERROR: pdb identifiers occur multiple times')
        self.pdb_identifier_list.extend(other_instance.pdb_identifier_list)

        for scoreterm in self.score_term_list[1:]:
            self.res_type_all_score_dict[scoreterm].extend(other_instance.res_type_all_score_dict[scoreterm])



    def add_residue_energies(self,  ResidueEnergies_instance):
        if self.res_type != ResidueEnergies_instance.get_res_type():
            sys.exit("ERROR in function add_residue_energies: score terms of ResidueEnergies_instance are added to wrong residue_type!")
        self.num_entries += 1
        #print "adding residue energies to %s" % self.res_type
        #print self.res_type_all_score_dict
        for score_term in self.res_type_all_score_dict.keys():
            self.res_type_all_score_dict[score_term].append( ResidueEnergies_instance.get_value(score_term) )
        #print "after adding"

    def get_mean_val(self, score_term):
        #print "starting mean val for %s and %s" %(self.res_type, score_term)
        #print self.res_type_all_score_dict
        return np.mean( self.res_type_all_score_dict[score_term] )

    def get_stddev(self, score_term):
        return np.std( self.res_type_all_score_dict[score_term] )

    def get_scores_for_scoreterm( self, score_term):
        return self.res_type_all_score_dict[score_term]

    def pickle_res_type_average_scores(self, filename):
        #self.filename = '../pickled-files/'+self.res_type+'.txt'
        pickle_file = open(filename, 'w')
        cPickle.dump(self, pickle_file)
        pickle_file.close()

    def make_histogram_for_scoreterm(self, score_term):
        data = self.res_type_all_score_dict[score_term]
        minx = int( np.floor(np.min(data)) )
        maxx = int( np.ceil(np.max(data)) )
        plt.hist( data, bins=int( (maxx - minx)/0.25), range=[minx, maxx], label=score_term, histtype='step' )
        plt.show()
        plt.savefig('test_single-histogram.pdf')