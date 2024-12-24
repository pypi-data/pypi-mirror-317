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
		RBRACKET=9, ARROW=10, LT=11, GT=12, IMPORT=13, INTERFACE=14, NAMESPACE=15, 
		ENUM=16, INTEGER=17, NUMBER=18, FLOAT=19, DATE=20, TIME=21, DATETIME=22, 
		STRING=23, BOOLEAN=24, BYTES=25, STREAM=26, LIST=27, MAP=28, INHERITS=29, 
		EXTERNAL=30, PROPERTY=31, METHOD=32, READONLY=33, ASYNC=34, CONSTRAINT=35, 
		IDENTIFIER=36, WS=37, DOCUMENT_LINE=38, LINE_COMMENT=39, BLOCK_COMMENT=40;
	public static final int
		RULE_contract = 0, RULE_import_rule = 1, RULE_namespace = 2, RULE_namespace_elements = 3, 
		RULE_interface = 4, RULE_interface_element = 5, RULE_interface_property = 6, 
		RULE_interface_method = 7, RULE_interface_method_param = 8, RULE_type = 9, 
		RULE_primitive_type = 10, RULE_reference_type = 11, RULE_list_type = 12, 
		RULE_map_type = 13, RULE_qualifiedName = 14, RULE_inherits = 15, RULE_enum = 16, 
		RULE_enum_element = 17, RULE_generic = 18, RULE_generic_type = 19;
	private static String[] makeRuleNames() {
		return new String[] {
			"contract", "import_rule", "namespace", "namespace_elements", "interface", 
			"interface_element", "interface_property", "interface_method", "interface_method_param", 
			"type", "primitive_type", "reference_type", "list_type", "map_type", 
			"qualifiedName", "inherits", "enum", "enum_element", "generic", "generic_type"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'.'", "','", "':'", "'('", "')'", "'{'", "'}'", "'['", "']'", 
			"'=>'", "'<'", "'>'", "'import'", "'interface'", "'namespace'", "'enum'", 
			"'integer'", "'number'", "'float'", "'date'", "'time'", "'dateTime'", 
			"'string'", "'boolean'", "'bytes'", "'stream'", "'list'", "'map'", "'inherits'", 
			"'external'", "'property'", "'method'", "'readonly'", "'async'", "'constraint'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "DOT", "COMMA", "SEMI", "LPAREN", "RPAREN", "LCURLY", "RCURLY", 
			"LBARCKET", "RBRACKET", "ARROW", "LT", "GT", "IMPORT", "INTERFACE", "NAMESPACE", 
			"ENUM", "INTEGER", "NUMBER", "FLOAT", "DATE", "TIME", "DATETIME", "STRING", 
			"BOOLEAN", "BYTES", "STREAM", "LIST", "MAP", "INHERITS", "EXTERNAL", 
			"PROPERTY", "METHOD", "READONLY", "ASYNC", "CONSTRAINT", "IDENTIFIER", 
			"WS", "DOCUMENT_LINE", "LINE_COMMENT", "BLOCK_COMMENT"
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
			while (_la==NAMESPACE || _la==DOCUMENT_LINE) {
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
			setState(60);
			match(IMPORT);
			setState(61);
			qualifiedName();
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
			setState(66);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOCUMENT_LINE) {
				{
				{
				setState(63);
				match(DOCUMENT_LINE);
				}
				}
				setState(68);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(69);
			match(NAMESPACE);
			setState(70);
			qualifiedName();
			setState(71);
			match(LCURLY);
			setState(75);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 274877988864L) != 0)) {
				{
				{
				setState(72);
				namespace_elements();
				}
				}
				setState(77);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(78);
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
			setState(82);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,5,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(80);
				interface_();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(81);
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
		public GenericContext generic() {
			return getRuleContext(GenericContext.class,0);
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
			setState(90);
			match(INTERFACE);
			setState(91);
			match(IDENTIFIER);
			setState(93);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==LT) {
				{
				setState(92);
				generic();
				}
			}

			setState(96);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==INHERITS) {
				{
				setState(95);
				inherits();
				}
			}

			setState(98);
			match(LCURLY);
			setState(102);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 307090227200L) != 0)) {
				{
				{
				setState(99);
				interface_element();
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
			setState(110);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,10,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(107);
				interface_method();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(108);
				interface_property();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(109);
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
			setState(115);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOCUMENT_LINE) {
				{
				{
				setState(112);
				match(DOCUMENT_LINE);
				}
				}
				setState(117);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(119);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==READONLY) {
				{
				setState(118);
				match(READONLY);
				}
			}

			setState(121);
			match(PROPERTY);
			setState(122);
			match(IDENTIFIER);
			setState(123);
			match(SEMI);
			setState(124);
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
		public TerminalNode ASYNC() { return getToken(UniContractGrammar.ASYNC, 0); }
		public GenericContext generic() {
			return getRuleContext(GenericContext.class,0);
		}
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
			setState(129);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOCUMENT_LINE) {
				{
				{
				setState(126);
				match(DOCUMENT_LINE);
				}
				}
				setState(131);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(133);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ASYNC) {
				{
				setState(132);
				match(ASYNC);
				}
			}

			setState(135);
			match(METHOD);
			setState(136);
			match(IDENTIFIER);
			setState(138);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==LT) {
				{
				setState(137);
				generic();
				}
			}

			setState(140);
			match(LPAREN);
			{
			setState(142);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==IDENTIFIER || _la==DOCUMENT_LINE) {
				{
				setState(141);
				interface_method_param();
				}
			}

			setState(148);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(144);
				match(COMMA);
				setState(145);
				interface_method_param();
				}
				}
				setState(150);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
			setState(151);
			match(RPAREN);
			setState(154);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ARROW) {
				{
				setState(152);
				match(ARROW);
				setState(153);
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
			setState(159);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOCUMENT_LINE) {
				{
				{
				setState(156);
				match(DOCUMENT_LINE);
				}
				}
				setState(161);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(162);
			match(IDENTIFIER);
			setState(163);
			match(SEMI);
			setState(164);
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
			setState(170);
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
				setState(166);
				primitive_type();
				}
				break;
			case IDENTIFIER:
				enterOuterAlt(_localctx, 2);
				{
				setState(167);
				reference_type();
				}
				break;
			case LIST:
				enterOuterAlt(_localctx, 3);
				{
				setState(168);
				list_type();
				}
				break;
			case MAP:
				enterOuterAlt(_localctx, 4);
				{
				setState(169);
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
			setState(172);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 134086656L) != 0)) ) {
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
		public GenericContext generic() {
			return getRuleContext(GenericContext.class,0);
		}
		public Reference_typeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_reference_type; }
	}

	public final Reference_typeContext reference_type() throws RecognitionException {
		Reference_typeContext _localctx = new Reference_typeContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_reference_type);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(174);
			qualifiedName();
			setState(176);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==LT) {
				{
				setState(175);
				generic();
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
			setState(178);
			match(LIST);
			setState(179);
			match(LBARCKET);
			setState(180);
			type();
			setState(181);
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
			setState(183);
			match(MAP);
			setState(184);
			match(LBARCKET);
			setState(185);
			type();
			setState(186);
			match(COMMA);
			setState(187);
			type();
			setState(188);
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
		enterRule(_localctx, 28, RULE_qualifiedName);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(190);
			match(IDENTIFIER);
			setState(195);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOT) {
				{
				{
				setState(191);
				match(DOT);
				setState(192);
				match(IDENTIFIER);
				}
				}
				setState(197);
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
		enterRule(_localctx, 30, RULE_inherits);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(198);
			match(INHERITS);
			setState(199);
			qualifiedName();
			setState(204);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(200);
				match(COMMA);
				setState(201);
				qualifiedName();
				}
				}
				setState(206);
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
		enterRule(_localctx, 32, RULE_enum);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(210);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOCUMENT_LINE) {
				{
				{
				setState(207);
				match(DOCUMENT_LINE);
				}
				}
				setState(212);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(213);
			match(ENUM);
			setState(214);
			match(IDENTIFIER);
			setState(215);
			match(LCURLY);
			setState(217);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==IDENTIFIER || _la==DOCUMENT_LINE) {
				{
				setState(216);
				enum_element();
				}
			}

			setState(223);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(219);
				match(COMMA);
				setState(220);
				enum_element();
				}
				}
				setState(225);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(226);
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
		public Enum_elementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_enum_element; }
	}

	public final Enum_elementContext enum_element() throws RecognitionException {
		Enum_elementContext _localctx = new Enum_elementContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_enum_element);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(231);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==DOCUMENT_LINE) {
				{
				{
				setState(228);
				match(DOCUMENT_LINE);
				}
				}
				setState(233);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(234);
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

	@SuppressWarnings("CheckReturnValue")
	public static class GenericContext extends ParserRuleContext {
		public TerminalNode LT() { return getToken(UniContractGrammar.LT, 0); }
		public List<Generic_typeContext> generic_type() {
			return getRuleContexts(Generic_typeContext.class);
		}
		public Generic_typeContext generic_type(int i) {
			return getRuleContext(Generic_typeContext.class,i);
		}
		public TerminalNode GT() { return getToken(UniContractGrammar.GT, 0); }
		public List<TerminalNode> COMMA() { return getTokens(UniContractGrammar.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(UniContractGrammar.COMMA, i);
		}
		public GenericContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_generic; }
	}

	public final GenericContext generic() throws RecognitionException {
		GenericContext _localctx = new GenericContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_generic);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(236);
			match(LT);
			setState(237);
			generic_type();
			setState(242);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(238);
				match(COMMA);
				setState(239);
				generic_type();
				}
				}
				setState(244);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(245);
			match(GT);
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
	public static class Generic_typeContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(UniContractGrammar.IDENTIFIER, 0); }
		public TerminalNode CONSTRAINT() { return getToken(UniContractGrammar.CONSTRAINT, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public Generic_typeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_generic_type; }
	}

	public final Generic_typeContext generic_type() throws RecognitionException {
		Generic_typeContext _localctx = new Generic_typeContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_generic_type);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(247);
			match(IDENTIFIER);
			setState(250);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==CONSTRAINT) {
				{
				setState(248);
				match(CONSTRAINT);
				setState(249);
				qualifiedName();
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

	public static final String _serializedATN =
		"\u0004\u0001(\u00fd\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0002"+
		"\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007\u000f"+
		"\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011\u0002\u0012\u0007\u0012"+
		"\u0002\u0013\u0007\u0013\u0001\u0000\u0005\u0000*\b\u0000\n\u0000\f\u0000"+
		"-\t\u0000\u0001\u0000\u0005\u00000\b\u0000\n\u0000\f\u00003\t\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0001\u0005\u00018\b\u0001\n\u0001\f\u0001;\t"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0002\u0005\u0002A\b"+
		"\u0002\n\u0002\f\u0002D\t\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001"+
		"\u0002\u0005\u0002J\b\u0002\n\u0002\f\u0002M\t\u0002\u0001\u0002\u0001"+
		"\u0002\u0001\u0003\u0001\u0003\u0003\u0003S\b\u0003\u0001\u0004\u0005"+
		"\u0004V\b\u0004\n\u0004\f\u0004Y\t\u0004\u0001\u0004\u0001\u0004\u0001"+
		"\u0004\u0003\u0004^\b\u0004\u0001\u0004\u0003\u0004a\b\u0004\u0001\u0004"+
		"\u0001\u0004\u0005\u0004e\b\u0004\n\u0004\f\u0004h\t\u0004\u0001\u0004"+
		"\u0001\u0004\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005o\b\u0005"+
		"\u0001\u0006\u0005\u0006r\b\u0006\n\u0006\f\u0006u\t\u0006\u0001\u0006"+
		"\u0003\u0006x\b\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006"+
		"\u0001\u0006\u0001\u0007\u0005\u0007\u0080\b\u0007\n\u0007\f\u0007\u0083"+
		"\t\u0007\u0001\u0007\u0003\u0007\u0086\b\u0007\u0001\u0007\u0001\u0007"+
		"\u0001\u0007\u0003\u0007\u008b\b\u0007\u0001\u0007\u0001\u0007\u0003\u0007"+
		"\u008f\b\u0007\u0001\u0007\u0001\u0007\u0005\u0007\u0093\b\u0007\n\u0007"+
		"\f\u0007\u0096\t\u0007\u0001\u0007\u0001\u0007\u0001\u0007\u0003\u0007"+
		"\u009b\b\u0007\u0001\b\u0005\b\u009e\b\b\n\b\f\b\u00a1\t\b\u0001\b\u0001"+
		"\b\u0001\b\u0001\b\u0001\t\u0001\t\u0001\t\u0001\t\u0003\t\u00ab\b\t\u0001"+
		"\n\u0001\n\u0001\u000b\u0001\u000b\u0003\u000b\u00b1\b\u000b\u0001\f\u0001"+
		"\f\u0001\f\u0001\f\u0001\f\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001"+
		"\r\u0001\r\u0001\u000e\u0001\u000e\u0001\u000e\u0005\u000e\u00c2\b\u000e"+
		"\n\u000e\f\u000e\u00c5\t\u000e\u0001\u000f\u0001\u000f\u0001\u000f\u0001"+
		"\u000f\u0005\u000f\u00cb\b\u000f\n\u000f\f\u000f\u00ce\t\u000f\u0001\u0010"+
		"\u0005\u0010\u00d1\b\u0010\n\u0010\f\u0010\u00d4\t\u0010\u0001\u0010\u0001"+
		"\u0010\u0001\u0010\u0001\u0010\u0003\u0010\u00da\b\u0010\u0001\u0010\u0001"+
		"\u0010\u0005\u0010\u00de\b\u0010\n\u0010\f\u0010\u00e1\t\u0010\u0001\u0010"+
		"\u0001\u0010\u0001\u0011\u0005\u0011\u00e6\b\u0011\n\u0011\f\u0011\u00e9"+
		"\t\u0011\u0001\u0011\u0001\u0011\u0001\u0012\u0001\u0012\u0001\u0012\u0001"+
		"\u0012\u0005\u0012\u00f1\b\u0012\n\u0012\f\u0012\u00f4\t\u0012\u0001\u0012"+
		"\u0001\u0012\u0001\u0013\u0001\u0013\u0001\u0013\u0003\u0013\u00fb\b\u0013"+
		"\u0001\u0013\u0000\u0000\u0014\u0000\u0002\u0004\u0006\b\n\f\u000e\u0010"+
		"\u0012\u0014\u0016\u0018\u001a\u001c\u001e \"$&\u0000\u0001\u0001\u0000"+
		"\u0011\u001a\u0109\u0000+\u0001\u0000\u0000\u0000\u00029\u0001\u0000\u0000"+
		"\u0000\u0004B\u0001\u0000\u0000\u0000\u0006R\u0001\u0000\u0000\u0000\b"+
		"W\u0001\u0000\u0000\u0000\nn\u0001\u0000\u0000\u0000\fs\u0001\u0000\u0000"+
		"\u0000\u000e\u0081\u0001\u0000\u0000\u0000\u0010\u009f\u0001\u0000\u0000"+
		"\u0000\u0012\u00aa\u0001\u0000\u0000\u0000\u0014\u00ac\u0001\u0000\u0000"+
		"\u0000\u0016\u00ae\u0001\u0000\u0000\u0000\u0018\u00b2\u0001\u0000\u0000"+
		"\u0000\u001a\u00b7\u0001\u0000\u0000\u0000\u001c\u00be\u0001\u0000\u0000"+
		"\u0000\u001e\u00c6\u0001\u0000\u0000\u0000 \u00d2\u0001\u0000\u0000\u0000"+
		"\"\u00e7\u0001\u0000\u0000\u0000$\u00ec\u0001\u0000\u0000\u0000&\u00f7"+
		"\u0001\u0000\u0000\u0000(*\u0003\u0002\u0001\u0000)(\u0001\u0000\u0000"+
		"\u0000*-\u0001\u0000\u0000\u0000+)\u0001\u0000\u0000\u0000+,\u0001\u0000"+
		"\u0000\u0000,1\u0001\u0000\u0000\u0000-+\u0001\u0000\u0000\u0000.0\u0003"+
		"\u0004\u0002\u0000/.\u0001\u0000\u0000\u000003\u0001\u0000\u0000\u0000"+
		"1/\u0001\u0000\u0000\u000012\u0001\u0000\u0000\u000024\u0001\u0000\u0000"+
		"\u000031\u0001\u0000\u0000\u000045\u0005\u0000\u0000\u00015\u0001\u0001"+
		"\u0000\u0000\u000068\u0005&\u0000\u000076\u0001\u0000\u0000\u00008;\u0001"+
		"\u0000\u0000\u000097\u0001\u0000\u0000\u00009:\u0001\u0000\u0000\u0000"+
		":<\u0001\u0000\u0000\u0000;9\u0001\u0000\u0000\u0000<=\u0005\r\u0000\u0000"+
		"=>\u0003\u001c\u000e\u0000>\u0003\u0001\u0000\u0000\u0000?A\u0005&\u0000"+
		"\u0000@?\u0001\u0000\u0000\u0000AD\u0001\u0000\u0000\u0000B@\u0001\u0000"+
		"\u0000\u0000BC\u0001\u0000\u0000\u0000CE\u0001\u0000\u0000\u0000DB\u0001"+
		"\u0000\u0000\u0000EF\u0005\u000f\u0000\u0000FG\u0003\u001c\u000e\u0000"+
		"GK\u0005\u0006\u0000\u0000HJ\u0003\u0006\u0003\u0000IH\u0001\u0000\u0000"+
		"\u0000JM\u0001\u0000\u0000\u0000KI\u0001\u0000\u0000\u0000KL\u0001\u0000"+
		"\u0000\u0000LN\u0001\u0000\u0000\u0000MK\u0001\u0000\u0000\u0000NO\u0005"+
		"\u0007\u0000\u0000O\u0005\u0001\u0000\u0000\u0000PS\u0003\b\u0004\u0000"+
		"QS\u0003 \u0010\u0000RP\u0001\u0000\u0000\u0000RQ\u0001\u0000\u0000\u0000"+
		"S\u0007\u0001\u0000\u0000\u0000TV\u0005&\u0000\u0000UT\u0001\u0000\u0000"+
		"\u0000VY\u0001\u0000\u0000\u0000WU\u0001\u0000\u0000\u0000WX\u0001\u0000"+
		"\u0000\u0000XZ\u0001\u0000\u0000\u0000YW\u0001\u0000\u0000\u0000Z[\u0005"+
		"\u000e\u0000\u0000[]\u0005$\u0000\u0000\\^\u0003$\u0012\u0000]\\\u0001"+
		"\u0000\u0000\u0000]^\u0001\u0000\u0000\u0000^`\u0001\u0000\u0000\u0000"+
		"_a\u0003\u001e\u000f\u0000`_\u0001\u0000\u0000\u0000`a\u0001\u0000\u0000"+
		"\u0000ab\u0001\u0000\u0000\u0000bf\u0005\u0006\u0000\u0000ce\u0003\n\u0005"+
		"\u0000dc\u0001\u0000\u0000\u0000eh\u0001\u0000\u0000\u0000fd\u0001\u0000"+
		"\u0000\u0000fg\u0001\u0000\u0000\u0000gi\u0001\u0000\u0000\u0000hf\u0001"+
		"\u0000\u0000\u0000ij\u0005\u0007\u0000\u0000j\t\u0001\u0000\u0000\u0000"+
		"ko\u0003\u000e\u0007\u0000lo\u0003\f\u0006\u0000mo\u0003 \u0010\u0000"+
		"nk\u0001\u0000\u0000\u0000nl\u0001\u0000\u0000\u0000nm\u0001\u0000\u0000"+
		"\u0000o\u000b\u0001\u0000\u0000\u0000pr\u0005&\u0000\u0000qp\u0001\u0000"+
		"\u0000\u0000ru\u0001\u0000\u0000\u0000sq\u0001\u0000\u0000\u0000st\u0001"+
		"\u0000\u0000\u0000tw\u0001\u0000\u0000\u0000us\u0001\u0000\u0000\u0000"+
		"vx\u0005!\u0000\u0000wv\u0001\u0000\u0000\u0000wx\u0001\u0000\u0000\u0000"+
		"xy\u0001\u0000\u0000\u0000yz\u0005\u001f\u0000\u0000z{\u0005$\u0000\u0000"+
		"{|\u0005\u0003\u0000\u0000|}\u0003\u0012\t\u0000}\r\u0001\u0000\u0000"+
		"\u0000~\u0080\u0005&\u0000\u0000\u007f~\u0001\u0000\u0000\u0000\u0080"+
		"\u0083\u0001\u0000\u0000\u0000\u0081\u007f\u0001\u0000\u0000\u0000\u0081"+
		"\u0082\u0001\u0000\u0000\u0000\u0082\u0085\u0001\u0000\u0000\u0000\u0083"+
		"\u0081\u0001\u0000\u0000\u0000\u0084\u0086\u0005\"\u0000\u0000\u0085\u0084"+
		"\u0001\u0000\u0000\u0000\u0085\u0086\u0001\u0000\u0000\u0000\u0086\u0087"+
		"\u0001\u0000\u0000\u0000\u0087\u0088\u0005 \u0000\u0000\u0088\u008a\u0005"+
		"$\u0000\u0000\u0089\u008b\u0003$\u0012\u0000\u008a\u0089\u0001\u0000\u0000"+
		"\u0000\u008a\u008b\u0001\u0000\u0000\u0000\u008b\u008c\u0001\u0000\u0000"+
		"\u0000\u008c\u008e\u0005\u0004\u0000\u0000\u008d\u008f\u0003\u0010\b\u0000"+
		"\u008e\u008d\u0001\u0000\u0000\u0000\u008e\u008f\u0001\u0000\u0000\u0000"+
		"\u008f\u0094\u0001\u0000\u0000\u0000\u0090\u0091\u0005\u0002\u0000\u0000"+
		"\u0091\u0093\u0003\u0010\b\u0000\u0092\u0090\u0001\u0000\u0000\u0000\u0093"+
		"\u0096\u0001\u0000\u0000\u0000\u0094\u0092\u0001\u0000\u0000\u0000\u0094"+
		"\u0095\u0001\u0000\u0000\u0000\u0095\u0097\u0001\u0000\u0000\u0000\u0096"+
		"\u0094\u0001\u0000\u0000\u0000\u0097\u009a\u0005\u0005\u0000\u0000\u0098"+
		"\u0099\u0005\n\u0000\u0000\u0099\u009b\u0003\u0012\t\u0000\u009a\u0098"+
		"\u0001\u0000\u0000\u0000\u009a\u009b\u0001\u0000\u0000\u0000\u009b\u000f"+
		"\u0001\u0000\u0000\u0000\u009c\u009e\u0005&\u0000\u0000\u009d\u009c\u0001"+
		"\u0000\u0000\u0000\u009e\u00a1\u0001\u0000\u0000\u0000\u009f\u009d\u0001"+
		"\u0000\u0000\u0000\u009f\u00a0\u0001\u0000\u0000\u0000\u00a0\u00a2\u0001"+
		"\u0000\u0000\u0000\u00a1\u009f\u0001\u0000\u0000\u0000\u00a2\u00a3\u0005"+
		"$\u0000\u0000\u00a3\u00a4\u0005\u0003\u0000\u0000\u00a4\u00a5\u0003\u0012"+
		"\t\u0000\u00a5\u0011\u0001\u0000\u0000\u0000\u00a6\u00ab\u0003\u0014\n"+
		"\u0000\u00a7\u00ab\u0003\u0016\u000b\u0000\u00a8\u00ab\u0003\u0018\f\u0000"+
		"\u00a9\u00ab\u0003\u001a\r\u0000\u00aa\u00a6\u0001\u0000\u0000\u0000\u00aa"+
		"\u00a7\u0001\u0000\u0000\u0000\u00aa\u00a8\u0001\u0000\u0000\u0000\u00aa"+
		"\u00a9\u0001\u0000\u0000\u0000\u00ab\u0013\u0001\u0000\u0000\u0000\u00ac"+
		"\u00ad\u0007\u0000\u0000\u0000\u00ad\u0015\u0001\u0000\u0000\u0000\u00ae"+
		"\u00b0\u0003\u001c\u000e\u0000\u00af\u00b1\u0003$\u0012\u0000\u00b0\u00af"+
		"\u0001\u0000\u0000\u0000\u00b0\u00b1\u0001\u0000\u0000\u0000\u00b1\u0017"+
		"\u0001\u0000\u0000\u0000\u00b2\u00b3\u0005\u001b\u0000\u0000\u00b3\u00b4"+
		"\u0005\b\u0000\u0000\u00b4\u00b5\u0003\u0012\t\u0000\u00b5\u00b6\u0005"+
		"\t\u0000\u0000\u00b6\u0019\u0001\u0000\u0000\u0000\u00b7\u00b8\u0005\u001c"+
		"\u0000\u0000\u00b8\u00b9\u0005\b\u0000\u0000\u00b9\u00ba\u0003\u0012\t"+
		"\u0000\u00ba\u00bb\u0005\u0002\u0000\u0000\u00bb\u00bc\u0003\u0012\t\u0000"+
		"\u00bc\u00bd\u0005\t\u0000\u0000\u00bd\u001b\u0001\u0000\u0000\u0000\u00be"+
		"\u00c3\u0005$\u0000\u0000\u00bf\u00c0\u0005\u0001\u0000\u0000\u00c0\u00c2"+
		"\u0005$\u0000\u0000\u00c1\u00bf\u0001\u0000\u0000\u0000\u00c2\u00c5\u0001"+
		"\u0000\u0000\u0000\u00c3\u00c1\u0001\u0000\u0000\u0000\u00c3\u00c4\u0001"+
		"\u0000\u0000\u0000\u00c4\u001d\u0001\u0000\u0000\u0000\u00c5\u00c3\u0001"+
		"\u0000\u0000\u0000\u00c6\u00c7\u0005\u001d\u0000\u0000\u00c7\u00cc\u0003"+
		"\u001c\u000e\u0000\u00c8\u00c9\u0005\u0002\u0000\u0000\u00c9\u00cb\u0003"+
		"\u001c\u000e\u0000\u00ca\u00c8\u0001\u0000\u0000\u0000\u00cb\u00ce\u0001"+
		"\u0000\u0000\u0000\u00cc\u00ca\u0001\u0000\u0000\u0000\u00cc\u00cd\u0001"+
		"\u0000\u0000\u0000\u00cd\u001f\u0001\u0000\u0000\u0000\u00ce\u00cc\u0001"+
		"\u0000\u0000\u0000\u00cf\u00d1\u0005&\u0000\u0000\u00d0\u00cf\u0001\u0000"+
		"\u0000\u0000\u00d1\u00d4\u0001\u0000\u0000\u0000\u00d2\u00d0\u0001\u0000"+
		"\u0000\u0000\u00d2\u00d3\u0001\u0000\u0000\u0000\u00d3\u00d5\u0001\u0000"+
		"\u0000\u0000\u00d4\u00d2\u0001\u0000\u0000\u0000\u00d5\u00d6\u0005\u0010"+
		"\u0000\u0000\u00d6\u00d7\u0005$\u0000\u0000\u00d7\u00d9\u0005\u0006\u0000"+
		"\u0000\u00d8\u00da\u0003\"\u0011\u0000\u00d9\u00d8\u0001\u0000\u0000\u0000"+
		"\u00d9\u00da\u0001\u0000\u0000\u0000\u00da\u00df\u0001\u0000\u0000\u0000"+
		"\u00db\u00dc\u0005\u0002\u0000\u0000\u00dc\u00de\u0003\"\u0011\u0000\u00dd"+
		"\u00db\u0001\u0000\u0000\u0000\u00de\u00e1\u0001\u0000\u0000\u0000\u00df"+
		"\u00dd\u0001\u0000\u0000\u0000\u00df\u00e0\u0001\u0000\u0000\u0000\u00e0"+
		"\u00e2\u0001\u0000\u0000\u0000\u00e1\u00df\u0001\u0000\u0000\u0000\u00e2"+
		"\u00e3\u0005\u0007\u0000\u0000\u00e3!\u0001\u0000\u0000\u0000\u00e4\u00e6"+
		"\u0005&\u0000\u0000\u00e5\u00e4\u0001\u0000\u0000\u0000\u00e6\u00e9\u0001"+
		"\u0000\u0000\u0000\u00e7\u00e5\u0001\u0000\u0000\u0000\u00e7\u00e8\u0001"+
		"\u0000\u0000\u0000\u00e8\u00ea\u0001\u0000\u0000\u0000\u00e9\u00e7\u0001"+
		"\u0000\u0000\u0000\u00ea\u00eb\u0005$\u0000\u0000\u00eb#\u0001\u0000\u0000"+
		"\u0000\u00ec\u00ed\u0005\u000b\u0000\u0000\u00ed\u00f2\u0003&\u0013\u0000"+
		"\u00ee\u00ef\u0005\u0002\u0000\u0000\u00ef\u00f1\u0003&\u0013\u0000\u00f0"+
		"\u00ee\u0001\u0000\u0000\u0000\u00f1\u00f4\u0001\u0000\u0000\u0000\u00f2"+
		"\u00f0\u0001\u0000\u0000\u0000\u00f2\u00f3\u0001\u0000\u0000\u0000\u00f3"+
		"\u00f5\u0001\u0000\u0000\u0000\u00f4\u00f2\u0001\u0000\u0000\u0000\u00f5"+
		"\u00f6\u0005\f\u0000\u0000\u00f6%\u0001\u0000\u0000\u0000\u00f7\u00fa"+
		"\u0005$\u0000\u0000\u00f8\u00f9\u0005#\u0000\u0000\u00f9\u00fb\u0003\u001c"+
		"\u000e\u0000\u00fa\u00f8\u0001\u0000\u0000\u0000\u00fa\u00fb\u0001\u0000"+
		"\u0000\u0000\u00fb\'\u0001\u0000\u0000\u0000\u001e+19BKRW]`fnsw\u0081"+
		"\u0085\u008a\u008e\u0094\u009a\u009f\u00aa\u00b0\u00c3\u00cc\u00d2\u00d9"+
		"\u00df\u00e7\u00f2\u00fa";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}