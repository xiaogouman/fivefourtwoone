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


# input is list of fds, left and right side are set
def union_fds(fds):
	unioned_fds = []
	unioned = False
	fd_dict = defaultdict(set)
	for fd in fds:
		fd_dict[frozenset(fd[0])]=fd_dict[frozenset(fd[0])].union(fd[1])
	for fd in fd_dict.items():
		unioned_fds.append([set(fd[0]),fd[1]])
	if len(fds) > len(unioned_fds):
		unioned = True
	return unioned, unioned_fds

def simplify_fd(fds):
	simplied_fds = fds[:]
	n = len(fds)
	simplied = False
	for i in range(n):
		simplied_fds = simplied_fds[i]
		for j in range(n):
			if i!=j:
				current_fd = simplied_fds[j]
				fd_attr = current_fd[0].union(current_fd[1])
				if simplied_fds[0] >= fd_attr:
					simplied = True
					simplied_fds[0] = simplied_fds[0] - current_fd[1]
				if simplied_fds[1] >= fd_attr:
					simplied = True
					simplied_fds[1] = simplied_fds[1] - current_fd[1]
	return simplied, simplied_fds

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
	# all_closures_dict = all_closures_to_dict(all_closures(R, FD))
	lhs_reduced_fds = [] 
	for fd in fds:
		left_options = set()
		reduced_options = []
		can_be_reduce = False
		for permutation in permutations(list(fd[0])):
			left = fd[0]
			reduced = False
			for attr in permutation:
				attr_set = set([attr])
				rest_set = left - attr_set
				if set(closure(R, FD, list(rest_set))) > attr_set:
					# remove attr from left side
					reduced = True
					can_be_reduce = True
					left = left - attr_set
			if (reduced):
				left_options.add(frozenset(left))
		for left in left_options:
			reduced_options.append([set(left), fd[1]])
		if not can_be_reduce:
			reduced_options.append(fd)
		lhs_reduced_fds.append(reduced_options)

	# all combinations
	min_cover_combinations = [list(attr) for attr in list(product(*lhs_reduced_fds))]:

	# remove all redundant 
	min_covers_set = set()
	for combination in min_cover_combinations:
		for permutation in permutations(range(len(combination))):
			for i in permutation:
				


		min_covers_set.add(frozenset(combination))

	return []

## Return all minimal covers of a given schema R and functional dependencies F.
## NOTE: This function is not graded for CS4221 students.
def all_min_covers(R, FD):
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
print min_covers(R, FD)



