# !/usr/bin/python

import csv
from collections import defaultdict
from math import sqrt
import sys
import time

new_data_dict = {}
with open('/home/dheeraj/python/rec_sys/movie_rating.csv', 'r') as data_file:
	data_file.next()
	for row in data_file:
		row = row.strip().split(",")
		new_data_dict.setdefault(row[0], {})[row[1]] = int(row[2])
		

# calculating similarity score using euclidean distance
def euc_similarity(data, user1, user2):
	similar_items = {}
	for item in data[user1]:
		if item in data[user2]:
			similar_items[item] = 1
	if len(similar_items) == 0:
		return 0

	sum_of_square = sum([pow(data[user1][item] - data[user2][item], 2) for item in data[user1] if item in data[user2]])
	return (1./(1 + sum_of_square))

def pearson_similarity(data, user1, user2):
	similar_items = {}
	for item in data[user1]:
		if item in data[user2]:
			similar_items[item] = 1
	n = len(similar_items)
	if n == 0:
		return 0

	#Adding ratings
	sum_user1 = sum([data[user1][item] for item in similar_items])
	sum_user2 = sum([data[user2][item] for item in similar_items])

	#Adding square of ratings
	sum_square_user1 = sum([pow(data[user1][item], 2) for item in similar_items])
	sum_square_user2 = sum([pow(data[user2][item], 2) for item in similar_items])

	#Adding product
	sum_product = sum([data[user1][item] * data[user2][item] for item in similar_items])

	#calculating pearson coefficient
	out = sum_product - (sum_user1*sum_user2/n)
	den = sqrt((sum_square_user1-pow(sum_user1, 2)/n)*(sum_square_user2-pow(sum_user2, 2)/n))
	if den == 0:
		return 0
	r = out/den
	return r

def similar_person(data, user, n, similarity_method):
	out = [(similarity_method(data, user, other), other) for other in data if other != user]
	out.sort()
	out.reverse()
	return out[0:n]

def recommend_movie(data, user, n, similarity_method):
	totals = {}
	similarity_sum = {}
	for other in data:
		if other == user:
			continue
		sim = similarity_method(data, user, other)
		if sim <= 0:
			continue
		for item in data[other]:
			if item not in data[user] or data[user][item] == 0:
				totals.setdefault(item, 0)
				totals[item] += data[other][item]*sim
				similarity_sum.setdefault(item, 0)
				similarity_sum[item] += sim
	ranking = [(total/similarity_sum[item], item) for item, total in totals.items()]
	ranking.sort()
	ranking.reverse()
	return ranking[0:n]

if __name__ == "__main__":
	user = input('Recommendation for which user? Type user id between 1 and 943: \n')
	recommendations = input('How many recommendations you want to see ? \n')
	similarity_name = input('Which similarity method you want to use: ' + 'pearson_similarity ' + 'or euc_similarity ? \n' )
	print '\n'
	print 'Searching top recommended movies for you....\n'
	time.sleep(5)
	print recommend_movie(new_data_dict, str(user), int(recommendations), similarity_name)