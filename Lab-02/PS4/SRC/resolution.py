from PS4.SRC.main import inverse_literal, is_inverse


class logic_resolution:
    LOGICAL_EXPRESSIONS = ['OR']

    def __init__(self, kb : list, alpha : list) -> None:
        self.__kb = kb
        self.__alpha = alpha
        self.__has_solution = False
        self.__output_clauses = []
    
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
            if literal not in logic_resolution.LOGICAL_EXPRESSIONS:
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
        return inverse_literal(literal_a) == literal_b

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
                if (is_inverse(clause[i], clause[j])):
                    return True
        return False