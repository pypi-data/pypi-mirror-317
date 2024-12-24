import unittest
import unicontract
from unicontract.Engine import *


class TestBuild(unittest.TestCase):

    def test_empty_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText(""))
        root = engine.Build(session)
        self.assertIsInstance(root, contract)
        self.assertEqual(0, len(root.namespaces))

    def test_line_comments_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
// line comment 1
// line comment 1"""))
        root = engine.Build(session)
        self.assertIsInstance(root, contract)
        self.assertEqual(0, len(root.namespaces))

    def test_block_comments_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
/* comment 1
  comment 1*/"""))
        root = engine.Build(session)
        self.assertIsInstance(root, contract)
        self.assertEqual(0, len(root.namespaces))

    def test_lines_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace someNamespace{
}
"""))
        root = engine.Build(session)
        self.assertIsInstance(root, contract)
        element: unicontract.namespace = root.namespaces[0]
        self.assertEqual(element.line, 2)
        self.assertEqual(element.column, 0)
        self.assertEqual(element.fileName, "internal string")

    def test_document_lines_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
#doc line 1
#doc line 2
namespace someNamespace {}
"""))
        root = engine.Build(session)
        self.assertIsInstance(root, contract)
        self.assertEqual(1, len(root.namespaces))
        namespace: unicontract.namespace = root.namespaces[0]
        self.assertEqual(2, len(namespace.document_lines))
        self.assertEqual(namespace.document_lines[0], "doc line 1")
        self.assertEqual(namespace.document_lines[1], "doc line 2")

    def test_decorator_simple_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
@simple
namespace someNamespace {}
"""))
        root = engine.Build(session)
        self.assertIsInstance(root, contract)
        self.assertEqual(1, len(root.namespaces))
        namespace: unicontract.namespace = root.namespaces[0]
        self.assertEqual(1, len(namespace.decorators))
        decorator: unicontract.decorator = namespace.decorators[0]
        self.assertEqual(decorator.name, "simple")

    def test_decorator_multiple_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
