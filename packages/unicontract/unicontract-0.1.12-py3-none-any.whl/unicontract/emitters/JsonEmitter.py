import json
import os
from typing import Any, Dict
from pathlib import Path
from unicontract.elements.Elements import *
from unicontract.Engine import Session


def DoEmit(session: Session, output_dir: str, configuration: Dict[str, str]):
    jsonEmmiter = JsonEmitter()

    indent = 4
    if "json.indent" in configuration:
        indent = int(configuration["json.indent"])

    ensure_ascii = True
    if "json.ensure_ascii" in configuration:
        ensure_ascii = bool(configuration["json.ensure_ascii"])

    sort_keys = False
    if "json.sort_keys" in configuration:
        sort_keys = bool(configuration["json.sort_keys"])

    json_result = jsonEmmiter.Emit(session, indent, ensure_ascii, sort_keys)
    json_path = os.path.join(output_dir, Path(session.source.fileName).stem + ".json")
    with open(json_path, "w") as file:
        file.write(json_result)
    return json_result


class JsonEmitter(ElementVisitor):
    def __init__(self, withLocation: bool = True):
        self.dict = {}
        self.withLocation = withLocation

    def Emit(self, session: Session, indent=4, ensure_ascii=True, sort_keys=False) -> str:
        data = session.main.visit(self, None)
        json_result = json.dumps(data,
                                 indent=indent,
                                 ensure_ascii=ensure_ascii,
                                 sort_keys=sort_keys)
        return json_result

    def visitContract(self, contract: contract, parentData: Any) -> Any:
        self.dict = {
            "$type": "contract",
            "imports": [],
            "namespaces": [],
        }
        return self.dict

    def visitNamespace(self,  namespace: namespace, parentData: Any) -> Any:
        data = {
            "$type": "namespace",
            "name": namespace.name.getText(),
            "decorators": [],
            "enums": [],
            "interfaces": [],
        }
        parentData['namespaces'].append(data)
        return data

    def visitEnum(self, enum: enum, parentData: Any) -> Any:
        data = {
            "$type": "enum",
            "decorators": [],
            "name": enum.name,
            "enum_elements": [],
        }
        parentData['enums'].append(data)
        return data

    def visitEnumElement(self, enum_element: enum_element, parentData: Any) -> Any:
        data = {
            "$type": "enum_element",
            "decorators": [],
            "value": enum_element.value,
        }
        parentData['enum_elements'].append(data)
        return data

    def visitInterface(self, interface: interface, parentData: Any) -> Any:
        data = {
            "$type": "interface",
            "decorators": [],
            "name": interface.name,
            "enums": [],
            "methods": [],
            "properties": [],
        }
        parentData['interfaces'].append(data)
        return data

    def visitInterfaceProperty(self, interface_property: interface_property, parentData: Any) -> Any:
        data = {
            "$type": "interface_property",
            "decorators": [],
            "name": interface_property.name,
            "type": {},
            "isReadonly": interface_property.isReadonly,
        }
        parentData['properties'].append(data)
        return data

    def visitInterfaceMethod(self, interface_method: interface_method, parentData: Any) -> Any:
        data = {
            "$type": "interface_method",
            "decorators": [],
            "name": interface_method.name,
            "params": [],
            "return_type": {},
            "isAsync": interface_method.isAsync,
        }
        parentData['methods'].append(data)
        return data

    def visitInterfaceMethodParam(self, interface_method_param: interface_method_param, parentData: Any) -> Any:
        data = {
            "$type": "interface_method_param",
            "decorators": [],
            "name": interface_method_param.name,
            "type": {},
        }
        parentData['params'].append(data)
        return data

    def visitType(self, type: type, parentData: Any, memberName: str) -> Any:
        data = {
            "kind": str(type.kind)
        }
        parentData[memberName] = data
        return data

    def visitPrimitiveType(self, primtiveType: primitive_type, parentData: Any, memberName: str) -> Any:
        data = {
            "$type": "primitive_type",
            "kind": str(primtiveType.kind),
            "primtiveKind": str(primtiveType.primtiveKind)
        }
        parentData[memberName] = data
        return data

    def visitReferenceType(self, reference_type: reference_type, parentData: Any, memberName: str) -> Any:
        data = {
            "$type": "reference_type",
            "kind": str(reference_type.kind),
            "isExternal": reference_type.isExternal,
            "reference_name": str(reference_type.reference_name.getText())
        }
        parentData[memberName] = data
        return data

    def visitListType(self, list_type: list_type, parentData: Any, memberName: str) -> Any:
        data = {
            "$type": "list_type",
            "kind": str(list_type.kind),
            "item_type": {}
        }
        parentData[memberName] = data
        return data

    def visitMapType(self, map_type: map_type, parentData: Any, memberName: str) -> Any:
        data = {
            "$type": "list_type",
            "kind": str(map_type.kind),
            "key_type": {},
            "value_type": {}
        }
        parentData[memberName] = data
        return data

    def visitHintedElement(self, hinted_element: hinted_base_element, parentData: Any) -> Any:
        parentData["decorators"] = []
        parentData["document_lines"] = []
        return parentData

    def visitDecorator(self, decorator: decorator, parentData: Any) -> Any:
        data = {
            "$type": "decorator",
            "name": decorator.name,
            "params": [],
        }
        parentData["decorators"].append(data)
        return data

    def visitDecoratorParam(self, decorator_param: decorator_param, parentData: Any) -> Any:
        data = {
            "$type": "d3i.decorator_param",
            "kind": str(decorator_param.kind),
            "value": (
                decorator_param.value.getText() if decorator_param.kind == decorator_param.Kind.QualifiedName else
                str(decorator_param.value)
            ),
        }
        parentData['params'].append(data)
        return data

    def visitDocumentLine(self, document_line: str, parentData: Any) -> Any:
        parentData['document_lines'].append(document_line)

    def visitBaseElement(self, base_element: base_element, parentData: Any) -> Any:
        if (self.withLocation == True):
            data = {
                "fileName": base_element.fileName,
                "line": base_element.line,
                "column": base_element.column
            }
            parentData["location"] = data
            return data
        else:
            return None


if __name__ == "__main__":
    pass
