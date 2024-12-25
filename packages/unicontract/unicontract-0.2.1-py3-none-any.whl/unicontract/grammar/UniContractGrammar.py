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
        4,1,40,253,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,1,0,
        5,0,42,8,0,10,0,12,0,45,9,0,1,0,5,0,48,8,0,10,0,12,0,51,9,0,1,0,
        1,0,1,1,5,1,56,8,1,10,1,12,1,59,9,1,1,1,1,1,1,1,1,2,5,2,65,8,2,10,
        2,12,2,68,9,2,1,2,1,2,1,2,1,2,5,2,74,8,2,10,2,12,2,77,9,2,1,2,1,
        2,1,3,1,3,3,3,83,8,3,1,4,5,4,86,8,4,10,4,12,4,89,9,4,1,4,1,4,1,4,
        3,4,94,8,4,1,4,3,4,97,8,4,1,4,1,4,5,4,101,8,4,10,4,12,4,104,9,4,
        1,4,1,4,1,5,1,5,1,5,3,5,111,8,5,1,6,5,6,114,8,6,10,6,12,6,117,9,
        6,1,6,3,6,120,8,6,1,6,1,6,1,6,1,6,1,6,1,7,5,7,128,8,7,10,7,12,7,
        131,9,7,1,7,3,7,134,8,7,1,7,1,7,1,7,3,7,139,8,7,1,7,1,7,3,7,143,
        8,7,1,7,1,7,5,7,147,8,7,10,7,12,7,150,9,7,1,7,1,7,1,7,3,7,155,8,
        7,1,8,5,8,158,8,8,10,8,12,8,161,9,8,1,8,1,8,1,8,1,8,1,9,1,9,1,9,
        1,9,3,9,171,8,9,1,10,1,10,1,11,1,11,3,11,177,8,11,1,12,1,12,1,12,
        1,12,1,12,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,14,1,14,1,14,5,14,
        194,8,14,10,14,12,14,197,9,14,1,15,1,15,1,15,1,15,5,15,203,8,15,
        10,15,12,15,206,9,15,1,16,5,16,209,8,16,10,16,12,16,212,9,16,1,16,
        1,16,1,16,1,16,3,16,218,8,16,1,16,1,16,5,16,222,8,16,10,16,12,16,
        225,9,16,1,16,1,16,1,17,5,17,230,8,17,10,17,12,17,233,9,17,1,17,
        1,17,1,18,1,18,1,18,1,18,5,18,241,8,18,10,18,12,18,244,9,18,1,18,
        1,18,1,19,1,19,1,19,3,19,251,8,19,1,19,0,0,20,0,2,4,6,8,10,12,14,
        16,18,20,22,24,26,28,30,32,34,36,38,0,1,1,0,17,26,265,0,43,1,0,0,
        0,2,57,1,0,0,0,4,66,1,0,0,0,6,82,1,0,0,0,8,87,1,0,0,0,10,110,1,0,
        0,0,12,115,1,0,0,0,14,129,1,0,0,0,16,159,1,0,0,0,18,170,1,0,0,0,
        20,172,1,0,0,0,22,174,1,0,0,0,24,178,1,0,0,0,26,183,1,0,0,0,28,190,
        1,0,0,0,30,198,1,0,0,0,32,210,1,0,0,0,34,231,1,0,0,0,36,236,1,0,
        0,0,38,247,1,0,0,0,40,42,3,2,1,0,41,40,1,0,0,0,42,45,1,0,0,0,43,
        41,1,0,0,0,43,44,1,0,0,0,44,49,1,0,0,0,45,43,1,0,0,0,46,48,3,4,2,
        0,47,46,1,0,0,0,48,51,1,0,0,0,49,47,1,0,0,0,49,50,1,0,0,0,50,52,
        1,0,0,0,51,49,1,0,0,0,52,53,5,0,0,1,53,1,1,0,0,0,54,56,5,38,0,0,
        55,54,1,0,0,0,56,59,1,0,0,0,57,55,1,0,0,0,57,58,1,0,0,0,58,60,1,
        0,0,0,59,57,1,0,0,0,60,61,5,13,0,0,61,62,3,28,14,0,62,3,1,0,0,0,
        63,65,5,38,0,0,64,63,1,0,0,0,65,68,1,0,0,0,66,64,1,0,0,0,66,67,1,
        0,0,0,67,69,1,0,0,0,68,66,1,0,0,0,69,70,5,15,0,0,70,71,3,28,14,0,
        71,75,5,6,0,0,72,74,3,6,3,0,73,72,1,0,0,0,74,77,1,0,0,0,75,73,1,
        0,0,0,75,76,1,0,0,0,76,78,1,0,0,0,77,75,1,0,0,0,78,79,5,7,0,0,79,
        5,1,0,0,0,80,83,3,8,4,0,81,83,3,32,16,0,82,80,1,0,0,0,82,81,1,0,
        0,0,83,7,1,0,0,0,84,86,5,38,0,0,85,84,1,0,0,0,86,89,1,0,0,0,87,85,
        1,0,0,0,87,88,1,0,0,0,88,90,1,0,0,0,89,87,1,0,0,0,90,91,5,14,0,0,
        91,93,5,36,0,0,92,94,3,36,18,0,93,92,1,0,0,0,93,94,1,0,0,0,94,96,
        1,0,0,0,95,97,3,30,15,0,96,95,1,0,0,0,96,97,1,0,0,0,97,98,1,0,0,
        0,98,102,5,6,0,0,99,101,3,10,5,0,100,99,1,0,0,0,101,104,1,0,0,0,
        102,100,1,0,0,0,102,103,1,0,0,0,103,105,1,0,0,0,104,102,1,0,0,0,
        105,106,5,7,0,0,106,9,1,0,0,0,107,111,3,14,7,0,108,111,3,12,6,0,
        109,111,3,32,16,0,110,107,1,0,0,0,110,108,1,0,0,0,110,109,1,0,0,
        0,111,11,1,0,0,0,112,114,5,38,0,0,113,112,1,0,0,0,114,117,1,0,0,
        0,115,113,1,0,0,0,115,116,1,0,0,0,116,119,1,0,0,0,117,115,1,0,0,
        0,118,120,5,33,0,0,119,118,1,0,0,0,119,120,1,0,0,0,120,121,1,0,0,
        0,121,122,5,31,0,0,122,123,5,36,0,0,123,124,5,3,0,0,124,125,3,18,
        9,0,125,13,1,0,0,0,126,128,5,38,0,0,127,126,1,0,0,0,128,131,1,0,
        0,0,129,127,1,0,0,0,129,130,1,0,0,0,130,133,1,0,0,0,131,129,1,0,
        0,0,132,134,5,34,0,0,133,132,1,0,0,0,133,134,1,0,0,0,134,135,1,0,
        0,0,135,136,5,32,0,0,136,138,5,36,0,0,137,139,3,36,18,0,138,137,
        1,0,0,0,138,139,1,0,0,0,139,140,1,0,0,0,140,142,5,4,0,0,141,143,
        3,16,8,0,142,141,1,0,0,0,142,143,1,0,0,0,143,148,1,0,0,0,144,145,
        5,2,0,0,145,147,3,16,8,0,146,144,1,0,0,0,147,150,1,0,0,0,148,146,
        1,0,0,0,148,149,1,0,0,0,149,151,1,0,0,0,150,148,1,0,0,0,151,154,
        5,5,0,0,152,153,5,10,0,0,153,155,3,18,9,0,154,152,1,0,0,0,154,155,
        1,0,0,0,155,15,1,0,0,0,156,158,5,38,0,0,157,156,1,0,0,0,158,161,
        1,0,0,0,159,157,1,0,0,0,159,160,1,0,0,0,160,162,1,0,0,0,161,159,
        1,0,0,0,162,163,5,36,0,0,163,164,5,3,0,0,164,165,3,18,9,0,165,17,
        1,0,0,0,166,171,3,20,10,0,167,171,3,22,11,0,168,171,3,24,12,0,169,
        171,3,26,13,0,170,166,1,0,0,0,170,167,1,0,0,0,170,168,1,0,0,0,170,
        169,1,0,0,0,171,19,1,0,0,0,172,173,7,0,0,0,173,21,1,0,0,0,174,176,
        3,28,14,0,175,177,3,36,18,0,176,175,1,0,0,0,176,177,1,0,0,0,177,
        23,1,0,0,0,178,179,5,27,0,0,179,180,5,8,0,0,180,181,3,18,9,0,181,
        182,5,9,0,0,182,25,1,0,0,0,183,184,5,28,0,0,184,185,5,8,0,0,185,
        186,3,18,9,0,186,187,5,2,0,0,187,188,3,18,9,0,188,189,5,9,0,0,189,
        27,1,0,0,0,190,195,5,36,0,0,191,192,5,1,0,0,192,194,5,36,0,0,193,
        191,1,0,0,0,194,197,1,0,0,0,195,193,1,0,0,0,195,196,1,0,0,0,196,
        29,1,0,0,0,197,195,1,0,0,0,198,199,5,29,0,0,199,204,3,28,14,0,200,
        201,5,2,0,0,201,203,3,28,14,0,202,200,1,0,0,0,203,206,1,0,0,0,204,
        202,1,0,0,0,204,205,1,0,0,0,205,31,1,0,0,0,206,204,1,0,0,0,207,209,
        5,38,0,0,208,207,1,0,0,0,209,212,1,0,0,0,210,208,1,0,0,0,210,211,
        1,0,0,0,211,213,1,0,0,0,212,210,1,0,0,0,213,214,5,16,0,0,214,215,
        5,36,0,0,215,217,5,6,0,0,216,218,3,34,17,0,217,216,1,0,0,0,217,218,
        1,0,0,0,218,223,1,0,0,0,219,220,5,2,0,0,220,222,3,34,17,0,221,219,
        1,0,0,0,222,225,1,0,0,0,223,221,1,0,0,0,223,224,1,0,0,0,224,226,
        1,0,0,0,225,223,1,0,0,0,226,227,5,7,0,0,227,33,1,0,0,0,228,230,5,
        38,0,0,229,228,1,0,0,0,230,233,1,0,0,0,231,229,1,0,0,0,231,232,1,
        0,0,0,232,234,1,0,0,0,233,231,1,0,0,0,234,235,5,36,0,0,235,35,1,
        0,0,0,236,237,5,11,0,0,237,242,3,38,19,0,238,239,5,2,0,0,239,241,
        3,38,19,0,240,238,1,0,0,0,241,244,1,0,0,0,242,240,1,0,0,0,242,243,
        1,0,0,0,243,245,1,0,0,0,244,242,1,0,0,0,245,246,5,12,0,0,246,37,
        1,0,0,0,247,250,5,36,0,0,248,249,5,35,0,0,249,251,3,28,14,0,250,
        248,1,0,0,0,250,251,1,0,0,0,251,39,1,0,0,0,30,43,49,57,66,75,82,
        87,93,96,102,110,115,119,129,133,138,142,148,154,159,170,176,195,
        204,210,217,223,231,242,250
    ]

