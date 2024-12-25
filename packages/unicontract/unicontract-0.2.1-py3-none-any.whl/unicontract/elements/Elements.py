from __future__ import annotations
from typing import List
from enum import Enum
from .ElementVisitor import *


class IScope:
    def getChildren(self) -> List[base_element]:
        return []


class base_element:
    def __init__(self, fileName, pos):
        self.fileName: str = fileName
        self.line: int = pos.line
        self.column: int = pos.column
        self.parent: base_element = None

    def visit(self, visitor: ElementVisitor, parentData: Any) -> Any:
        data = visitor.visitBaseElement(self, parentData)
        return data

    def locationText(self):
        return f"'{self.fileName}({self.line},{self.column})'"


class hinted_base_element(base_element):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.document_lines: List[str] = []

    def visit(self, visitor: ElementVisitor, parentData: Any) -> Any:
        visitor.visitHintedElement(self, parentData)
        super().visit(visitor, parentData)
        for document_line in self.document_lines:
            visitor.visitDocumentLine(document_line, parentData)
        return parentData


class internal_scoped_base_element(hinted_base_element, IScope):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.enums: List[enum] = []

    def getChildren(self) -> List[base_element]:
        return self.enums


class qualified_name(base_element):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.names: List[str] = []

    def getText(self):
        return '.'.join(self.names)


class import_(hinted_base_element):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.name: str = ""
        self.contract: contract = ""


class contract(IScope):
    def __init__(self):
        self.imports: List[import_] = []
        self.namespaces: List[namespace] = []

    def visit(self, visitor: ElementVisitor, parentData: Any) -> Any:
        data = visitor.visitContract(self, parentData)
        for namespace in self.namespaces:
            namespace.visit(visitor, data)
        return data

    def getChildren(self) -> List[base_element]:
        return self.namespaces


class namespace(internal_scoped_base_element):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.name: qualified_name = None
        self.interfaces: List[interface] = []

    def visit(self, visitor: ElementVisitor, parentData: Any):
        data = visitor.visitNamespace(self, parentData)
        super().visit(visitor, data)
        for enum in self.enums:
            enum.visit(visitor, data)
        for interface in self.interfaces:
            interface.visit(visitor, data)

    def getChildren(self) -> List[base_element]:
        return super().getChildren() + self.interfaces


class enum(hinted_base_element):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.name: str = None
        self.enum_elements: List[enum_element] = []

    def visit(self, visitor: ElementVisitor, parentData: Any):
        data = visitor.visitEnum(self, parentData)
        super().visit(visitor, data)
        for enum_element in self.enum_elements:
            enum_element.visit(visitor, data)


class enum_element(hinted_base_element):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.value = None

    def visit(self, visitor: ElementVisitor, parentData: Any):
        data = visitor.visitEnumElement(self, parentData)
        super().visit(visitor, data)


class interface(internal_scoped_base_element):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.inherits: List[qualified_name] = []
        self.name: str = None
        self.generic: generic = None
        self.methods: List[interface_method] = []
        self.properties: List[interface_property] = []

    def visit(self, visitor: ElementVisitor, parentData: Any):
        data = visitor.visitInterface(self, parentData)
        super().visit(visitor, data)
        if (self.generic != None):
            self.generic.visit(visitor, data)
        for property in self.properties:
            property.visit(visitor, data)
        for method in self.methods:
            method.visit(visitor, data)
        for internal_enum in self.enums:
            internal_enum.visit(visitor, data)


class interface_property(hinted_base_element):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.name: str = None
        self.type: type = None
        self.isReadonly: bool = False

    def visit(self, visitor: ElementVisitor, parentData: Any):
        data = visitor.visitInterfaceProperty(self, parentData)
        if (self.type != None):
            self.type.visit(visitor, data, "type")
        super().visit(visitor, data)


class interface_method(hinted_base_element):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.name: str = None
        self.params: List[interface_method_param] = []
        self.return_type: type = None
        self.isAsync: bool = False
        self.generic: generic = None

    def visit(self, visitor: ElementVisitor, parentData: Any):
        data = visitor.visitInterfaceMethod(self, parentData)
        super().visit(visitor, data)
        if (self.generic != None):
            self.generic.visit(visitor, data)
        for param in self.params:
            param.visit(visitor, data)
        if (self.return_type != None):
            self.return_type.visit(visitor, data, "return_type")


class interface_method_param(hinted_base_element):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.name: str = None
        self.type: type = None

    def visit(self, visitor: ElementVisitor, parentData: Any):
        data = visitor.visitInterfaceMethodParam(self, parentData)
        if (self.type != None):
            self.type.visit(visitor, data, "type")
        super().visit(visitor, data)


class type(base_element):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.kind: type.Kind = None

    class Kind(Enum):
        Primitive = 1
        Reference = 2
        List = 3
        Map = 4

    def visit(self, visitor: ElementVisitor, parentData: Any, memberName: str):
        match self.kind:
            case type.Kind.Primitive:
                data = visitor.visitPrimitiveType(self, parentData, memberName)
            case type.Kind.Reference:
                data = visitor.visitReferenceType(self, parentData, memberName)
                if (self.generic):
                    visitor.visitGeneric(self.generic, parentData)
            case type.Kind.List:
                data = visitor.visitListType(self, parentData, memberName)
                if (self.item_type != None):
                    self.item_type.visit(visitor, data, "item_type")
            case type.Kind.Map:
                data = visitor.visitMapType(self, parentData, memberName)
                if (self.key_type != None):
                    self.key_type.visit(visitor, data, "key_type")
                if (self.value_type != None):
                    self.value_type.visit(visitor, data, "value_type")

        super().visit(visitor, data)


class primitive_type(type):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.primtiveKind: primitive_type.PrimtiveKind = None

    class PrimtiveKind(Enum):
        Integer = 1
        Number = 2
        Float = 2
        Date = 3,
        Time = 4,
        DateTime = 5,
        String = 6,
        Boolean = 7,
        Bytes = 8,
        Stream = 8,


class reference_type(type):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.reference_name: qualified_name = None
        self.generic: generic = None


class list_type(type):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.item_type = None


class map_type(type):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.key_type = None
        self.value_type = None


class generic(base_element):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.types: List[generic_type] = []

    def visit(self, visitor: ElementVisitor, parentData: Any):
        data = visitor.visitGeneric(self, parentData)
        super().visit(visitor, data)
        for type in self.types:
            type.visit(visitor, data)


class generic_type(base_element):
    def __init__(self, fileName, pos):
        super().__init__(fileName, pos)
        self.type_name: str = ""
        self.constraint: qualified_name = None

    def visit(self, visitor: ElementVisitor, parentData: Any):
        data = visitor.visitGenericType(self, parentData)
        super().visit(visitor, data)
