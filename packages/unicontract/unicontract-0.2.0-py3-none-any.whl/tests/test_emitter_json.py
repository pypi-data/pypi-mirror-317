import unittest
from unicontract.Engine import *
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
        enum CustomerType {
            PrivatePerson,
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
            "enums": [
                {
                    "$type": "enum",
                    "name": "CustomerType",
                    "enum_elements": [
                        {
                            "$type": "enum_element",
                            "value": "PrivatePerson",
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 4,
                                "column": 12
                            }
                        },
                        {
                            "$type": "enum_element",
                            "value": "Company",
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 5,
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
        enum CustomerType {
            PrivatePerson,
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
            "enums": [],
            "interfaces": [
                {
                    "$type": "interface",
                    "name": "Customer",
                    "generic": {},
                    "enums": [
                        {
                            "$type": "enum",
                            "name": "CustomerType",
                            "enum_elements": [
                                {
                                    "$type": "enum_element",
                                    "value": "PrivatePerson",
                                    "document_lines": [],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 5,
                                        "column": 12
                                    }
                                },
                                {
                                    "$type": "enum_element",
                                    "value": "Company",
                                    "document_lines": [],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 6,
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
        property country:Country
        readonly property address:string
        property zipCode:integer
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
            "enums": [],
            "interfaces": [
                {
                    "$type": "interface",
                    "name": "PartnerAddress",
                    "generic": {},
                    "enums": [],
                    "methods": [],
                    "properties": [
                        {
                            "$type": "interface_property",
                            "name": "type",
                            "type": {
                                "$type": "reference_type",
                                "kind": "Kind.Reference",
                                "reference_name": "AddressType",
                                "generic": {},
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
                            "name": "country",
                            "type": {
                                "$type": "reference_type",
                                "kind": "Kind.Reference",
                                "reference_name": "Country",
                                "generic": {},
                                "location": {
                                    "fileName": "internal string",
                                    "line": 5,
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
                            "name": "address",
                            "type": {
                                "$type": "primitive_type",
                                "kind": "Kind.Primitive",
                                "primtiveKind": "PrimtiveKind.String",
                                "location": {
                                    "fileName": "internal string",
                                    "line": 6,
                                    "column": 34
                                }
                            },
                            "isReadonly": true,
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 6,
                                "column": 8
                            }
                        },
                        {
                            "$type": "interface_property",
                            "name": "zipCode",
                            "type": {
                                "$type": "primitive_type",
                                "kind": "Kind.Primitive",
                                "primtiveKind": "PrimtiveKind.Integer",
                                "location": {
                                    "fileName": "internal string",
                                    "line": 7,
                                    "column": 25
                                }
                            },
                            "isReadonly": false,
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 7,
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
    interface CustomerService {
        method CreateCustomer( id: string ) => Customer
        method DumpAllCustomer()
        async method CreateCustomerAsync( id: string ) => Customer
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
            "enums": [],
            "interfaces": [
                {
                    "$type": "interface",
                    "name": "CustomerService",
                    "generic": {},
                    "enums": [],
                    "methods": [
                        {
                            "$type": "interface_method",
                            "name": "CreateCustomer",
                            "generic": {},
                            "params": [
                                {
                                    "$type": "interface_method_param",
                                    "name": "id",
                                    "type": {
                                        "$type": "primitive_type",
                                        "kind": "Kind.Primitive",
                                        "primtiveKind": "PrimtiveKind.String",
                                        "location": {
                                            "fileName": "internal string",
                                            "line": 4,
                                            "column": 35
                                        }
                                    },
                                    "document_lines": [],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 4,
                                        "column": 31
                                    }
                                }
                            ],
                            "return_type": {
                                "$type": "reference_type",
                                "kind": "Kind.Reference",
                                "reference_name": "Customer",
                                "generic": {},
                                "location": {
                                    "fileName": "internal string",
                                    "line": 4,
                                    "column": 47
                                }
                            },
                            "isAsync": false,
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 4,
                                "column": 8
                            }
                        },
                        {
                            "$type": "interface_method",
                            "name": "DumpAllCustomer",
                            "generic": {},
                            "params": [],
                            "return_type": {},
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
                            "name": "CreateCustomerAsync",
                            "generic": {},
                            "params": [
                                {
                                    "$type": "interface_method_param",
                                    "name": "id",
                                    "type": {
                                        "$type": "primitive_type",
                                        "kind": "Kind.Primitive",
                                        "primtiveKind": "PrimtiveKind.String",
                                        "location": {
                                            "fileName": "internal string",
                                            "line": 6,
                                            "column": 46
                                        }
                                    },
                                    "document_lines": [],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 6,
                                        "column": 42
                                    }
                                }
                            ],
                            "return_type": {
                                "$type": "reference_type",
                                "kind": "Kind.Reference",
                                "reference_name": "Customer",
                                "generic": {},
                                "location": {
                                    "fileName": "internal string",
                                    "line": 6,
                                    "column": 58
                                }
                            },
                            "isAsync": true,
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 6,
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

    def tests_interface_generic_ok(self):
        engine = Engine()
        session = Session(Source.CreateFromText("""
namespace someNamespace {
    interface CustomerService<T> {
        method CreateCustomer<T>( id: string ) => Customer
        method DumpAllCustomer()
        async method CreateCustomerAsync<T constraint Something>( id: string ) => Customer
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
            "enums": [],
            "interfaces": [
                {
                    "$type": "interface",
                    "name": "CustomerService",
                    "generic": {
                        "$type": "generic",
                        "types": [
                            {
                                "$type": "generic_type",
                                "type_name": "T",
                                "constraint": "",
                                "location": {
                                    "fileName": "internal string",
                                    "line": 3,
                                    "column": 30
                                }
                            }
                        ],
                        "location": {
                            "fileName": "internal string",
                            "line": 3,
                            "column": 29
                        }
                    },
                    "enums": [],
                    "methods": [
                        {
                            "$type": "interface_method",
                            "name": "CreateCustomer",
                            "generic": {
                                "$type": "generic",
                                "types": [
                                    {
                                        "$type": "generic_type",
                                        "type_name": "T",
                                        "constraint": "",
                                        "location": {
                                            "fileName": "internal string",
                                            "line": 4,
                                            "column": 30
                                        }
                                    }
                                ],
                                "location": {
                                    "fileName": "internal string",
                                    "line": 4,
                                    "column": 29
                                }
                            },
                            "params": [
                                {
                                    "$type": "interface_method_param",
                                    "name": "id",
                                    "type": {
                                        "$type": "primitive_type",
                                        "kind": "Kind.Primitive",
                                        "primtiveKind": "PrimtiveKind.String",
                                        "location": {
                                            "fileName": "internal string",
                                            "line": 4,
                                            "column": 38
                                        }
                                    },
                                    "document_lines": [],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 4,
                                        "column": 34
                                    }
                                }
                            ],
                            "return_type": {
                                "$type": "reference_type",
                                "kind": "Kind.Reference",
                                "reference_name": "Customer",
                                "generic": {},
                                "location": {
                                    "fileName": "internal string",
                                    "line": 4,
                                    "column": 50
                                }
                            },
                            "isAsync": false,
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 4,
                                "column": 8
                            }
                        },
                        {
                            "$type": "interface_method",
                            "name": "DumpAllCustomer",
                            "generic": {},
                            "params": [],
                            "return_type": {},
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
                            "name": "CreateCustomerAsync",
                            "generic": {
                                "$type": "generic",
                                "types": [
                                    {
                                        "$type": "generic_type",
                                        "type_name": "T",
                                        "constraint": "Something",
                                        "location": {
                                            "fileName": "internal string",
                                            "line": 6,
                                            "column": 41
                                        }
                                    }
                                ],
                                "location": {
                                    "fileName": "internal string",
                                    "line": 6,
                                    "column": 40
                                }
                            },
                            "params": [
                                {
                                    "$type": "interface_method_param",
                                    "name": "id",
                                    "type": {
                                        "$type": "primitive_type",
                                        "kind": "Kind.Primitive",
                                        "primtiveKind": "PrimtiveKind.String",
                                        "location": {
                                            "fileName": "internal string",
                                            "line": 6,
                                            "column": 70
                                        }
                                    },
                                    "document_lines": [],
                                    "location": {
                                        "fileName": "internal string",
                                        "line": 6,
                                        "column": 66
                                    }
                                }
                            ],
                            "return_type": {
                                "$type": "reference_type",
                                "kind": "Kind.Reference",
                                "reference_name": "Customer",
                                "generic": {},
                                "location": {
                                    "fileName": "internal string",
                                    "line": 6,
                                    "column": 82
                                }
                            },
                            "isAsync": true,
                            "document_lines": [],
                            "location": {
                                "fileName": "internal string",
                                "line": 6,
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
