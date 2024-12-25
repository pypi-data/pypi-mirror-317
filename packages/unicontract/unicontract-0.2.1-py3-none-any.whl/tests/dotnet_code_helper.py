from io import StringIO
import os
import tempfile
from unicontract import *
from unicontract.emitters.DotnetEmitter import *


class dotnet_code_helper:

    @staticmethod
    def init_roslyn():
        from pathlib import Path
        from pythonnet import get_runtime_info, set_runtime
        set_runtime("coreclr")
        import clr
        print(get_runtime_info())

        clr.AddReference(str(Path("./tools/dotnet_dlls/netstandard2.0/Microsoft.CodeAnalysis.dll").resolve()))
        clr.AddReference(str(Path("./tools/dotnet_dlls/netstandard2.0/Microsoft.CodeAnalysis.CSharp.dll").resolve()))

    def compare_and_extract_diff(code1: str, code2: str, with_comments: bool = False, with_pragmas: bool = False) -> tuple[bool, int, str]:
        """
        Compares two strings and returns:
        - A boolean indicating if the strings are identical.
        - An integer representing the index of the first differing character (-1 if identical).
        - A string containing up to 30 characters from the differing part of the second string.

        :param str1: The first string to compare.
        :param str2: The second string to compare.
        :return: A tuple (is_equal, diff_index, diff_part).
        """
        code1 = dotnet_code_helper.__compress_code(code1, with_comments, with_pragmas)
        code2 = dotnet_code_helper.__compress_code(code2, with_comments, with_pragmas)

        # Find the first index where the strings differ
        diff_index = -1
        for i, (char1, char2) in enumerate(zip(code1, code2)):
            if char1 != char2:
                diff_index = i
                break

        # Handle cases where one string is a prefix of the other
        if diff_index == -1:
            if len(code1) == len(code2):
                return True, -1, "", ""  # Strings are identical
            diff_index = min(len(code1), len(code2))

        # Extract up to 30 characters from the differing part of str2
        diff_part_1 = code1[diff_index-10:diff_index + 50] if diff_index < len(code1) else ""
        diff_part_2 = code2[diff_index-10:diff_index + 50] if diff_index < len(code2) else ""

        # Return the result
        return False, diff_index, diff_part_1, diff_part_2

    @staticmethod
    def compare_by_text(code1: str, code2: str, with_comments: bool = False, with_pragmas: bool = False) -> bool:
        """
        Compares two pieces of code by compressing and normalizing them, then checking for equality.

        :param code1: The first code as a string.
        :param code2: The second code as a string.
        :param with_comments: Whether to include comments in the comparison.
        :param with_pragmas: Whether to include pragmas in the comparison.
        :return: True if the compressed versions of the code are identical, otherwise False.
        """
        compressed_code1 = dotnet_code_helper.__compress_code(code1, with_comments, with_pragmas)
        compressed_code2 = dotnet_code_helper.__compress_code(code2, with_comments, with_pragmas)

        return compressed_code1 == compressed_code2

    @staticmethod
    def __compress_code(code: str, with_comments: bool = False, with_pragmas: bool = False) -> str:
        """
        Compresses the given code by performing several transformations such as removing comments, pragmas, and white spaces.

        :param code: The input code as a string.
        :param with_comments: Whether to remove comments from the code.
        :param with_pragmas: Whether to remove pragmas from the code.
        :return: The compressed code as a string.
        """
        compressed_code = code

        if with_comments == False:
            compressed_code = dotnet_code_helper.__remove_line_comments(compressed_code)

        if with_pragmas == False:
            compressed_code = dotnet_code_helper.__remove_line_pragmas(compressed_code)

        compressed_code = dotnet_code_helper.__resolve_brackets(compressed_code)
        compressed_code = dotnet_code_helper.__resolve_operators(compressed_code)
        compressed_code = dotnet_code_helper.__resolve_commas(compressed_code)
        compressed_code = dotnet_code_helper.__remove_whitespaces(compressed_code)
        compressed_code = dotnet_code_helper.__remove_empty_lines(compressed_code)

        return compressed_code.replace("\r", "")

    @staticmethod
    def __remove_line_comments(code: str) -> str:
        """
        Removes line comments from the code.

        :param code: The input code as a string.
        :return: The code without line comments.
        """
        reader = StringIO(code)
        writer = StringIO()

        while True:
            line = reader.readline()
            if not line:  # End of the input
                break

            # If it's not a line comment, write it to the output
            if not dotnet_code_helper.__is_line_comment(line):
                writer.write(line)

        return writer.getvalue()

    @staticmethod
    def __remove_line_pragmas(code: str) -> str:
        """
        Removes line pragmas from the code.

        :param code: The input code as a string.
        :return: The code without line pragmas.
        """
        reader = StringIO(code)
        writer = StringIO()

        while True:
            line = reader.readline()
            if not line:  # End of the input
                break

            # If it's not a line pragma, write it to the output
            if not dotnet_code_helper.__is_line_pragma(line):
                writer.write(line)

        return writer.getvalue()

    @staticmethod
    def __remove_empty_lines(code: str) -> str:
        """
        Removes empty lines from the code.

        :param code: The input code as a string.
        :return: The code without empty lines.
        """
        reader = StringIO(code)
        writer = StringIO()

        while True:
            line = reader.readline()
            if not line:  # End of the input
                break

            # If it's not an empty line, write it to the output
            if not dotnet_code_helper.__is_empty_line(line):
                writer.write(line)

        return writer.getvalue()

    @staticmethod
    def __remove_whitespaces(code: str) -> str:
        """
        Removes unnecessary whitespaces from the beginning and end of lines,
        replaces double spaces with single spaces, and replaces tabs with spaces.

        :param code: The input code as a string.
        :return: The code with normalized whitespace.
        """
        reader = StringIO(code)
        writer = StringIO()

        while True:
            line = reader.readline()
            if not line:
                break

            line = line.rstrip("\n")

            if len(line) > 0:
                # Remove leading whitespaces
                while line and line[0].isspace():
                    line = line[1:]

                # Remove trailing whitespaces
                while line and line[-1].isspace():
                    line = line[:-1]

                # Replace double spaces with single spaces and tabs with spaces
                before_length = 0
                after_length = 0
                while True:
                    before_length = len(line)
                    line = line.replace("  ", "")  # Replace double spaces
                    line = line.replace("\t", " ")  # Replace tabs with spaces
                    after_length = len(line)

                    if before_length == after_length:
                        break

            writer.write(line + "\n")

        return writer.getvalue()

    @staticmethod
    def __is_line_comment(line: str) -> bool:
        """
        Checks if the given line is a comment.

        :param line: A single line of code.
        :return: True if the line is a comment, otherwise False.
        """
        line = dotnet_code_helper.__remove_whitespaces(line)

        if len(line) < 2:
            return False
        return line.startswith("//")

    @staticmethod
    def __is_line_pragma(line: str) -> bool:
        """
        Checks if the given line is a pragma directive.

        :param line: A single line of code.
        :return: True if the line is a pragma directive, otherwise False.
        """
        line = dotnet_code_helper.__remove_whitespaces(line)

        return line.startswith("#line")

    @staticmethod
    def __is_empty_line(line: str) -> bool:
        """
        Checks if the given line is empty or contains only whitespace characters.

        :param line: A single line of code.
        :return: True if the line is empty or contains only whitespace, otherwise False.
        """
        return not line.strip()

    @staticmethod
    def __resolve_brackets(code: str) -> str:
        """
        Resolves bracket spacing issues by removing unnecessary spaces
        and adjusting line endings for brackets.

        :param code: The input code as a string.
        :return: The code with resolved bracket spacing.
        """
        code = dotnet_code_helper.__remove_whitespaces(code)

        reader = StringIO(code)
        writer = StringIO()

        while True:
            line = reader.readline()
            if not line:
                break

            line = (line.replace(" (", "(")
                    .replace("( ", "(")
                    .replace(") ", ")")
                    .replace(" )", ")")
                    .replace(" {", "{")
                    .replace("{ ", "{")
                    .replace("} ", "}")
                    .replace(" }", "}"))

            # Adjust lines ending with '{'
            if len(line) > 2 and line.endswith("{"):
                line = line[:-1].strip() + "\n{"

            writer.write(line + "\n")

        return writer.getvalue()

    @staticmethod
    def __resolve_commas(code: str) -> str:
        """
        Resolves spacing issues around commas.

        :param code: The input code as a string.
        :return: The code with resolved comma spacing.
        """
        code = dotnet_code_helper.__remove_whitespaces(code)

        reader = StringIO(code)
        writer = StringIO()

        while True:
            line = reader.readline()
            if not line:
                break

            line = (line.replace(", ", ",")
                    .replace(" ,", ",")
                    .replace(" , ", ","))

            writer.write(line + "\n")

        return writer.getvalue()

    @staticmethod
    def __resolve_operators(code: str) -> str:
        """
        Resolves spacing issues around operators.

        :param code: The input code as a string.
        :return: The code with resolved operator spacing.
        """
        code = dotnet_code_helper.__remove_whitespaces(code)

        reader = StringIO(code)
        writer = StringIO()

        while True:
            line = reader.readline()
            if not line:
                break

            line = (line.replace(" <", "<")
                    .replace("< ", "<")
                    .replace("> ", ">")
                    .replace(" >", ">")
                    .replace("= ", "=")
                    .replace(" =", "=")
                    .replace("== ", "==")
                    .replace(" ==", "==")
                    .replace("!= ", "!=")
                    .replace(" !=", "!=")
                    .replace(">= ", ">=")
                    .replace(" >=", ">=")
                    .replace("<= ", "<=")
                    .replace(" <=", "<=")
                    .replace("+ ", "+")
                    .replace(" +", "+")
                    .replace("- ", "-")
                    .replace(" -", "-")
                    .replace("* ", "*")
                    .replace(" *", "*"))

            writer.write(line + "\n")

        return writer.getvalue()

    def compile_debug(sources: List[dotnet_code], assembly_name: str, additional_foldername: str = None):
        # Create the folder to store temporary files.
        folder = os.path.join(tempfile.gettempdir(), additional_foldername if additional_foldername else '')
        os.makedirs(folder, exist_ok=True)

        # Process each source code in the `sources` list.
        for source in sources:
            # Set the full path where the source file will be stored
            source.fullPath = os.path.join(folder, source.fileName)
            # Write the source content to the respective file
            with open(source.fullPath, 'w', encoding='utf-8') as file:
                file.write(source.content)

        syntax_trees = []

        try:
            for source in sources:
                # Import Roslyn's CSharpSyntaxTree from the .NET libraries (Python.NET)
                from Microsoft.CodeAnalysis.CSharp import CSharpSyntaxTree, CSharpCompilation, CSharpCompilationOptions
                from Microsoft.CodeAnalysis import DiagnosticFormatter, OutputKind

                # Parse the source code to create a SyntaxTree object for Roslyn compilation
                syntax_tree = CSharpSyntaxTree.ParseText(source.content, path=source.fullPath)
                syntax_trees.append(syntax_tree)

            from Microsoft.CodeAnalysis import SyntaxTree
            from Microsoft.CodeAnalysis import MetadataReference
            from System.Collections.Generic import List as CSharpList
            import System

            enumerable_syntax_trees = CSharpList[SyntaxTree]()
            for i in range(len(syntax_trees)):
                enumerable_syntax_trees.Add(syntax_trees[i])

            enumerable_references = CSharpList[MetadataReference]()
            enumerable_references.Add(MetadataReference.CreateFromFile( enumerable_references.GetType().Assembly.Location ))
            options = CSharpCompilationOptions( OutputKind.DynamicallyLinkedLibrary)

            # Create Roslyn compilation settings
            # CSharpCompilation.Create generates the assembly based on the SyntaxTrees (source code).
            compilation = CSharpCompilation.Create( assembly_name,  # The name of the assembly
                enumerable_syntax_trees,  # The collection of parsed SyntaxTree objects
                enumerable_references,  # Add necessary references here (e.g., System.dll, Microsoft.CSharp.dll, etc.)
                options  # Optional compilation settings, such as whether to optimize the code
            )

            # Import MemoryStream from System.IO to handle the byte streams of the compiled assembly and PDB.
            from System.IO import MemoryStream
            from System.Reflection import Assembly

            # Compilation and generation of the output (DLL and PDB) in memory.
            emit_stream = MemoryStream()
            # Emit (generate) the compiled assembly and PDB (debugging symbols)
            result = compilation.Emit(emit_stream)

            # Check if the compilation was successful
            if not result.Success:
                # In case of errors, print the diagnostics (errors encountered during the compilation)
                diagnostics = result.Diagnostics
                diagnostic_formatter = DiagnosticFormatter()
                compile_errors = []
                for diagnostic in diagnostics:
                    compile_errors.append(diagnostic_formatter.Format(diagnostic))
                return False, compile_errors, None  # If the compilation failed, return False, and errors

            # compilation ha no error
            return True, [], Assembly.Load( emit_stream.ToArray() )
        except Exception as e:
            print(f"Hiba történt: {e}")
            return False, [f"Hiba történt: {e}"]
            

    def GetAssemblyReferences():
        # Az assembly referencia lista, amit a Roslyn-hez adunk
        # Ezt bővíteni kell a szükséges .NET hivatkozásokkal
        references = [
            # Példa referencia: az alábbi fájlok elérhetősége szükséges
            # clr.AddReference("System.Core") # Add references if needed
        ]
        return references

    @staticmethod
    def assembly_name() -> str:
        import inspect
        # The caller is the second item in the stack (the first item is the current function)
        caller_frame = inspect.stack()[1]
        # Get the function name from the caller's frame
        return caller_frame.function + ".dll"
       
