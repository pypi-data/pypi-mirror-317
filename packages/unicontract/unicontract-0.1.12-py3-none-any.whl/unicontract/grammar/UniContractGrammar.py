# Generated from ./unicontract/grammar/UniContractGrammar.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,41,320,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,1,0,
        5,0,42,8,0,10,0,12,0,45,9,0,1,0,5,0,48,8,0,10,0,12,0,51,9,0,1,0,
        1,0,1,1,5,1,56,8,1,10,1,12,1,59,9,1,1,1,5,1,62,8,1,10,1,12,1,65,
        9,1,1,1,1,1,1,1,5,1,70,8,1,10,1,12,1,73,9,1,1,1,5,1,76,8,1,10,1,
        12,1,79,9,1,1,1,1,1,3,1,83,8,1,1,2,5,2,86,8,2,10,2,12,2,89,9,2,1,
        2,5,2,92,8,2,10,2,12,2,95,9,2,1,2,1,2,1,2,1,2,5,2,101,8,2,10,2,12,
        2,104,9,2,1,2,1,2,1,3,1,3,3,3,110,8,3,1,4,5,4,113,8,4,10,4,12,4,
        116,9,4,1,4,5,4,119,8,4,10,4,12,4,122,9,4,1,4,1,4,1,4,3,4,127,8,
        4,1,4,1,4,5,4,131,8,4,10,4,12,4,134,9,4,1,4,1,4,1,5,1,5,1,5,3,5,
        141,8,5,1,6,5,6,144,8,6,10,6,12,6,147,9,6,1,6,5,6,150,8,6,10,6,12,
        6,153,9,6,1,6,3,6,156,8,6,1,6,1,6,1,6,1,6,1,6,1,7,5,7,164,8,7,10,
        7,12,7,167,9,7,1,7,5,7,170,8,7,10,7,12,7,173,9,7,1,7,3,7,176,8,7,
        1,7,1,7,1,7,1,7,3,7,182,8,7,1,7,1,7,5,7,186,8,7,10,7,12,7,189,9,
        7,1,7,1,7,1,7,3,7,194,8,7,1,8,5,8,197,8,8,10,8,12,8,200,9,8,1,8,
        5,8,203,8,8,10,8,12,8,206,9,8,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,3,
        9,216,8,9,1,10,1,10,1,11,1,11,1,11,1,11,1,11,3,11,225,8,11,1,12,
        1,12,1,12,1,12,1,12,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,14,1,14,
        1,14,1,14,1,14,1,14,1,14,1,14,5,14,247,8,14,10,14,12,14,250,9,14,
        1,14,1,14,3,14,254,8,14,1,15,1,15,1,15,1,15,3,15,260,8,15,1,16,1,
        16,1,16,5,16,265,8,16,10,16,12,16,268,9,16,1,17,1,17,1,17,1,17,5,
        17,274,8,17,10,17,12,17,277,9,17,1,18,5,18,280,8,18,10,18,12,18,
        283,9,18,1,18,5,18,286,8,18,10,18,12,18,289,9,18,1,18,1,18,1,18,
        1,18,3,18,295,8,18,1,18,1,18,5,18,299,8,18,10,18,12,18,302,9,18,
        1,18,1,18,1,19,5,19,307,8,19,10,19,12,19,310,9,19,1,19,5,19,313,
        8,19,10,19,12,19,316,9,19,1,19,1,19,1,19,0,0,20,0,2,4,6,8,10,12,
        14,16,18,20,22,24,26,28,30,32,34,36,38,0,1,1,0,16,25,344,0,43,1,
        0,0,0,2,82,1,0,0,0,4,87,1,0,0,0,6,109,1,0,0,0,8,114,1,0,0,0,10,140,
        1,0,0,0,12,145,1,0,0,0,14,165,1,0,0,0,16,198,1,0,0,0,18,215,1,0,
        0,0,20,217,1,0,0,0,22,224,1,0,0,0,24,226,1,0,0,0,26,231,1,0,0,0,
        28,253,1,0,0,0,30,259,1,0,0,0,32,261,1,0,0,0,34,269,1,0,0,0,36,281,
        1,0,0,0,38,308,1,0,0,0,40,42,3,2,1,0,41,40,1,0,0,0,42,45,1,0,0,0,
        43,41,1,0,0,0,43,44,1,0,0,0,44,49,1,0,0,0,45,43,1,0,0,0,46,48,3,
        4,2,0,47,46,1,0,0,0,48,51,1,0,0,0,49,47,1,0,0,0,49,50,1,0,0,0,50,
        52,1,0,0,0,51,49,1,0,0,0,52,53,5,0,0,1,53,1,1,0,0,0,54,56,5,39,0,
        0,55,54,1,0,0,0,56,59,1,0,0,0,57,55,1,0,0,0,57,58,1,0,0,0,58,63,
        1,0,0,0,59,57,1,0,0,0,60,62,3,28,14,0,61,60,1,0,0,0,62,65,1,0,0,
        0,63,61,1,0,0,0,63,64,1,0,0,0,64,66,1,0,0,0,65,63,1,0,0,0,66,67,
        5,12,0,0,67,83,3,32,16,0,68,70,5,39,0,0,69,68,1,0,0,0,70,73,1,0,
        0,0,71,69,1,0,0,0,71,72,1,0,0,0,72,77,1,0,0,0,73,71,1,0,0,0,74,76,
        3,28,14,0,75,74,1,0,0,0,76,79,1,0,0,0,77,75,1,0,0,0,77,78,1,0,0,
        0,78,80,1,0,0,0,79,77,1,0,0,0,80,81,5,12,0,0,81,83,5,36,0,0,82,57,
        1,0,0,0,82,71,1,0,0,0,83,3,1,0,0,0,84,86,5,39,0,0,85,84,1,0,0,0,
        86,89,1,0,0,0,87,85,1,0,0,0,87,88,1,0,0,0,88,93,1,0,0,0,89,87,1,
        0,0,0,90,92,3,28,14,0,91,90,1,0,0,0,92,95,1,0,0,0,93,91,1,0,0,0,
        93,94,1,0,0,0,94,96,1,0,0,0,95,93,1,0,0,0,96,97,5,14,0,0,97,98,3,
        32,16,0,98,102,5,6,0,0,99,101,3,6,3,0,100,99,1,0,0,0,101,104,1,0,
        0,0,102,100,1,0,0,0,102,103,1,0,0,0,103,105,1,0,0,0,104,102,1,0,
        0,0,105,106,5,7,0,0,106,5,1,0,0,0,107,110,3,8,4,0,108,110,3,36,18,
        0,109,107,1,0,0,0,109,108,1,0,0,0,110,7,1,0,0,0,111,113,5,39,0,0,
        112,111,1,0,0,0,113,116,1,0,0,0,114,112,1,0,0,0,114,115,1,0,0,0,
        115,120,1,0,0,0,116,114,1,0,0,0,117,119,3,28,14,0,118,117,1,0,0,
        0,119,122,1,0,0,0,120,118,1,0,0,0,120,121,1,0,0,0,121,123,1,0,0,
        0,122,120,1,0,0,0,123,124,5,13,0,0,124,126,5,37,0,0,125,127,3,34,
        17,0,126,125,1,0,0,0,126,127,1,0,0,0,127,128,1,0,0,0,128,132,5,6,
        0,0,129,131,3,10,5,0,130,129,1,0,0,0,131,134,1,0,0,0,132,130,1,0,
        0,0,132,133,1,0,0,0,133,135,1,0,0,0,134,132,1,0,0,0,135,136,5,7,
        0,0,136,9,1,0,0,0,137,141,3,14,7,0,138,141,3,12,6,0,139,141,3,36,
        18,0,140,137,1,0,0,0,140,138,1,0,0,0,140,139,1,0,0,0,141,11,1,0,
        0,0,142,144,5,39,0,0,143,142,1,0,0,0,144,147,1,0,0,0,145,143,1,0,
        0,0,145,146,1,0,0,0,146,151,1,0,0,0,147,145,1,0,0,0,148,150,3,28,
        14,0,149,148,1,0,0,0,150,153,1,0,0,0,151,149,1,0,0,0,151,152,1,0,
        0,0,152,155,1,0,0,0,153,151,1,0,0,0,154,156,5,32,0,0,155,154,1,0,
        0,0,155,156,1,0,0,0,156,157,1,0,0,0,157,158,5,30,0,0,158,159,5,37,
        0,0,159,160,5,3,0,0,160,161,3,18,9,0,161,13,1,0,0,0,162,164,5,39,
        0,0,163,162,1,0,0,0,164,167,1,0,0,0,165,163,1,0,0,0,165,166,1,0,
        0,0,166,171,1,0,0,0,167,165,1,0,0,0,168,170,3,28,14,0,169,168,1,
        0,0,0,170,173,1,0,0,0,171,169,1,0,0,0,171,172,1,0,0,0,172,175,1,
        0,0,0,173,171,1,0,0,0,174,176,5,33,0,0,175,174,1,0,0,0,175,176,1,
        0,0,0,176,177,1,0,0,0,177,178,5,31,0,0,178,179,5,37,0,0,179,181,
        5,4,0,0,180,182,3,16,8,0,181,180,1,0,0,0,181,182,1,0,0,0,182,187,
        1,0,0,0,183,184,5,2,0,0,184,186,3,16,8,0,185,183,1,0,0,0,186,189,
        1,0,0,0,187,185,1,0,0,0,187,188,1,0,0,0,188,190,1,0,0,0,189,187,
        1,0,0,0,190,193,5,5,0,0,191,192,5,11,0,0,192,194,3,18,9,0,193,191,
        1,0,0,0,193,194,1,0,0,0,194,15,1,0,0,0,195,197,5,39,0,0,196,195,
        1,0,0,0,197,200,1,0,0,0,198,196,1,0,0,0,198,199,1,0,0,0,199,204,
        1,0,0,0,200,198,1,0,0,0,201,203,3,28,14,0,202,201,1,0,0,0,203,206,
        1,0,0,0,204,202,1,0,0,0,204,205,1,0,0,0,205,207,1,0,0,0,206,204,
        1,0,0,0,207,208,5,37,0,0,208,209,5,3,0,0,209,210,3,18,9,0,210,17,
        1,0,0,0,211,216,3,20,10,0,212,216,3,22,11,0,213,216,3,24,12,0,214,
        216,3,26,13,0,215,211,1,0,0,0,215,212,1,0,0,0,215,213,1,0,0,0,215,
        214,1,0,0,0,216,19,1,0,0,0,217,218,7,0,0,0,218,21,1,0,0,0,219,225,
        3,32,16,0,220,221,5,29,0,0,221,222,5,8,0,0,222,223,5,36,0,0,223,
        225,5,9,0,0,224,219,1,0,0,0,224,220,1,0,0,0,225,23,1,0,0,0,226,227,
        5,26,0,0,227,228,5,8,0,0,228,229,3,18,9,0,229,230,5,9,0,0,230,25,
        1,0,0,0,231,232,5,27,0,0,232,233,5,8,0,0,233,234,3,18,9,0,234,235,
        5,2,0,0,235,236,3,18,9,0,236,237,5,9,0,0,237,27,1,0,0,0,238,239,
        5,10,0,0,239,254,5,37,0,0,240,241,5,10,0,0,241,242,5,37,0,0,242,
        243,5,4,0,0,243,248,3,30,15,0,244,245,5,2,0,0,245,247,3,30,15,0,
        246,244,1,0,0,0,247,250,1,0,0,0,248,246,1,0,0,0,248,249,1,0,0,0,
        249,251,1,0,0,0,250,248,1,0,0,0,251,252,5,5,0,0,252,254,1,0,0,0,
        253,238,1,0,0,0,253,240,1,0,0,0,254,29,1,0,0,0,255,260,3,32,16,0,
        256,260,5,34,0,0,257,260,5,35,0,0,258,260,5,36,0,0,259,255,1,0,0,
        0,259,256,1,0,0,0,259,257,1,0,0,0,259,258,1,0,0,0,260,31,1,0,0,0,
        261,266,5,37,0,0,262,263,5,1,0,0,263,265,5,37,0,0,264,262,1,0,0,
        0,265,268,1,0,0,0,266,264,1,0,0,0,266,267,1,0,0,0,267,33,1,0,0,0,
        268,266,1,0,0,0,269,270,5,28,0,0,270,275,3,32,16,0,271,272,5,2,0,
        0,272,274,3,32,16,0,273,271,1,0,0,0,274,277,1,0,0,0,275,273,1,0,
        0,0,275,276,1,0,0,0,276,35,1,0,0,0,277,275,1,0,0,0,278,280,5,39,
        0,0,279,278,1,0,0,0,280,283,1,0,0,0,281,279,1,0,0,0,281,282,1,0,
        0,0,282,287,1,0,0,0,283,281,1,0,0,0,284,286,3,28,14,0,285,284,1,
        0,0,0,286,289,1,0,0,0,287,285,1,0,0,0,287,288,1,0,0,0,288,290,1,
        0,0,0,289,287,1,0,0,0,290,291,5,15,0,0,291,292,5,37,0,0,292,294,
        5,6,0,0,293,295,3,38,19,0,294,293,1,0,0,0,294,295,1,0,0,0,295,300,
        1,0,0,0,296,297,5,2,0,0,297,299,3,38,19,0,298,296,1,0,0,0,299,302,
        1,0,0,0,300,298,1,0,0,0,300,301,1,0,0,0,301,303,1,0,0,0,302,300,
        1,0,0,0,303,304,5,7,0,0,304,37,1,0,0,0,305,307,5,39,0,0,306,305,
        1,0,0,0,307,310,1,0,0,0,308,306,1,0,0,0,308,309,1,0,0,0,309,314,
        1,0,0,0,310,308,1,0,0,0,311,313,3,28,14,0,312,311,1,0,0,0,313,316,
        1,0,0,0,314,312,1,0,0,0,314,315,1,0,0,0,315,317,1,0,0,0,316,314,
        1,0,0,0,317,318,5,37,0,0,318,39,1,0,0,0,40,43,49,57,63,71,77,82,
        87,93,102,109,114,120,126,132,140,145,151,155,165,171,175,181,187,
        193,198,204,215,224,248,253,259,266,275,281,287,294,300,308,314
    ]

