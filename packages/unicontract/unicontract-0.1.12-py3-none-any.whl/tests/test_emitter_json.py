import unittest
from unicontract import *
from unicontract.emitters.JsonEmitter import *
import jsondiff


class TestEmitterJson(unittest.TestCase):

    def test_empty_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText(""))
        engine.Build(session)
        self.assertFalse(session.HasAnyError())

        jsonEmmiter = JsonEmitter()
        result = jsonEmmiter.Emit(session)
        expected = """{
    "$type": "contract",
    "imports": [],
    "namespaces": []
}"""
        diff = jsondiff.diff(result, expected, syntax='symmetric')
        self.assertEqual(0, len(diff))

    def tests_decorators_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
@without_params
@with_params( "string", 1, 3.14, identifier.sub.sub )
namespace SomeNamespace{
}
"""))
        engine.Build(session)
        self.assertFalse(session.HasAnyError())

        jsonEmmiter = JsonEmitter()
        result = jsonEmmiter.Emit(session)
        expected = """{
    "$type": "contract",
    "imports": [],
    "namespaces": [
        {
            "$type": "namespace",
            "name": "SomeNamespace",
            "decorators": [
                {
                    "$type": "decorator",
                    "name": "without_params",
                    "params": [],
                    "location": {
                        "fileName": "internal string",
                        "line": 2,
                        "column": 0
                    }
                },
                {
                    "$type": "decorator",
                    "name": "with_params",
                    "params": [
                        {
                            "$type": "d3i.decorator_param",
                            "kind": "Kind.String",
                            "value": "string",
                            "location": {
                                "fileName": "internal string",
                                "line": 3,
                                "column": 14
                            }
                        },
                        {
                            "$type": "d3i.decorator_param",
                            "kind": "Kind.Integer",
                            "value": "1",
                            "location": {
                                "fileName": "internal string",
                                "line": 3,
                                "column": 24
                            }
                        },
                        {
                            "$type": "d3i.decorator_param",
                            "kind": "Kind.Number",
                            "value": "3.14",
                            "location": {
                                "fileName": "internal string",
                                "line": 3,
                                "column": 27
                            }
                        },
                        {
                            "$type": "d3i.decorator_param",
                            "kind": "Kind.QualifiedName",
                            "value": "identifier.sub.sub",
                            "location": {
                                "fileName": "internal string",
                                "line": 3,
                                "column": 33
                            }
                        }
                    ],
                    "location": {
                        "fileName": "internal string",
                        "line": 3,
                        "column": 0
                    }
                }
            ],
            "enums": [],
            "interfaces": [],
            "document_lines": [],
            "location": {
                "fileName": "internal string",
                "line": 2,
                "column": 0
            }
        }
    ]
}"""
        diff = jsondiff.diff(result, expected, syntax='symmetric')
        self.assertEqual(0, len(diff))

    def tests_document_lines_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
#doc line 1
#doc line 2
namespace SomeNamespace{
}
"""))
        engine.Build(session)
        self.assertFalse(session.HasAnyError())

        jsonEmmiter = JsonEmitter()
        result = jsonEmmiter.Emit(session)
        expected = """{
    "$type": "contract",
    "imports": [],
    "namespaces": [
        {
            "$type": "namespace",
            "name": "SomeNamespace",
            "decorators": [],
            "enums": [],
            "interfaces": [],
            "document_lines": [
                "doc line 1",
                "doc line 2"
            ],
            "location": {
                "fileName": "internal string",
                "line": 2,
                "column": 0
            }
        }
    ]
}"""
        diff = jsondiff.diff(result, expected, syntax='symmetric')
        self.assertEqual(0, len(diff))


    def tests_namespace_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
