parser grammar UniContractGrammar;
options { 
    tokenVocab=UniContractLexer; 
    caseInsensitive = true;
}

contract
    : import_rule* namespace* EOF
    ;

import_rule
    : DOCUMENT_LINE* decorator* 'import' qualifiedName
    | DOCUMENT_LINE* decorator* 'import' STRING_LITERAL
    ;

namespace
    : DOCUMENT_LINE* decorator* 'namespace' qualifiedName '{' namespace_elements* '}'
    ;

namespace_elements
    : interface
    | enum
    ;
   
interface
    : DOCUMENT_LINE* decorator* 'interface' IDENTIFIER inherits? '{' interface_element* '}'
    ;

    interface_element
        : interface_method
        | interface_property
        | enum
        ;
        
        interface_property
            : DOCUMENT_LINE* decorator* 'readonly'? 'property' IDENTIFIER ':' type
            ;

   
        interface_method
            : DOCUMENT_LINE* decorator* 'async'? 'method' IDENTIFIER '(' (interface_method_param? (',' interface_method_param)*) ')' ('=>' type )?
            ;

        interface_method_param
            : DOCUMENT_LINE* decorator* IDENTIFIER ':' type
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
        : qualifiedName
        | 'external' '[' STRING_LITERAL ']'
        ;

    list_type
        : 'list' '[' type ']'
        ;

    map_type
        : 'map' '[' type ',' type ']'
        ;
        
decorator
    : '@' IDENTIFIER
    | '@' IDENTIFIER '(' decorator_param (',' decorator_param)* ')' ;
    
    decorator_param
        : qualifiedName
        | INTEGER_CONSTANS
        | NUMBER_CONSTANS 
        | STRING_LITERAL
        ;

qualifiedName 
    : IDENTIFIER ('.' IDENTIFIER)* 
    ;

inherits
    : 'inherits' qualifiedName (',' qualifiedName)*
    ;

enum
    : DOCUMENT_LINE* decorator* 'enum' IDENTIFIER '{' enum_element? (',' enum_element)* '}'
    ;

    enum_element
        : DOCUMENT_LINE* decorator* IDENTIFIER
        ;