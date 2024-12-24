# Generated from ./unicontract/grammar/UniContractGrammar.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .UniContractGrammar import UniContractGrammar
else:
    from UniContractGrammar import UniContractGrammar

# This class defines a complete listener for a parse tree produced by UniContractGrammar.
class UniContractGrammarListener(ParseTreeListener):

    # Enter a parse tree produced by UniContractGrammar#contract.
    def enterContract(self, ctx:UniContractGrammar.ContractContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#contract.
    def exitContract(self, ctx:UniContractGrammar.ContractContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#import_rule.
    def enterImport_rule(self, ctx:UniContractGrammar.Import_ruleContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#import_rule.
    def exitImport_rule(self, ctx:UniContractGrammar.Import_ruleContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#namespace.
    def enterNamespace(self, ctx:UniContractGrammar.NamespaceContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#namespace.
    def exitNamespace(self, ctx:UniContractGrammar.NamespaceContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#namespace_elements.
    def enterNamespace_elements(self, ctx:UniContractGrammar.Namespace_elementsContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#namespace_elements.
    def exitNamespace_elements(self, ctx:UniContractGrammar.Namespace_elementsContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#interface.
    def enterInterface(self, ctx:UniContractGrammar.InterfaceContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#interface.
    def exitInterface(self, ctx:UniContractGrammar.InterfaceContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#interface_element.
    def enterInterface_element(self, ctx:UniContractGrammar.Interface_elementContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#interface_element.
    def exitInterface_element(self, ctx:UniContractGrammar.Interface_elementContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#interface_property.
    def enterInterface_property(self, ctx:UniContractGrammar.Interface_propertyContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#interface_property.
    def exitInterface_property(self, ctx:UniContractGrammar.Interface_propertyContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#interface_method.
    def enterInterface_method(self, ctx:UniContractGrammar.Interface_methodContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#interface_method.
    def exitInterface_method(self, ctx:UniContractGrammar.Interface_methodContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#interface_method_param.
    def enterInterface_method_param(self, ctx:UniContractGrammar.Interface_method_paramContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#interface_method_param.
    def exitInterface_method_param(self, ctx:UniContractGrammar.Interface_method_paramContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#type.
    def enterType(self, ctx:UniContractGrammar.TypeContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#type.
    def exitType(self, ctx:UniContractGrammar.TypeContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#primitive_type.
    def enterPrimitive_type(self, ctx:UniContractGrammar.Primitive_typeContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#primitive_type.
    def exitPrimitive_type(self, ctx:UniContractGrammar.Primitive_typeContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#reference_type.
    def enterReference_type(self, ctx:UniContractGrammar.Reference_typeContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#reference_type.
    def exitReference_type(self, ctx:UniContractGrammar.Reference_typeContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#list_type.
    def enterList_type(self, ctx:UniContractGrammar.List_typeContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#list_type.
    def exitList_type(self, ctx:UniContractGrammar.List_typeContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#map_type.
    def enterMap_type(self, ctx:UniContractGrammar.Map_typeContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#map_type.
    def exitMap_type(self, ctx:UniContractGrammar.Map_typeContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#qualifiedName.
    def enterQualifiedName(self, ctx:UniContractGrammar.QualifiedNameContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#qualifiedName.
    def exitQualifiedName(self, ctx:UniContractGrammar.QualifiedNameContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#inherits.
    def enterInherits(self, ctx:UniContractGrammar.InheritsContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#inherits.
    def exitInherits(self, ctx:UniContractGrammar.InheritsContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#enum.
    def enterEnum(self, ctx:UniContractGrammar.EnumContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#enum.
    def exitEnum(self, ctx:UniContractGrammar.EnumContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#enum_element.
    def enterEnum_element(self, ctx:UniContractGrammar.Enum_elementContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#enum_element.
    def exitEnum_element(self, ctx:UniContractGrammar.Enum_elementContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#generic.
    def enterGeneric(self, ctx:UniContractGrammar.GenericContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#generic.
    def exitGeneric(self, ctx:UniContractGrammar.GenericContext):
        pass


    # Enter a parse tree produced by UniContractGrammar#generic_type.
    def enterGeneric_type(self, ctx:UniContractGrammar.Generic_typeContext):
        pass

    # Exit a parse tree produced by UniContractGrammar#generic_type.
    def exitGeneric_type(self, ctx:UniContractGrammar.Generic_typeContext):
        pass



del UniContractGrammar