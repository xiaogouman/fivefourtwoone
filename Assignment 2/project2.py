############################################################
## project2.py - Code template for Project 2 - Normalization 
## Both for CS5421 and CS4221 students 
############################################################


### IMPORTANT! Change this to your metric number for grading
student_no = 'A0105505U' 

from itertools import chain, combinations
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
	return chain.from_iterable(combinations(S, r) for r in range(len(S)+1))

# remove trival fds
def reduce_fds(F):
	fds = []
	for fd in F:
		left = set(fd[0])
		right = set(fd[1])
		interc = left.intersection(right)
		if interc != right:
			fds.append([left-interc, right-interc])
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
					all_closures.append([sorted(subset), subset_closure])
			else:
				all_closures.append([sorted(subset), subset_closure])
	print all_closures
	return all_closures

## Return the candidate keys of a given schema R and functional dependencies F.
## NOTE: This function is not graded for CS5421 students.
def candidate_keys(R, F): 
	Schema = set(R)
	L = set()
	RR = set()
	keys = []
	for fd in F:
		L.update(fd[0])
		RR.update(fd[1])
	M = L.intersection(RR)
	ALL = L.union(RR)
	L = L - M
	RR = RR - M

	# initalized candidate key as left side only attributes and missing attribute
	K = L.union(Schema-ALL)
	for subset in all_subsets(M):
		key = K.union(subset)
		# skip for super key
		if not is_super_key(key, keys) and set(closure(R, F, key)) == Schema:
			keys.append(sorted(key))
	return keys

# input is list of fds, left and right side are set
def union_fds(fds):
	unioned_fds = []
	fd_dict = defaultdict(set)
	for fd in fds:
		fd_dict[frozenset(fd[0])]=fd_dict[frozenset(fd[0])].union(fd[1])
	for fd in fd_dict.items():
		unioned_fds.append([set(fd[0]),fd[1]])
	return unioned_fds
    
## Return a minimal cover of the functional dependencies of a given schema R and functional dependencies F.
def min_cover(R, FD): 
	# reference: https://www.inf.usi.ch/faculty/soule/teaching/2014-spring/cover.pdf
	fds = reduce_fds(FD)
	print "fds: ", fds
	# union simplificaiton
	unioned_fds = union_fds(fds)

	# simplify left side


	# simplify right side
	return []

## Return all minimal covers reachable from the functional dependencies of a given schema R and functional dependencies F.
## NOTE: This function is not graded for CS4221 students.
def min_covers(R, FD):
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
print min_cover(R, FD) 

R = ['A', 'B', 'C']
FD = [[['A', 'B'], ['C']],[['A'], ['B']], [['B'], ['A']]] 
# print min_covers(R, FD) 
# print all_min_covers(R, FD) 

## Tutorial questions
R = ['A', 'B', 'C', 'D', 'E']
FD = [[['A', 'B'],['C']], [['D'],['D', 'B']], [['B'],['E']], [['E'],['D']], [['A', 'B', 'D'],['A', 'B', 'C', 'D']]]

# print candidate_keys(R, FD)
print min_cover(R, FD)
# print min_covers(R, FD)
# print all_min_covers(R, FD) 
