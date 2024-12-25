import os
from pathlib import Path
from antlr4.error.ErrorListener import ErrorListener
from antlr4 import *
from typing import Dict
from unicontract.grammar import *
from unicontract.elements.ElementBuilder import *

class Source:
    """
    Represents the source of a contract, which could be a file or a text string.
    Provides methods to create Source instances from either.
    """
    def __init__(self):
        self.fileName: str = None
        self.content: str = None

    @staticmethod
    def CreateFromText(content, fileName="internal string"):
        """
        Creates a Source instance from a given text content.
        """
        source = Source()
        source.content = content
        source.fileName = fileName
        return source

    @staticmethod
    def CreateFromFile(fileName):
        """
        Creates a Source instance from a file.
        Reads the content of the file.
        """
        source = Source()
        # Normalize and get the absolute path of the file
        source.fileName = os.path.normpath(os.path.abspath(fileName))
        # Open and read the file content
        with open(fileName, 'r') as file:
            source.content = file.read()
        return source

class Session:
    """
    Manages the state of a contract processing session, including diagnostics and syntax trees.
    """
    def __init__(self, source: Source):
        self.source: Source = source
        self.syntaxTree: UniContractGrammar.ContractContext = []
        self.diagnostics: List[Diagnostic] = []
        self.main: contract = None
        self.all: Dict[str, contract] = {}

    def HasDiagnostic(self):
        """
        Checks if there are any diagnostics recorded.
        """
        # Return true if diagnostics list is not empty
        return len(self.diagnostics) > 0

    def HasAnyError(self):
        """
        Checks if there are any errors in diagnostics.
        """
        # Iterate through diagnostics and look for errors
        for msg in self.diagnostics:
            if msg.severity == Diagnostic.Severity.Error:
                return True
        return False

    def HasAnyWarning(self):
        """
        Checks if there are any warnings in diagnostics.
        """
        # Iterate through diagnostics and look for warnings
        for msg in self.diagnostics:
            if msg.severity == Diagnostic.Severity.Warning:
                return True
        return False

    def PrintDiagnostics(self):
        """
        Prints all recorded diagnostics.
        """
        for msg in self.diagnostics:
            print(f"{msg.toText()}")

    def ClearDiagnostics(self):
        """
        Clears all diagnostics from the session.
        """
        self.diagnostics.clear()

    def ReportDiagnostic(self, message, severity, fileName="", line=0, column=0):
        """
        Records a new diagnostic message.
        """
        # Create a new Diagnostic instance and populate its fields
        diagnostic: Diagnostic = Diagnostic()
        diagnostic.severity = severity
        diagnostic.fileName = fileName
        diagnostic.line = line
        diagnostic.column = column
        diagnostic.message = message
        # Append the diagnostic to the list
        self.diagnostics.append(diagnostic)

class Engine:
    """
    Processes contract sources, generating syntax and element trees.
    """
    def __init__(self, configuration: Dict[str, str] = {}):
        self.configuration: Dict[str, str] = configuration

    def Build(self, session: Session):
        """
        Builds the contract by generating syntax and element trees.
        """
        # Create syntax tree from the source
        session.syntaxTree = self.__create_syntax_tree(session.source, session)
        # Create element tree from the syntax tree
        session.main = self.__create_element_tree(session.syntaxTree, session.source, session)
        # Merge contracts into the main contract
        session.main = self.__merge_contracts(session)

        return session.main

    def __create_syntax_tree(self, source: Source, session: Session):
        """
        Generates a syntax tree for the given source.
        """
        # Initialize the lexer and parser for the source content
        lexer = UniContractLexer(InputStream(source.content))
        grammar = UniContractGrammar(CommonTokenStream(lexer))

        # Set up error handling
        error_listener = Engine.__syntaxErrorListener__(source.fileName, session)
        grammar.removeErrorListeners()
        grammar.addErrorListener(error_listener)

        return grammar.contract()

    def __create_element_tree(self, syntaxTree: UniContractGrammar.ContractContext, source: Source, session: Session):
        """
        Creates an element tree from the syntax tree.
        """
        # Build elements using a visitor pattern
        visitor = ElementBuilder(source.fileName)
        _contract: contract = visitor.visit(syntaxTree)
        # Store the contract in the session
        session.all[source.fileName] = _contract

        # Process imported contracts
        for _import in _contract.imports:
            import_path = os.path.normpath(os.path.join(Path(source.fileName).parent, _import.name + ".contract"))
            # Import only if not already processed
            if import_path not in session.all:
                imported_contract = self.__import_contract(import_path, _import, session)
            else:
                imported_contract = session.all[import_path]
            _import.contract = imported_contract

        return _contract

    def __import_contract(self, import_path: str, _import: import_, session: Session):
        """
        Imports a contract from a given path.
        """
        # Check if the file exists
        if not os.path.exists(import_path):
            session.ReportDiagnostic(
                f"import '{import_path}' file not found",
                Diagnostic.Severity.Error,
                _import.fileName,
                _import.line,
                _import.column
            )
        # Create source from file and build its syntax and element trees
        import_source = Source.CreateFromFile(import_path)
        import_syntaxTree = self.__create_syntax_tree(import_source, session)
        imported_contract = self.__create_element_tree(import_syntaxTree, import_source, session)

        return imported_contract

    def __merge_contracts(self, session: Session):
        """
        Merges all imported contracts into the main contract.
        """
        for imported_contract in session.all.values():
            # Skip the main contract
            if imported_contract is session.main:
                continue

            for imported_namespace in imported_contract.namespaces:
                # Find or create the namespace in the main contract
                namespace_already: namespace = self.__find_namespace_by_name(imported_namespace.name, session)
                if namespace_already is None:
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

    def __find_namespace_by_name(self, namespace_name: qualified_name, session: Session):
        """
        Finds a namespace by its name in the main contract.
        """
        for namespace in session.main.namespaces:
            if namespace.name.getText() == namespace_name.getText():
                return namespace

        return None

    class __syntaxErrorListener__(ErrorListener):
        """
        Custom error listener for syntax errors during parsing.
        """
        def __init__(self, fileName, session: Session):
            super(Engine.__syntaxErrorListener__, self).__init__()
            self.fileName = fileName
            self.session = session

        def syntaxError(self, recognizer, offendingSymbol, line, column, message, e):
            # Report syntax error as a diagnostic
            self.session.ReportDiagnostic(
                message,
                Diagnostic.Severity.Error,
                self.fileName,
                line,
                column
            )

class Diagnostic:
    """
    Represents a diagnostic message with severity, location, and text.
    """
    def __init__(self):
        self.severity: Diagnostic.Severity = Diagnostic.Severity.Message
        self.fileName: str = None
        self.line: int = None
        self.column: int = None
        self.message: int = None

    def toText(self):
        """
        Converts the diagnostic to a textual representation.
        """
        return f"{self.fileName}({self.line},{self.column}): {self.severity} :{self.message}"

    class Severity(Enum):
        """
        Enumeration of diagnostic severity levels.
        """
        Message = 1
        Warning = 2
        Error = 3