@simple_1
@simple_2
namespace someNamespace {}
"""))
        root = engine.Build(session)
        self.assertIsInstance(root, contract)
        self.assertEqual(1, len(root.namespaces))
        namespace: unicontract.namespace = root.namespaces[0]
        self.assertEqual(2, len(namespace.decorators))
        decorator: unicontract.decorator = namespace.decorators[0]
        self.assertEqual(decorator.name, "simple_1")
        decorator: unicontract.decorator = namespace.decorators[1]
        self.assertEqual(decorator.name, "simple_2")

    def test_decorator_complex_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
@simple( "string", 1, 3.14, identifier.sub.sub )
namespace someNamespace {}
"""))
        root = engine.Build(session)
        self.assertIsInstance(root, contract)
        self.assertEqual(1, len(root.namespaces))
        namespace: unicontract.namespace = root.namespaces[0]
        self.assertEqual(1, len(namespace.decorators))
        decorator: unicontract.decorator = namespace.decorators[0]
        self.assertEqual(decorator.name, "simple")
        self.assertEqual(4, len(decorator.params))
        param: unicontract.decorator_param = decorator.params[0]
        self.assertEqual(param.kind, unicontract.decorator_param.Kind.String)
        self.assertEqual(param.value, "string")
        param: unicontract.decorator_param = decorator.params[1]
        self.assertEqual(param.kind, unicontract.decorator_param.Kind.Integer)
        self.assertEqual(param.value, 1)
        param: unicontract.decorator_param = decorator.params[2]
        self.assertEqual(param.kind, unicontract.decorator_param.Kind.Number)
        self.assertEqual(param.value, Decimal('3.14'))
        param: unicontract.decorator_param = decorator.params[3]
        self.assertEqual(param.kind, unicontract.decorator_param.Kind.QualifiedName)
        self.assertEqual(param.value.getText(), "identifier.sub.sub")

    def test_enum(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace someNamespace {
    @decorator_enum
    enum WeekDays {
        @first
        Monday,
        Tuesday,
        Wednesday,
        Thursday,
        @last
        Friday
    }
}
"""))
        root = engine.Build(session)
        namespace: unicontract.namespace = root.namespaces[0]
        enum: unicontract.enum = namespace.enums[0]
        self.assertEqual(enum.name, "WeekDays")
        self.assertEqual(len(enum.decorators), 1)
        self.assertEqual(len(enum.enum_elements), 5)
        self.assertEqual(enum.enum_elements[0].value, "Monday")
        self.assertEqual(enum.enum_elements[1].value, "Tuesday")
        self.assertEqual(enum.enum_elements[2].value, "Wednesday")
        self.assertEqual(enum.enum_elements[3].value, "Thursday")
        self.assertEqual(enum.enum_elements[4].value, "Friday")
        self.assertEqual(enum.enum_elements[0].decorators[0].name, "first")
        self.assertEqual(enum.enum_elements[4].decorators[0].name, "last")

    def test_interface_inner_enum(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace someNamespace {
    @decorator
    interface Address {
        enum InnerEnum{
            Value1,
            Value2
        }
    }
}
"""))
        root = engine.Build(session)
        namespace: unicontract.namespace = root.namespaces[0]
        interface: unicontract.interface = namespace.interfaces[0]
        self.assertEqual(len(interface.decorators), 1)
        self.assertEqual(interface.name, "Address")
        self.assertEqual(len(interface.properties), 0)
        enum_inner: unicontract.enum = interface.enums[0]
        self.assertEqual(enum_inner.name, "InnerEnum")
        self.assertEqual(len(enum_inner.enum_elements), 2)

    def test_interface_property(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace someNamespace {
    @decorator
    interface Address {
        property country:General.Country
        @required
        property city: string
        @required
        property zipCode: integer

        readonly property addressText: string
    }
}
"""))
        root = engine.Build(session)
        namespace: unicontract.namespace = root.namespaces[0]
        interface: unicontract.interface = namespace.interfaces[0]
        self.assertEqual(len(interface.properties), 4)

        property: unicontract.interface_property = interface.properties[0]
        self.assertEqual(property.name, "country")
        self.assertEqual(property.isReadonly, False)
        self.assertEqual(property.type.kind, unicontract.type.Kind.Reference)
        self.assertEqual(property.type.reference_name.getText(), "General.Country")

        property: unicontract.interface_property = interface.properties[1]
        self.assertEqual(property.name, "city")
        self.assertEqual(property.isReadonly, False)
        self.assertEqual(property.type.kind, unicontract.type.Kind.Primitive)
        self.assertEqual(property.type.primtiveKind, unicontract.primitive_type.PrimtiveKind.String)
        self.assertEqual(property.decorators[0].name, "required")

        property: unicontract.interface_property = interface.properties[2]
        self.assertEqual(property.name, "zipCode")
        self.assertEqual(property.isReadonly, False)
        self.assertEqual(property.type.kind, unicontract.type.Kind.Primitive)
        self.assertEqual(property.type.primtiveKind, unicontract.primitive_type.PrimtiveKind.Integer)

        property: unicontract.interface_property = interface.properties[3]
        self.assertEqual(property.name, "addressText")
        self.assertEqual(property.isReadonly, True)
        self.assertEqual(property.type.kind, unicontract.type.Kind.Primitive)
        self.assertEqual(property.type.primtiveKind, unicontract.primitive_type.PrimtiveKind.String)

    def test_interface_method(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace someNamespace {
    @decorator
    interface CustomerService {
        @decorator_method
        method CreateCustomer( @required id: string ) => Customer
        
        @decorator_method
        method DumpAllCustomer()

        @decorator_method
        async method CreateCustomerAsync( @required id: string ) => Customer
    }
}
"""))
        root = engine.Build(session)
        namespace: unicontract.namespace = root.namespaces[0]
        interface: unicontract.interface = namespace.interfaces[0]
        self.assertEqual(len(interface.properties), 0)
        self.assertEqual(len(interface.methods), 3)

        method: unicontract.interface_method = interface.methods[0]
        self.assertEqual(method.name, "CreateCustomer")
        self.assertEqual(method.isAsync, False)
        self.assertEqual(method.return_type.kind, unicontract.type.Kind.Reference)
        self.assertEqual(method.return_type.reference_name.getText(), "Customer")
        self.assertEqual(method.decorators[0].name, "decorator_method")
        self.assertEqual(len(method.params), 1)
        param: unicontract.interface_method_param = method.params[0]
        self.assertEqual(param.name, "id")
        self.assertEqual(param.type.kind, unicontract.type.Kind.Primitive)
        self.assertEqual(param.type.primtiveKind, unicontract.primitive_type.PrimtiveKind.String)
        self.assertEqual(param.decorators[0].name, "required")

        method: unicontract.interface_method = interface.methods[1]
        self.assertEqual(method.name, "DumpAllCustomer")
        self.assertEqual(method.isAsync, False)
        self.assertEqual(method.return_type, None)
        self.assertEqual(method.decorators[0].name, "decorator_method")
        self.assertEqual(len(method.params), 0)

        method: unicontract.interface_method = interface.methods[2]
        self.assertEqual(method.name, "CreateCustomerAsync")
        self.assertEqual(method.isAsync, True)
        self.assertEqual(method.return_type.kind, unicontract.type.Kind.Reference)
        self.assertEqual(method.return_type.reference_name.getText(), "Customer")
        self.assertEqual(method.decorators[0].name, "decorator_method")
        self.assertEqual(len(method.params), 1)
        param: unicontract.interface_method_param = method.params[0]
        self.assertEqual(param.name, "id")
        self.assertEqual(param.type.kind, unicontract.type.Kind.Primitive)
        self.assertEqual(param.type.primtiveKind, unicontract.primitive_type.PrimtiveKind.String)
        self.assertEqual(param.decorators[0].name, "required")

if __name__ == "__main__":
    unittest.main()
