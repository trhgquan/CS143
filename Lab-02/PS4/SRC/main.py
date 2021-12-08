import sys
import collections

LOGICAL_EXPRESSIONS = ['OR']

output_clauses = []
finished = False

def preprocess(phrase : str) -> list:
    '''Split a phrase into literals

    Args:
        phrase (str) : phrase to split.
    
    Returns:
        list: splitted list of literals.
    '''
    phrase = phrase.split(' ')

    preprocessed_ = []

    for literal in phrase:
        if literal not in LOGICAL_EXPRESSIONS:
            preprocessed_.append(literal)
    return preprocessed_

def inverse_literal(x : str) -> str:
    '''Inverting a literal.

    Args:
        x (str) : literal to invert.
    
    Returns:
        str : inverted literal.
    '''
    if '-' in x:
        return x.replace('-', '')
    return '-' + x

def is_inverse(x1 : str, x2 : str) -> bool:
    '''Check if a literal is another literal's inverse

    Args:
        x1 (str) : first literal.
        x2 (str) : second literal.
    
    Returns:
        bool : True if both are others inverse.
    '''
    return inverse_literal(x1) == x2

def standardlise(clause : list) -> list:
    unique_clause = set(clause)
    return sorted(list(unique_clause))

def is_always_valid(clause : list) -> bool:
    '''Check if this is an always-true clause.

    Args:
        - clause (list) : clause to check
    
    Returns:
        - bool
    '''

    for i in range(len(clause) - 1):
        for j in range(i + 1, len(clause)):
            if is_inverse(clause[i], clause[j]):
                return True
    return False

def pl_resolve(clause_a : list, clause_b : list) -> list:
    resolvents_ = []
    for i in range(len(clause_a)):
        for j in range(len(clause_b)):
            if is_inverse(clause_a[i], clause_b[j]):
                resolvent = clause_a[:i] + clause_a[i + 1:] + clause_b[:j] + clause_b[j + 1:]
                resolvents_.append(standardlise(resolvent))
    return resolvents_

def pl_resolution(kb : list, alpha : list) -> bool:
    clauses_ = kb;

    for literal in alpha:
        if [literal] not in kb:
            clauses_.append([literal])

    finished = False

    while True:
        output_clauses.append([])
        new_clauses = []
        for i in range(len(kb) - 1):
            for j in range(i + 1, len(kb)):
                resolvents = pl_resolve(kb[i], kb[j])
                if [] in resolvents:
                    new_clauses.append([])
                    finished = True
                    break

                for resolvent_ in resolvents:
                    if is_always_valid(resolvent_): break
                    if resolvent_ not in clauses_ and resolvent_ not in output_clauses[-1]:
                        new_clauses.append(resolvent_)
            
            if finished: break

        if len(new_clauses) == 0:
            return False
        
        output_clauses[-1] = new_clauses
        for x in new_clauses: clauses_.append(x)
        
        if finished:
            return True

def cnf_string_format(clauses : list) -> str:
    '''Print the clause in CNF format.

    Args:
        - clauses (list) : List of literals forming a clause, by default is OR.
    
    Returns:
        - str
    '''
    res_string = ''

    if len(clauses) == 0:
        res_string = '{}'

    elif len(clauses) == 1:
        res_string = clauses[0]

    else:
        for clause_ in clauses[:-1]:
            res_string += clause_
            res_string += ' OR '
        res_string += clauses[-1]

    return res_string


def main():
    with open('input.txt', 'r+', encoding = 'utf-8') as f:
        alpha = preprocess(f.readline().strip())
        alpha = [inverse_literal(l) for l in alpha]

        n = int(f.readline().strip())

        kb_ = []
        for i in range(0, n):
            kb_.append(preprocess(f.readline().strip()))

        result = pl_resolution(kb_, alpha)

        for clause in output_clauses:
            print(len(clause))
            for c in clause:
                print(cnf_string_format(c))
        
        print('YES') if result else print('NO')

if __name__ == '__main__':
    main()