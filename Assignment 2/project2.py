############################################################
## project2.py - Code template for Project 2 - Normalization 
## Both for CS5421 and CS4221 students 
############################################################


### IMPORTANT! Change this to your metric number for grading
student_no = 'A0105505U' 

from itertools import chain, combinations, permutations, product
from collections import defaultdict

def get_derived_attributes(S, fds):
	derived_attr = set()
	input_attr = set(S)
	for fd in fds:
		if fd[0] == input_attr:
			derived_attr.update(fd[1])
			fds.remove(fd)
	return derived_attr, fds

def all_subsets(S):
	tuples = chain.from_iterable(combinations(S, r) for r in range(len(S)+1))
	result = []
	for a_tuple in tuples:
		result.append(set(a_tuple))
	return result

# remove trival fds
def reduce_fds(F):
	fds = []
	for fd in F:
		left = set(fd[0])
		right = set(fd[1])
		interc = left.intersection(right)
		if interc != right:
			fds.append([left, right-interc])
	return fds

## Determine the closure of set of attribute S given the schema R and functional dependency F
def closure(R, F, S):
	# initialize the closure as S
	closure = set()
	closure.update(S)
	fds = reduce_fds(F)
	while True:
		subsets = all_subsets(closure)
		closure_len_prev = len(closure)
		for subset in subsets:
			if len(F) > 0:
				derived_attr, fds = get_derived_attributes(subset, fds)
				closure.update(derived_attr)
		if len(closure) == closure_len_prev:
			break
	return sorted(closure)

def is_super_key(key, candidate_keys):
	for current_key in candidate_keys:
		if key >= current_key:
			return True
	return False

## Determine the all the attribute closure excluding superkeys that are not candidate keys given the schema R and functional dependency F
def all_closures(R, F): 
	schema = set(R)
	all_closures = []
	keys = []
	for subset in all_subsets(R):
		if len(subset) > 0:
			subset_closure = closure(R, F, subset)
			if set(subset_closure) == schema:
				if not is_super_key(subset, keys):
					keys.append(subset)
					all_closures.append([list(subset), subset_closure])
			else:
				all_closures.append([list(subset), subset_closure])
	return all_closures

## Return the candidate keys of a given schema R and functional dependencies F.
## NOTE: This function is not graded for CS5421 students.
def candidate_keys(R, F): 
	schema = set(R)
	keys = []
	for attr_closure in all_closures(R, F):
		if set(attr_closure[1]) == schema:
			keys.append(attr_closure[0])
	return keys

def rhs_to_singlton(fds):
	new_fds = []
	for fd in fds:
		for attr in fd[1]:
			new_fds.append([fd[0], set([attr])])
	return new_fds

def all_closures_to_dict(all_closures):
	all_closure_dict = {}
	for attr_closure in all_closures:
		all_closure_dict[frozenset(attr_closure[0])] = set(attr_closure[1])
	return all_closure_dict

def covers_original_fds(original_fds, fds):
	for original_fd in original_fds:
		if not set(closure([],fds,original_fd[0])).issuperset(original_fd[1]):
			return False
	return True

def is_reachable(fds, attrs_left, attrs_right):
	return closure([], fds, attrs_left) > set(attrs_right)

def is_subset_a_key(fds, subset, target_set):
	return set(closure([], fds, subset)) >= target_set

def lhs_reduced_subsets(fds, attr_list):
	result = []
	target_set = set(attr_list)
	for subset in all_subsets(attr_list):
		if not is_super_key(subset, result) and is_subset_a_key(fds, subset, target_set):
			result.append(subset)
	return result
    
## Return a minimal cover of the functional dependencies of a given schema R and functional dependencies F.
def min_cover(R, FD): 
	# reference: https://www.inf.usi.ch/faculty/soule/teaching/2014-spring/cover.pdf
	# fds = reduce_fds(FD)
	# print "fds: ", fds
	# while True:
	# 	# union simplificaiton
	# 	unioned, fds = union_fds(fds)
	# 	# simplify left and right side
	# 	simplied, fds = simplify_fd(fds)
	# 	if not unioned and not simplied:
	# 		break 
	# print fds

	# create 
	fds = reduce_fds(FD)
	# 

	# from notes
	return []

