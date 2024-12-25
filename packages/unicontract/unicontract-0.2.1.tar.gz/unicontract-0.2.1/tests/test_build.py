from __future__ import annotations
import unittest
from unicontract.Engine import *
from unicontract.elements.Elements import *


class TestBuild(unittest.TestCase):

    def test_empty_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText(""))
        root = engine.Build(session)
        self.assertFalse(session.HasAnyError())

        self.assertIsInstance(root, contract)
        self.assertEqual(0, len(root.namespaces))

    def test_line_comments_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
// line comment 1
// line comment 1"""))
        root = engine.Build(session)
        self.assertFalse(session.HasAnyError())

        self.assertIsInstance(root, contract)
        self.assertEqual(0, len(root.namespaces))

    def test_block_comments_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
/* comment 1
  comment 1*/"""))
        root = engine.Build(session)
        self.assertFalse(session.HasAnyError())

        self.assertIsInstance(root, contract)
        self.assertEqual(0, len(root.namespaces))

    def test_lines_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace someNamespace{
}
"""))
        root = engine.Build(session)
        self.assertFalse(session.HasAnyError())

        self.assertIsInstance(root, contract)
        element: namespace = root.namespaces[0]
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
        self.assertFalse(session.HasAnyError())

        self.assertIsInstance(root, contract)
        self.assertEqual(1, len(root.namespaces))
        namespace: namespace = root.namespaces[0]
        self.assertEqual(2, len(namespace.document_lines))
        self.assertEqual(namespace.document_lines[0], "doc line 1")
        self.assertEqual(namespace.document_lines[1], "doc line 2")

    def test_enum_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace someNamespace {
    enum WeekDays {
        Monday,
        Tuesday,
        Wednesday,
        Thursday,
        Friday
    }
}
"""))
        root = engine.Build(session)
        self.assertFalse(session.HasAnyError())

        namespace: namespace = root.namespaces[0]
        enum: enum = namespace.enums[0]
        self.assertEqual(enum.name, "WeekDays")
        self.assertEqual(len(enum.enum_elements), 5)
        self.assertEqual(enum.enum_elements[0].value, "Monday")
        self.assertEqual(enum.enum_elements[1].value, "Tuesday")
        self.assertEqual(enum.enum_elements[2].value, "Wednesday")
        self.assertEqual(enum.enum_elements[3].value, "Thursday")
        self.assertEqual(enum.enum_elements[4].value, "Friday")

    def test_interface_inner_enum_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace someNamespace {
    interface Address {
        enum InnerEnum{
            Value1,
            Value2
        }
    }
}
"""))
        root = engine.Build(session)
        self.assertFalse(session.HasAnyError())

        namespace: namespace = root.namespaces[0]
        interface: interface = namespace.interfaces[0]
        self.assertEqual(interface.name, "Address")
        self.assertEqual(len(interface.properties), 0)
        enum_inner: enum = interface.enums[0]
        self.assertEqual(enum_inner.name, "InnerEnum")
        self.assertEqual(len(enum_inner.enum_elements), 2)

    def test_interface_property_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace someNamespace {
    interface Address {
        property country:General.Country
        property city: string
        property zipCode: integer
        readonly property addressText: string
    }
}
"""))
        root = engine.Build(session)
        self.assertFalse(session.HasAnyError())

        namespace: namespace = root.namespaces[0]
        interface: interface = namespace.interfaces[0]
        self.assertEqual(len(interface.properties), 4)

        property: interface_property = interface.properties[0]
        self.assertEqual(property.name, "country")
        self.assertEqual(property.isReadonly, False)
        self.assertEqual(property.type.kind, type.Kind.Reference)
        self.assertEqual(property.type.reference_name.getText(), "General.Country")

        property: interface_property = interface.properties[1]
        self.assertEqual(property.name, "city")
        self.assertEqual(property.isReadonly, False)
        self.assertEqual(property.type.kind, type.Kind.Primitive)
        self.assertEqual(property.type.primtiveKind, primitive_type.PrimtiveKind.String)

        property: interface_property = interface.properties[2]
        self.assertEqual(property.name, "zipCode")
        self.assertEqual(property.isReadonly, False)
        self.assertEqual(property.type.kind, type.Kind.Primitive)
        self.assertEqual(property.type.primtiveKind, primitive_type.PrimtiveKind.Integer)

        property: interface_property = interface.properties[3]
        self.assertEqual(property.name, "addressText")
        self.assertEqual(property.isReadonly, True)
        self.assertEqual(property.type.kind, type.Kind.Primitive)
        self.assertEqual(property.type.primtiveKind, primitive_type.PrimtiveKind.String)

    def test_interface_method_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace someNamespace {
    interface CustomerService {
        method CreateCustomer( id: string ) => Customer
        method DumpAllCustomer()
        async method CreateCustomerAsync( id: string ) => Customer
    }
}
"""))
        root = engine.Build(session)
        self.assertFalse(session.HasAnyError())

        namespace: namespace = root.namespaces[0]
        interface: interface = namespace.interfaces[0]
        self.assertEqual(len(interface.properties), 0)
        self.assertEqual(len(interface.methods), 3)

        method: interface_method = interface.methods[0]
        self.assertEqual(method.name, "CreateCustomer")
        self.assertEqual(method.isAsync, False)
        self.assertEqual(method.return_type.kind, type.Kind.Reference)
        self.assertEqual(method.return_type.reference_name.getText(), "Customer")
        self.assertEqual(len(method.params), 1)
        param: interface_method_param = method.params[0]
        self.assertEqual(param.name, "id")
        self.assertEqual(param.type.kind, type.Kind.Primitive)
        self.assertEqual(param.type.primtiveKind, primitive_type.PrimtiveKind.String)

        method: interface_method = interface.methods[1]
        self.assertEqual(method.name, "DumpAllCustomer")
        self.assertEqual(method.isAsync, False)
        self.assertEqual(method.return_type, None)
        self.assertEqual(len(method.params), 0)

        method: interface_method = interface.methods[2]
        self.assertEqual(method.name, "CreateCustomerAsync")
        self.assertEqual(method.isAsync, True)
        self.assertEqual(method.return_type.kind, type.Kind.Reference)
        self.assertEqual(method.return_type.reference_name.getText(), "Customer")
        self.assertEqual(len(method.params), 1)
        param: interface_method_param = method.params[0]
        self.assertEqual(param.name, "id")
        self.assertEqual(param.type.kind, type.Kind.Primitive)
        self.assertEqual(param.type.primtiveKind, primitive_type.PrimtiveKind.String)

    def test_interface_generic_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace someNamespace {
    interface Normal {
    }
    interface Generic1<T> {
    }
    interface Generic2<T1,T2> {
    }
    interface Generic3<T constraint Normal> {
    }
}
"""))
        root = engine.Build(session)
        self.assertFalse(session.HasAnyError())

        namespace: namespace = root.namespaces[0]
        self.assertEqual(len(namespace.interfaces), 4)

        interface: interface = namespace.interfaces[0]
        self.assertEqual(interface.name, "Normal")
        self.assertIsNone(interface.generic)

        interface: interface = namespace.interfaces[1]
        self.assertEqual(interface.name, "Generic1")
        self.assertIsNotNone(interface.generic)
        self.assertEqual(len(interface.generic.types), 1)
        self.assertEqual(interface.generic.types[0].type_name, "T")
        self.assertEqual(interface.generic.types[0].constraint, None)

        interface: interface = namespace.interfaces[2]
        self.assertEqual(interface.name, "Generic2")
        self.assertIsNotNone(interface.generic)
        self.assertEqual(len(interface.generic.types), 2)
        self.assertEqual(interface.generic.types[0].type_name, "T1")
        self.assertEqual(interface.generic.types[0].constraint, None)
        self.assertEqual(interface.generic.types[1].type_name, "T2")
        self.assertEqual(interface.generic.types[1].constraint, None)

        interface: interface = namespace.interfaces[3]
        self.assertEqual(interface.name, "Generic3")
        self.assertIsNotNone(interface.generic)
        self.assertEqual(len(interface.generic.types), 1)
        self.assertEqual(interface.generic.types[0].type_name, "T")
        self.assertEqual(interface.generic.types[0].constraint.getText(), "Normal")

    def test_interface_generic_method_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace someNamespace {
    interface Generic {
        method Func1()
        method Func2<T>()
        method Func3<T1,T2>()
        method Func4<T constraint Normal>()
    }
}
"""))
        root = engine.Build(session)
        self.assertFalse(session.HasAnyError())

        namespace: namespace = root.namespaces[0]
        self.assertEqual(len(namespace.interfaces), 1)
        interface: interface = namespace.interfaces[0]

        method: interface_method = interface.methods[0]
        self.assertEqual(method.name, "Func1")
        self.assertEqual(method.generic, None)

        method: interface = interface.methods[1]
        self.assertEqual(method.name, "Func2")
        self.assertIsNotNone(method.generic)
        self.assertEqual(len(method.generic.types), 1)
        self.assertEqual(method.generic.types[0].type_name, "T")
        self.assertEqual(method.generic.types[0].constraint, None)

        method: interface = interface.methods[2]
        self.assertEqual(method.name, "Func3")
        self.assertIsNotNone(method.generic)
        self.assertEqual(len(method.generic.types), 2)
        self.assertEqual(method.generic.types[0].type_name, "T1")
        self.assertEqual(method.generic.types[0].constraint, None)
        self.assertEqual(method.generic.types[1].type_name, "T2")
        self.assertEqual(method.generic.types[1].constraint, None)

        method: interface = interface.methods[3]
        self.assertEqual(method.name, "Func4")
        self.assertIsNotNone(method.generic)
        self.assertEqual(len(method.generic.types), 1)
        self.assertEqual(method.generic.types[0].type_name, "T")
        self.assertEqual(method.generic.types[0].constraint.getText(), "Normal")


if __name__ == "__main__":
    unittest.main()
