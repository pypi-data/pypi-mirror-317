from decimal import Decimal
from ..grammar.UniContractGrammar import *
from ..grammar.UniContractGrammarVisitor import *
from .Elements import *


class ElementBuilder(UniContractGrammarVisitor):
    def __init__(self, fileName: str):
        self.elementTree = contract()
        self.fileName: str = fileName

    # Visit a parse tree produced by UniContractGrammar#contract.
    def visitContract(self, ctx: UniContractGrammar.ContractContext):

        counter = 0
        while True:
            import_rule = ctx.import_rule((counter))
            if (import_rule == None):
                break
            counter = counter + 1
            self.elementTree.imports.append(self.visit(import_rule))

        counter = 0
        while True:
            namespace = ctx.namespace((counter))
            if (namespace == None):
                break
            counter = counter + 1
            self.elementTree.namespaces.append(self.visit(namespace))

        return self.elementTree

    # Visit a parse tree produced by UniContractGrammar#import_rule.
    def visitImport_rule(self, ctx: UniContractGrammar.Import_ruleContext):
        result = import_(self.fileName, ctx.start)

        counter = 0
        while True:
            decorator = ctx.decorator((counter))
            if (decorator == None):
                break
            counter = counter + 1
            child = self.visit(decorator)
            child.parent = result
            result.decorators.append(child)

        counter = 0
        while True:
            document_line = ctx.DOCUMENT_LINE((counter))
            if (document_line == None):
                break
            counter = counter + 1
            result.document_lines.append(document_line.getText()[1:])

        if (ctx.qualifiedName() != None):
            result.kind = import_.Kind.ContractNamespace
            result.value = self.visit(ctx.qualifiedName()).getText()
        else:
            result.kind = import_.Kind.ExternalNamespace
            result.value = ctx.STRING_LITERAL().getText().strip('"')
        
        return result

    # Visit a parse tree produced by UniContractGrammar#namespace.
    def visitNamespace(self, ctx: UniContractGrammar.NamespaceContext):
        result: namespace = namespace(self.fileName, ctx.start)
        if (ctx.qualifiedName() != None):
            result.name = self.visit(ctx.qualifiedName())

        counter = 0
        while True:
            decorator = ctx.decorator((counter))
            if (decorator == None):
                break
            counter = counter + 1
            child = self.visit(decorator)
            child.parent = result
            result.decorators.append(child)

        counter = 0
        while True:
            document_line = ctx.DOCUMENT_LINE((counter))
            if (document_line == None):
                break
            counter = counter + 1
            result.document_lines.append(document_line.getText()[1:])

        counter = 0
        while True:
            namespace_element: UniContractGrammar.Namespace_elementsContext = ctx.namespace_elements(
                (counter))
            if (namespace_element == None):
                break
            elif (namespace_element.interface() != None):
                child = self.visit(namespace_element.interface())
                child.parent = result
                result.interfaces.append(child)
            elif (namespace_element.enum() != None):
                child = self.visit(namespace_element.enum())
                child.parent = result
                result.enums.append(child)
            counter = counter + 1

        return result

    # Visit a parse tree produced by UniContractGrammar#namespace_elements.
    def visitNamespace_elements(self, ctx: UniContractGrammar.Namespace_elementsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by UniContractGrammar#interface.
    def visitInterface(self, ctx: UniContractGrammar.InterfaceContext):
        result = interface(self.fileName, ctx.start)
        if (ctx.IDENTIFIER() != None):
            result.name = ctx.IDENTIFIER().getText()

        if (ctx.inherits() != None):
            result.inherits = result.value = self.visit(ctx.inherits())

        counter = 0
        while True:
            decorator = ctx.decorator((counter))
            if (decorator == None):
                break
            counter = counter + 1
            child = self.visit(decorator)
            child.parent = result
            result.decorators.append(child)

        counter = 0
        while True:
            document_line = ctx.DOCUMENT_LINE((counter))
            if (document_line == None):
                break
            counter = counter + 1
            result.document_lines.append(document_line.getText()[1:])

        counter = 0
        while True:
            context_element: UniContractGrammar.Interface_elementContext = ctx.interface_element(
                (counter))
            if (context_element == None):
                break
            elif (context_element.enum() != None):
                child = self.visit(context_element.enum())
                child.parent = result
                result.enums.append(child)
            elif (context_element.interface_method() != None):
                child = self.visit(context_element.interface_method())
                child.parent = result
                result.methods.append(child)
            elif (context_element.interface_property() != None):
                child = self.visit(context_element.interface_property())
                child.parent = result
                result.properties.append(child)
            counter = counter + 1

        return result

    # Visit a parse tree produced by UniContractGrammar#interface_element.
    def visitInterface_element(self, ctx: UniContractGrammar.Interface_elementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by UniContractGrammar#interface_property.
    def visitInterface_property(self, ctx: UniContractGrammar.Interface_propertyContext):
        result = interface_property(self.fileName, ctx.start)
        if (ctx.IDENTIFIER() != None):
            result.name = ctx.IDENTIFIER().getText()
        if (ctx.type_() != None):
            result.type = self.visit(ctx.type_())
            result.type.parent = result
        if (ctx.READONLY() != None):
            result.isReadonly = True

        counter = 0
        while True:
            decorator = ctx.decorator((counter))
            if (decorator == None):
                break
            counter = counter + 1
            child = self.visit(decorator)
            child.parent = result
            result.decorators.append(child)

        counter = 0
        while True:
            document_line = ctx.DOCUMENT_LINE((counter))
            if (document_line == None):
                break
            counter = counter + 1
            result.document_lines.append(document_line.getText()[1:])

        return result

    # Visit a parse tree produced by UniContractGrammar#interface_method.
    def visitInterface_method(self, ctx: UniContractGrammar.Interface_methodContext):
        result = interface_method(self.fileName, ctx.start)
        if (ctx.IDENTIFIER() != None):
            result.name = ctx.IDENTIFIER().getText()
        if (ctx.type_() != None):
            result.return_type = self.visit(ctx.type_())
            result.return_type.parent = result
        if (ctx.ASYNC() != None):
            result.isAsync = True

        counter = 0
        while True:
            decorator = ctx.decorator((counter))
            if (decorator == None):
                break
            counter = counter + 1
            child = self.visit(decorator)
            child.parent = result
            result.decorators.append(child)

        counter = 0
        while True:
            document_line = ctx.DOCUMENT_LINE((counter))
            if (document_line == None):
                break
            counter = counter + 1
            result.document_lines.append(document_line.getText()[1:])

        counter = 0
        while True:
            method_param = ctx.interface_method_param((counter))
            if (method_param == None):
                break
            counter = counter + 1
            child = self.visit(method_param)
            child.parent = result
            result.params.append(child)

        return result

    # Visit a parse tree produced by UniContractGrammar#interface_method_param.
    def visitInterface_method_param(self, ctx: UniContractGrammar.Interface_method_paramContext):
        result = interface_method_param(self.fileName, ctx.start)
        if (ctx.IDENTIFIER() != None):
            result.name = ctx.IDENTIFIER().getText()
        if (ctx.type_() != None):
            result.type = self.visit(ctx.type_())
            result.type.parent = result

        counter = 0
        while True:
            decorator = ctx.decorator((counter))
            if (decorator == None):
                break
            counter = counter + 1
            child = self.visit(decorator)
            child.parent = result
            result.decorators.append(child)

        counter = 0
        while True:
            document_line = ctx.DOCUMENT_LINE((counter))
            if (document_line == None):
                break
            counter = counter + 1
            result.document_lines.append(document_line.getText()[1:])

        return result

    # Visit a parse tree produced by UniContractGrammar#type.
    def visitType(self, ctx: UniContractGrammar.TypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by UniContractGrammar#primitive_type.
    def visitPrimitive_type(self, ctx: UniContractGrammar.Primitive_typeContext):
        result = primitive_type(self.fileName, ctx.start)
        result.kind = type.Kind.Primitive

        if (ctx.INTEGER() != None):
            result.primtiveKind = primitive_type.PrimtiveKind.Integer
        elif (ctx.NUMBER() != None):
            result.primtiveKind = primitive_type.PrimtiveKind.Number
        elif (ctx.FLOAT() != None):
            result.primtiveKind = primitive_type.PrimtiveKind.Float
        elif (ctx.DATE() != None):
            result.primtiveKind = primitive_type.PrimtiveKind.Date
        elif (ctx.TIME() != None):
            result.primtiveKind = primitive_type.PrimtiveKind.Time
        elif (ctx.DATETIME() != None):
            result.primtiveKind = primitive_type.PrimtiveKind.DateTime
        elif (ctx.STRING() != None):
            result.primtiveKind = primitive_type.PrimtiveKind.String
        elif (ctx.BOOLEAN() != None):
            result.primtiveKind = primitive_type.PrimtiveKind.Boolean
        elif (ctx.BYTES() != None):
            result.primtiveKind = primitive_type.PrimtiveKind.Bytes
        elif (ctx.STREAM() != None):
            result.primtiveKind = primitive_type.PrimtiveKind.Stream

        return result

    # Visit a parse tree produced by UniContractGrammar#reference_type.
    def visitReference_type(self, ctx: UniContractGrammar.Reference_typeContext):
        result = reference_type(self.fileName, ctx.start)
        result.kind = type.Kind.Reference
        if (ctx.qualifiedName() != None):
            result.isExternal = False
            result.reference_name = self.visit(ctx.qualifiedName())
            result.reference_name.parent = result
        elif (ctx.EXTERNAL() != None):
            result.isExternal = True
            result.reference_name = qualified_name(self.fileName, ctx.start)
            result.reference_name.names.append(ctx.STRING_LITERAL().getText().strip('"'))

        return result

    # Visit a parse tree produced by UniContractGrammar#list_type.
    def visitList_type(self, ctx: UniContractGrammar.List_typeContext):
        result = list_type(self.fileName, ctx.start)
        result.kind = type.Kind.List
        result.item_type = self.visit(ctx.type_())

        return result

    # Visit a parse tree produced by UniContractGrammar#map_type.
    def visitMap_type(self, ctx: UniContractGrammar.Map_typeContext):
        result = map_type(self.fileName, ctx.start)
        result.kind = type.Kind.Map
        result.key_type = self.visit(ctx.type_(0))
        result.value_type = self.visit(ctx.type_(1))

        return result

    # Visit a parse tree produced by UniContractGrammar#qualifiedName.
    def visitQualifiedName(self, ctx: UniContractGrammar.QualifiedNameContext):
        result = qualified_name(self.fileName, ctx.start)

        counter = 0
        while True:
            identifier = ctx.IDENTIFIER(counter)
            if (identifier == None):
                break
            counter = counter + 1
            result.names.append(identifier.getText())

        return result

    # Visit a parse tree produced by UniContractGrammar#decorator.
    def visitDecorator(self, ctx: UniContractGrammar.DecoratorContext):
        result = decorator(self.fileName, ctx.start)
        if (ctx.IDENTIFIER() != None):
            result.name = ctx.IDENTIFIER().getText()

        counter = 0
        while True:
            param = ctx.decorator_param(counter)
            if (param == None):
                break
            counter = counter + 1
            child = self.visit(param)
            child.parent = result
            result.params.append(child)

        return result

    # Visit a parse tree produced by UniContractGrammar#decorator_param.
    def visitDecorator_param(self, ctx: UniContractGrammar.Decorator_paramContext):
        result = decorator_param(self.fileName, ctx.start)
        if (ctx.qualifiedName() != None):
            result.kind = decorator_param.Kind.QualifiedName
            result.value = self.visit(ctx.qualifiedName())
            result.value.parent = result
        elif (ctx.INTEGER_CONSTANS() != None):
            result.kind = decorator_param.Kind.Integer
            result.value = int(ctx.INTEGER_CONSTANS().getText())
        elif (ctx.NUMBER_CONSTANS() != None):
            result.kind = decorator_param.Kind.Number
            result.value = Decimal(ctx.NUMBER_CONSTANS().getText())
        else:
            result.kind = decorator_param.Kind.String
            result.value = ctx.STRING_LITERAL().getText().strip('"')

        return result

    # Visit a parse tree produced by UniContractGrammar#enum.
    def visitEnum(self, ctx: UniContractGrammar.EnumContext):
        result = enum(self.fileName, ctx.start)
        if (ctx.IDENTIFIER() != None):
            result.name = ctx.IDENTIFIER().getText()

        counter = 0
        while True:
            decorator = ctx.decorator((counter))
            if (decorator == None):
                break
            counter = counter + 1
            child = self.visit(decorator)
            child.parent = result
            result.decorators.append(child)

        counter = 0
        while True:
            document_line = ctx.DOCUMENT_LINE((counter))
            if (document_line == None):
                break
            counter = counter + 1
            result.document_lines.append(document_line.getText()[1:])

        counter = 0
        while True:
            enum_element = ctx.enum_element((counter))
            if (enum_element == None):
                break
            counter = counter + 1
            child = self.visit(enum_element)
            child.parent = result
            result.enum_elements.append(child)

        return result

    # Visit a parse tree produced by UniContractGrammar#enum_element.
    def visitEnum_element(self, ctx: UniContractGrammar.Enum_elementContext):
        result = enum_element(self.fileName, ctx.start)
        if (ctx.IDENTIFIER() != None):
            result.value = ctx.IDENTIFIER().getText()

        counter = 0
        while True:
            decorator = ctx.decorator((counter))
            if (decorator == None):
                break
            counter = counter + 1
            child = self.visit(decorator)
            child.parent = result
            result.decorators.append(child)

        counter = 0
        while True:
            document_line = ctx.DOCUMENT_LINE((counter))
            if (document_line == None):
                break
            counter = counter + 1
            result.document_lines.append(document_line.getText()[1:])

        return result

    # Visit a parse tree produced by UniContractGrammar#inherits.
    def visitInherits(self, ctx: UniContractGrammar.InheritsContext):
        result: List[qualified_name] = []

        counter = 0
        while True:
            base_class = ctx.qualifiedName((counter))
            if (base_class == None):
                break
            counter = counter + 1
            child: qualified_name = self.visit(base_class)
            child.parent = result
            result.append(child)

        return result
