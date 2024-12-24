// Generated from d:/Projects.OWN/UniContract/unicontract/grammar/UniContractGrammar.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class UniContractGrammar extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		DOT=1, COMMA=2, SEMI=3, LPAREN=4, RPAREN=5, LCURLY=6, RCURLY=7, LBARCKET=8, 
		RBRACKET=9, AT=10, ARROW=11, IMPORT=12, INTERFACE=13, NAMESPACE=14, ENUM=15, 
		INTEGER=16, NUMBER=17, FLOAT=18, DATE=19, TIME=20, DATETIME=21, STRING=22, 
		BOOLEAN=23, BYTES=24, STREAM=25, LIST=26, MAP=27, INHERITS=28, EXTERNAL=29, 
		PROPERTY=30, METHOD=31, READONLY=32, ASYNC=33, INTEGER_CONSTANS=34, NUMBER_CONSTANS=35, 
		STRING_LITERAL=36, IDENTIFIER=37, WS=38, DOCUMENT_LINE=39, LINE_COMMENT=40, 
		BLOCK_COMMENT=41;
	public static final int
		RULE_contract = 0, RULE_import_rule = 1, RULE_namespace = 2, RULE_namespace_elements = 3, 
		RULE_interface = 4, RULE_interface_element = 5, RULE_interface_property = 6, 
		RULE_interface_method = 7, RULE_interface_method_param = 8, RULE_type = 9, 
		RULE_primitive_type = 10, RULE_reference_type = 11, RULE_list_type = 12, 
		RULE_map_type = 13, RULE_decorator = 14, RULE_decorator_param = 15, RULE_qualifiedName = 16, 
		RULE_inherits = 17, RULE_enum = 18, RULE_enum_element = 19;
	private static String[] makeRuleNames() {
		return new String[] {
			"contract", "import_rule", "namespace", "namespace_elements", "interface", 
			"interface_element", "interface_property", "interface_method", "interface_method_param", 
			"type", "primitive_type", "reference_type", "list_type", "map_type", 
			"decorator", "decorator_param", "qualifiedName", "inherits", "enum", 
			"enum_element"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'.'", "','", "':'", "'('", "')'", "'{'", "'}'", "'['", "']'", 
			"'@'", "'=>'", "'import'", "'interface'", "'namespace'", "'enum'", "'integer'", 
			"'number'", "'float'", "'date'", "'time'", "'dateTime'", "'string'", 
			"'boolean'", "'bytes'", "'stream'", "'list'", "'map'", "'inherits'", 
			"'external'", "'property'", "'method'", "'readonly'", "'async'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "DOT", "COMMA", "SEMI", "LPAREN", "RPAREN", "LCURLY", "RCURLY", 
			"LBARCKET", "RBRACKET", "AT", "ARROW", "IMPORT", "INTERFACE", "NAMESPACE", 
			"ENUM", "INTEGER", "NUMBER", "FLOAT", "DATE", "TIME", "DATETIME", "STRING", 
			"BOOLEAN", "BYTES", "STREAM", "LIST", "MAP", "INHERITS", "EXTERNAL", 
			"PROPERTY", "METHOD", "READONLY", "ASYNC", "INTEGER_CONSTANS", "NUMBER_CONSTANS", 
			"STRING_LITERAL", "IDENTIFIER", "WS", "DOCUMENT_LINE", "LINE_COMMENT", 
			"BLOCK_COMMENT"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "UniContractGrammar.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public UniContractGrammar(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ContractContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(UniContractGrammar.EOF, 0); }
		public List<Import_ruleContext> import_rule() {
			return getRuleContexts(Import_ruleContext.class);
		}
		public Import_ruleContext import_rule(int i) {
			return getRuleContext(Import_ruleContext.class,i);
		}
		public List<NamespaceContext> namespace() {
			return getRuleContexts(NamespaceContext.class);
		}
		public NamespaceContext namespace(int i) {
			return getRuleContext(NamespaceContext.class,i);
		}
		public ContractContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_contract; }
	}

	public final ContractContext contract() throws RecognitionException {
		ContractContext _localctx = new ContractContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_contract);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(43);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,0,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(40);
					import_rule();
					}
					} 
				}
				setState(45);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,0,_ctx);
			}
			setState(49);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 549755831296L) != 0)) {
				{
				{
				setState(46);
				namespace();
				}
				}
				setState(51);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(52);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Import_ruleContext extends ParserRuleContext {
		public TerminalNode IMPORT() { return getToken(UniContractGrammar.IMPORT, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public List<TerminalNode> DOCUMENT_LINE() { return getTokens(UniContractGrammar.DOCUMENT_LINE); }
		public TerminalNode DOCUMENT_LINE(int i) {
			return getToken(UniContractGrammar.DOCUMENT_LINE, i);
		}
		public List<DecoratorContext> decorator() {
			return getRuleContexts(DecoratorContext.class);
		}
		public DecoratorContext decorator(int i) {
			return getRuleContext(DecoratorContext.class,i);
		}
		public TerminalNode STRING_LITERAL() { return getToken(UniContractGrammar.STRING_LITERAL, 0); }
		public Import_ruleContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_import_rule; }
	}

	public final Import_ruleContext import_rule() throws RecognitionException {
		Import_ruleContext _localctx = new Import_ruleContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_import_rule);
		int _la;
		try {
			setState(82);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,6,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(57);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==DOCUMENT_LINE) {
					{
					{
					setState(54);
					match(DOCUMENT_LINE);
					}
					}
					setState(59);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(63);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==AT) {
					{
					{
					setState(60);
					decorator();
					}
					}
					setState(65);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(66);
				match(IMPORT);
				setState(67);
				qualifiedName();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(71);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==DOCUMENT_LINE) {
					{
					{
					setState(68);
					match(DOCUMENT_LINE);
					}
					}
					setState(73);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(77);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==AT) {
					{
					{
					setState(74);
					decorator();
					}
					}
					setState(79);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(80);
				match(IMPORT);
				setState(81);
				match(STRING_LITERAL);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class NamespaceContext extends ParserRuleContext {
		public TerminalNode NAMESPACE() { return getToken(UniContractGrammar.NAMESPACE, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode LCURLY() { return getToken(UniContractGrammar.LCURLY, 0); }
		public TerminalNode RCURLY() { return getToken(UniContractGrammar.RCURLY, 0); }
		public List<TerminalNode> DOCUMENT_LINE() { return getTokens(UniContractGrammar.DOCUMENT_LINE); }
		public TerminalNode DOCUMENT_LINE(int i) {
			return getToken(UniContractGrammar.DOCUMENT_LINE, i);
		}
		public List<DecoratorContext> decorator() {
			return getRuleContexts(DecoratorContext.class);
		}
		public DecoratorContext decorator(int i) {
			return getRuleContext(DecoratorContext.class,i);
		}
		public List<Namespace_elementsContext> namespace_elements() {
			return getRuleContexts(Namespace_elementsContext.class);
		}
		public Namespace_elementsContext namespace_elements(int i) {
			return getRuleContext(Namespace_elementsContext.class,i);
		}
		public NamespaceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_namespace; }
	}

	public final NamespaceContext namespace() throws RecognitionException {
		NamespaceContext _localctx = new NamespaceContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_namespace);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(87);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOCUMENT_LINE) {
				{
				{
				setState(84);
				match(DOCUMENT_LINE);
				}
				}
				setState(89);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(93);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==AT) {
				{
				{
				setState(90);
				decorator();
				}
				}
				setState(95);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(96);
			match(NAMESPACE);
			setState(97);
			qualifiedName();
			setState(98);
			match(LCURLY);
			setState(102);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 549755855872L) != 0)) {
				{
				{
				setState(99);
				namespace_elements();
				}
				}
				setState(104);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(105);
			match(RCURLY);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Namespace_elementsContext extends ParserRuleContext {
		public InterfaceContext interface_() {
			return getRuleContext(InterfaceContext.class,0);
		}
		public EnumContext enum_() {
			return getRuleContext(EnumContext.class,0);
		}
		public Namespace_elementsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_namespace_elements; }
	}

	public final Namespace_elementsContext namespace_elements() throws RecognitionException {
		Namespace_elementsContext _localctx = new Namespace_elementsContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_namespace_elements);
		try {
			setState(109);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,10,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(107);
				interface_();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(108);
				enum_();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InterfaceContext extends ParserRuleContext {
		public TerminalNode INTERFACE() { return getToken(UniContractGrammar.INTERFACE, 0); }
		public TerminalNode IDENTIFIER() { return getToken(UniContractGrammar.IDENTIFIER, 0); }
		public TerminalNode LCURLY() { return getToken(UniContractGrammar.LCURLY, 0); }
		public TerminalNode RCURLY() { return getToken(UniContractGrammar.RCURLY, 0); }
		public List<TerminalNode> DOCUMENT_LINE() { return getTokens(UniContractGrammar.DOCUMENT_LINE); }
		public TerminalNode DOCUMENT_LINE(int i) {
			return getToken(UniContractGrammar.DOCUMENT_LINE, i);
		}
		public List<DecoratorContext> decorator() {
			return getRuleContexts(DecoratorContext.class);
		}
		public DecoratorContext decorator(int i) {
			return getRuleContext(DecoratorContext.class,i);
		}
		public InheritsContext inherits() {
			return getRuleContext(InheritsContext.class,0);
		}
		public List<Interface_elementContext> interface_element() {
			return getRuleContexts(Interface_elementContext.class);
		}
		public Interface_elementContext interface_element(int i) {
			return getRuleContext(Interface_elementContext.class,i);
		}
		public InterfaceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_interface; }
	}

	public final InterfaceContext interface_() throws RecognitionException {
		InterfaceContext _localctx = new InterfaceContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_interface);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(114);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOCUMENT_LINE) {
				{
				{
				setState(111);
				match(DOCUMENT_LINE);
				}
				}
				setState(116);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(120);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==AT) {
				{
				{
				setState(117);
				decorator();
				}
				}
				setState(122);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(123);
			match(INTERFACE);
			setState(124);
			match(IDENTIFIER);
			setState(126);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==INHERITS) {
				{
				setState(125);
				inherits();
				}
			}

			setState(128);
			match(LCURLY);
			setState(132);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 565861975040L) != 0)) {
				{
				{
				setState(129);
				interface_element();
				}
				}
				setState(134);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(135);
			match(RCURLY);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Interface_elementContext extends ParserRuleContext {
		public Interface_methodContext interface_method() {
			return getRuleContext(Interface_methodContext.class,0);
		}
		public Interface_propertyContext interface_property() {
			return getRuleContext(Interface_propertyContext.class,0);
		}
		public EnumContext enum_() {
			return getRuleContext(EnumContext.class,0);
		}
		public Interface_elementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_interface_element; }
	}

	public final Interface_elementContext interface_element() throws RecognitionException {
		Interface_elementContext _localctx = new Interface_elementContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_interface_element);
		try {
			setState(140);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,15,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(137);
				interface_method();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(138);
				interface_property();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(139);
				enum_();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Interface_propertyContext extends ParserRuleContext {
		public TerminalNode PROPERTY() { return getToken(UniContractGrammar.PROPERTY, 0); }
		public TerminalNode IDENTIFIER() { return getToken(UniContractGrammar.IDENTIFIER, 0); }
		public TerminalNode SEMI() { return getToken(UniContractGrammar.SEMI, 0); }
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public List<TerminalNode> DOCUMENT_LINE() { return getTokens(UniContractGrammar.DOCUMENT_LINE); }
		public TerminalNode DOCUMENT_LINE(int i) {
			return getToken(UniContractGrammar.DOCUMENT_LINE, i);
		}
		public List<DecoratorContext> decorator() {
			return getRuleContexts(DecoratorContext.class);
		}
		public DecoratorContext decorator(int i) {
			return getRuleContext(DecoratorContext.class,i);
		}
		public TerminalNode READONLY() { return getToken(UniContractGrammar.READONLY, 0); }
		public Interface_propertyContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_interface_property; }
	}

	public final Interface_propertyContext interface_property() throws RecognitionException {
		Interface_propertyContext _localctx = new Interface_propertyContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_interface_property);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(145);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOCUMENT_LINE) {
				{
				{
				setState(142);
				match(DOCUMENT_LINE);
				}
				}
				setState(147);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(151);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==AT) {
				{
				{
				setState(148);
				decorator();
				}
				}
				setState(153);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(155);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==READONLY) {
				{
				setState(154);
				match(READONLY);
				}
			}

			setState(157);
			match(PROPERTY);
			setState(158);
			match(IDENTIFIER);
			setState(159);
			match(SEMI);
			setState(160);
			type();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Interface_methodContext extends ParserRuleContext {
		public TerminalNode METHOD() { return getToken(UniContractGrammar.METHOD, 0); }
		public TerminalNode IDENTIFIER() { return getToken(UniContractGrammar.IDENTIFIER, 0); }
		public TerminalNode LPAREN() { return getToken(UniContractGrammar.LPAREN, 0); }
		public TerminalNode RPAREN() { return getToken(UniContractGrammar.RPAREN, 0); }
		public List<TerminalNode> DOCUMENT_LINE() { return getTokens(UniContractGrammar.DOCUMENT_LINE); }
		public TerminalNode DOCUMENT_LINE(int i) {
			return getToken(UniContractGrammar.DOCUMENT_LINE, i);
		}
		public List<DecoratorContext> decorator() {
			return getRuleContexts(DecoratorContext.class);
		}
		public DecoratorContext decorator(int i) {
			return getRuleContext(DecoratorContext.class,i);
		}
		public TerminalNode ASYNC() { return getToken(UniContractGrammar.ASYNC, 0); }
		public TerminalNode ARROW() { return getToken(UniContractGrammar.ARROW, 0); }
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public List<Interface_method_paramContext> interface_method_param() {
			return getRuleContexts(Interface_method_paramContext.class);
		}
		public Interface_method_paramContext interface_method_param(int i) {
			return getRuleContext(Interface_method_paramContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(UniContractGrammar.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(UniContractGrammar.COMMA, i);
		}
		public Interface_methodContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_interface_method; }
	}

	public final Interface_methodContext interface_method() throws RecognitionException {
		Interface_methodContext _localctx = new Interface_methodContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_interface_method);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(165);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOCUMENT_LINE) {
				{
				{
				setState(162);
				match(DOCUMENT_LINE);
				}
				}
				setState(167);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(171);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==AT) {
				{
				{
				setState(168);
				decorator();
				}
				}
				setState(173);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(175);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ASYNC) {
				{
				setState(174);
				match(ASYNC);
				}
			}

			setState(177);
			match(METHOD);
			setState(178);
			match(IDENTIFIER);
			setState(179);
			match(LPAREN);
			{
			setState(181);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 687194768384L) != 0)) {
				{
				setState(180);
				interface_method_param();
				}
			}

			setState(187);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(183);
				match(COMMA);
				setState(184);
				interface_method_param();
				}
				}
				setState(189);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
			setState(190);
			match(RPAREN);
			setState(193);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ARROW) {
				{
				setState(191);
				match(ARROW);
				setState(192);
				type();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Interface_method_paramContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(UniContractGrammar.IDENTIFIER, 0); }
		public TerminalNode SEMI() { return getToken(UniContractGrammar.SEMI, 0); }
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public List<TerminalNode> DOCUMENT_LINE() { return getTokens(UniContractGrammar.DOCUMENT_LINE); }
		public TerminalNode DOCUMENT_LINE(int i) {
			return getToken(UniContractGrammar.DOCUMENT_LINE, i);
		}
		public List<DecoratorContext> decorator() {
			return getRuleContexts(DecoratorContext.class);
		}
		public DecoratorContext decorator(int i) {
			return getRuleContext(DecoratorContext.class,i);
		}
		public Interface_method_paramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_interface_method_param; }
	}

	public final Interface_method_paramContext interface_method_param() throws RecognitionException {
		Interface_method_paramContext _localctx = new Interface_method_paramContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_interface_method_param);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(198);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOCUMENT_LINE) {
				{
				{
				setState(195);
				match(DOCUMENT_LINE);
				}
				}
				setState(200);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(204);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==AT) {
				{
				{
				setState(201);
				decorator();
				}
				}
				setState(206);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(207);
			match(IDENTIFIER);
			setState(208);
			match(SEMI);
			setState(209);
			type();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class TypeContext extends ParserRuleContext {
		public Primitive_typeContext primitive_type() {
			return getRuleContext(Primitive_typeContext.class,0);
		}
		public Reference_typeContext reference_type() {
			return getRuleContext(Reference_typeContext.class,0);
		}
		public List_typeContext list_type() {
			return getRuleContext(List_typeContext.class,0);
		}
		public Map_typeContext map_type() {
			return getRuleContext(Map_typeContext.class,0);
		}
		public TypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_type; }
	}

	public final TypeContext type() throws RecognitionException {
		TypeContext _localctx = new TypeContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_type);
		try {
			setState(215);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case INTEGER:
			case NUMBER:
			case FLOAT:
			case DATE:
			case TIME:
			case DATETIME:
			case STRING:
			case BOOLEAN:
			case BYTES:
			case STREAM:
				enterOuterAlt(_localctx, 1);
				{
				setState(211);
				primitive_type();
				}
				break;
			case EXTERNAL:
			case IDENTIFIER:
				enterOuterAlt(_localctx, 2);
				{
				setState(212);
				reference_type();
				}
				break;
			case LIST:
				enterOuterAlt(_localctx, 3);
				{
				setState(213);
				list_type();
				}
				break;
			case MAP:
				enterOuterAlt(_localctx, 4);
				{
				setState(214);
				map_type();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Primitive_typeContext extends ParserRuleContext {
		public TerminalNode INTEGER() { return getToken(UniContractGrammar.INTEGER, 0); }
		public TerminalNode NUMBER() { return getToken(UniContractGrammar.NUMBER, 0); }
		public TerminalNode FLOAT() { return getToken(UniContractGrammar.FLOAT, 0); }
		public TerminalNode DATE() { return getToken(UniContractGrammar.DATE, 0); }
		public TerminalNode TIME() { return getToken(UniContractGrammar.TIME, 0); }
		public TerminalNode DATETIME() { return getToken(UniContractGrammar.DATETIME, 0); }
		public TerminalNode STRING() { return getToken(UniContractGrammar.STRING, 0); }
		public TerminalNode BOOLEAN() { return getToken(UniContractGrammar.BOOLEAN, 0); }
		public TerminalNode BYTES() { return getToken(UniContractGrammar.BYTES, 0); }
		public TerminalNode STREAM() { return getToken(UniContractGrammar.STREAM, 0); }
		public Primitive_typeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_primitive_type; }
	}

	public final Primitive_typeContext primitive_type() throws RecognitionException {
		Primitive_typeContext _localctx = new Primitive_typeContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_primitive_type);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(217);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 67043328L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Reference_typeContext extends ParserRuleContext {
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode EXTERNAL() { return getToken(UniContractGrammar.EXTERNAL, 0); }
		public TerminalNode LBARCKET() { return getToken(UniContractGrammar.LBARCKET, 0); }
		public TerminalNode STRING_LITERAL() { return getToken(UniContractGrammar.STRING_LITERAL, 0); }
		public TerminalNode RBRACKET() { return getToken(UniContractGrammar.RBRACKET, 0); }
		public Reference_typeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_reference_type; }
	}

	public final Reference_typeContext reference_type() throws RecognitionException {
		Reference_typeContext _localctx = new Reference_typeContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_reference_type);
		try {
			setState(224);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case IDENTIFIER:
				enterOuterAlt(_localctx, 1);
				{
				setState(219);
				qualifiedName();
				}
				break;
			case EXTERNAL:
				enterOuterAlt(_localctx, 2);
				{
				setState(220);
				match(EXTERNAL);
				setState(221);
				match(LBARCKET);
				setState(222);
				match(STRING_LITERAL);
				setState(223);
				match(RBRACKET);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class List_typeContext extends ParserRuleContext {
		public TerminalNode LIST() { return getToken(UniContractGrammar.LIST, 0); }
		public TerminalNode LBARCKET() { return getToken(UniContractGrammar.LBARCKET, 0); }
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public TerminalNode RBRACKET() { return getToken(UniContractGrammar.RBRACKET, 0); }
		public List_typeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_list_type; }
	}

	public final List_typeContext list_type() throws RecognitionException {
		List_typeContext _localctx = new List_typeContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_list_type);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(226);
			match(LIST);
			setState(227);
			match(LBARCKET);
			setState(228);
			type();
			setState(229);
			match(RBRACKET);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Map_typeContext extends ParserRuleContext {
		public TerminalNode MAP() { return getToken(UniContractGrammar.MAP, 0); }
		public TerminalNode LBARCKET() { return getToken(UniContractGrammar.LBARCKET, 0); }
		public List<TypeContext> type() {
			return getRuleContexts(TypeContext.class);
		}
		public TypeContext type(int i) {
			return getRuleContext(TypeContext.class,i);
		}
		public TerminalNode COMMA() { return getToken(UniContractGrammar.COMMA, 0); }
		public TerminalNode RBRACKET() { return getToken(UniContractGrammar.RBRACKET, 0); }
		public Map_typeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_map_type; }
	}

	public final Map_typeContext map_type() throws RecognitionException {
		Map_typeContext _localctx = new Map_typeContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_map_type);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(231);
			match(MAP);
			setState(232);
			match(LBARCKET);
			setState(233);
			type();
			setState(234);
			match(COMMA);
			setState(235);
			type();
			setState(236);
			match(RBRACKET);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class DecoratorContext extends ParserRuleContext {
		public TerminalNode AT() { return getToken(UniContractGrammar.AT, 0); }
		public TerminalNode IDENTIFIER() { return getToken(UniContractGrammar.IDENTIFIER, 0); }
		public TerminalNode LPAREN() { return getToken(UniContractGrammar.LPAREN, 0); }
		public List<Decorator_paramContext> decorator_param() {
			return getRuleContexts(Decorator_paramContext.class);
		}
		public Decorator_paramContext decorator_param(int i) {
			return getRuleContext(Decorator_paramContext.class,i);
		}
		public TerminalNode RPAREN() { return getToken(UniContractGrammar.RPAREN, 0); }
		public List<TerminalNode> COMMA() { return getTokens(UniContractGrammar.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(UniContractGrammar.COMMA, i);
		}
		public DecoratorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_decorator; }
	}

	public final DecoratorContext decorator() throws RecognitionException {
		DecoratorContext _localctx = new DecoratorContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_decorator);
		int _la;
		try {
			setState(253);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,30,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(238);
				match(AT);
				setState(239);
				match(IDENTIFIER);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(240);
				match(AT);
				setState(241);
				match(IDENTIFIER);
				setState(242);
				match(LPAREN);
				setState(243);
				decorator_param();
				setState(248);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==COMMA) {
					{
					{
					setState(244);
					match(COMMA);
					setState(245);
					decorator_param();
					}
					}
					setState(250);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(251);
				match(RPAREN);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Decorator_paramContext extends ParserRuleContext {
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode INTEGER_CONSTANS() { return getToken(UniContractGrammar.INTEGER_CONSTANS, 0); }
		public TerminalNode NUMBER_CONSTANS() { return getToken(UniContractGrammar.NUMBER_CONSTANS, 0); }
		public TerminalNode STRING_LITERAL() { return getToken(UniContractGrammar.STRING_LITERAL, 0); }
		public Decorator_paramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_decorator_param; }
	}

	public final Decorator_paramContext decorator_param() throws RecognitionException {
		Decorator_paramContext _localctx = new Decorator_paramContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_decorator_param);
		try {
			setState(259);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case IDENTIFIER:
				enterOuterAlt(_localctx, 1);
				{
				setState(255);
				qualifiedName();
				}
				break;
			case INTEGER_CONSTANS:
				enterOuterAlt(_localctx, 2);
				{
				setState(256);
				match(INTEGER_CONSTANS);
				}
				break;
			case NUMBER_CONSTANS:
				enterOuterAlt(_localctx, 3);
				{
				setState(257);
				match(NUMBER_CONSTANS);
				}
				break;
			case STRING_LITERAL:
				enterOuterAlt(_localctx, 4);
				{
				setState(258);
				match(STRING_LITERAL);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class QualifiedNameContext extends ParserRuleContext {
		public List<TerminalNode> IDENTIFIER() { return getTokens(UniContractGrammar.IDENTIFIER); }
		public TerminalNode IDENTIFIER(int i) {
			return getToken(UniContractGrammar.IDENTIFIER, i);
		}
		public List<TerminalNode> DOT() { return getTokens(UniContractGrammar.DOT); }
		public TerminalNode DOT(int i) {
			return getToken(UniContractGrammar.DOT, i);
		}
		public QualifiedNameContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_qualifiedName; }
	}

	public final QualifiedNameContext qualifiedName() throws RecognitionException {
		QualifiedNameContext _localctx = new QualifiedNameContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_qualifiedName);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(261);
			match(IDENTIFIER);
			setState(266);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOT) {
				{
				{
				setState(262);
				match(DOT);
				setState(263);
				match(IDENTIFIER);
				}
				}
				setState(268);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InheritsContext extends ParserRuleContext {
		public TerminalNode INHERITS() { return getToken(UniContractGrammar.INHERITS, 0); }
		public List<QualifiedNameContext> qualifiedName() {
			return getRuleContexts(QualifiedNameContext.class);
		}
		public QualifiedNameContext qualifiedName(int i) {
			return getRuleContext(QualifiedNameContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(UniContractGrammar.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(UniContractGrammar.COMMA, i);
		}
		public InheritsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_inherits; }
	}

	public final InheritsContext inherits() throws RecognitionException {
		InheritsContext _localctx = new InheritsContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_inherits);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(269);
			match(INHERITS);
			setState(270);
			qualifiedName();
			setState(275);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(271);
				match(COMMA);
				setState(272);
				qualifiedName();
				}
				}
				setState(277);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class EnumContext extends ParserRuleContext {
		public TerminalNode ENUM() { return getToken(UniContractGrammar.ENUM, 0); }
		public TerminalNode IDENTIFIER() { return getToken(UniContractGrammar.IDENTIFIER, 0); }
		public TerminalNode LCURLY() { return getToken(UniContractGrammar.LCURLY, 0); }
		public TerminalNode RCURLY() { return getToken(UniContractGrammar.RCURLY, 0); }
		public List<TerminalNode> DOCUMENT_LINE() { return getTokens(UniContractGrammar.DOCUMENT_LINE); }
		public TerminalNode DOCUMENT_LINE(int i) {
			return getToken(UniContractGrammar.DOCUMENT_LINE, i);
		}
		public List<DecoratorContext> decorator() {
			return getRuleContexts(DecoratorContext.class);
		}
		public DecoratorContext decorator(int i) {
			return getRuleContext(DecoratorContext.class,i);
		}
		public List<Enum_elementContext> enum_element() {
			return getRuleContexts(Enum_elementContext.class);
		}
		public Enum_elementContext enum_element(int i) {
			return getRuleContext(Enum_elementContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(UniContractGrammar.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(UniContractGrammar.COMMA, i);
		}
		public EnumContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_enum; }
	}

	public final EnumContext enum_() throws RecognitionException {
		EnumContext _localctx = new EnumContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_enum);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(281);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOCUMENT_LINE) {
				{
				{
				setState(278);
				match(DOCUMENT_LINE);
				}
				}
				setState(283);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(287);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==AT) {
				{
				{
				setState(284);
				decorator();
				}
				}
				setState(289);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(290);
			match(ENUM);
			setState(291);
			match(IDENTIFIER);
			setState(292);
			match(LCURLY);
			setState(294);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 687194768384L) != 0)) {
				{
				setState(293);
				enum_element();
				}
			}

			setState(300);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(296);
				match(COMMA);
				setState(297);
				enum_element();
				}
				}
				setState(302);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(303);
			match(RCURLY);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Enum_elementContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(UniContractGrammar.IDENTIFIER, 0); }
		public List<TerminalNode> DOCUMENT_LINE() { return getTokens(UniContractGrammar.DOCUMENT_LINE); }
		public TerminalNode DOCUMENT_LINE(int i) {
			return getToken(UniContractGrammar.DOCUMENT_LINE, i);
		}
		public List<DecoratorContext> decorator() {
			return getRuleContexts(DecoratorContext.class);
		}
		public DecoratorContext decorator(int i) {
			return getRuleContext(DecoratorContext.class,i);
		}
		public Enum_elementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_enum_element; }
	}

	public final Enum_elementContext enum_element() throws RecognitionException {
		Enum_elementContext _localctx = new Enum_elementContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_enum_element);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(308);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOCUMENT_LINE) {
				{
				{
				setState(305);
				match(DOCUMENT_LINE);
				}
				}
				setState(310);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(314);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==AT) {
				{
				{
				setState(311);
				decorator();
				}
				}
				setState(316);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(317);
			match(IDENTIFIER);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u0001)\u0140\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0002"+
		"\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007\u000f"+
		"\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011\u0002\u0012\u0007\u0012"+
		"\u0002\u0013\u0007\u0013\u0001\u0000\u0005\u0000*\b\u0000\n\u0000\f\u0000"+
		"-\t\u0000\u0001\u0000\u0005\u00000\b\u0000\n\u0000\f\u00003\t\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0001\u0005\u00018\b\u0001\n\u0001\f\u0001;\t"+
		"\u0001\u0001\u0001\u0005\u0001>\b\u0001\n\u0001\f\u0001A\t\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0005\u0001F\b\u0001\n\u0001\f\u0001I\t"+
		"\u0001\u0001\u0001\u0005\u0001L\b\u0001\n\u0001\f\u0001O\t\u0001\u0001"+
		"\u0001\u0001\u0001\u0003\u0001S\b\u0001\u0001\u0002\u0005\u0002V\b\u0002"+
		"\n\u0002\f\u0002Y\t\u0002\u0001\u0002\u0005\u0002\\\b\u0002\n\u0002\f"+
		"\u0002_\t\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0005"+
		"\u0002e\b\u0002\n\u0002\f\u0002h\t\u0002\u0001\u0002\u0001\u0002\u0001"+
		"\u0003\u0001\u0003\u0003\u0003n\b\u0003\u0001\u0004\u0005\u0004q\b\u0004"+
		"\n\u0004\f\u0004t\t\u0004\u0001\u0004\u0005\u0004w\b\u0004\n\u0004\f\u0004"+
		"z\t\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0003\u0004\u007f\b\u0004"+
		"\u0001\u0004\u0001\u0004\u0005\u0004\u0083\b\u0004\n\u0004\f\u0004\u0086"+
		"\t\u0004\u0001\u0004\u0001\u0004\u0001\u0005\u0001\u0005\u0001\u0005\u0003"+
		"\u0005\u008d\b\u0005\u0001\u0006\u0005\u0006\u0090\b\u0006\n\u0006\f\u0006"+
		"\u0093\t\u0006\u0001\u0006\u0005\u0006\u0096\b\u0006\n\u0006\f\u0006\u0099"+
		"\t\u0006\u0001\u0006\u0003\u0006\u009c\b\u0006\u0001\u0006\u0001\u0006"+
		"\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0007\u0005\u0007\u00a4\b\u0007"+
		"\n\u0007\f\u0007\u00a7\t\u0007\u0001\u0007\u0005\u0007\u00aa\b\u0007\n"+
		"\u0007\f\u0007\u00ad\t\u0007\u0001\u0007\u0003\u0007\u00b0\b\u0007\u0001"+
		"\u0007\u0001\u0007\u0001\u0007\u0001\u0007\u0003\u0007\u00b6\b\u0007\u0001"+
		"\u0007\u0001\u0007\u0005\u0007\u00ba\b\u0007\n\u0007\f\u0007\u00bd\t\u0007"+
		"\u0001\u0007\u0001\u0007\u0001\u0007\u0003\u0007\u00c2\b\u0007\u0001\b"+
		"\u0005\b\u00c5\b\b\n\b\f\b\u00c8\t\b\u0001\b\u0005\b\u00cb\b\b\n\b\f\b"+
		"\u00ce\t\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\t\u0001\t\u0001\t\u0001"+
		"\t\u0003\t\u00d8\b\t\u0001\n\u0001\n\u0001\u000b\u0001\u000b\u0001\u000b"+
		"\u0001\u000b\u0001\u000b\u0003\u000b\u00e1\b\u000b\u0001\f\u0001\f\u0001"+
		"\f\u0001\f\u0001\f\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001"+
		"\r\u0001\u000e\u0001\u000e\u0001\u000e\u0001\u000e\u0001\u000e\u0001\u000e"+
		"\u0001\u000e\u0001\u000e\u0005\u000e\u00f7\b\u000e\n\u000e\f\u000e\u00fa"+
		"\t\u000e\u0001\u000e\u0001\u000e\u0003\u000e\u00fe\b\u000e\u0001\u000f"+
		"\u0001\u000f\u0001\u000f\u0001\u000f\u0003\u000f\u0104\b\u000f\u0001\u0010"+
		"\u0001\u0010\u0001\u0010\u0005\u0010\u0109\b\u0010\n\u0010\f\u0010\u010c"+
		"\t\u0010\u0001\u0011\u0001\u0011\u0001\u0011\u0001\u0011\u0005\u0011\u0112"+
		"\b\u0011\n\u0011\f\u0011\u0115\t\u0011\u0001\u0012\u0005\u0012\u0118\b"+
		"\u0012\n\u0012\f\u0012\u011b\t\u0012\u0001\u0012\u0005\u0012\u011e\b\u0012"+
		"\n\u0012\f\u0012\u0121\t\u0012\u0001\u0012\u0001\u0012\u0001\u0012\u0001"+
		"\u0012\u0003\u0012\u0127\b\u0012\u0001\u0012\u0001\u0012\u0005\u0012\u012b"+
		"\b\u0012\n\u0012\f\u0012\u012e\t\u0012\u0001\u0012\u0001\u0012\u0001\u0013"+
		"\u0005\u0013\u0133\b\u0013\n\u0013\f\u0013\u0136\t\u0013\u0001\u0013\u0005"+
		"\u0013\u0139\b\u0013\n\u0013\f\u0013\u013c\t\u0013\u0001\u0013\u0001\u0013"+
		"\u0001\u0013\u0000\u0000\u0014\u0000\u0002\u0004\u0006\b\n\f\u000e\u0010"+
		"\u0012\u0014\u0016\u0018\u001a\u001c\u001e \"$&\u0000\u0001\u0001\u0000"+
		"\u0010\u0019\u0158\u0000+\u0001\u0000\u0000\u0000\u0002R\u0001\u0000\u0000"+
		"\u0000\u0004W\u0001\u0000\u0000\u0000\u0006m\u0001\u0000\u0000\u0000\b"+
		"r\u0001\u0000\u0000\u0000\n\u008c\u0001\u0000\u0000\u0000\f\u0091\u0001"+
		"\u0000\u0000\u0000\u000e\u00a5\u0001\u0000\u0000\u0000\u0010\u00c6\u0001"+
		"\u0000\u0000\u0000\u0012\u00d7\u0001\u0000\u0000\u0000\u0014\u00d9\u0001"+
		"\u0000\u0000\u0000\u0016\u00e0\u0001\u0000\u0000\u0000\u0018\u00e2\u0001"+
		"\u0000\u0000\u0000\u001a\u00e7\u0001\u0000\u0000\u0000\u001c\u00fd\u0001"+
		"\u0000\u0000\u0000\u001e\u0103\u0001\u0000\u0000\u0000 \u0105\u0001\u0000"+
		"\u0000\u0000\"\u010d\u0001\u0000\u0000\u0000$\u0119\u0001\u0000\u0000"+
		"\u0000&\u0134\u0001\u0000\u0000\u0000(*\u0003\u0002\u0001\u0000)(\u0001"+
		"\u0000\u0000\u0000*-\u0001\u0000\u0000\u0000+)\u0001\u0000\u0000\u0000"+
		"+,\u0001\u0000\u0000\u0000,1\u0001\u0000\u0000\u0000-+\u0001\u0000\u0000"+
		"\u0000.0\u0003\u0004\u0002\u0000/.\u0001\u0000\u0000\u000003\u0001\u0000"+
		"\u0000\u00001/\u0001\u0000\u0000\u000012\u0001\u0000\u0000\u000024\u0001"+
		"\u0000\u0000\u000031\u0001\u0000\u0000\u000045\u0005\u0000\u0000\u0001"+
		"5\u0001\u0001\u0000\u0000\u000068\u0005\'\u0000\u000076\u0001\u0000\u0000"+
		"\u00008;\u0001\u0000\u0000\u000097\u0001\u0000\u0000\u00009:\u0001\u0000"+
		"\u0000\u0000:?\u0001\u0000\u0000\u0000;9\u0001\u0000\u0000\u0000<>\u0003"+
		"\u001c\u000e\u0000=<\u0001\u0000\u0000\u0000>A\u0001\u0000\u0000\u0000"+
		"?=\u0001\u0000\u0000\u0000?@\u0001\u0000\u0000\u0000@B\u0001\u0000\u0000"+
		"\u0000A?\u0001\u0000\u0000\u0000BC\u0005\f\u0000\u0000CS\u0003 \u0010"+
		"\u0000DF\u0005\'\u0000\u0000ED\u0001\u0000\u0000\u0000FI\u0001\u0000\u0000"+
		"\u0000GE\u0001\u0000\u0000\u0000GH\u0001\u0000\u0000\u0000HM\u0001\u0000"+
		"\u0000\u0000IG\u0001\u0000\u0000\u0000JL\u0003\u001c\u000e\u0000KJ\u0001"+
		"\u0000\u0000\u0000LO\u0001\u0000\u0000\u0000MK\u0001\u0000\u0000\u0000"+
		"MN\u0001\u0000\u0000\u0000NP\u0001\u0000\u0000\u0000OM\u0001\u0000\u0000"+
		"\u0000PQ\u0005\f\u0000\u0000QS\u0005$\u0000\u0000R9\u0001\u0000\u0000"+
		"\u0000RG\u0001\u0000\u0000\u0000S\u0003\u0001\u0000\u0000\u0000TV\u0005"+
		"\'\u0000\u0000UT\u0001\u0000\u0000\u0000VY\u0001\u0000\u0000\u0000WU\u0001"+
		"\u0000\u0000\u0000WX\u0001\u0000\u0000\u0000X]\u0001\u0000\u0000\u0000"+
		"YW\u0001\u0000\u0000\u0000Z\\\u0003\u001c\u000e\u0000[Z\u0001\u0000\u0000"+
		"\u0000\\_\u0001\u0000\u0000\u0000][\u0001\u0000\u0000\u0000]^\u0001\u0000"+
		"\u0000\u0000^`\u0001\u0000\u0000\u0000_]\u0001\u0000\u0000\u0000`a\u0005"+
		"\u000e\u0000\u0000ab\u0003 \u0010\u0000bf\u0005\u0006\u0000\u0000ce\u0003"+
		"\u0006\u0003\u0000dc\u0001\u0000\u0000\u0000eh\u0001\u0000\u0000\u0000"+
		"fd\u0001\u0000\u0000\u0000fg\u0001\u0000\u0000\u0000gi\u0001\u0000\u0000"+
		"\u0000hf\u0001\u0000\u0000\u0000ij\u0005\u0007\u0000\u0000j\u0005\u0001"+
		"\u0000\u0000\u0000kn\u0003\b\u0004\u0000ln\u0003$\u0012\u0000mk\u0001"+
		"\u0000\u0000\u0000ml\u0001\u0000\u0000\u0000n\u0007\u0001\u0000\u0000"+
		"\u0000oq\u0005\'\u0000\u0000po\u0001\u0000\u0000\u0000qt\u0001\u0000\u0000"+
		"\u0000rp\u0001\u0000\u0000\u0000rs\u0001\u0000\u0000\u0000sx\u0001\u0000"+
		"\u0000\u0000tr\u0001\u0000\u0000\u0000uw\u0003\u001c\u000e\u0000vu\u0001"+
		"\u0000\u0000\u0000wz\u0001\u0000\u0000\u0000xv\u0001\u0000\u0000\u0000"+
		"xy\u0001\u0000\u0000\u0000y{\u0001\u0000\u0000\u0000zx\u0001\u0000\u0000"+
		"\u0000{|\u0005\r\u0000\u0000|~\u0005%\u0000\u0000}\u007f\u0003\"\u0011"+
		"\u0000~}\u0001\u0000\u0000\u0000~\u007f\u0001\u0000\u0000\u0000\u007f"+
		"\u0080\u0001\u0000\u0000\u0000\u0080\u0084\u0005\u0006\u0000\u0000\u0081"+
		"\u0083\u0003\n\u0005\u0000\u0082\u0081\u0001\u0000\u0000\u0000\u0083\u0086"+
		"\u0001\u0000\u0000\u0000\u0084\u0082\u0001\u0000\u0000\u0000\u0084\u0085"+
		"\u0001\u0000\u0000\u0000\u0085\u0087\u0001\u0000\u0000\u0000\u0086\u0084"+
		"\u0001\u0000\u0000\u0000\u0087\u0088\u0005\u0007\u0000\u0000\u0088\t\u0001"+
		"\u0000\u0000\u0000\u0089\u008d\u0003\u000e\u0007\u0000\u008a\u008d\u0003"+
		"\f\u0006\u0000\u008b\u008d\u0003$\u0012\u0000\u008c\u0089\u0001\u0000"+
		"\u0000\u0000\u008c\u008a\u0001\u0000\u0000\u0000\u008c\u008b\u0001\u0000"+
		"\u0000\u0000\u008d\u000b\u0001\u0000\u0000\u0000\u008e\u0090\u0005\'\u0000"+
		"\u0000\u008f\u008e\u0001\u0000\u0000\u0000\u0090\u0093\u0001\u0000\u0000"+
		"\u0000\u0091\u008f\u0001\u0000\u0000\u0000\u0091\u0092\u0001\u0000\u0000"+
		"\u0000\u0092\u0097\u0001\u0000\u0000\u0000\u0093\u0091\u0001\u0000\u0000"+
		"\u0000\u0094\u0096\u0003\u001c\u000e\u0000\u0095\u0094\u0001\u0000\u0000"+
		"\u0000\u0096\u0099\u0001\u0000\u0000\u0000\u0097\u0095\u0001\u0000\u0000"+
		"\u0000\u0097\u0098\u0001\u0000\u0000\u0000\u0098\u009b\u0001\u0000\u0000"+
		"\u0000\u0099\u0097\u0001\u0000\u0000\u0000\u009a\u009c\u0005 \u0000\u0000"+
		"\u009b\u009a\u0001\u0000\u0000\u0000\u009b\u009c\u0001\u0000\u0000\u0000"+
		"\u009c\u009d\u0001\u0000\u0000\u0000\u009d\u009e\u0005\u001e\u0000\u0000"+
		"\u009e\u009f\u0005%\u0000\u0000\u009f\u00a0\u0005\u0003\u0000\u0000\u00a0"+
		"\u00a1\u0003\u0012\t\u0000\u00a1\r\u0001\u0000\u0000\u0000\u00a2\u00a4"+
		"\u0005\'\u0000\u0000\u00a3\u00a2\u0001\u0000\u0000\u0000\u00a4\u00a7\u0001"+
		"\u0000\u0000\u0000\u00a5\u00a3\u0001\u0000\u0000\u0000\u00a5\u00a6\u0001"+
		"\u0000\u0000\u0000\u00a6\u00ab\u0001\u0000\u0000\u0000\u00a7\u00a5\u0001"+
		"\u0000\u0000\u0000\u00a8\u00aa\u0003\u001c\u000e\u0000\u00a9\u00a8\u0001"+
		"\u0000\u0000\u0000\u00aa\u00ad\u0001\u0000\u0000\u0000\u00ab\u00a9\u0001"+
		"\u0000\u0000\u0000\u00ab\u00ac\u0001\u0000\u0000\u0000\u00ac\u00af\u0001"+
		"\u0000\u0000\u0000\u00ad\u00ab\u0001\u0000\u0000\u0000\u00ae\u00b0\u0005"+
		"!\u0000\u0000\u00af\u00ae\u0001\u0000\u0000\u0000\u00af\u00b0\u0001\u0000"+
		"\u0000\u0000\u00b0\u00b1\u0001\u0000\u0000\u0000\u00b1\u00b2\u0005\u001f"+
		"\u0000\u0000\u00b2\u00b3\u0005%\u0000\u0000\u00b3\u00b5\u0005\u0004\u0000"+
		"\u0000\u00b4\u00b6\u0003\u0010\b\u0000\u00b5\u00b4\u0001\u0000\u0000\u0000"+
		"\u00b5\u00b6\u0001\u0000\u0000\u0000\u00b6\u00bb\u0001\u0000\u0000\u0000"+
		"\u00b7\u00b8\u0005\u0002\u0000\u0000\u00b8\u00ba\u0003\u0010\b\u0000\u00b9"+
		"\u00b7\u0001\u0000\u0000\u0000\u00ba\u00bd\u0001\u0000\u0000\u0000\u00bb"+
		"\u00b9\u0001\u0000\u0000\u0000\u00bb\u00bc\u0001\u0000\u0000\u0000\u00bc"+
		"\u00be\u0001\u0000\u0000\u0000\u00bd\u00bb\u0001\u0000\u0000\u0000\u00be"+
		"\u00c1\u0005\u0005\u0000\u0000\u00bf\u00c0\u0005\u000b\u0000\u0000\u00c0"+
		"\u00c2\u0003\u0012\t\u0000\u00c1\u00bf\u0001\u0000\u0000\u0000\u00c1\u00c2"+
		"\u0001\u0000\u0000\u0000\u00c2\u000f\u0001\u0000\u0000\u0000\u00c3\u00c5"+
		"\u0005\'\u0000\u0000\u00c4\u00c3\u0001\u0000\u0000\u0000\u00c5\u00c8\u0001"+
		"\u0000\u0000\u0000\u00c6\u00c4\u0001\u0000\u0000\u0000\u00c6\u00c7\u0001"+
		"\u0000\u0000\u0000\u00c7\u00cc\u0001\u0000\u0000\u0000\u00c8\u00c6\u0001"+
		"\u0000\u0000\u0000\u00c9\u00cb\u0003\u001c\u000e\u0000\u00ca\u00c9\u0001"+
		"\u0000\u0000\u0000\u00cb\u00ce\u0001\u0000\u0000\u0000\u00cc\u00ca\u0001"+
		"\u0000\u0000\u0000\u00cc\u00cd\u0001\u0000\u0000\u0000\u00cd\u00cf\u0001"+
		"\u0000\u0000\u0000\u00ce\u00cc\u0001\u0000\u0000\u0000\u00cf\u00d0\u0005"+
		"%\u0000\u0000\u00d0\u00d1\u0005\u0003\u0000\u0000\u00d1\u00d2\u0003\u0012"+
		"\t\u0000\u00d2\u0011\u0001\u0000\u0000\u0000\u00d3\u00d8\u0003\u0014\n"+
		"\u0000\u00d4\u00d8\u0003\u0016\u000b\u0000\u00d5\u00d8\u0003\u0018\f\u0000"+
		"\u00d6\u00d8\u0003\u001a\r\u0000\u00d7\u00d3\u0001\u0000\u0000\u0000\u00d7"+
		"\u00d4\u0001\u0000\u0000\u0000\u00d7\u00d5\u0001\u0000\u0000\u0000\u00d7"+
		"\u00d6\u0001\u0000\u0000\u0000\u00d8\u0013\u0001\u0000\u0000\u0000\u00d9"+
		"\u00da\u0007\u0000\u0000\u0000\u00da\u0015\u0001\u0000\u0000\u0000\u00db"+
		"\u00e1\u0003 \u0010\u0000\u00dc\u00dd\u0005\u001d\u0000\u0000\u00dd\u00de"+
		"\u0005\b\u0000\u0000\u00de\u00df\u0005$\u0000\u0000\u00df\u00e1\u0005"+
		"\t\u0000\u0000\u00e0\u00db\u0001\u0000\u0000\u0000\u00e0\u00dc\u0001\u0000"+
		"\u0000\u0000\u00e1\u0017\u0001\u0000\u0000\u0000\u00e2\u00e3\u0005\u001a"+
		"\u0000\u0000\u00e3\u00e4\u0005\b\u0000\u0000\u00e4\u00e5\u0003\u0012\t"+
		"\u0000\u00e5\u00e6\u0005\t\u0000\u0000\u00e6\u0019\u0001\u0000\u0000\u0000"+
		"\u00e7\u00e8\u0005\u001b\u0000\u0000\u00e8\u00e9\u0005\b\u0000\u0000\u00e9"+
		"\u00ea\u0003\u0012\t\u0000\u00ea\u00eb\u0005\u0002\u0000\u0000\u00eb\u00ec"+
		"\u0003\u0012\t\u0000\u00ec\u00ed\u0005\t\u0000\u0000\u00ed\u001b\u0001"+
		"\u0000\u0000\u0000\u00ee\u00ef\u0005\n\u0000\u0000\u00ef\u00fe\u0005%"+
		"\u0000\u0000\u00f0\u00f1\u0005\n\u0000\u0000\u00f1\u00f2\u0005%\u0000"+
		"\u0000\u00f2\u00f3\u0005\u0004\u0000\u0000\u00f3\u00f8\u0003\u001e\u000f"+
		"\u0000\u00f4\u00f5\u0005\u0002\u0000\u0000\u00f5\u00f7\u0003\u001e\u000f"+
		"\u0000\u00f6\u00f4\u0001\u0000\u0000\u0000\u00f7\u00fa\u0001\u0000\u0000"+
		"\u0000\u00f8\u00f6\u0001\u0000\u0000\u0000\u00f8\u00f9\u0001\u0000\u0000"+
		"\u0000\u00f9\u00fb\u0001\u0000\u0000\u0000\u00fa\u00f8\u0001\u0000\u0000"+
		"\u0000\u00fb\u00fc\u0005\u0005\u0000\u0000\u00fc\u00fe\u0001\u0000\u0000"+
		"\u0000\u00fd\u00ee\u0001\u0000\u0000\u0000\u00fd\u00f0\u0001\u0000\u0000"+
		"\u0000\u00fe\u001d\u0001\u0000\u0000\u0000\u00ff\u0104\u0003 \u0010\u0000"+
		"\u0100\u0104\u0005\"\u0000\u0000\u0101\u0104\u0005#\u0000\u0000\u0102"+
		"\u0104\u0005$\u0000\u0000\u0103\u00ff\u0001\u0000\u0000\u0000\u0103\u0100"+
		"\u0001\u0000\u0000\u0000\u0103\u0101\u0001\u0000\u0000\u0000\u0103\u0102"+
		"\u0001\u0000\u0000\u0000\u0104\u001f\u0001\u0000\u0000\u0000\u0105\u010a"+
		"\u0005%\u0000\u0000\u0106\u0107\u0005\u0001\u0000\u0000\u0107\u0109\u0005"+
		"%\u0000\u0000\u0108\u0106\u0001\u0000\u0000\u0000\u0109\u010c\u0001\u0000"+
		"\u0000\u0000\u010a\u0108\u0001\u0000\u0000\u0000\u010a\u010b\u0001\u0000"+
		"\u0000\u0000\u010b!\u0001\u0000\u0000\u0000\u010c\u010a\u0001\u0000\u0000"+
		"\u0000\u010d\u010e\u0005\u001c\u0000\u0000\u010e\u0113\u0003 \u0010\u0000"+
		"\u010f\u0110\u0005\u0002\u0000\u0000\u0110\u0112\u0003 \u0010\u0000\u0111"+
		"\u010f\u0001\u0000\u0000\u0000\u0112\u0115\u0001\u0000\u0000\u0000\u0113"+
		"\u0111\u0001\u0000\u0000\u0000\u0113\u0114\u0001\u0000\u0000\u0000\u0114"+
		"#\u0001\u0000\u0000\u0000\u0115\u0113\u0001\u0000\u0000\u0000\u0116\u0118"+
		"\u0005\'\u0000\u0000\u0117\u0116\u0001\u0000\u0000\u0000\u0118\u011b\u0001"+
		"\u0000\u0000\u0000\u0119\u0117\u0001\u0000\u0000\u0000\u0119\u011a\u0001"+
		"\u0000\u0000\u0000\u011a\u011f\u0001\u0000\u0000\u0000\u011b\u0119\u0001"+
		"\u0000\u0000\u0000\u011c\u011e\u0003\u001c\u000e\u0000\u011d\u011c\u0001"+
		"\u0000\u0000\u0000\u011e\u0121\u0001\u0000\u0000\u0000\u011f\u011d\u0001"+
		"\u0000\u0000\u0000\u011f\u0120\u0001\u0000\u0000\u0000\u0120\u0122\u0001"+
		"\u0000\u0000\u0000\u0121\u011f\u0001\u0000\u0000\u0000\u0122\u0123\u0005"+
		"\u000f\u0000\u0000\u0123\u0124\u0005%\u0000\u0000\u0124\u0126\u0005\u0006"+
		"\u0000\u0000\u0125\u0127\u0003&\u0013\u0000\u0126\u0125\u0001\u0000\u0000"+
		"\u0000\u0126\u0127\u0001\u0000\u0000\u0000\u0127\u012c\u0001\u0000\u0000"+
		"\u0000\u0128\u0129\u0005\u0002\u0000\u0000\u0129\u012b\u0003&\u0013\u0000"+
		"\u012a\u0128\u0001\u0000\u0000\u0000\u012b\u012e\u0001\u0000\u0000\u0000"+
		"\u012c\u012a\u0001\u0000\u0000\u0000\u012c\u012d\u0001\u0000\u0000\u0000"+
		"\u012d\u012f\u0001\u0000\u0000\u0000\u012e\u012c\u0001\u0000\u0000\u0000"+
		"\u012f\u0130\u0005\u0007\u0000\u0000\u0130%\u0001\u0000\u0000\u0000\u0131"+
		"\u0133\u0005\'\u0000\u0000\u0132\u0131\u0001\u0000\u0000\u0000\u0133\u0136"+
		"\u0001\u0000\u0000\u0000\u0134\u0132\u0001\u0000\u0000\u0000\u0134\u0135"+
		"\u0001\u0000\u0000\u0000\u0135\u013a\u0001\u0000\u0000\u0000\u0136\u0134"+
		"\u0001\u0000\u0000\u0000\u0137\u0139\u0003\u001c\u000e\u0000\u0138\u0137"+
		"\u0001\u0000\u0000\u0000\u0139\u013c\u0001\u0000\u0000\u0000\u013a\u0138"+
		"\u0001\u0000\u0000\u0000\u013a\u013b\u0001\u0000\u0000\u0000\u013b\u013d"+
		"\u0001\u0000\u0000\u0000\u013c\u013a\u0001\u0000\u0000\u0000\u013d\u013e"+
		"\u0005%\u0000\u0000\u013e\'\u0001\u0000\u0000\u0000(+19?GMRW]fmrx~\u0084"+
		"\u008c\u0091\u0097\u009b\u00a5\u00ab\u00af\u00b5\u00bb\u00c1\u00c6\u00cc"+
		"\u00d7\u00e0\u00f8\u00fd\u0103\u010a\u0113\u0119\u011f\u0126\u012c\u0134"+
		"\u013a";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}