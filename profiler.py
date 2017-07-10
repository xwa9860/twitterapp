from twitterapp.services import topic
import pickle
import re


import cProfile, pstats
pr = cProfile.Profile()
pr.enable()
topic.data_set()
pr.disable()
sortby = 'cumulative'
stream = open('profiler_output', 'w');
stats = pstats.Stats(pr, stream=stream).sort_stats(sortby)
stats.print_stats()

#with open('data', 'rb') as data_file:
#    data = pickle.load(data_file)
#topic.model(data)
