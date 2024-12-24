import os
import io
from typing import Dict
from ..elements.Elements import *
from ..Engine import *


def DoEmit(session: Session, output_dir: str, configuration: Dict[str, str]):
    """
    Creates an instance of DotnetEmmiter, initializes it with the output directory and configuration,
    and then emits the dotnet code based on the provided session.
    """
    dotnetEmmiter = DotnetEmmiter(output_dir, configuration)

    # Generate the .NET code for the session
    result: List[dotnet_code] = dotnetEmmiter.Emit(session)


class DotnetEmmiter:
    def __init__(self, output_dir: str = "./", configuration: Dict[str, str] = {}):
        """
        Initializes the DotnetEmmiter instance with the provided output directory and configuration.
        """
        self.configuration: dotnet_configuration = dotnet_configuration(configuration, output_dir)

    def Emit(self, session: Session):
        """
        Emits the .NET code for all namespaces, enums, and interfaces found in the provided session.
        """
        result: List[dotnet_code] = []

        # Iterate over all namespaces in the session
        for namespace in session.main.namespaces:
            path: str = self.configuration.output_dir
            if self.configuration.createFolderStructure:
                # Create folder structure for the namespace if configured
                path = os.path.join(self.configuration.output_dir, *namespace.name.names)

            # Process all enums in the namespace
            for enum in namespace.enums:
                content: str = self.beginFile(namespace, session)
                content += self.enumText(enum, indent=1)
                content += self.endFile(namespace)
                result.append(dotnet_code(path, enum.name, content))

            # Process all interfaces in the namespace
            for interface in namespace.interfaces:
                content: str = self.beginFile(namespace, session)
                content += self.interfaceText(interface, indent=1)
                content += self.endFile(namespace)
                result.append(dotnet_code(path, interface.name, content))

        return result

    def fileHeader(self) -> str:
        """
        Returns the file header to be included in the generated .cs files.
        """
        return self.configuration.fileHeader

    def defaultUsings(self) -> str:
        """
        Returns the default 'using' statements to be included in the .cs files.
        """
        using_statements: List[str] = []

        for using in self.configuration.defaultUsings:
            using_statements.append(f"using {using};")

        return "\n".join(using_statements) + "\n"

    def importsText(self, session: Session) -> str:
        """
        Returns the refrenced by import 'using' statements to be included in the .cs files.
        """
        buffer = io.StringIO()

        for _import in session.main.imports:
            buffer.write(self.documentLines(_import, indent=0))
            buffer.write(f"using {_import.value};")

        return buffer.getvalue()

    def beginFile(self, namespace: namespace, session: Session) -> str:
        """
        Begins the file by writing the file header, usings, and namespace declaration.
        """
        buffer = io.StringIO()
        buffer.write(self.fileHeader())
        buffer.write("\n")
        buffer.write(self.defaultUsings())
        buffer.write(self.importsText(session))
        buffer.write("\n")
        buffer.write(f"namespace {namespace.name.getText()}\n")
        buffer.write("{\n")
        return buffer.getvalue()

    def endFile(self, namespace: namespace):
        """
        Ends the file by closing the namespace.
        """
        buffer = io.StringIO()
        buffer.write("\n")
        buffer.write("}\n")
        return buffer.getvalue()

    def documentLines(self, hinted_element: hinted_base_element, indent: int = 1):
        """
        Generates documentation lines for the provided element.
        """
        buffer = io.StringIO()
        for document_line in hinted_element.document_lines:
            buffer.write(f"{self.tab(indent)}///{document_line}")
            buffer.write("\n")

        return buffer.getvalue()

    def enumText(self, enum: enum, indent: int = 1):
        """
        Generates the .NET code for an enum.
        """
        buffer = io.StringIO()
        buffer.write("\n")
        buffer.write(self.documentLines(enum, indent))
        buffer.write(f"{self.tab(indent)}enum {enum.name}\n")
        buffer.write(f"{self.tab(indent)}{{\n")
        for enum_element in enum.enum_elements:
            buffer.write(self.documentLines(enum_element, indent))
            buffer.write(f"{self.tab(indent+1)}{enum_element.value},\n")
        buffer.write(f"{self.tab(indent)}}}\n")
        return buffer.getvalue()

    def interfaceText(self, interface: interface, indent: int = 1):
        """
        Generates the .NET code for an interface, including enums, properties, and methods.
        """
        buffer = io.StringIO()
        buffer.write("\n")
        buffer.write(self.documentLines(interface, indent))
        buffer.write(f"{self.tab(indent)}interface {interface.name}\n")
        buffer.write(f"{self.tab(indent)}{{\n")

        # Process nested enums in the interface
        for enum in interface.enums:
            buffer.write(f"{self.enumText(enum, indent+1)}")
        buffer.write("\n")

        # Process properties in the interface
        for property in interface.properties:
            buffer.write(f"{self.propertyText(property, indent+1)}")
        buffer.write("\n")

        # Process methods in the interface
        for method in interface.methods:
            buffer.write(f"{self.methodText(method, indent+1)}")
        buffer.write(f"{self.tab(indent)}}}\n")
        return buffer.getvalue()

    def propertyText(self, property: interface_property, indent: int):
        """
        Generates the .NET code for a property in an interface.
        """
        buffer = io.StringIO()
        buffer.write(self.documentLines(property, indent))
        buffer.write(f"{self.tab(indent)}public {self.typeText(property.type)} {property.name} {{ get; ")
        if not property.isReadonly:
            buffer.write("set;")
        buffer.write("}\n")
        return buffer.getvalue()

    def methodText(self, method: interface_method, indent: int):
        """
        Generates the .NET code for a method in an interface, including parameters and return type.
        """
        buffer = io.StringIO()
        buffer.write(self.documentLines(method, indent))
        buffer.write(f"{self.tab(indent)}")

        # Handle async and non-async methods with return types
        if method.return_type is not None:
            type_text = self.typeText(method.return_type)
            if method.isAsync:
                buffer.write(f"Task<{type_text}>")
            else:
                buffer.write(f"{type_text}")
        else:
            if method.isAsync:
                buffer.write(f"Task")
            else:
                buffer.write(f"void")
        buffer.write(f" {method.name}(")

        # Check if parameters should be broken into multiple lines
        break_lines = any(param.document_lines for param in method.params) or any(param.decorators for param in method.params) or len(method.params) >= 5

        # Iterate over method parameters
        firstParam: bool = True
        for param in method.params:
            if not firstParam:
                buffer.write(f", ")
            if break_lines:
                buffer.write(f"\n")
                buffer.write(self.documentLines(param, indent+1))
                buffer.write(f"{self.tab(indent+1)}")
            buffer.write(f"{self.typeText(param.type)} {param.name}")
            firstParam = False

        buffer.write(f");\n")
        return buffer.getvalue()

    def typeText(self, type: type):
        """
        Converts a given type to its .NET representation.
        """
        match type.kind:
            case type.Kind.Primitive:
                return self.typeTextPrimitive(type)
            case type.Kind.Reference:
                return self.typeTextReference(type)
            case type.Kind.List:
                return self.typeTextList(type)
            case type.Kind.Map:
                return self.typeTextMap(type)

    def typeTextPrimitive(self, type: primitive_type):
        """
        Converts a primitive type to its .NET representation.
        """
        match type.primtiveKind:
            case primitive_type.PrimtiveKind.Integer:
                return "int"
            case primitive_type.PrimtiveKind.Number:
                return "decimal"
            case primitive_type.PrimtiveKind.Float:
                return "double"
            case primitive_type.PrimtiveKind.Date:
                return "DateOnly"
            case primitive_type.PrimtiveKind.Time:
                return "TimeOnly"
            case primitive_type.PrimtiveKind.DateTime:
                return "DateTime"
            case primitive_type.PrimtiveKind.String:
                return "string"
            case primitive_type.PrimtiveKind.Boolean:
                return "bool"
            case primitive_type.PrimtiveKind.Bytes:
                return "byte[]"
            case primitive_type.PrimtiveKind.Stream:
                return "Stream"

    def typeTextReference(self, type: reference_type):
        """
        Converts a reference type to its .NET representation.
        """
        return type.reference_name.getText()

    def typeTextList(self, type: list_type):
        """
        Converts a list type to its .NET representation.
        """
        return f"System.Generic.List<{self.typeText(type.item_type)}>"

    def typeTextMap(self, type: map_type):
        """
        Converts a map type to its .NET representation.
        """
        return f"System.Generic.Dictionary<{self.typeText(type.key_type)},{self.typeText(type.value_type)}>"

    def tab(self,indent=1):
        return '\t'*indent

