# Generated from ./unicontract/grammar/UniContractGrammar.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .UniContractGrammar import UniContractGrammar
else:
    from UniContractGrammar import UniContractGrammar

# This class defines a complete generic visitor for a parse tree produced by UniContractGrammar.

class UniContractGrammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by UniContractGrammar#contract.
    def visitContract(self, ctx:UniContractGrammar.ContractContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#import_rule.
    def visitImport_rule(self, ctx:UniContractGrammar.Import_ruleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#namespace.
    def visitNamespace(self, ctx:UniContractGrammar.NamespaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#namespace_elements.
    def visitNamespace_elements(self, ctx:UniContractGrammar.Namespace_elementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#interface.
    def visitInterface(self, ctx:UniContractGrammar.InterfaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#interface_element.
    def visitInterface_element(self, ctx:UniContractGrammar.Interface_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#interface_property.
    def visitInterface_property(self, ctx:UniContractGrammar.Interface_propertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#interface_method.
    def visitInterface_method(self, ctx:UniContractGrammar.Interface_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#interface_method_param.
    def visitInterface_method_param(self, ctx:UniContractGrammar.Interface_method_paramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#type.
    def visitType(self, ctx:UniContractGrammar.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#primitive_type.
    def visitPrimitive_type(self, ctx:UniContractGrammar.Primitive_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#reference_type.
    def visitReference_type(self, ctx:UniContractGrammar.Reference_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#list_type.
    def visitList_type(self, ctx:UniContractGrammar.List_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#map_type.
    def visitMap_type(self, ctx:UniContractGrammar.Map_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#qualifiedName.
    def visitQualifiedName(self, ctx:UniContractGrammar.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#inherits.
    def visitInherits(self, ctx:UniContractGrammar.InheritsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#enum.
    def visitEnum(self, ctx:UniContractGrammar.EnumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#enum_element.
    def visitEnum_element(self, ctx:UniContractGrammar.Enum_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#generic.
    def visitGeneric(self, ctx:UniContractGrammar.GenericContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniContractGrammar#generic_type.
    def visitGeneric_type(self, ctx:UniContractGrammar.Generic_typeContext):
        return self.visitChildren(ctx)



del UniContractGrammar