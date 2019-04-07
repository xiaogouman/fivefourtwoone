# coding: utf-8
# Your code here!
############################################################
## project2.py - Code template for Project 2 - Normalization 
## Both for CS5421 and CS4221 students 
############################################################


### IMPORTANT! Change this to your metric number for grading
student_no = 'A0105505U' 

from itertools import chain, combinations, permutations, product
from collections import defaultdict, deque

# generate all subset of a set
def all_subsets(S):
	tuples = chain.from_iterable(combinations(S, r) for r in range(len(S)+1))
	result = []
	for a_tuple in tuples:
		result.append(set(a_tuple))
	return result

# remove trival fds and remove right common part from right hand side
# e.g.: A->ABC => A->BC
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
	while True:
		updated = False
		# loop through all functional dependencies, update if there is any reachable attributes that not in closure
		for fd in F:
			if closure >= set(fd[0]) and not closure.issuperset(set(fd[1])):
				closure.update(set(fd[1]))
				updated = True
		if not updated:
			break
	return list(closure)

# return True is key is a superkey of candidate keys
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

# split right hand side of functional dependencies to singleton
def rhs_to_singleton(fds):
	new_fds = []
	for fd in fds:
		for attr in fd[1]:
			new_fds.append([fd[0], set([attr])])
	return new_fds

# reduce left hand side of functional dependency
# return all combinations of minimal left hand side
def lhs_reduced_subsets(fds, lhs):
	result = []
	target_set = set(lhs)
	for subset in all_subsets(lhs):
		if not is_super_key(subset, result) and set(closure([], fds, subset)) >= target_set:
			result.append(subset)
	return result

# serialize functional dependency to a string
# e.g.: [['A'],['C','B']] => 'A->BC'
def serialize_fd(fd):
    return ','.join(sorted(fd[0]))+'-'+','.join(sorted(fd[1]))

def serialize_fds(fds):
    serialized_fds = []
    for fd in fds:
        serialized_fds.append(serialize_fd(fd))
    return serialized_fds

# deserialize functional dependency from a string
# e.g.: 'A->BC' => [['A'],['C','B']]
def de_serialize_fd(fd):
    left = set(fd.split('-')[0].split(','))
    right = set(fd.split('-')[1].split(','))
    return [left, right]
    
def de_serialize_fds(fds):
    result = []
    for fd in fds:
        result.append(de_serialize_fd(fd))
    return result
    
    
## Return a minimal cover of the functional dependencies of a given schema R and functional dependencies F.
def min_cover(R, FD): 
	# reference: https://www.inf.usi.ch/faculty/soule/teaching/2014-spring/cover.pdf
	print 'reduce fds'
	fds = reduce_fds(FD)
	# transform to singletons
	print 'rhs_to_singleton'
	fds = rhs_to_singleton(fds)
	# reduce left side
	print 'reduce lhs'
	lhs_reduced_serialized_fds = set()
	cover = []
	for fd in fds:
		left_serialized_options = set()
		lhs_subsets = lhs_reduced_subsets(fds, list(fd[0]))
		for left in lhs_subsets:
		    new_fd = [left, fd[1]]
		    serialized_fd = serialize_fd(new_fd)
		    if serialized_fd not in lhs_reduced_serialized_fds:
			    lhs_reduced_serialized_fds.add(serialized_fd)
			    cover.append(new_fd)

	# reduce fd until no fd can be reduced
	while True:
		can_reduce = False
		for fd in cover:
			reduced_cover = cover[:]
			reduced_cover.remove(fd)
			if set(closure([], reduced_cover, fd[0])) >= fd[1]:
				cover.remove(fd)
				can_reduce = True
		if not can_reduce:
			break
	return [[list(fd[0]), list(fd[1])] for fd in cover]

## Return all minimal covers reachable from the functional dependencies of a given schema R and functional dependencies F.
## NOTE: This function is not graded for CS4221 students.
def min_covers(R, FD):
	# remove all trivial dependencies 
	print 'reduce fds'
	fds = reduce_fds(FD)
	# transform to singltons
	print 'rhs_to_singleton'
	fds = rhs_to_singleton(fds)
	# reduce left side
	print 'reduce lhs'
	lhs_reduced_serialized_fds = set()
	lhs_reduced_fds = []
	for fd in fds:
		left_serialized_options = set()
		lhs_subsets = lhs_reduced_subsets(fds, list(fd[0]))
		for left in lhs_subsets:
		    new_fd = [left, fd[1]]
		    serialized_fd = serialize_fd(new_fd)
		    if serialized_fd not in lhs_reduced_serialized_fds:
			    lhs_reduced_serialized_fds.add(serialized_fd)
			    lhs_reduced_fds.append(new_fd)

	print 'run bfs to generage min covers'
	# get all minial covers uding bfs
	q = deque([lhs_reduced_fds])
	visited = set()
	all_min_covers = []
	
	while len(q) > 0:
		cover = q.popleft()
		# check if this cover is a mininum cover
		serialized_cover = frozenset(serialize_fds(cover))
		if serialized_cover in visited:
			continue
		can_be_reduce = False
		for fd in cover:
			reduced_cover = cover[:]
			reduced_cover.remove(fd)
			if set(closure([], reduced_cover, fd[0])) >= fd[1] and frozenset(serialize_fds(reduced_cover)) not in visited:
				can_be_reduce = True
				q.append(reduced_cover)
		if not can_be_reduce and serialized_cover not in visited:
			all_min_covers.append(cover)
		visited.add(serialized_cover)
	result = []
	for cover in all_min_covers:
		result.append([[list(fd[0]), list(fd[1])] for fd in cover])
	return result

# get functional dependencies from all closures
def all_fds(all_closures):
	all_fds = []
	for closure in all_closures:
		all_fds.append([closure[0], closure[1]])
	return all_fds

# reduce closure that left side == right side
# reduce closure that left side is superset and right side is subset of another closure
def reduce_closures(all_closures):
	closures = []
	# remove closure that left == right
	print all_closures
	for closure in all_closures:
		if not set(closure[0]) == set(closure[1]):
			closures.append([closure[0], list(set(closure[1])-set(closure[0]))])
	print closures
	# remove closure that left-hand side is a superset of another equality left-hand-side and its right-hand side is a subset of the right-hand side
	reduced_closures = []
	length = len(closures)
	for i in range(length):
		remove = False
		closure_i = closures[i]
		for j in range(length):
			closure_j = closures[j]
			if i!=j and set(closure_i[0]).issuperset(set(closure_j[0])) and set(closure_i[1]).issubset(set(closure_j[1])):
				remove = True
		if not remove:
			reduced_closures.append(closure_i)
	return reduced_closures


## Return all minimal covers of a given schema R and functional dependencies F.
## NOTE: This function is not graded for CS4221 students.
def all_min_covers(R, FD):
	my_all_closures = all_closures(R, FD)
	my_reduced_closures = reduce_closures(my_all_closures)
	my_all_fds = all_fds(my_reduced_closures)
	all_min_covers = min_covers(R, my_all_fds)
	print(len(all_min_covers))
	return all_min_covers

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

### Test case from tutorial
R = ['A', 'B', 'C', 'D', 'E']
FD = [[['A', 'B'],['C']], [['D'],['D', 'B']], [['B'],['E']], [['E'],['D']], [['A', 'B', 'D'],['A', 'B', 'C', 'D']]]
# print closure(R, FD, ['B'])
# print all_closures(R, FD)
# print candidate_keys(R, FD)
# print min_cover(R, FD)
print min_covers(R, FD) 
# print all_min_covers(R, FD)







