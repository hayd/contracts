from ..interface import Contract, ContractNotRespected, VariableRef
from ..syntax import W, add_contract, add_rvalue, oneOf, FollowedBy, NotAny


class BindVariable(Contract):
    
    def __init__(self, variable, allowed_types, where=None):
        assert isinstance(variable, str) and len(variable) == 1
        Contract.__init__(self, where)
        self.variable = variable
        self.allowed_types = allowed_types
    
    def check_contract(self, context, value):
        if context.has_variable(self.variable):
            expected = context.get_variable(self.variable)
            if not (expected == value):
                # TODO: add where it was bound
                error = ('Expected that %r = %r, got %r.' % 
                         (self.variable, expected, value))
                raise ContractNotRespected(contract=self, error=error,
                                           value=value, context=context)
            
        else:
            # bound variable
            if not isinstance(value, self.allowed_types):
                error = ('Variable %r can only bind to %r, not %r.' % 
                         (self.variable, self.allowed_types,
                          value.__class__.__name__))
                raise ContractNotRespected(self, error, value, context)
            
            context.set_variable(self.variable, value, origin=self)
            
    def __str__(self):
        return self.variable
        
    def __repr__(self):
        # XXX: invalid if tuple
        return 'BindVariable(%r,%s)' % (self.variable, self.allowed_types.__name__)
        
    @staticmethod
    def parse_action(allowed_types):
        def parse(s, loc, tokens):
            where = W(s, loc)
            variable = tokens[0]
            assert len(variable) == 1, \
                    'Wrong syntax, matched %r as variable in %r.' % (variable, s)
            # print ('Matched %r as variable in %r.' % (variable, s))
            return BindVariable(variable, allowed_types, where=where)
        return parse


alphabetu = 'A B C D E F G H I J K L M N O P Q R S T U W V X Y Z'
alphabetl = 'a b c d e f g h i j k l m n o p q r s t u w v x y z'
int_variables = oneOf(alphabetu.split()) 
# These must be followed by whitespace; punctuation
#misc_variables = oneOf(alphabet.lower()) + FollowedBy(White()) 
misc_variables = oneOf(alphabetl.split()) + FollowedBy(NotAny(oneOf(alphabetl.split())))

int_variables_contract = int_variables.copy().setParseAction(BindVariable.parse_action(int))
misc_variables_contract = misc_variables.copy().setParseAction(BindVariable.parse_action(object))  

def create_var_ref(s, loc, tokens):
    where = W(s, loc)
    return VariableRef(tokens[0], where=where)

add_rvalue(int_variables.copy().setParseAction(create_var_ref))
add_rvalue(misc_variables.copy().setParseAction(create_var_ref))