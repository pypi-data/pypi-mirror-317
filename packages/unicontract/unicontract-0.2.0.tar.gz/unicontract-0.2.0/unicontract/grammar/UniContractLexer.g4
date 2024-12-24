lexer grammar UniContractLexer;

channels {
	COMMENT_CHANNEL
}

options {
	caseInsensitive = true;
}
// syntax elements
DOT: '.';
COMMA: ',';
SEMI: ':';
LPAREN: '(';
RPAREN: ')';
LCURLY: '{';
RCURLY: '}';
LBARCKET: '[';
RBRACKET: ']';
ARROW: '=>';
LT: '<';
GT: '>';

// controls keywords
IMPORT: 'import';

// declaration keywords
INTERFACE: 'interface';
NAMESPACE: 'namespace';
ENUM: 'enum';

// built-in types
INTEGER: 'integer';
NUMBER: 'number';
FLOAT: 'float';
DATE: 'date';
TIME: 'time';
DATETIME: 'dateTime';
STRING: 'string';
BOOLEAN: 'boolean';
BYTES: 'bytes';
STREAM: 'stream';
LIST: 'list';
MAP: 'map';

// qualifiers
INHERITS: 'inherits';
EXTERNAL: 'external';
PROPERTY: 'property';
METHOD: 'method';
READONLY: 'readonly';
ASYNC: 'async';
CONSTRAINT: 'constraint';

// syntax controllers
IDENTIFIER: [a-z][a-z_0-9]*;
WS: [ \t\n\r\f]+ -> skip;

DOCUMENT_LINE: '#' ~[\r\n]*;
LINE_COMMENT: '//' ~[\r\n]* -> channel(COMMENT_CHANNEL);
BLOCK_COMMENT: '/*' .*? '*/' -> channel(COMMENT_CHANNEL);