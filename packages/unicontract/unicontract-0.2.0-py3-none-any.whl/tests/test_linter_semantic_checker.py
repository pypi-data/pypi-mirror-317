import unittest
from unicontract.Engine import *
from unicontract.linters.SemanticChecker import *

class TestLinterSemanticChecker(unittest.TestCase):

    def test_empty_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText(""))
        root = engine.Build(session)

        self.assertFalse(session.HasAnyError())
        checker = SemanticChecker(session)
        data = root.visit(checker, None)
        self.assertEqual(len(session.diagnostics), 0)

    def test_conflict_interface_fail(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace SomeNamespace {
    interface TheInterface {
    }
    interface TheInterface {
    }
    interface OtherInterface {
    }
}
"""))
        root = engine.Build(session)

        self.assertFalse(session.HasAnyError())
        checker = SemanticChecker(session)
        data = root.visit(checker, None)
        self.assertEqual(len(session.diagnostics), 2)
        self.assertTrue(all(location in session.diagnostics[0].toText() for location in ["TheInterface","(3,4):", "(5,4)"]))

    def test_conflict_enum_fail(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace SomeNamespace {
    enum TheEnum {
    }
    enum TheEnum {
    }
    enum OtherEnum {
    }
}
"""))
        root = engine.Build(session)

        self.assertFalse(session.HasAnyError())
        checker = SemanticChecker(session)
        data = root.visit(checker, None)
        self.assertEqual(len(session.diagnostics), 2)
        self.assertTrue(all(location in session.diagnostics[0].toText() for location in ["TheEnum","(3,4):", "(5,4)"]))

    def test_conflict_inner_enum_fail(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace SomeNamespace {
    interface TheInterface {
        enum TheEnum {
        }
        enum TheEnum {
        }
        enum OtherEnum {
        }
    }
}
"""))
        root = engine.Build(session)

        self.assertFalse(session.HasAnyError())
        checker = SemanticChecker(session)
        data = root.visit(checker, None)
        self.assertEqual(len(session.diagnostics), 2)
        self.assertTrue(all(location in session.diagnostics[0].toText() for location in ["TheEnum","(4,8):", "(6,8)"]))

    def test_conflict_enum_element_fail(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace SomeNamespace {
    enum TheEnum {
        TheValue,
        TheValue,
        OtherValue
    }
}
"""))
        root = engine.Build(session)

        self.assertFalse(session.HasAnyError())
        checker = SemanticChecker(session)
        data = root.visit(checker, None)
        self.assertEqual(len(session.diagnostics), 2)
        self.assertTrue(all(location in session.diagnostics[0].toText() for location in ["TheValue","(4,8):", "(5,8)"]))

    def test_inheritence_not_exists_fail(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace SomeNamespace {
    interface TheInterface inherits NotExist{
    }
}
"""))
        root = engine.Build(session)

        self.assertFalse(session.HasAnyError())
        checker = SemanticChecker(session)
        data = root.visit(checker, None)
        self.assertEqual(len(session.diagnostics), 1)
        self.assertTrue(all(location in session.diagnostics[0].toText() for location in ["NotExist","(3,36):"]))

    def test_inheritence_wrong_type_fail(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace SomeNamespace {
    enum TheEnum{
    }
    interface TheInterface inherits TheEnum{
    }
}
"""))
        root = engine.Build(session)

        self.assertFalse(session.HasAnyError())
        checker = SemanticChecker(session)
        data = root.visit(checker, None)
        self.assertEqual(len(session.diagnostics), 1)
        self.assertTrue(all(location in session.diagnostics[0].toText() for location in ["TheEnum","(5,36):"]))

    def test_reference_type_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace Namespace1 {
    enum Enum1{
    }
    interface Interface1<T constraint Namespace2.Interface2>{
        enum InnerEnum1{
        }

        property prop1: Interface1
        property prop2: InnerEnum1
        property prop3: Enum1
        property prop4: Namespace2.Enum2
        property prop5: Namespace2.Interface2
        property prop6: Namespace2.Interface2.InnerEnum1
        property prop7: T
                                                
        method Something<K constraint Namespace2.Interface2>()
    }
}
namespace Namespace2 {
    enum Enum2{
    }
    interface Interface2{
        enum InnerEnum1{
        }
    }
}
"""))
        root = engine.Build(session)

        self.assertFalse(session.HasAnyError())
        checker = SemanticChecker(session)
        data = root.visit(checker, None)
        self.assertFalse(session.HasAnyError())

if __name__ == "__main__":
    unittest.main()