class utils:
    @staticmethod
    def create_folder(output_dir: str, folder_name: str):
        """
        Creates a folder at the specified path.
        """
        folder_path = os.path.join(output_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)

    @staticmethod
    def create_cs_file(output_dir: str, file_name: str, content: str):
        """
        Creates a .cs file with the given content at the specified path.
        """
        file_path = os.path.join(output_dir, file_name + ".cs")
        with open(file_path, "w") as file:
            file.write(content)


class dotnet_configuration:
    def __init__(self, configuration: Dict[str, str], output_dir: str):
        """
        Initializes the dotnet configuration with the provided settings.
        """
        self.output_dir = output_dir

        self.__read_fileHeader(configuration)
        self.__read_defaultUsings(configuration)
        self.__read_createFolderStructure(configuration)

    def __read_fileHeader(self, configuration: Dict[str, str]):
        """
        Reads the file header configuration.
        """
        self.fileHeader: str = """ 
// <auto-generated>
//     This code was generated by unicontract
//     see more information: https://github.com/gyorgy-gulyas/UniContract
//
//     Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
// </auto-generated>
"""

        if "dotnet.file_header_lines" in configuration:
            value = configuration["dotnet.file_header_lines"]
            if isinstance(value, list) and all(isinstance(item, str) for item in value):
                self.fileHeader = "\n".join(value)

    def __read_defaultUsings(self, configuration: Dict[str, str]):
        """
        Reads the default 'using' statements configuration.
        """
        self.defaultUsings: List[str] = ["System", "System.Threading.Tasks", "System.Collections.Generic"]
        if "dotnet.default_usings" in configuration:
            value = configuration["dotnet.default_usings"]
            if isinstance(value, list) and all(isinstance(item, str) for item in value):
                self.defaultUsings = value

    def __read_createFolderStructure(self, configuration: Dict[str, str]):
        """
        Reads the folder structure creation flag from the configuration.
        """
        self.createFolderStructure: bool = True
        if "dotnet.create_folder_structure" in configuration:
            self.createFolderStructure = bool(configuration["dotnet.create_folder_structure"])


class dotnet_code:
    def __init__(self, directory: str, name: str, content: str):
        """
        Initializes a dotnet_code instance with the file path, file name, and content.
        """
        self.fileName: str = name + ".cs"
        self.fullPath: str = os.path.join(directory, self.fileName)
        self.content: str = content