## Return all minimal covers reachable from the functional dependencies of a given schema R and functional dependencies F.
## NOTE: This function is not graded for CS4221 students.
def min_covers(R, FD):
	# remove all trivial dependencies 
	fds = reduce_fds(FD)
	# transform to singltons
	fds = rhs_to_singlton(fds)
	# reduce left side
	lhs_reduced_serialized_fds = set()
	for fd in fds:
		left_serialized_options = set()
		lhs_subsets = lhs_reduced_subsets(fds, list(fd[0]))
		for left in lhs_subsets:
			lhs_reduced_serialized_fds.add(','.join(sorted(left))+'-'+','.join(sorted(fd[1])))
	
	print lhs_reduced_serialized_fds

	all_min_covers = []
	for serialized_cover in all_subsets(lhs_reduced_serialized_fds):
		# print serialized_cover
		cover = []
		for serialized_fd in serialized_cover:
			left = set(serialized_fd.split('-')[0].split(','))
			right = set(serialized_fd.split('-')[1].split(','))
			cover.append([left, right]) 
		print 'all_min_covers', all_min_covers
		if not is_super_key(serialized_cover, all_min_covers) and covers_original_fds(fds, cover):
			all_min_covers.append(serialized_cover)
	print all_min_covers
	return []

def all_fds(all_closures):
	all_serialized_fds = set()

	for all_closure in all_closures:
		left = all_closure[0]
		right = []
		for subset in all_subsets(all_closure[1]):
			if not set(left).issuperset(subset):
				all_serialized_fds.add(','.join(sorted(left))+'-'+','.join(sorted(subset)))
	all_fds = []
	for serialized_fd in all_serialized_fds:
		left = set(serialized_fd.split('-')[0].split(','))
		right = set(serialized_fd.split('-')[1].split(','))
		all_fds.append([left, right]) 
	return all_fds

def reduce_closures(all_closures):
	closures = []
	length = len(all_closures)
	for i in range(length):
		remove = False
		closure_i = all_closures[i]
		for j in range(length):
			closure_j = all_closures[j]
			if i!=j and set(closure_i[0]).issuperset(set(closure_j[0])) and set(closure_i[0]).issubset(set(closure_j[1])):
				remove = True
		if not remove and set(closure_i[0]) < set(closure_i[1]) :
			closures.append([closure_i[0], list(set(closure_i[1])-set(closure_i[0]))])
	return closures


## Return all minimal covers of a given schema R and functional dependencies F.
## NOTE: This function is not graded for CS4221 students.
def all_min_covers(R, FD):
	my_all_closures = all_closures(R, FD)
	my_reduced_closures = reduce_closures(my_all_closures)
	my_all_fds = all_fds(my_reduced_closures)
	# print my_all_fds
	min_covers(R, my_all_fds)
	return []

### Test case from the project
R = ['A', 'B', 'C', 'D']
FD = [[['A', 'B'], ['C']], [['C'], ['D']]]

# print closure(R, FD, ['A'])
# print closure(R, FD, ['A', 'B'])
# print all_closures(R, FD)
# print candidate_keys(R, FD)

R = ['A', 'B', 'C', 'D', 'E', 'F']
FD = [[['A'], ['B', 'C']],[['B'], ['C','D']], [['D'], ['B']],[['A','B','E'], ['F']]]
# print min_cover(R, FD) 

R = ['A', 'B', 'C']
FD = [[['A', 'B'], ['C']],[['A'], ['B']], [['B'], ['A']]] 
# print min_covers(R, FD) 
# print all_min_covers(R, FD) 

## Tutorial questions
R = ['A', 'B', 'C', 'D', 'E']
FD = [[['A', 'B'],['C']], [['A'],['B']], [['D'],['D', 'B']], [['B'],['E']], [['E'],['D']], [['A', 'B', 'D'],['A', 'B', 'C', 'D']]]

# print candidate_keys(R, FD)
# print min_cover(R, FD)
# print min_covers(R, FD)
# print all_min_covers(R, FD) 

R = ['A', 'B', 'C', 'D', 'E']
FD = [[['A', 'B'],['C']], [['D'],['D', 'B']], [['B'],['E']], [['E'],['D']], [['A', 'B', 'D'],['A', 'B', 'C', 'D']]]
# print all_closures(R, FD)
# print candidate_keys(R, FD)
# print min_covers(R, FD)
print all_min_covers(R, FD) 