@decorator  
@decorator_with_param( "decorator_value")
namespace SomeNamespace {
}
"""))
        engine.Build(session)
        self.assertFalse(session.HasAnyError())

        jsonEmmiter = JsonEmitter()
        result = jsonEmmiter.Emit(session)
        expected = """{
    "$type": "contract",
    "imports": [],
    "namespaces": [
        {
            "$type": "namespace",
            "name": "SomeNamespace",
            "decorators": [
                {
                    "$type": "decorator",
                    "name": "decorator",
                    "params": [],
                    "location": {
                        "fileName": "internal string",
                        "line": 2,
                        "column": 0
                    }
                },
                {
                    "$type": "decorator",
                    "name": "decorator_with_param",
                    "params": [
                        {
                            "$type": "d3i.decorator_param",
                            "kind": "Kind.String",
                            "value": "decorator_value",
                            "location": {
                                "fileName": "internal string",
                                "line": 3,
                                "column": 23
                            }
                        }
                    ],
                    "location": {
                        "fileName": "internal string",
                        "line": 3,
                        "column": 0
                    }
                }
            ],
            "enums": [],
            "interfaces": [],
            "document_lines": [],
            "location": {
                "fileName": "internal string",
                "line": 2,
                "column": 0
            }
        }
    ]
}"""
        diff = jsondiff.diff(result, expected, syntax='symmetric')
        self.assertEqual(0, len(diff))

    def tests_enum_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace SomeNamespace {
        @enum_decorator  
        @enum_decorator_with_param( "decorator_value")
        enum CustomerType {
            @value( 1 )
            PrivatePerson,
            @value( 2 )
            Company
        }
}
"""))
        engine.Build(session)
        self.assertFalse(session.HasAnyError())

        jsonEmmiter = JsonEmitter()
        result = jsonEmmiter.Emit(session)
        expected = """{
    "$type": "contract",
    "imports": [],
    "namespaces": [
        {
            "$type": "namespace",
            "name": "SomeNamespace",
            "decorators": [],
            "enums": [
                {
                    "$type": "enum",
                    "decorators": [
                        {
                            "$type": "decorator",
                            "name": "enum_decorator",
                            "params": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 3,
                                "column": 8
                            }
                        },
                        {
                            "$type": "decorator",
                            "name": "enum_decorator_with_param",
                            "params": [
                                {
                                    "$type": "d3i.decorator_param",
                                    "kind": "Kind.String",
                                    "value": "decorator_value",
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 4,
                                        "column": 36
                                    }
                                }
                            ],
                            "location": {
                                "fileName": "internal string",
                                "line": 4,
                                "column": 8
                            }
                        }
                    ],
                    "name": "CustomerType",
                    "enum_elements": [
                        {
                            "$type": "enum_element",
                            "decorators": [
                                {
                                    "$type": "decorator",
                                    "name": "value",
                                    "params": [
                                        {
                                            "$type": "d3i.decorator_param",
                                            "kind": "Kind.Integer",
                                            "value": "1",
                                            "location": {
                                                "fileName": "internal string",
                                                "line": 6,
                                                "column": 20
                                            }
                                        }
                                    ],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 6,
                                        "column": 12
                                    }
                                }
                            ],
                            "value": "PrivatePerson",
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 6,
                                "column": 12
                            }
                        },
                        {
                            "$type": "enum_element",
                            "decorators": [
                                {
                                    "$type": "decorator",
                                    "name": "value",
                                    "params": [
                                        {
                                            "$type": "d3i.decorator_param",
                                            "kind": "Kind.Integer",
                                            "value": "2",
                                            "location": {
                                                "fileName": "internal string",
                                                "line": 8,
                                                "column": 20
                                            }
                                        }
                                    ],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 8,
                                        "column": 12
                                    }
                                }
                            ],
                            "value": "Company",
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 8,
                                "column": 12
                            }
                        }
                    ],
                    "document_lines": [],
                    "location": {
                        "fileName": "internal string",
                        "line": 3,
                        "column": 8
                    }
                }
            ],
            "interfaces": [],
            "document_lines": [],
            "location": {
                "fileName": "internal string",
                "line": 2,
                "column": 0
            }
        }
    ]
}"""
        diff = jsondiff.diff(result, expected, syntax='symmetric')
        self.assertEqual(0, len(diff))

    def tests_interface_internal_enum_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace SomeDomain {
    interface Customer{
        @enum_decorator  
        @enum_decorator_with_param( "decorator_value")
        enum CustomerType {
            @value( 1 )
            PrivatePerson,
            @value( 2 )
            Company
        }
    }
}
"""))
        engine.Build(session)
        self.assertFalse(session.HasAnyError())

        jsonEmmiter = JsonEmitter()
        result = jsonEmmiter.Emit(session)
        expected = """{
    "$type": "contract",
    "imports": [],
    "namespaces": [
        {
            "$type": "namespace",
            "name": "SomeDomain",
            "decorators": [],
            "enums": [],
            "interfaces": [
                {
                    "$type": "interface",
                    "decorators": [],
                    "name": "Customer",
                    "enums": [
                        {
                            "$type": "enum",
                            "decorators": [
                                {
                                    "$type": "decorator",
                                    "name": "enum_decorator",
                                    "params": [],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 4,
                                        "column": 8
                                    }
                                },
                                {
                                    "$type": "decorator",
                                    "name": "enum_decorator_with_param",
                                    "params": [
                                        {
                                            "$type": "d3i.decorator_param",
                                            "kind": "Kind.String",
                                            "value": "decorator_value",
                                            "location": {
                                                "fileName": "internal string",
                                                "line": 5,
                                                "column": 36
                                            }
                                        }
                                    ],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 5,
                                        "column": 8
                                    }
                                }
                            ],
                            "name": "CustomerType",
                            "enum_elements": [
                                {
                                    "$type": "enum_element",
                                    "decorators": [
                                        {
                                            "$type": "decorator",
                                            "name": "value",
                                            "params": [
                                                {
                                                    "$type": "d3i.decorator_param",
                                                    "kind": "Kind.Integer",
                                                    "value": "1",
                                                    "location": {
                                                        "fileName": "internal string",
                                                        "line": 7,
                                                        "column": 20
                                                    }
                                                }
                                            ],
                                            "location": {
                                                "fileName": "internal string",
                                                "line": 7,
                                                "column": 12
                                            }
                                        }
                                    ],
                                    "value": "PrivatePerson",
                                    "document_lines": [],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 7,
                                        "column": 12
                                    }
                                },
                                {
                                    "$type": "enum_element",
                                    "decorators": [
                                        {
                                            "$type": "decorator",
                                            "name": "value",
                                            "params": [
                                                {
                                                    "$type": "d3i.decorator_param",
                                                    "kind": "Kind.Integer",
                                                    "value": "2",
                                                    "location": {
                                                        "fileName": "internal string",
                                                        "line": 9,
                                                        "column": 20
                                                    }
                                                }
                                            ],
                                            "location": {
                                                "fileName": "internal string",
                                                "line": 9,
                                                "column": 12
                                            }
                                        }
                                    ],
                                    "value": "Company",
                                    "document_lines": [],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 9,
                                        "column": 12
                                    }
                                }
                            ],
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 4,
                                "column": 8
                            }
                        }
                    ],
                    "methods": [],
                    "properties": [],
                    "document_lines": [],
                    "location": {
                        "fileName": "internal string",
                        "line": 3,
                        "column": 4
                    }
                }
            ],
            "document_lines": [],
            "location": {
                "fileName": "internal string",
                "line": 2,
                "column": 0
            }
        }
    ]
}"""
        diff = jsondiff.diff(result, expected, syntax='symmetric')
        self.assertEqual(0, len(diff))

    def tests_interface_property_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace SomeNameSpace {
    interface PartnerAddress {
        property type:AddressType
        @sample_decorator( "listOfContries" )
        property country:Country
        @max_length( 100 )
        readonly property address:string
        property zipCode:integer
        property private_member:external["java.util.map.HashMap<>"]
    }
}
"""))
        engine.Build(session)
        self.assertFalse(session.HasAnyError())

        jsonEmmiter = JsonEmitter()
        result = jsonEmmiter.Emit(session)

        expected = """{
    "$type": "contract",
    "imports": [],
    "namespaces": [
        {
            "$type": "namespace",
            "name": "SomeNameSpace",
            "decorators": [],
            "enums": [],
            "interfaces": [
                {
                    "$type": "interface",
                    "decorators": [],
                    "name": "PartnerAddress",
                    "enums": [],
                    "methods": [],
                    "properties": [
                        {
                            "$type": "interface_property",
                            "decorators": [],
                            "name": "type",
                            "type": {
                                "$type": "reference_type",
                                "kind": "Kind.Reference",
                                "isExternal": false,
                                "reference_name": "AddressType",
                                "location": {
                                    "fileName": "internal string",
                                    "line": 4,
                                    "column": 22
                                }
                            },
                            "isReadonly": false,
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 4,
                                "column": 8
                            }
                        },
                        {
                            "$type": "interface_property",
                            "decorators": [
                                {
                                    "$type": "decorator",
                                    "name": "sample_decorator",
                                    "params": [
                                        {
                                            "$type": "d3i.decorator_param",
                                            "kind": "Kind.String",
                                            "value": "listOfContries",
                                            "location": {
                                                "fileName": "internal string",
                                                "line": 5,
                                                "column": 27
                                            }
                                        }
                                    ],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 5,
                                        "column": 8
                                    }
                                }
                            ],
                            "name": "country",
                            "type": {
                                "$type": "reference_type",
                                "kind": "Kind.Reference",
                                "isExternal": false,
                                "reference_name": "Country",
                                "location": {
                                    "fileName": "internal string",
                                    "line": 6,
                                    "column": 25
                                }
                            },
                            "isReadonly": false,
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 5,
                                "column": 8
                            }
                        },
                        {
                            "$type": "interface_property",
                            "decorators": [
                                {
                                    "$type": "decorator",
                                    "name": "max_length",
                                    "params": [
                                        {
                                            "$type": "d3i.decorator_param",
                                            "kind": "Kind.Integer",
                                            "value": "100",
                                            "location": {
                                                "fileName": "internal string",
                                                "line": 7,
                                                "column": 21
                                            }
                                        }
                                    ],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 7,
                                        "column": 8
                                    }
                                }
                            ],
                            "name": "address",
                            "type": {
                                "$type": "primitive_type",
                                "kind": "Kind.Primitive",
                                "primtiveKind": "PrimtiveKind.String",
                                "location": {
                                    "fileName": "internal string",
                                    "line": 8,
                                    "column": 34
                                }
                            },
                            "isReadonly": true,
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 7,
                                "column": 8
                            }
                        },
                        {
                            "$type": "interface_property",
                            "decorators": [],
                            "name": "zipCode",
                            "type": {
                                "$type": "primitive_type",
                                "kind": "Kind.Primitive",
                                "primtiveKind": "PrimtiveKind.Integer",
                                "location": {
                                    "fileName": "internal string",
                                    "line": 9,
                                    "column": 25
                                }
                            },
                            "isReadonly": false,
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 9,
                                "column": 8
                            }
                        },
                        {
                            "$type": "interface_property",
                            "decorators": [],
                            "name": "private_member",
                            "type": {
                                "$type": "reference_type",
                                "kind": "Kind.Reference",
                                "isExternal": true,
                                "reference_name": "java.util.map.HashMap<>",
                                "location": {
                                    "fileName": "internal string",
                                    "line": 10,
                                    "column": 32
                                }
                            },
                            "isReadonly": false,
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 10,
                                "column": 8
                            }
                        }
                    ],
                    "document_lines": [],
                    "location": {
                        "fileName": "internal string",
                        "line": 3,
                        "column": 4
                    }
                }
            ],
            "document_lines": [],
            "location": {
                "fileName": "internal string",
                "line": 2,
                "column": 0
            }
        }
    ]
}"""
        diff = jsondiff.diff(result, expected, syntax='symmetric')
        self.assertEqual(0, len(diff))

    def tests_interface_methods_ok(self):
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
        engine.Build(session)

        jsonEmmiter = JsonEmitter()
        result = jsonEmmiter.Emit(session)

        expected = """{
    "$type": "contract",
    "imports": [],
    "namespaces": [
        {
            "$type": "namespace",
            "name": "someNamespace",
            "decorators": [],
            "enums": [],
            "interfaces": [
                {
                    "$type": "interface",
                    "decorators": [
                        {
                            "$type": "decorator",
                            "name": "decorator",
                            "params": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 3,
                                "column": 4
                            }
                        }
                    ],
                    "name": "CustomerService",
                    "enums": [],
                    "methods": [
                        {
                            "$type": "interface_method",
                            "decorators": [
                                {
                                    "$type": "decorator",
                                    "name": "decorator_method",
                                    "params": [],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 5,
                                        "column": 8
                                    }
                                }
                            ],
                            "name": "CreateCustomer",
                            "params": [
                                {
                                    "$type": "interface_method_param",
                                    "decorators": [
                                        {
                                            "$type": "decorator",
                                            "name": "required",
                                            "params": [],
                                            "location": {
                                                "fileName": "internal string",
                                                "line": 6,
                                                "column": 31
                                            }
                                        }
                                    ],
                                    "name": "id",
                                    "type": {
                                        "$type": "primitive_type",
                                        "kind": "Kind.Primitive",
                                        "primtiveKind": "PrimtiveKind.String",
                                        "location": {
                                            "fileName": "internal string",
                                            "line": 6,
                                            "column": 45
                                        }
                                    },
                                    "document_lines": [],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 6,
                                        "column": 31
                                    }
                                }
                            ],
                            "return_type": {
                                "$type": "reference_type",
                                "kind": "Kind.Reference",
                                "isExternal": false,
                                "reference_name": "Customer",
                                "location": {
                                    "fileName": "internal string",
                                    "line": 6,
                                    "column": 57
                                }
                            },
                            "isAsync": false,
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 5,
                                "column": 8
                            }
                        },
                        {
                            "$type": "interface_method",
                            "decorators": [
                                {
                                    "$type": "decorator",
                                    "name": "decorator_method",
                                    "params": [],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 8,
                                        "column": 8
                                    }
                                }
                            ],
                            "name": "DumpAllCustomer",
                            "params": [],
                            "return_type": {},
                            "isAsync": false,
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 8,
                                "column": 8
                            }
                        },
                        {
                            "$type": "interface_method",
                            "decorators": [
                                {
                                    "$type": "decorator",
                                    "name": "decorator_method",
                                    "params": [],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 11,
                                        "column": 8
                                    }
                                }
                            ],
                            "name": "CreateCustomerAsync",
                            "params": [
                                {
                                    "$type": "interface_method_param",
                                    "decorators": [
                                        {
                                            "$type": "decorator",
                                            "name": "required",
                                            "params": [],
                                            "location": {
                                                "fileName": "internal string",
                                                "line": 12,
                                                "column": 42
                                            }
                                        }
                                    ],
                                    "name": "id",
                                    "type": {
                                        "$type": "primitive_type",
                                        "kind": "Kind.Primitive",
                                        "primtiveKind": "PrimtiveKind.String",
                                        "location": {
                                            "fileName": "internal string",
                                            "line": 12,
                                            "column": 56
                                        }
                                    },
                                    "document_lines": [],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 12,
                                        "column": 42
                                    }
                                }
                            ],
                            "return_type": {
                                "$type": "reference_type",
                                "kind": "Kind.Reference",
                                "isExternal": false,
                                "reference_name": "Customer",
                                "location": {
                                    "fileName": "internal string",
                                    "line": 12,
                                    "column": 68
                                }
                            },
                            "isAsync": true,
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 11,
                                "column": 8
                            }
                        }
                    ],
                    "properties": [],
                    "document_lines": [],
                    "location": {
                        "fileName": "internal string",
                        "line": 3,
                        "column": 4
                    }
                }
            ],
            "document_lines": [],
            "location": {
                "fileName": "internal string",
                "line": 2,
                "column": 0
            }
        }
    ]
}"""
        diff = jsondiff.diff(result, expected, syntax='symmetric')
        self.assertEqual(0, len(diff))


if __name__ == "__main__":
    unittest.main()
