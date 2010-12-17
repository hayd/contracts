from contracts.interface import Contract, ContractNotRespected
from contracts.syntax import W, add_contract, contract, S
from pyparsing import Literal
import numbers

class CheckType(Contract):
    def __init__(self, where, types, type_string=None):
        Contract.__init__(self, where)
        self.types = types
        if type_string is None:
            self.type_string = types.__name__
        else:
            self.type_string = type_string
            
    def check_contract(self, context, value):
        if not isinstance(value, self.types):
            error = 'Expected type %r, got %r.' % (self.types.__name__,
                                                   value.__class__.__name__)
            raise ContractNotRespected(contract=self, error=error,
                                       value=value, context=context)
    
    def __str__(self):
        return self.type_string
    
    def __repr__(self):
        return 'CheckType(%s)' % (self.types.__name__)

    @staticmethod
    def parse_action(types):
        def parse(s, loc, tokens):
            return CheckType(W(s, loc), types, tokens[0]) #@UnusedVariable
        return parse

add_contract(Literal('int').setParseAction(CheckType.parse_action(int)))
add_contract(Literal('float').setParseAction(CheckType.parse_action(float)))
add_contract(Literal('bool').setParseAction(CheckType.parse_action(bool)))
add_contract(Literal('number').setParseAction(CheckType.parse_action(numbers.Number)))



class Type(Contract):
    def __init__(self, where, type_constraint):
        Contract.__init__(self, where)
        self.type_constraint = type_constraint
        
    def check_contract(self, context, value): 
        self.type_constraint.check_contract(context, type(value))
    
    def __str__(self):
        return 'type(%s)' % self.type_constraint

    def __repr__(self):
        return 'Type(%r)' % self.type_constraint

    @staticmethod
    def parse_action(s, loc, tokens):
        type_constraint = tokens['type_constraint']
        return Type(W(s, loc), type_constraint) #@UnusedVariable


type_contract = S('type') + S('(') + contract('type_constraint') + S(')')

add_contract(type_contract.setParseAction(Type.parse_action))



