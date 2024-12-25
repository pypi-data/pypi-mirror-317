parser grammar UniContractGrammar;
options { 
    tokenVocab=UniContractLexer; 
    caseInsensitive = true;
}

contract
    : import_rule* namespace* EOF
    ;

import_rule
    : DOCUMENT_LINE* 'import' qualifiedName
    ;

namespace
    : DOCUMENT_LINE* 'namespace' qualifiedName '{' namespace_elements* '}'
    ;

namespace_elements
    : interface
    | enum
    ;
   
interface
    : DOCUMENT_LINE* 'interface' IDENTIFIER generic? inherits? '{' interface_element* '}'
    ;

    interface_element
        : interface_method
        | interface_property
        | enum
        ;
        
        interface_property
            : DOCUMENT_LINE* 'readonly'? 'property' IDENTIFIER ':' type
            ;

   
        interface_method
            : DOCUMENT_LINE* 'async'? 'method' IDENTIFIER generic? '(' (interface_method_param? (',' interface_method_param)*) ')' ('=>' type )?
            ;

        interface_method_param
            : DOCUMENT_LINE* IDENTIFIER ':' type
            ;

type
    : primitive_type
    | reference_type
    | list_type
    | map_type
    ;
    
    primitive_type
        : 'integer'
        | 'number'
        | 'float'
        | 'date'
        | 'time'
        | 'dateTime'
        | 'string'
        | 'boolean'
        | 'bytes'
        | 'stream'
        ;

    reference_type
        : qualifiedName generic?
        ;

    list_type
        : 'list' '[' type ']'
        ;

    map_type
        : 'map' '[' type ',' type ']'
        ;
        
qualifiedName 
    : IDENTIFIER ('.' IDENTIFIER)* 
    ;

inherits
    : 'inherits' qualifiedName (',' qualifiedName)*
    ;

enum
    : DOCUMENT_LINE* 'enum' IDENTIFIER '{' enum_element? (',' enum_element)* '}'
    ;

    enum_element
        : DOCUMENT_LINE* IDENTIFIER
        ;

generic
    : '<' generic_type (',' generic_type )* '>'
    ;

    generic_type
        : IDENTIFIER ('constraint' qualifiedName)?
        ;

