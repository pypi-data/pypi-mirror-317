from __future__ import annotations
from typing import Any
from .Elements import *

class ElementVisitor:

    def visitContract(self, contract: contract, parentData: Any) -> Any:
        pass

    def visitNamespace(self,  namespace: namespace, parentData: Any) -> Any:
        pass

    def visitEnum(self, enum: enum, parentData: Any) -> Any:
        pass

    def visitEnumElement(self, enum_element: enum_element, parentData: Any) -> Any:
        pass

    def visitInterface(self, interface: interface, parentData: Any) -> Any:
        pass

    def visitInterfaceProperty(self, interface_property: interface_property, parentData: Any) -> Any:
        pass

    def visitInterfaceMethod(self, interface_method: interface_method, parentData: Any) -> Any:
        pass

    def visitInterfaceMethodParam(self, interface_method_param: interface_method_param, parentData: Any) -> Any:
        pass

    def visitType(self, type: type, parentData: Any, memberName: str) -> Any:
        pass

    def visitPrimitiveType(self, primtiveType: primitive_type, parentData: Any, memberName: str) -> Any:
        pass

    def visitReferenceType(self, reference_type: reference_type, parentData: Any, memberName: str) -> Any:
        pass

    def visitListType(self, list_type: list_type, parentData: Any, memberName: str) -> Any:
        pass

    def visitMapType(self, map_type: map_type, parentData: Any, memberName: str) -> Any:
        pass

    def visitHintedElement(self, hinted_element: hinted_base_element, parentData: Any) -> Any:
        pass

    def visitDocumentLine(self, document_line: str, parentData: Any) -> Any:
        pass

    def visitBaseElement(self, base_element: base_element, parentData: Any) -> Any:
        pass

    def visitGeneric(self, generic: generic, parentData: Any) -> Any:
        pass

    def visitGenericType(self, generic_type: generic_type, parentData: Any) -> Any:
        pass
