from typing import Any, Dict
from unicontract.elements.ElementVisitor import *
from unicontract.Engine import *


def DoLint(session: Session, output_dir: str, args: Dict[str, str]):
    linter = SemanticChecker(session)
    data = session.main.visit(linter, None)

class SemanticChecker(ElementVisitor):
    def __init__(self, session: Session):
        self.session: Session = session

    def visitContract(self, contract: contract, parentData: Any) -> Any:
        pass

    def visitNamespace(self,  namespace: namespace, parentData: Any) -> Any:
        pass

    def visitEnum(self, enum: enum, parentData: Any) -> Any:
        scope = self.__get_current_scope(enum.parent)
        for neighbour in scope.getChildren():
            if (neighbour is enum):
                continue
            if (neighbour.name == enum.name):
                self.__error(enum, f"An enum '{enum.name}' conflicts with same name with element in {neighbour.locationText()}.")

    def visitEnumElement(self, enum_element: enum_element, parentData: Any) -> Any:
        parent_enum: enum = enum_element.parent
        for neighbour in parent_enum.enum_elements:
            if (neighbour is enum_element):
                continue
            if (neighbour.value == enum_element.value):
                self.__error(enum_element, f"An enum element '{enum_element.value}' with this value already exists in {neighbour.locationText()}.")

    def visitInterface(self, _interface: interface, parentData: Any) -> Any:
        scope = self.__get_current_scope(_interface.parent)

        for inherit in _interface.inherits:
            base_class, message = self.__get_referenced_element(_interface.parent, inherit)
            if (base_class == None):
                self.__error(inherit, f"The element '{inherit.getText()}' referred in inheritance is not found. {message}")
            elif (isinstance(base_class, interface) == False):
                self.__error(inherit, f"The element '{inherit.getText()}' referred in inheritance is not an event.")

        for neighbour in scope.getChildren():
            if (neighbour is _interface):
                continue
            if (neighbour.name == _interface.name):
                self.__error(_interface, f"A value object '{_interface.name}' conflicts with same name with element in {neighbour.locationText()}.")

    def visitInterfaceProperty(self, interface_property: interface_property, parentData: Any) -> Any:
        parent_interface: interface = interface_property.parent
        for neighbour in parent_interface.properties:
            if (neighbour is interface_property):
                continue
            if (neighbour.name == interface_property.name):
                self.__error(interface_property, f"An property '{interface_property.name}' conflicts with same name with element in {neighbour.locationText()}.")

        for method in parent_interface.methods:
            if (method.name == interface_property.name):
                self.__error(interface_property, f"An property '{interface_property.name}' conflicts with same name with element in {neighbour.locationText()}.")

    def visitInterfaceMethod(self, interface_method: interface_method, parentData: Any) -> Any:
        pass

    def visitInterfaceMethodParam(self, interface_method_param: interface_method_param, parentData: Any) -> Any:
        parent_method: interface_method = interface_method_param.parent
        for neighbour in parent_method.params:
            if (neighbour is interface_method_param):
                continue
            if (neighbour.name == interface_method_param.name):
                self.__error(interface_method_param, f"An methos parameter '{interface_method_param.name}' with same name is already exists in {neighbour.locationText()}.")

    def visitType(self, type: type, parentData: Any, memberName: str) -> Any:
        pass

    def visitPrimitiveType(self, primtiveType: primitive_type, parentData: Any, memberName: str) -> Any:
        pass

    def visitReferenceType(self, reference_type: reference_type, parentData: Any, memberName: str) -> Any:
        if (len(reference_type.reference_name.names) == 0):
            self.__error(reference_type, f"Empty referenced name.")

        if (reference_type.isExternal == True):
            return

        element, message = self.__get_referenced_element(reference_type.parent, reference_type.reference_name)
        if (element == None):
            self.__error(reference_type, message)


    def visitListType(self, list_type: list_type, parentData: Any, memberName: str) -> Any:
        pass

    def visitMapType(self, map_type: map_type, parentData: Any, memberName: str) -> Any:
        pass

    def visitDecoratedElement(self, decorated_element: hinted_base_element, parentData: Any) -> Any:
        pass

    def visitDecorator(self, decorator: decorator, parentData: Any) -> Any:
        pass

    def visitDecoratorParam(self, decorator_param: decorator_param, parentData: Any) -> Any:
        pass

    def visitBaseElement(self, base_element: base_element, parentData: Any) -> Any:
        pass


    def __warning(self, element: base_element, msg: str):
        self.session.ReportDiagnostic(msg, Diagnostic.Severity.Warning, element.fileName, element.line, element.column)

    def __error(self, element: base_element, msg: str):
        self.session.ReportDiagnostic(msg, Diagnostic.Severity.Error, element.fileName, element.line, element.column)

    def __get_current_scope(self, element: base_element) -> IScope:
        current_scope = element
        while True:
            if isinstance(current_scope, IScope):
                break
            elif (current_scope == None):
                break
            current_scope = current_scope.parent

        return current_scope

    def __get_referenced_element(self, parent: base_element, name: qualified_name) -> IScope:

        scope = self.__get_current_scope(parent)
        element = None
        # go up until we find the element for the first part of the name
        while True:
            if (scope == None):
                break

            # is the scope that has a child with the name we are looking for
            for child in scope.getChildren():
                if (child.name == name.names[0]):
                    element = child
                    break

            if (element != None):
                break

            scope = scope.parent

        #if we cannot found the name, try chank the globals.
        for namespace in self.session.main.namespaces:
            if(namespace.name.getText() == name.names[0]):
                element = namespace
                break

        if (element == None):
            return None, f"The first part of the referenced name '{name.names[0]}' cannot be resolved."

        # processing the rest of the name part if exist
        for name_part in name.names[1:]:
            if (isinstance(element, IScope) == False):
                return None, f"The referenced name '{name.names[0]}' cannot have an expected child: '{name_part}'."

            scope: IScope = element
            element = None
            for child in scope.getChildren():
                if (child.name == name_part):
                    element = child

            if (element == None):
                return None, f"The referenced name '{scope.name}' does not have an expected child: '{name_part}'."

        return element, "ok"
