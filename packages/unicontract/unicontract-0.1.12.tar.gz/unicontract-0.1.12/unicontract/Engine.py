from antlr4.error.ErrorListener import ErrorListener
from antlr4 import *
from typing import Dict
from unicontract.grammar import *
from unicontract.elements.ElementBuilder import *


class Source:
    def __init__(self):
        self.fileName: str = None
        self.content: str = None

    @staticmethod
    def CreateFromText(content, fileName="internal string"):
        source = Source()
        source.content = content
        source.fileName = fileName
        return source

    @staticmethod
    def CreateFromFile(fileName):
        source = Source()
        source.fileName = fileName
        with open(fileName, 'r') as file:
            source.content = file.read()
        return source


class Session:
    def __init__(self, source: Source):
        self.source: Source = source
        self.syntaxTree: UniContractGrammar.ContractContext = []
        self.diagnostics: List[Diagnostic] = []
        self.main: contract = None
        self.imports: Dict[str, contract] = {}

    def HasDiagnostic(self):
        if (len(self.diagnostics) > 0):
            return True
        return False

    def HasAnyError(self):
        for msg in self.diagnostics:
            if (msg.severity == Diagnostic.Severity.Error):
                return True
        return False

    def HasAnyWarning(self):
        for msg in self.diagnostics:
            if (msg.severity == Diagnostic.Severity.Warning):
                return True
        return False

    def PrintDiagnostics(self):
        for msg in self.diagnostics:
            print(f"{msg.toText()}")

    def ClearDiagnostics(self):
        self.diagnostics.clear()

    def ReportDiagnostic(self, message, severity, fileName="", line=0, column=0):
        diagnostic: Diagnostic = Diagnostic()
        diagnostic.severity = severity
        diagnostic.fileName = fileName
        diagnostic.line = line
        diagnostic.column = column
        diagnostic.message = message
        self.diagnostics.append(diagnostic)


class Engine:
    def __init__(self, configuration: Dict[str, str]={}):
        self.configuration: Dict[str, str] = configuration

    def Build(self, session: Session):
        session.syntaxTree = self.__create_syntax_tree(session.source, session)
        session.main = self.__create_element_tree(session.syntaxTree, session.source, session)
        session.main = self.__merge_contracts(session)

        return session.main

    def __create_syntax_tree(self, source: Source, session: Session):
        lexer = UniContractLexer(InputStream(source.content))
        grammar = UniContractGrammar(CommonTokenStream(lexer))

        error_listener = Engine.__syntaxErrorListener__(source.fileName, session)
        grammar.removeErrorListeners()
        grammar.addErrorListener(error_listener)

        return grammar.contract()

    def __create_element_tree(self, syntaxTree: UniContractGrammar.ContractContext, source: Source, session: Session):
        visitor = ElementBuilder(source.fileName)

        _contract: contract = visitor.visit(syntaxTree)

        for _import in _contract.imports:
            if( _import.kind == import_.Kind.ExternalNamespace):
                continue
            if (_import in session.imports):
                imported_contract = session.imports[_import]
            else:
                imported_contract = self.__import_contract(_import.value, session)
                session.imports[_import] = imported_contract

        return _contract

    def __import_contract(self, import_name: qualified_name, session: Session):
        import_source = Source.CreateFromFile(import_name.getText()+".contract")
        import_syntaxTree = self.__create_syntax_tree(import_source, session)
        import_contract = self.__create_element_tree(import_syntaxTree, import_source, session)

        return import_contract

    def __merge_contracts( self, session: Session ):

        for imported_contract in session.imports.values():
            if(imported_contract is session.main):
                continue

            for imported_namespace in imported_contract.namespaces:
                # find domain in merged
                namespace_already: namespace = self.__find_namespace_by_name(imported_namespace.name,session)
                if (namespace_already == None):
                    # append domain to merged
                    session.main.namespaces.append(imported_namespace)
                else:
                    # merge enums
                    for imported_enum in imported_namespace.enums:
                        imported_enum.parent = namespace_already
                        namespace_already.enums.append(imported_enum)
                    
                    # merge interfaces
                    for imported_interface in imported_namespace.interfaces:
                        imported_interface.parent = namespace_already
                        namespace_already.interfaces.append(imported_interface)

        return session.main
    
    def __find_namespace_by_name(namespace_name:qualified_name,session: Session):
        for namespace in session.main.namespaces:
            if (namespace.name.getText() == namespace_name.getText()):
                return namespace

        return None
      

    class __syntaxErrorListener__(ErrorListener):
        def __init__(self, fileName, session: Session):
            super(Engine.__syntaxErrorListener__, self).__init__()
            self.fileName = fileName
            self.session = session

        def syntaxError(self, recognizer, offendingSymbol, line, column, message, e):
            self.session.ReportDiagnostic(message, Diagnostic.Severity.Error, self.fileName, line, column)


class Diagnostic:
    def __init__(self):
        self.severity: Diagnostic.Severity = Diagnostic.Severity.Message
        self.fileName: str = None
        self.line: int = None
        self.column: int = None
        self.message: int = None

    def toText(self):
        return f"{self.fileName}({self.line},{self.column}): {self.severity} :{self.message}"

    class Severity(Enum):
        Message = 1,
        Warning = 2,
        Error = 3,