class UniContractGrammar ( Parser ):

    grammarFileName = "UniContractGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'.'", "','", "':'", "'('", "')'", "'{'", 
                     "'}'", "'['", "']'", "'=>'", "'<'", "'>'", "'import'", 
                     "'interface'", "'namespace'", "'enum'", "'integer'", 
                     "'number'", "'float'", "'date'", "'time'", "'dateTime'", 
                     "'string'", "'boolean'", "'bytes'", "'stream'", "'list'", 
                     "'map'", "'inherits'", "'external'", "'property'", 
                     "'method'", "'readonly'", "'async'", "'constraint'" ]

    symbolicNames = [ "<INVALID>", "DOT", "COMMA", "SEMI", "LPAREN", "RPAREN", 
                      "LCURLY", "RCURLY", "LBARCKET", "RBRACKET", "ARROW", 
                      "LT", "GT", "IMPORT", "INTERFACE", "NAMESPACE", "ENUM", 
                      "INTEGER", "NUMBER", "FLOAT", "DATE", "TIME", "DATETIME", 
                      "STRING", "BOOLEAN", "BYTES", "STREAM", "LIST", "MAP", 
                      "INHERITS", "EXTERNAL", "PROPERTY", "METHOD", "READONLY", 
                      "ASYNC", "CONSTRAINT", "IDENTIFIER", "WS", "DOCUMENT_LINE", 
                      "LINE_COMMENT", "BLOCK_COMMENT" ]

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
    RULE_qualifiedName = 14
    RULE_inherits = 15
    RULE_enum = 16
    RULE_enum_element = 17
    RULE_generic = 18
    RULE_generic_type = 19

    ruleNames =  [ "contract", "import_rule", "namespace", "namespace_elements", 
                   "interface", "interface_element", "interface_property", 
                   "interface_method", "interface_method_param", "type", 
                   "primitive_type", "reference_type", "list_type", "map_type", 
                   "qualifiedName", "inherits", "enum", "enum_element", 
                   "generic", "generic_type" ]

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
    ARROW=10
    LT=11
    GT=12
    IMPORT=13
    INTERFACE=14
    NAMESPACE=15
    ENUM=16
    INTEGER=17
    NUMBER=18
    FLOAT=19
    DATE=20
    TIME=21
    DATETIME=22
    STRING=23
    BOOLEAN=24
    BYTES=25
    STREAM=26
    LIST=27
    MAP=28
    INHERITS=29
    EXTERNAL=30
    PROPERTY=31
    METHOD=32
    READONLY=33
    ASYNC=34
    CONSTRAINT=35
    IDENTIFIER=36
    WS=37
    DOCUMENT_LINE=38
    LINE_COMMENT=39
    BLOCK_COMMENT=40

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
            while _la==15 or _la==38:
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
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 54
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 59
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 60
            self.match(UniContractGrammar.IMPORT)
            self.state = 61
            self.qualifiedName()
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
            self.state = 66
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 63
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 68
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 69
            self.match(UniContractGrammar.NAMESPACE)
            self.state = 70
            self.qualifiedName()
            self.state = 71
            self.match(UniContractGrammar.LCURLY)
            self.state = 75
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 274877988864) != 0):
                self.state = 72
                self.namespace_elements()
                self.state = 77
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 78
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
            self.state = 82
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 80
                self.interface()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 81
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

        def generic(self):
            return self.getTypedRuleContext(UniContractGrammar.GenericContext,0)


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
            self.state = 87
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 84
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 89
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 90
            self.match(UniContractGrammar.INTERFACE)
            self.state = 91
            self.match(UniContractGrammar.IDENTIFIER)
            self.state = 93
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==11:
                self.state = 92
                self.generic()


            self.state = 96
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==29:
                self.state = 95
                self.inherits()


            self.state = 98
            self.match(UniContractGrammar.LCURLY)
            self.state = 102
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 307090227200) != 0):
                self.state = 99
                self.interface_element()
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
            self.state = 110
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 107
                self.interface_method()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 108
                self.interface_property()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 109
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
            self.state = 115
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 112
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 117
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 119
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==33:
                self.state = 118
                self.match(UniContractGrammar.READONLY)


            self.state = 121
            self.match(UniContractGrammar.PROPERTY)
            self.state = 122
            self.match(UniContractGrammar.IDENTIFIER)
            self.state = 123
            self.match(UniContractGrammar.SEMI)
            self.state = 124
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

        def ASYNC(self):
            return self.getToken(UniContractGrammar.ASYNC, 0)

        def generic(self):
            return self.getTypedRuleContext(UniContractGrammar.GenericContext,0)


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
            self.state = 129
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 126
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 131
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 133
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==34:
                self.state = 132
                self.match(UniContractGrammar.ASYNC)


            self.state = 135
            self.match(UniContractGrammar.METHOD)
            self.state = 136
            self.match(UniContractGrammar.IDENTIFIER)
            self.state = 138
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==11:
                self.state = 137
                self.generic()


            self.state = 140
            self.match(UniContractGrammar.LPAREN)

            self.state = 142
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==36 or _la==38:
                self.state = 141
                self.interface_method_param()


            self.state = 148
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==2:
                self.state = 144
                self.match(UniContractGrammar.COMMA)
                self.state = 145
                self.interface_method_param()
                self.state = 150
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 151
            self.match(UniContractGrammar.RPAREN)
            self.state = 154
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 152
                self.match(UniContractGrammar.ARROW)
                self.state = 153
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
            self.state = 159
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 156
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 161
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 162
            self.match(UniContractGrammar.IDENTIFIER)
            self.state = 163
            self.match(UniContractGrammar.SEMI)
            self.state = 164
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
            self.state = 170
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17, 18, 19, 20, 21, 22, 23, 24, 25, 26]:
                self.enterOuterAlt(localctx, 1)
                self.state = 166
                self.primitive_type()
                pass
            elif token in [36]:
                self.enterOuterAlt(localctx, 2)
                self.state = 167
                self.reference_type()
                pass
            elif token in [27]:
                self.enterOuterAlt(localctx, 3)
                self.state = 168
                self.list_type()
                pass
            elif token in [28]:
                self.enterOuterAlt(localctx, 4)
                self.state = 169
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
            self.state = 172
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 134086656) != 0)):
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


        def generic(self):
            return self.getTypedRuleContext(UniContractGrammar.GenericContext,0)


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
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 174
            self.qualifiedName()
            self.state = 176
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==11:
                self.state = 175
                self.generic()


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
            self.state = 178
            self.match(UniContractGrammar.LIST)
            self.state = 179
            self.match(UniContractGrammar.LBARCKET)
            self.state = 180
            self.type_()
            self.state = 181
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
            self.state = 183
            self.match(UniContractGrammar.MAP)
            self.state = 184
            self.match(UniContractGrammar.LBARCKET)
            self.state = 185
            self.type_()
            self.state = 186
            self.match(UniContractGrammar.COMMA)
            self.state = 187
            self.type_()
            self.state = 188
            self.match(UniContractGrammar.RBRACKET)
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
        self.enterRule(localctx, 28, self.RULE_qualifiedName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 190
            self.match(UniContractGrammar.IDENTIFIER)
            self.state = 195
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 191
                self.match(UniContractGrammar.DOT)
                self.state = 192
                self.match(UniContractGrammar.IDENTIFIER)
                self.state = 197
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
        self.enterRule(localctx, 30, self.RULE_inherits)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 198
            self.match(UniContractGrammar.INHERITS)
            self.state = 199
            self.qualifiedName()
            self.state = 204
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==2:
                self.state = 200
                self.match(UniContractGrammar.COMMA)
                self.state = 201
                self.qualifiedName()
                self.state = 206
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
        self.enterRule(localctx, 32, self.RULE_enum)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 210
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 207
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 212
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 213
            self.match(UniContractGrammar.ENUM)
            self.state = 214
            self.match(UniContractGrammar.IDENTIFIER)
            self.state = 215
            self.match(UniContractGrammar.LCURLY)
            self.state = 217
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==36 or _la==38:
                self.state = 216
                self.enum_element()


            self.state = 223
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==2:
                self.state = 219
                self.match(UniContractGrammar.COMMA)
                self.state = 220
                self.enum_element()
                self.state = 225
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 226
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
        self.enterRule(localctx, 34, self.RULE_enum_element)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 231
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 228
                self.match(UniContractGrammar.DOCUMENT_LINE)
                self.state = 233
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 234
            self.match(UniContractGrammar.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GenericContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LT(self):
            return self.getToken(UniContractGrammar.LT, 0)

        def generic_type(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UniContractGrammar.Generic_typeContext)
            else:
                return self.getTypedRuleContext(UniContractGrammar.Generic_typeContext,i)


        def GT(self):
            return self.getToken(UniContractGrammar.GT, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UniContractGrammar.COMMA)
            else:
                return self.getToken(UniContractGrammar.COMMA, i)

        def getRuleIndex(self):
            return UniContractGrammar.RULE_generic

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGeneric" ):
                listener.enterGeneric(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGeneric" ):
                listener.exitGeneric(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGeneric" ):
                return visitor.visitGeneric(self)
            else:
                return visitor.visitChildren(self)




    def generic(self):

        localctx = UniContractGrammar.GenericContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_generic)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 236
            self.match(UniContractGrammar.LT)
            self.state = 237
            self.generic_type()
            self.state = 242
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==2:
                self.state = 238
                self.match(UniContractGrammar.COMMA)
                self.state = 239
                self.generic_type()
                self.state = 244
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 245
            self.match(UniContractGrammar.GT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Generic_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(UniContractGrammar.IDENTIFIER, 0)

        def CONSTRAINT(self):
            return self.getToken(UniContractGrammar.CONSTRAINT, 0)

        def qualifiedName(self):
            return self.getTypedRuleContext(UniContractGrammar.QualifiedNameContext,0)


        def getRuleIndex(self):
            return UniContractGrammar.RULE_generic_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGeneric_type" ):
                listener.enterGeneric_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGeneric_type" ):
                listener.exitGeneric_type(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGeneric_type" ):
                return visitor.visitGeneric_type(self)
            else:
                return visitor.visitChildren(self)




    def generic_type(self):

        localctx = UniContractGrammar.Generic_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_generic_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 247
            self.match(UniContractGrammar.IDENTIFIER)
            self.state = 250
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==35:
                self.state = 248
                self.match(UniContractGrammar.CONSTRAINT)
                self.state = 249
                self.qualifiedName()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





