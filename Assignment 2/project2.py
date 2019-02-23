############################################################
## project2.py - Code template for Project 2 - Normalization 
## Both for CS5421 and CS4221 students 
############################################################


### IMPORTANT! Change this to your metric number for grading
student_no = 'A0105505U' 

from itertools import chain, combinations

def get_derived_attributes(S, F):
	derived_attr = set()
	input_attr = set(S)
	for fd in F:
		if set(fd[0]) == input_attr:
			derived_attr.update(fd[1])
			F.remove(fd)
	return derived_attr, F

def all_subsets(S):
	return chain.from_iterable(combinations(S, r) for r in range(len(S)+1))

## Determine the closure of set of attribute S given the schema R and functional dependency F
def closure(R, F, S):
	# initialize the closure as S
	closure = set()
	closure.update(S)
	fds = F[:]
	print "closure: ", closure
	while True:
		subsets = all_subsets(closure)
		closure_len_prev = len(closure)
		for subset in subsets:
			if len(subset) > 0 and len(F) > 0:
				derived_attr, fds = get_derived_attributes(subset, fds)
				print "derived: ", derived_attr
				closure.update(derived_attr)
		if len(closure) == closure_len_prev:
			break
	print "closure: ", sorted(closure)
	return sorted(closure)

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
	print "L: ", L
	print "RR: ", RR
	print "M: ", M


	# initalized candidate key as left side only attributes and missing attribute
	K = L.union(Schema-ALL)
	print "K: ", K
	for subset in all_subsets(M):
		print "subset: ", subset
		key = K.union(subset)
		# skip for super key
		is_super_key = False
		for current_key in keys:
			if key >= set(current_key):
				is_super_key = True
				break

		print "key: ", key
		if not is_super_key and set(closure(R, F, key)) == Schema:
			keys.append(sorted(key))


	print "keys: ", keys
	return []

## Determine the all the attribute closure excluding superkeys that are not candidate keys given the schema R and functional dependency F
def all_closures(R, F): 
    return []
    
## Return a minimal cover of the functional dependencies of a given schema R and functional dependencies F.
def min_cover(R, FD): 
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
print min_covers(R, FD) 
print all_min_covers(R, FD) 

## Tutorial questions
R = ['A', 'B', 'C', 'D', 'E']
FD = [[['A', 'B'],['C']], [['D'],['D', 'B']], [['B'],['E']], [['E'],['D']], [['A', 'B', 'D'],['A', 'B', 'C', 'D']]]

print closure(R, FD, ['A', 'E'])
# print candidate_keys(R, FD)
print min_cover(R, FD)
print min_covers(R, FD)
print all_min_covers(R, FD) 
