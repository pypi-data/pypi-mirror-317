from __future__ import annotations
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
        """
        Processes an enumeration (enum) element, validating that its name does not conflict 
        with other elements in the same scope.
        """

        # Retrieve the current scope of the parent element of the enum.
        scope = self.__get_current_scope(enum.parent)

        # Iterate through all elements in the current scope.
        for neighbour in scope.getChildren():
            # Skip the current enum being validated.
            if neighbour is enum:
                continue
            # If another element in the scope has the same name, raise a conflict error.
            if neighbour.name == enum.name:
                self.__error(enum, f"An enum '{enum.name}' conflicts with the same name as an element in {neighbour.locationText()}.")

    def visitEnumElement(self, enum_element: enum_element, parentData: Any) -> Any:
        """
        Processes an individual enumeration (enum) element, validating that its value 
        does not conflict with other elements in the same enum.
        """

        # Retrieve the parent enum of the current enum element.
        parent_enum: enum = enum_element.parent

        # Iterate through all elements in the parent enum.
        for neighbour in parent_enum.enum_elements:
            # Skip the current enum element being validated.
            if neighbour is enum_element:
                continue
            # If another enum element has the same value, raise a conflict error.
            if neighbour.value == enum_element.value:
                self.__error(
                    enum_element,
                    f"An enum element '{enum_element.value}' with this value already exists in {neighbour.locationText()}."
                )

    def visitInterface(self, _interface: interface, parentData: Any) -> Any:
        """
        Processes an interface element, verifying its inheritance, uniqueness, and generic type constraints.
        """

        # Get the current scope of the parent element of the interface.
        scope = self.__get_current_scope(_interface.parent)

        # Validate each inherited interface.
        for inherit in _interface.inherits:
            # Attempt to resolve the inherited interface and retrieve any error message.
            base_class, message = self.__get_referenced_element(_interface.parent, inherit)

            if base_class == None:
                # If the inherited element cannot be resolved, raise an error.
                self.__error(inherit, f"The element '{inherit.getText()}' referred in inheritance is not found. {message}")
            elif not isinstance(base_class, interface):
                # If the inherited element is not an interface, raise an error.
                self.__error(inherit, f"The element '{inherit.getText()}' referred in inheritance is not an event.")

        # Check for naming conflicts with other elements in the same scope.
        for neighbour in scope.getChildren():
            # Skip if the neighbor is the current interface being processed.
            if neighbour is _interface:
                continue
            # If another element has the same name, raise a conflict error.
            if neighbour.name == _interface.name:
                self.__error(_interface, f"A value object '{_interface.name}' conflicts with the same name as an element in {neighbour.locationText()}.")

        # If the interface has generic types, validate their constraints.
        if _interface.generic != None:
            for generic_type in _interface.generic.types:
                # If the generic type specifies an `extends` constraint, resolve it.
                if generic_type.constraint != None:
                    extends, message = self.__get_referenced_element(_interface.parent, generic_type.constraint)

                    if extends == None:
                        # Raise an error if the `extends` reference cannot be resolved.
                        self.__error(generic_type, f"The generic type extend reference '{generic_type.constraint.getText()}' not found. {message}")

    def visitInterfaceProperty(self, interface_property: interface_property, parentData: Any) -> Any:
        """
        Processes an interface property, validating that its name does not conflict with other properties or methods
        in the same interface.
        """

        # Retrieve the parent interface of the property.
        parent_interface: interface = interface_property.parent

        # Check for naming conflicts with other properties in the interface.
        for neighbour in parent_interface.properties:
            # Skip the current property being validated.
            if neighbour is interface_property:
                continue
            # If another property has the same name, raise an error.
            if neighbour.name == interface_property.name:
                self.__error(
                    interface_property,
                    f"A property '{interface_property.name}' conflicts with the same name as another property in {neighbour.locationText()}."
                )

        # Check for naming conflicts with methods in the same interface.
        for method in parent_interface.methods:
            # If a method has the same name as the property, raise an error.
            if method.name == interface_property.name:
                self.__error(
                    interface_property,
                    f"A property '{interface_property.name}' conflicts with the same name as a method in {method.locationText()}."
                )

    def visitInterfaceMethod(self, interface_method: interface_method, parentData: Any) -> Any:
        """
        Validates an interface method, specifically checking constraints for generic types.
        """

        # Check if the method has generic types defined.
        if interface_method.generic != None:
            # Iterate over all generic types in the method.
            for generic_type in interface_method.generic.types:
                # If a generic type specifies an 'extends' constraint, resolve it.
                if generic_type.constraint != None:
                    extends, message = self.__get_referenced_element(interface_method.parent, generic_type.constraint)
                    # Raise an error if the 'extends' reference cannot be resolved.
                    if extends == None:
                        self.__error(generic_type, f"The generic type extend reference '{generic_type.constraint.getText()}' not found. {message}")

    def visitInterfaceMethodParam(self, interface_method_param: interface_method_param, parentData: Any) -> Any:
        """
        Validates an interface method parameter, ensuring its name does not conflict with other parameters in the same method.
        """

        # Retrieve the parent method of the parameter.
        parent_method: interface_method = interface_method_param.parent

        # Iterate through all parameters of the parent method.
        for neighbour in parent_method.params:
            # Skip the current parameter being validated.
            if neighbour is interface_method_param:
                continue
            # If another parameter has the same name, raise a conflict error.
            if neighbour.name == interface_method_param.name:
                self.__error(
                    interface_method_param,
                    f"A method parameter '{interface_method_param.name}' with the same name already exists in {neighbour.locationText()}.")

    def visitType(self, type: type, parentData: Any, memberName: str) -> Any:
        pass

    def visitPrimitiveType(self, primtiveType: primitive_type, parentData: Any, memberName: str) -> Any:
        pass

    def visitReferenceType(self, reference_type: reference_type, parentData: Any, memberName: str) -> Any:
        # Check if the reference name list is empty
        if (len(reference_type.reference_name.names) == 0):
            # Raise an error indicating the referenced name is empty
            self.__error(reference_type, f"Empty referenced name.")

        # Try to resolve the referenced element and retrieve it along with an error message if applicable
        element, message = self.__get_referenced_element(reference_type.parent, reference_type.reference_name)

        # If the element could not be resolved
        if (element == None):
            # Attempt to resolve a generic type with the same name
            generic = self.__get_generic_type(reference_type.parent, reference_type.reference_name)

            # If no generic type can be resolved, raise an error with the associated message
            if (generic == None):
                self.__error(reference_type, message)

    def visitListType(self, list_type: list_type, parentData: Any, memberName: str) -> Any:
        pass

    def visitMapType(self, map_type: map_type, parentData: Any, memberName: str) -> Any:
        pass

    def visitDecoratedElement(self, decorated_element: hinted_base_element, parentData: Any) -> Any:
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

        # if we cannot found the name, try check the globals.
        for namespace in self.session.main.namespaces:
            if (namespace.name.getText() == name.names[0]):
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

    def __get_generic_type(self, parent: base_element, name: qualified_name) -> generic_type:
        """
        Attempts to resolve a generic type based on the given parent element and name.
        """

        # If the reference name has more than one part, it cannot be a generic type.
        if (len(name.names) != 1):
            return None

        # Get the current scope of the provided parent element.
        scope = self.__get_current_scope(parent)

        # Traverse up the scope hierarchy to find an interface with a generic definition.
        while True:
            # If no more scopes exist, break out of the loop.
            if (scope == None):
                break

            # Check if the current scope is an interface.
            if isinstance(scope, interface):
                _interface: interface = scope

                # If the interface has generic types defined, search through them.
                if _interface.generic != None:
                    for generic_type in _interface.generic.types:
                        # Return the generic type if its name matches the provided name.
                        if generic_type.type_name == name.names[0]:
                            return generic_type

            # Move to the parent scope and continue the search.
            scope = scope.parent

        # Return None if no matching generic type is found.
        return None