class UniContractGrammar ( Parser ):

    grammarFileName = "UniContractGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'.'", "','", "':'", "'('", "')'", "'{'", 
                     "'}'", "'['", "']'", "'@'", "'=>'", "'import'", "'interface'", 
                     "'namespace'", "'enum'", "'integer'", "'number'", "'float'", 
                     "'date'", "'time'", "'dateTime'", "'string'", "'boolean'", 
                     "'bytes'", "'stream'", "'list'", "'map'", "'inherits'", 
                     "'external'", "'property'", "'method'", "'readonly'", 
                     "'async'" ]

    symbolicNames = [ "<INVALID>", "DOT", "COMMA", "SEMI", "LPAREN", "RPAREN", 
                      "LCURLY", "RCURLY", "LBARCKET", "RBRACKET", "AT", 
                      "ARROW", "IMPORT", "INTERFACE", "NAMESPACE", "ENUM", 
                      "INTEGER", "NUMBER", "FLOAT", "DATE", "TIME", "DATETIME", 
                      "STRING", "BOOLEAN", "BYTES", "STREAM", "LIST", "MAP", 
                      "INHERITS", "EXTERNAL", "PROPERTY", "METHOD", "READONLY", 
                      "ASYNC", "INTEGER_CONSTANS", "NUMBER_CONSTANS", "STRING_LITERAL", 
                      "IDENTIFIER", "WS", "DOCUMENT_LINE", "LINE_COMMENT", 
                      "BLOCK_COMMENT" ]

    RULE_contract = 0
    RULE_import_rule = 1
    RULE_namespace = 2
    RULE_namespace_elements = 3
    RULE_interface = 4
    RULE_interface_element = 5
    RULE_interface_property = 6
    RULE_interface_method = 7
    RULE_interface_method_param = 8
    RULE_type = 9
    RULE_primitive_type = 10
    RULE_reference_type = 11
    RULE_list_type = 12
    RULE_map_type = 13
    RULE_decorator = 14
    RULE_decorator_param = 15
    RULE_qualifiedName = 16
    RULE_inherits = 17
    RULE_enum = 18
    RULE_enum_element = 19

    ruleNames =  [ "contract", "import_rule", "namespace", "namespace_elements", 
                   "interface", "interface_element", "interface_property", 
                   "interface_method", "interface_method_param", "type", 
                   "primitive_type", "reference_type", "list_type", "map_type", 
                   "decorator", "decorator_param", "qualifiedName", "inherits", 
                   "enum", "enum_element" ]

    EOF = Token.EOF
    DOT=1
    COMMA=2
    SEMI=3
    LPAREN=4
    RPAREN=5
    LCURLY=6
    RCURLY=7
    LBARCKET=8
    RBRACKET=9
    AT=10
    ARROW=11
    IMPORT=12
    INTERFACE=13
    NAMESPACE=14
    ENUM=15
    INTEGER=16
    NUMBER=17
    FLOAT=18
    DATE=19
    TIME=20
    DATETIME=21
    STRING=22
    BOOLEAN=23
    BYTES=24
    STREAM=25
    LIST=26
    MAP=27
    INHERITS=28
    EXTERNAL=29
    PROPERTY=30
    METHOD=31
    READONLY=32
    ASYNC=33
    INTEGER_CONSTANS=34
    NUMBER_CONSTANS=35
    STRING_LITERAL=36
    IDENTIFIER=37
    WS=38
    DOCUMENT_LINE=39
    LINE_COMMENT=40
    BLOCK_COMMENT=41

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ContractContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(UniContractGrammar.EOF, 0)

        def import_rule(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.Import_ruleContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.Import_ruleContext,i)


        def namespace(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.NamespaceContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.NamespaceContext,i)


        def getRuleIndex(self):
            return UniContractGrammar.RULE_contract

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContract" ):
                listener.enterContract(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContract" ):
                listener.exitContract(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContract" ):
                return visitor.visitContract(self)
            else:
                return visitor.visitChildren(self)




    def contract(self):

        localctx = UniContractGrammar.ContractContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_contract)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 40
                    self.import_rule() 
                self.state = 45
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 49
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 549755831296) != 0):
                self.state = 46
                self.namespace()
                self.state = 51
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 52
            self.match(UniContractGrammar.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Import_ruleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IMPORT(self):
            return self.getToken(UniContractGrammar.IMPORT, 0)

        def qualifiedName(self):
            return self.getTypedRuleContext(UniContractGrammar.QualifiedNameContext,0)


        def DOCUMENT_LINE(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.DOCUMENT_LINE)
            else:
                return self.getToken(UniContractGrammar.DOCUMENT_LINE, i)

        def decorator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.DecoratorContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.DecoratorContext,i)


        def STRING_LITERAL(self):
            return self.getToken(UniContractGrammar.STRING_LITERAL, 0)

        def getRuleIndex(self):
            return UniContractGrammar.RULE_import_rule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_rule" ):
                listener.enterImport_rule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_rule" ):
                listener.exitImport_rule(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImport_rule" ):
                return visitor.visitImport_rule(self)
            else:
                return visitor.visitChildren(self)




    def import_rule(self):

        localctx = UniContractGrammar.Import_ruleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_import_rule)
        self._la = 0 # Token type
        try:
            self.state = 82
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 57
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==39:
                    self.state = 54
                    self.match(UniContractGrammar.DOCUMENT_LINE)
                    self.state = 59
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 63
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==10:
                    self.state = 60
                    self.decorator()
                    self.state = 65
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 66
                self.match(UniContractGrammar.IMPORT)
                self.state = 67
                self.qualifiedName()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 71
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==39:
                    self.state = 68
                    self.match(UniContractGrammar.DOCUMENT_LINE)
                    self.state = 73
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 77
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==10:
                    self.state = 74
                    self.decorator()
                    self.state = 79
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 80
                self.match(UniContractGrammar.IMPORT)
                self.state = 81
                self.match(UniContractGrammar.STRING_LITERAL)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NamespaceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAMESPACE(self):
            return self.getToken(UniContractGrammar.NAMESPACE, 0)

        def qualifiedName(self):
            return self.getTypedRuleContext(UniContractGrammar.QualifiedNameContext,0)


        def LCURLY(self):
            return self.getToken(UniContractGrammar.LCURLY, 0)

        def RCURLY(self):
            return self.getToken(UniContractGrammar.RCURLY, 0)

        def DOCUMENT_LINE(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.DOCUMENT_LINE)
            else:
                return self.getToken(UniContractGrammar.DOCUMENT_LINE, i)

        def decorator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.DecoratorContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.DecoratorContext,i)


        def namespace_elements(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.Namespace_elementsContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.Namespace_elementsContext,i)


        def getRuleIndex(self):
            return UniContractGrammar.RULE_namespace

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNamespace" ):
                listener.enterNamespace(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNamespace" ):
                listener.exitNamespace(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNamespace" ):
                return visitor.visitNamespace(self)
            else:
                return visitor.visitChildren(self)




    def namespace(self):

        localctx = UniContractGrammar.NamespaceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_namespace)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 87
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==39:
                self.state = 84
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 89
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 93
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==10:
                self.state = 90
                self.decorator()
                self.state = 95
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 96
            self.match(UniContractGrammar.NAMESPACE)
            self.state = 97
            self.qualifiedName()
            self.state = 98
            self.match(UniContractGrammar.LCURLY)
            self.state = 102
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 549755855872) != 0):
                self.state = 99
                self.namespace_elements()
                self.state = 104
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 105
            self.match(UniContractGrammar.RCURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Namespace_elementsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def interface(self):
            return self.getTypedRuleContext(UniContractGrammar.InterfaceContext,0)


        def enum(self):
            return self.getTypedRuleContext(UniContractGrammar.EnumContext,0)


        def getRuleIndex(self):
            return UniContractGrammar.RULE_namespace_elements

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNamespace_elements" ):
                listener.enterNamespace_elements(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNamespace_elements" ):
                listener.exitNamespace_elements(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNamespace_elements" ):
                return visitor.visitNamespace_elements(self)
            else:
                return visitor.visitChildren(self)




    def namespace_elements(self):

        localctx = UniContractGrammar.Namespace_elementsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_namespace_elements)
        try:
            self.state = 109
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 107
                self.interface()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 108
                self.enum()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InterfaceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTERFACE(self):
            return self.getToken(UniContractGrammar.INTERFACE, 0)

        def IDENTIFIER(self):
            return self.getToken(UniContractGrammar.IDENTIFIER, 0)

        def LCURLY(self):
            return self.getToken(UniContractGrammar.LCURLY, 0)

        def RCURLY(self):
            return self.getToken(UniContractGrammar.RCURLY, 0)

        def DOCUMENT_LINE(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.DOCUMENT_LINE)
            else:
                return self.getToken(UniContractGrammar.DOCUMENT_LINE, i)

        def decorator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.DecoratorContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.DecoratorContext,i)


        def inherits(self):
            return self.getTypedRuleContext(UniContractGrammar.InheritsContext,0)


        def interface_element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.Interface_elementContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.Interface_elementContext,i)


        def getRuleIndex(self):
            return UniContractGrammar.RULE_interface

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInterface" ):
                listener.enterInterface(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInterface" ):
                listener.exitInterface(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInterface" ):
                return visitor.visitInterface(self)
            else:
                return visitor.visitChildren(self)




    def interface(self):

        localctx = UniContractGrammar.InterfaceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_interface)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 114
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==39:
                self.state = 111
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 116
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 120
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==10:
                self.state = 117
                self.decorator()
                self.state = 122
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 123
            self.match(UniContractGrammar.INTERFACE)
            self.state = 124
            self.match(UniContractGrammar.IDENTIFIER)
            self.state = 126
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==28:
                self.state = 125
                self.inherits()


            self.state = 128
            self.match(UniContractGrammar.LCURLY)
            self.state = 132
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 565861975040) != 0):
                self.state = 129
                self.interface_element()
                self.state = 134
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 135
            self.match(UniContractGrammar.RCURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Interface_elementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def interface_method(self):
            return self.getTypedRuleContext(UniContractGrammar.Interface_methodContext,0)


        def interface_property(self):
            return self.getTypedRuleContext(UniContractGrammar.Interface_propertyContext,0)


        def enum(self):
            return self.getTypedRuleContext(UniContractGrammar.EnumContext,0)


        def getRuleIndex(self):
            return UniContractGrammar.RULE_interface_element

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInterface_element" ):
                listener.enterInterface_element(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInterface_element" ):
                listener.exitInterface_element(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInterface_element" ):
                return visitor.visitInterface_element(self)
            else:
                return visitor.visitChildren(self)




    def interface_element(self):

        localctx = UniContractGrammar.Interface_elementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_interface_element)
        try:
            self.state = 140
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 137
                self.interface_method()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 138
                self.interface_property()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 139
                self.enum()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Interface_propertyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PROPERTY(self):
            return self.getToken(UniContractGrammar.PROPERTY, 0)

        def IDENTIFIER(self):
            return self.getToken(UniContractGrammar.IDENTIFIER, 0)

        def SEMI(self):
            return self.getToken(UniContractGrammar.SEMI, 0)

        def type_(self):
            return self.getTypedRuleContext(UniContractGrammar.TypeContext,0)


        def DOCUMENT_LINE(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.DOCUMENT_LINE)
            else:
                return self.getToken(UniContractGrammar.DOCUMENT_LINE, i)

        def decorator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.DecoratorContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.DecoratorContext,i)


        def READONLY(self):
            return self.getToken(UniContractGrammar.READONLY, 0)

        def getRuleIndex(self):
            return UniContractGrammar.RULE_interface_property

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInterface_property" ):
                listener.enterInterface_property(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInterface_property" ):
                listener.exitInterface_property(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInterface_property" ):
                return visitor.visitInterface_property(self)
            else:
                return visitor.visitChildren(self)




    def interface_property(self):

        localctx = UniContractGrammar.Interface_propertyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_interface_property)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 145
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==39:
                self.state = 142
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 147
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 151
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==10:
                self.state = 148
                self.decorator()
                self.state = 153
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 155
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==32:
                self.state = 154
                self.match(UniContractGrammar.READONLY)


            self.state = 157
            self.match(UniContractGrammar.PROPERTY)
            self.state = 158
            self.match(UniContractGrammar.IDENTIFIER)
            self.state = 159
            self.match(UniContractGrammar.SEMI)
            self.state = 160
            self.type_()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Interface_methodContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def METHOD(self):
            return self.getToken(UniContractGrammar.METHOD, 0)

        def IDENTIFIER(self):
            return self.getToken(UniContractGrammar.IDENTIFIER, 0)

        def LPAREN(self):
            return self.getToken(UniContractGrammar.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(UniContractGrammar.RPAREN, 0)

        def DOCUMENT_LINE(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.DOCUMENT_LINE)
            else:
                return self.getToken(UniContractGrammar.DOCUMENT_LINE, i)

        def decorator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.DecoratorContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.DecoratorContext,i)


        def ASYNC(self):
            return self.getToken(UniContractGrammar.ASYNC, 0)

        def ARROW(self):
            return self.getToken(UniContractGrammar.ARROW, 0)

        def type_(self):
            return self.getTypedRuleContext(UniContractGrammar.TypeContext,0)


        def interface_method_param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.Interface_method_paramContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.Interface_method_paramContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.COMMA)
            else:
                return self.getToken(UniContractGrammar.COMMA, i)

        def getRuleIndex(self):
            return UniContractGrammar.RULE_interface_method

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInterface_method" ):
                listener.enterInterface_method(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInterface_method" ):
                listener.exitInterface_method(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInterface_method" ):
                return visitor.visitInterface_method(self)
            else:
                return visitor.visitChildren(self)




    def interface_method(self):

        localctx = UniContractGrammar.Interface_methodContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_interface_method)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 165
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==39:
                self.state = 162
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 167
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 171
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==10:
                self.state = 168
                self.decorator()
                self.state = 173
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 175
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==33:
                self.state = 174
                self.match(UniContractGrammar.ASYNC)


            self.state = 177
            self.match(UniContractGrammar.METHOD)
            self.state = 178
            self.match(UniContractGrammar.IDENTIFIER)
            self.state = 179
            self.match(UniContractGrammar.LPAREN)

            self.state = 181
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 687194768384) != 0):
                self.state = 180
                self.interface_method_param()


            self.state = 187
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==2:
                self.state = 183
                self.match(UniContractGrammar.COMMA)
                self.state = 184
                self.interface_method_param()
                self.state = 189
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 190
            self.match(UniContractGrammar.RPAREN)
            self.state = 193
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==11:
                self.state = 191
                self.match(UniContractGrammar.ARROW)
                self.state = 192
                self.type_()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Interface_method_paramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(UniContractGrammar.IDENTIFIER, 0)

        def SEMI(self):
            return self.getToken(UniContractGrammar.SEMI, 0)

        def type_(self):
            return self.getTypedRuleContext(UniContractGrammar.TypeContext,0)


        def DOCUMENT_LINE(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.DOCUMENT_LINE)
            else:
                return self.getToken(UniContractGrammar.DOCUMENT_LINE, i)

        def decorator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.DecoratorContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.DecoratorContext,i)


        def getRuleIndex(self):
            return UniContractGrammar.RULE_interface_method_param

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInterface_method_param" ):
                listener.enterInterface_method_param(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInterface_method_param" ):
                listener.exitInterface_method_param(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInterface_method_param" ):
                return visitor.visitInterface_method_param(self)
            else:
                return visitor.visitChildren(self)




    def interface_method_param(self):

        localctx = UniContractGrammar.Interface_method_paramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_interface_method_param)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 198
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==39:
                self.state = 195
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 200
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 204
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==10:
                self.state = 201
                self.decorator()
                self.state = 206
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 207
            self.match(UniContractGrammar.IDENTIFIER)
            self.state = 208
            self.match(UniContractGrammar.SEMI)
            self.state = 209
            self.type_()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primitive_type(self):
            return self.getTypedRuleContext(UniContractGrammar.Primitive_typeContext,0)


        def reference_type(self):
            return self.getTypedRuleContext(UniContractGrammar.Reference_typeContext,0)


        def list_type(self):
            return self.getTypedRuleContext(UniContractGrammar.List_typeContext,0)


        def map_type(self):
            return self.getTypedRuleContext(UniContractGrammar.Map_typeContext,0)


        def getRuleIndex(self):
            return UniContractGrammar.RULE_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType" ):
                listener.enterType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType" ):
                listener.exitType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType" ):
                return visitor.visitType(self)
            else:
                return visitor.visitChildren(self)




    def type_(self):

        localctx = UniContractGrammar.TypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_type)
        try:
            self.state = 215
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [16, 17, 18, 19, 20, 21, 22, 23, 24, 25]:
                self.enterOuterAlt(localctx, 1)
                self.state = 211
                self.primitive_type()
                pass
            elif token in [29, 37]:
                self.enterOuterAlt(localctx, 2)
                self.state = 212
                self.reference_type()
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 3)
                self.state = 213
                self.list_type()
                pass
            elif token in [27]:
                self.enterOuterAlt(localctx, 4)
                self.state = 214
                self.map_type()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Primitive_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER(self):
            return self.getToken(UniContractGrammar.INTEGER, 0)

        def NUMBER(self):
            return self.getToken(UniContractGrammar.NUMBER, 0)

        def FLOAT(self):
            return self.getToken(UniContractGrammar.FLOAT, 0)

        def DATE(self):
            return self.getToken(UniContractGrammar.DATE, 0)

        def TIME(self):
            return self.getToken(UniContractGrammar.TIME, 0)

        def DATETIME(self):
            return self.getToken(UniContractGrammar.DATETIME, 0)

        def STRING(self):
            return self.getToken(UniContractGrammar.STRING, 0)

        def BOOLEAN(self):
            return self.getToken(UniContractGrammar.BOOLEAN, 0)

        def BYTES(self):
            return self.getToken(UniContractGrammar.BYTES, 0)

        def STREAM(self):
            return self.getToken(UniContractGrammar.STREAM, 0)

        def getRuleIndex(self):
            return UniContractGrammar.RULE_primitive_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimitive_type" ):
                listener.enterPrimitive_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimitive_type" ):
                listener.exitPrimitive_type(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimitive_type" ):
                return visitor.visitPrimitive_type(self)
            else:
                return visitor.visitChildren(self)




    def primitive_type(self):

        localctx = UniContractGrammar.Primitive_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_primitive_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 217
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 67043328) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Reference_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def qualifiedName(self):
            return self.getTypedRuleContext(UniContractGrammar.QualifiedNameContext,0)


        def EXTERNAL(self):
            return self.getToken(UniContractGrammar.EXTERNAL, 0)

        def LBARCKET(self):
            return self.getToken(UniContractGrammar.LBARCKET, 0)

        def STRING_LITERAL(self):
            return self.getToken(UniContractGrammar.STRING_LITERAL, 0)

        def RBRACKET(self):
            return self.getToken(UniContractGrammar.RBRACKET, 0)

        def getRuleIndex(self):
            return UniContractGrammar.RULE_reference_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReference_type" ):
                listener.enterReference_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReference_type" ):
                listener.exitReference_type(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReference_type" ):
                return visitor.visitReference_type(self)
            else:
                return visitor.visitChildren(self)




    def reference_type(self):

        localctx = UniContractGrammar.Reference_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_reference_type)
        try:
            self.state = 224
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [37]:
                self.enterOuterAlt(localctx, 1)
                self.state = 219
                self.qualifiedName()
                pass
            elif token in [29]:
                self.enterOuterAlt(localctx, 2)
                self.state = 220
                self.match(UniContractGrammar.EXTERNAL)
                self.state = 221
                self.match(UniContractGrammar.LBARCKET)
                self.state = 222
                self.match(UniContractGrammar.STRING_LITERAL)
                self.state = 223
                self.match(UniContractGrammar.RBRACKET)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class List_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LIST(self):
            return self.getToken(UniContractGrammar.LIST, 0)

        def LBARCKET(self):
            return self.getToken(UniContractGrammar.LBARCKET, 0)

        def type_(self):
            return self.getTypedRuleContext(UniContractGrammar.TypeContext,0)


        def RBRACKET(self):
            return self.getToken(UniContractGrammar.RBRACKET, 0)

        def getRuleIndex(self):
            return UniContractGrammar.RULE_list_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterList_type" ):
                listener.enterList_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitList_type" ):
                listener.exitList_type(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitList_type" ):
                return visitor.visitList_type(self)
            else:
                return visitor.visitChildren(self)




    def list_type(self):

        localctx = UniContractGrammar.List_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_list_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 226
            self.match(UniContractGrammar.LIST)
            self.state = 227
            self.match(UniContractGrammar.LBARCKET)
            self.state = 228
            self.type_()
            self.state = 229
            self.match(UniContractGrammar.RBRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Map_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MAP(self):
            return self.getToken(UniContractGrammar.MAP, 0)

        def LBARCKET(self):
            return self.getToken(UniContractGrammar.LBARCKET, 0)

        def type_(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.TypeContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.TypeContext,i)


        def COMMA(self):
            return self.getToken(UniContractGrammar.COMMA, 0)

        def RBRACKET(self):
            return self.getToken(UniContractGrammar.RBRACKET, 0)

        def getRuleIndex(self):
            return UniContractGrammar.RULE_map_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMap_type" ):
                listener.enterMap_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMap_type" ):
                listener.exitMap_type(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMap_type" ):
                return visitor.visitMap_type(self)
            else:
                return visitor.visitChildren(self)




    def map_type(self):

        localctx = UniContractGrammar.Map_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_map_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 231
            self.match(UniContractGrammar.MAP)
            self.state = 232
            self.match(UniContractGrammar.LBARCKET)
            self.state = 233
            self.type_()
            self.state = 234
            self.match(UniContractGrammar.COMMA)
            self.state = 235
            self.type_()
            self.state = 236
            self.match(UniContractGrammar.RBRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DecoratorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AT(self):
            return self.getToken(UniContractGrammar.AT, 0)

        def IDENTIFIER(self):
            return self.getToken(UniContractGrammar.IDENTIFIER, 0)

        def LPAREN(self):
            return self.getToken(UniContractGrammar.LPAREN, 0)

        def decorator_param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.Decorator_paramContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.Decorator_paramContext,i)


        def RPAREN(self):
            return self.getToken(UniContractGrammar.RPAREN, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.COMMA)
            else:
                return self.getToken(UniContractGrammar.COMMA, i)

        def getRuleIndex(self):
            return UniContractGrammar.RULE_decorator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDecorator" ):
                listener.enterDecorator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDecorator" ):
                listener.exitDecorator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDecorator" ):
                return visitor.visitDecorator(self)
            else:
                return visitor.visitChildren(self)




    def decorator(self):

        localctx = UniContractGrammar.DecoratorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_decorator)
        self._la = 0 # Token type
        try:
            self.state = 253
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 238
                self.match(UniContractGrammar.AT)
                self.state = 239
                self.match(UniContractGrammar.IDENTIFIER)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 240
                self.match(UniContractGrammar.AT)
                self.state = 241
                self.match(UniContractGrammar.IDENTIFIER)
                self.state = 242
                self.match(UniContractGrammar.LPAREN)
                self.state = 243
                self.decorator_param()
                self.state = 248
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==2:
                    self.state = 244
                    self.match(UniContractGrammar.COMMA)
                    self.state = 245
                    self.decorator_param()
                    self.state = 250
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 251
                self.match(UniContractGrammar.RPAREN)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Decorator_paramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def qualifiedName(self):
            return self.getTypedRuleContext(UniContractGrammar.QualifiedNameContext,0)


        def INTEGER_CONSTANS(self):
            return self.getToken(UniContractGrammar.INTEGER_CONSTANS, 0)

        def NUMBER_CONSTANS(self):
            return self.getToken(UniContractGrammar.NUMBER_CONSTANS, 0)

        def STRING_LITERAL(self):
            return self.getToken(UniContractGrammar.STRING_LITERAL, 0)

        def getRuleIndex(self):
            return UniContractGrammar.RULE_decorator_param

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDecorator_param" ):
                listener.enterDecorator_param(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDecorator_param" ):
                listener.exitDecorator_param(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDecorator_param" ):
                return visitor.visitDecorator_param(self)
            else:
                return visitor.visitChildren(self)




    def decorator_param(self):

        localctx = UniContractGrammar.Decorator_paramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_decorator_param)
        try:
            self.state = 259
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [37]:
                self.enterOuterAlt(localctx, 1)
                self.state = 255
                self.qualifiedName()
                pass
            elif token in [34]:
                self.enterOuterAlt(localctx, 2)
                self.state = 256
                self.match(UniContractGrammar.INTEGER_CONSTANS)
                pass
            elif token in [35]:
                self.enterOuterAlt(localctx, 3)
                self.state = 257
                self.match(UniContractGrammar.NUMBER_CONSTANS)
                pass
            elif token in [36]:
                self.enterOuterAlt(localctx, 4)
                self.state = 258
                self.match(UniContractGrammar.STRING_LITERAL)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QualifiedNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.IDENTIFIER)
            else:
                return self.getToken(UniContractGrammar.IDENTIFIER, i)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.DOT)
            else:
                return self.getToken(UniContractGrammar.DOT, i)

        def getRuleIndex(self):
            return UniContractGrammar.RULE_qualifiedName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQualifiedName" ):
                listener.enterQualifiedName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQualifiedName" ):
                listener.exitQualifiedName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQualifiedName" ):
                return visitor.visitQualifiedName(self)
            else:
                return visitor.visitChildren(self)




    def qualifiedName(self):

        localctx = UniContractGrammar.QualifiedNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_qualifiedName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 261
            self.match(UniContractGrammar.IDENTIFIER)
            self.state = 266
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 262
                self.match(UniContractGrammar.DOT)
                self.state = 263
                self.match(UniContractGrammar.IDENTIFIER)
                self.state = 268
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InheritsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INHERITS(self):
            return self.getToken(UniContractGrammar.INHERITS, 0)

        def qualifiedName(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.QualifiedNameContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.QualifiedNameContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.COMMA)
            else:
                return self.getToken(UniContractGrammar.COMMA, i)

        def getRuleIndex(self):
            return UniContractGrammar.RULE_inherits

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInherits" ):
                listener.enterInherits(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInherits" ):
                listener.exitInherits(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInherits" ):
                return visitor.visitInherits(self)
            else:
                return visitor.visitChildren(self)




    def inherits(self):

        localctx = UniContractGrammar.InheritsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_inherits)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 269
            self.match(UniContractGrammar.INHERITS)
            self.state = 270
            self.qualifiedName()
            self.state = 275
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==2:
                self.state = 271
                self.match(UniContractGrammar.COMMA)
                self.state = 272
                self.qualifiedName()
                self.state = 277
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnumContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENUM(self):
            return self.getToken(UniContractGrammar.ENUM, 0)

        def IDENTIFIER(self):
            return self.getToken(UniContractGrammar.IDENTIFIER, 0)

        def LCURLY(self):
            return self.getToken(UniContractGrammar.LCURLY, 0)

        def RCURLY(self):
            return self.getToken(UniContractGrammar.RCURLY, 0)

        def DOCUMENT_LINE(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.DOCUMENT_LINE)
            else:
                return self.getToken(UniContractGrammar.DOCUMENT_LINE, i)

        def decorator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.DecoratorContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.DecoratorContext,i)


        def enum_element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.Enum_elementContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.Enum_elementContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.COMMA)
            else:
                return self.getToken(UniContractGrammar.COMMA, i)

        def getRuleIndex(self):
            return UniContractGrammar.RULE_enum

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnum" ):
                listener.enterEnum(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnum" ):
                listener.exitEnum(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnum" ):
                return visitor.visitEnum(self)
            else:
                return visitor.visitChildren(self)




    def enum(self):

        localctx = UniContractGrammar.EnumContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_enum)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 281
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==39:
                self.state = 278
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 283
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 287
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==10:
                self.state = 284
                self.decorator()
                self.state = 289
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 290
            self.match(UniContractGrammar.ENUM)
            self.state = 291
            self.match(UniContractGrammar.IDENTIFIER)
            self.state = 292
            self.match(UniContractGrammar.LCURLY)
            self.state = 294
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 687194768384) != 0):
                self.state = 293
                self.enum_element()


            self.state = 300
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==2:
                self.state = 296
                self.match(UniContractGrammar.COMMA)
                self.state = 297
                self.enum_element()
                self.state = 302
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 303
            self.match(UniContractGrammar.RCURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Enum_elementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(UniContractGrammar.IDENTIFIER, 0)

        def DOCUMENT_LINE(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.DOCUMENT_LINE)
            else:
                return self.getToken(UniContractGrammar.DOCUMENT_LINE, i)

        def decorator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.DecoratorContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.DecoratorContext,i)


        def getRuleIndex(self):
            return UniContractGrammar.RULE_enum_element

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnum_element" ):
                listener.enterEnum_element(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnum_element" ):
                listener.exitEnum_element(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnum_element" ):
                return visitor.visitEnum_element(self)
            else:
                return visitor.visitChildren(self)




    def enum_element(self):

        localctx = UniContractGrammar.Enum_elementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_enum_element)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 308
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==39:
                self.state = 305
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 310
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 314
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==10:
                self.state = 311
                self.decorator()
                self.state = 316
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 317
            self.match(UniContractGrammar.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





