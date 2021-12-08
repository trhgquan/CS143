from io import FileIO

class logic_resolution:
    LOGICAL_EXPRESSIONS = ['OR']

    def __init__(self, kb : list, alpha : list) -> None:
        self.__has_solution = False
        self.__output_clauses = []
        self.__kb = []

        # Preprocessing KB
        for clause in kb:
            self.__kb.append(self.preprocess(clause.strip()))

        # Get inverse of alpha clauses.
        # And insert them into knowledge base KB.
        alpha = [self.inverse_literal(a) for a in self.preprocess(alpha)]
        for literal in alpha:
            if [literal] not in kb:
                self.__kb.append(self.standardlise([literal]))
    
    @staticmethod
    def preprocess(clause : str) -> list:
        '''Preprocess a Logic clause to list of literals,
        By default, they are linked by OR.

        Args:
            - clause (str) : logic clause
        
        Returns:
            - list
        '''
        preprocessed_ = []
        
        for literal in clause.split(' '):
            if len(literal) > 0 and literal not in logic_resolution.LOGICAL_EXPRESSIONS:
                preprocessed_.append(literal)
        
        return preprocessed_
    
    @staticmethod
    def inverse_literal(literal : str) -> str:
        '''Inverting a literal.

        Args:
            - literal (str) : literal to convert.
        
        Returns:
            str : inverted literal.
        '''
        if '-' in literal:
            return literal.replace('-', '')
        return '-' + literal
    
    @staticmethod
    def is_inverse(literal_a : str, literal_b : str) -> bool:
        '''Check if two literals are eachother inverse.

        Args:
            - literal_a (str) : first literal.
            - literal_b (str) : second literal.

        Returns:
            - bool
        '''
        return logic_resolution.inverse_literal(literal_a) == literal_b

    @staticmethod
    def is_always_valid(clause : list) -> bool:
        '''Check if a clause is always valid.

        Args:
            - clause (list) : clause to check

        Returns:
            - bool
        '''
        for i in range(len(clause) - 1):
            for j in range(i + 1, len(clause)):
                if (logic_resolution.is_inverse(clause[i], clause[j])):
                    return True
        return False
    
    @staticmethod
    def standardlise(clause : list) -> list:
        '''Sorting a clause.

        Args:
            - clause (list) : clause to sort.
        
        Returns:
            - list
        '''
        # Removing duplicates from clause.
        unique = set(clause)

        # Sort clauses, ignoring the sign before (-A and A will be treated the same).
        return sorted(list(unique), key = lambda x: x[-1])

    @staticmethod
    def cnf_format(clause : list) -> list:
        '''Print the clause in CNF format.

        Args:
            - clauses (list) : List of literals forming a clause, by default is OR.
        
        Returns:
            - str
        '''
        res_string = ''

        if len(clause) == 0:
            res_string = '{}'
        
        elif len(clause) == 1:
            res_string = clause[0]

        else:
            for literal in clause[:-1]:
                res_string += literal
                res_string += ' OR '
            res_string += clause[-1]
        
        return res_string

    @staticmethod
    def pl_resolve(clause_a : list, clause_b : list) -> list:
        '''Resolve two clause.

        Args:
            - clause_a (list) : first clause.
            - clause_b (list) : second clause.

        Returns:
            - list
        '''
        resolvents_ = []

        for i in range(len(clause_a)):
            for j in range(len(clause_b)):
                if logic_resolution.is_inverse(clause_a[i], clause_b[j]):
                    resolvent = clause_a[:i] + clause_a[i + 1:] + clause_b[:j] + clause_b[j + 1:]
                    resolvents_.append(logic_resolution.standardlise(resolvent))

        return resolvents_

    def pl_resolution(self) -> bool:
        '''Resolve given KB and alpha.

        Args:
            - self
        
        Returns:
            - bool
        '''
        while True:
            self.__output_clauses.append([])
            new_clauses = []

            for i in range(len(self.__kb) - 1):
                for j in range(i + 1, len(self.__kb)):
                    resolvents = self.pl_resolve(self.__kb[i], self.__kb[j])

                    if [] in resolvents:
                        new_clauses.append([])
                        self.__has_solution = True
                    
                    for resolvent_ in resolvents:
                        if self.is_always_valid(resolvent_):
                            continue
                        if resolvent_ not in self.__kb and resolvent_ not in self.__output_clauses[-1]:
                            new_clauses.append(resolvent_)
            
            if len(new_clauses) == 0:
                self.__has_solution = False
                return False

            for x in new_clauses:
                if x not in self.__kb: self.__kb.append(x)
                if x not in self.__output_clauses[-1]: self.__output_clauses[-1].append(x)

            if self.__has_solution:
                return True
    
    def print_output(self, f : FileIO = None) -> None:
        '''Print output to a readable form.

        Args:
            - f (FileIO) : file handle to print.
        '''
        for clause in self.__output_clauses:
            print(len(clause), file = f)
            for c in clause:
                print(self.cnf_format(c), file = f)
        
        print('YES', file = f) if self.__has_solution else print('NO', file = f)