"""Tests for the Quicklin transpiler."""

from __future__ import annotations

import unittest

from quicklin.lexer import Token, TokenType, tokenize
from quicklin.transpiler import transpile
from quicklin.keywords import KEYWORD_MAP, TYPE_MAP, OPERATOR_MAP


class TestKeywordTranspilation(unittest.TestCase):
    """Every keyword mapping should be correctly transpiled."""

    def test_all_keywords_standalone(self):
        """Each keyword in isolation should map correctly."""
        for qk, kt in KEYWORD_MAP.items():
            with self.subTest(quicklin=qk, kotlin=kt):
                result = transpile(qk)
                self.assertEqual(result, kt)

    def test_fn_to_fun(self):
        self.assertEqual(transpile("fn main() {}"), "fun main() {}")

    def test_vl_to_val(self):
        self.assertEqual(transpile("vl x = 5"), "val x = 5")

    def test_vr_to_var(self):
        self.assertEqual(transpile("vr y = 10"), "var y = 10")

    def test_rt_to_return(self):
        self.assertEqual(transpile("rt 42"), "return 42")

    def test_pr_to_println(self):
        self.assertEqual(transpile('pr("hello")'), 'println("hello")')

    def test_pt_to_print(self):
        self.assertEqual(transpile('pt("hi")'), 'print("hi")')

    def test_dc_to_data_class(self):
        self.assertEqual(
            transpile("dc User(vl name: Str)"),
            "data class User(val name: String)",
        )

    def test_wn_to_when(self):
        self.assertEqual(transpile("wn (x) {}"), "when (x) {}")

    def test_fr_to_for(self):
        self.assertEqual(transpile("fr (i in 1..10) {}"), "for (i in 1..10) {}")

    def test_wh_to_while(self):
        self.assertEqual(transpile("wh (tr) {}"), "while (true) {}")

    def test_el_to_else(self):
        self.assertEqual(transpile("el {}"), "else {}")

    def test_ob_to_object(self):
        self.assertEqual(transpile("ob Singleton {}"), "object Singleton {}")

    def test_ifc_to_interface(self):
        self.assertEqual(transpile("ifc Drawable {}"), "interface Drawable {}")

    def test_abs_to_abstract(self):
        self.assertEqual(transpile("abs cl Shape {}"), "abstract class Shape {}")

    def test_ovr_to_override(self):
        self.assertEqual(transpile("ovr fn draw() {}"), "override fun draw() {}")

    def test_imp_to_import(self):
        self.assertEqual(transpile("imp kotlin.io.*"), "import kotlin.io.*")

    def test_pkg_to_package(self):
        self.assertEqual(transpile("pkg com.example"), "package com.example")

    def test_prv_to_private(self):
        self.assertEqual(transpile("prv vl x = 1"), "private val x = 1")

    def test_pub_to_public(self):
        self.assertEqual(transpile("pub fn foo() {}"), "public fun foo() {}")

    def test_prt_to_protected(self):
        self.assertEqual(transpile("prt vl y = 2"), "protected val y = 2")

    def test_intl_to_internal(self):
        self.assertEqual(transpile("intl fn bar() {}"), "internal fun bar() {}")

    def test_sus_to_suspend(self):
        self.assertEqual(transpile("sus fn fetch() {}"), "suspend fun fetch() {}")

    def test_seal_cl(self):
        self.assertEqual(transpile("seal cl Result {}"), "sealed class Result {}")

    def test_cmp_ob(self):
        self.assertEqual(transpile("cmp ob {}"), "companion object {}")

    def test_enm_cl(self):
        self.assertEqual(transpile("enm cl Color {}"), "enum class Color {}")

    def test_nl_to_null(self):
        self.assertEqual(transpile("vl x = nl"), "val x = null")

    def test_tr_to_true(self):
        self.assertEqual(transpile("vl b = tr"), "val b = true")

    def test_fl_to_false(self):
        self.assertEqual(transpile("vl b = fl"), "val b = false")

    def test_br_to_break(self):
        self.assertEqual(transpile("br"), "break")

    def test_cnt_to_continue(self):
        self.assertEqual(transpile("cnt"), "continue")

    def test_thrw_to_throw(self):
        self.assertEqual(
            transpile('thrw Exception("error")'),
            'throw Exception("error")',
        )

    def test_ctch_fnly(self):
        self.assertEqual(
            transpile("try {} ctch (e: Exception) {} fnly {}"),
            "try {} catch (e: Exception) {} finally {}",
        )

    def test_ty_to_typealias(self):
        self.assertEqual(
            transpile("ty UserList = Lst<User>"),
            "typealias UserList = List<User>",
        )

    def test_inl_to_inline(self):
        self.assertEqual(transpile("inl fn run() {}"), "inline fun run() {}")

    def test_oprt_to_operator(self):
        self.assertEqual(transpile("oprt fn plus() {}"), "operator fun plus() {}")

    def test_infx_to_infix(self):
        self.assertEqual(transpile("infx fn to() {}"), "infix fun to() {}")

    def test_ltnt_to_lateinit(self):
        self.assertEqual(transpile("ltnt vr x: Str"), "lateinit var x: String")

    def test_opn_to_open(self):
        self.assertEqual(transpile("opn cl Base {}"), "open class Base {}")

    def test_ctr_to_constructor(self):
        self.assertEqual(transpile("ctr(x: Int)"), "constructor(x: Int)")


class TestTypeTranspilation(unittest.TestCase):
    """Type shortcuts should be correctly transpiled."""

    def test_all_types_standalone(self):
        for qk, kt in TYPE_MAP.items():
            with self.subTest(quicklin=qk, kotlin=kt):
                self.assertEqual(transpile(qk), kt)

    def test_str_in_context(self):
        self.assertEqual(
            transpile("vl name: Str = \"Alice\""),
            'val name: String = "Alice"',
        )

    def test_bool_in_context(self):
        self.assertEqual(
            transpile("vl flag: Bool = tr"),
            "val flag: Boolean = true",
        )

    def test_lst_in_context(self):
        self.assertEqual(
            transpile("vl items: Lst<Str>"),
            "val items: List<String>",
        )

    def test_mlst_in_context(self):
        self.assertEqual(
            transpile("vl items: MLst<Int>"),
            "val items: MutableList<Int>",
        )

    def test_mmap_in_context(self):
        self.assertEqual(
            transpile("vl m: MMap<Str, Int>"),
            "val m: MutableMap<String, Int>",
        )

    def test_arr_in_context(self):
        self.assertEqual(
            transpile("vl a: Arr<Int>"),
            "val a: Array<Int>",
        )


class TestOperatorSugar(unittest.TestCase):
    """Operator sugar should be correctly transpiled."""

    def test_double_question_to_elvis(self):
        self.assertEqual(
            transpile("vl x = name ?? \"default\""),
            'val x = name ?: "default"',
        )

    def test_elvis_not_double_replaced(self):
        """If someone writes Kotlin's ?: directly, it should pass through."""
        self.assertEqual(transpile("a ?: b"), "a ?: b")


class TestStringPreservation(unittest.TestCase):
    """Keywords inside strings must NOT be replaced."""

    def test_keyword_in_double_quoted_string(self):
        self.assertEqual(
            transpile('pr("fn is a keyword")'),
            'println("fn is a keyword")',
        )

    def test_keyword_in_triple_quoted_string(self):
        source = '\"\"\"fn vl vr rt\"\"\"'
        result = transpile(source)
        self.assertEqual(result, source)  # untouched

    def test_string_template_preserved(self):
        source = 'pr("Value: ${fn}")'
        # 'fn' inside the string template should NOT be replaced
        # but the leading pr should become println
        result = transpile(source)
        self.assertEqual(result, 'println("Value: ${fn}")')


class TestCommentPreservation(unittest.TestCase):
    """Keywords inside comments must NOT be replaced."""

    def test_keyword_in_line_comment(self):
        result = transpile("// fn is a keyword\nfn main() {}")
        self.assertEqual(result, "// fn is a keyword\nfun main() {}")

    def test_keyword_in_block_comment(self):
        result = transpile("/* fn vl vr */ fn main() {}")
        self.assertEqual(result, "/* fn vl vr */ fun main() {}")


class TestIdentifierSafety(unittest.TestCase):
    """Partial identifier matches must NOT be replaced."""

    def test_printer_not_mangled(self):
        """'pr' inside 'printer' should NOT become 'printlner'."""
        self.assertEqual(transpile("vl printer = 1"), "val printer = 1")

    def test_friend_not_mangled(self):
        """'fr' inside 'friend' should NOT become 'foriend'."""
        self.assertEqual(transpile("vl friend = 1"), "val friend = 1")

    def test_class_name_class_not_mangled(self):
        """'cl' inside 'clamp' should NOT become 'classamp'."""
        self.assertEqual(transpile("vl clamp = 1"), "val clamp = 1")

    def test_return_inside_returnValue(self):
        """'rt' inside 'rtValue' — but 'rtValue' is a single identifier, not 'rt'."""
        self.assertEqual(transpile("vl rtValue = 1"), "val rtValue = 1")

    def test_variable_named_fn(self):
        """If someone has backtick-quoted `fn`, it should not be replaced."""
        self.assertEqual(transpile("`fn`"), "`fn`")

    def test_true_keyword_not_in_trueValue(self):
        self.assertEqual(transpile("vl trueValue = 1"), "val trueValue = 1")


class TestWhitespacePreservation(unittest.TestCase):
    """Formatting should be preserved exactly."""

    def test_indentation_preserved(self):
        source = "fn main() {\n    pr(\"hi\")\n}"
        expected = "fun main() {\n    println(\"hi\")\n}"
        self.assertEqual(transpile(source), expected)

    def test_blank_lines_preserved(self):
        source = "vl x = 1\n\nvl y = 2"
        expected = "val x = 1\n\nval y = 2"
        self.assertEqual(transpile(source), expected)

    def test_tabs_preserved(self):
        source = "\tfn foo() {}"
        expected = "\tfun foo() {}"
        self.assertEqual(transpile(source), expected)


class TestComplexSnippets(unittest.TestCase):
    """End-to-end transpilation of realistic code snippets."""

    def test_full_function(self):
        source = (
            "fn greet(name: Str): Str {\n"
            "    rt \"Hello, $name!\"\n"
            "}"
        )
        expected = (
            "fun greet(name: String): String {\n"
            "    return \"Hello, $name!\"\n"
            "}"
        )
        self.assertEqual(transpile(source), expected)

    def test_data_class_with_types(self):
        source = "dc User(vl name: Str, vl age: Int, vl active: Bool)"
        expected = "data class User(val name: String, val age: Int, val active: Boolean)"
        self.assertEqual(transpile(source), expected)

    def test_when_expression(self):
        source = (
            "wn (x) {\n"
            "    1 -> pr(\"one\")\n"
            "    2 -> pr(\"two\")\n"
            "    el -> pr(\"other\")\n"
            "}"
        )
        expected = (
            "when (x) {\n"
            "    1 -> println(\"one\")\n"
            "    2 -> println(\"two\")\n"
            "    else -> println(\"other\")\n"
            "}"
        )
        self.assertEqual(transpile(source), expected)

    def test_null_safety_with_elvis(self):
        source = "vl result = name?.length ?? 0"
        expected = "val result = name?.length ?: 0"
        self.assertEqual(transpile(source), expected)

    def test_sealed_class_hierarchy(self):
        source = (
            "seal cl Result {\n"
            "    dc Success(vl data: Str) : Result()\n"
            "    dc Error(vl msg: Str) : Result()\n"
            "}"
        )
        expected = (
            "sealed class Result {\n"
            "    data class Success(val data: String) : Result()\n"
            "    data class Error(val msg: String) : Result()\n"
            "}"
        )
        self.assertEqual(transpile(source), expected)

    def test_suspend_function(self):
        source = "sus fn fetchData(): Lst<Str> {}"
        expected = "suspend fun fetchData(): List<String> {}"
        self.assertEqual(transpile(source), expected)

    def test_companion_object_factory(self):
        source = (
            "cl User prv ctr(vl name: Str) {\n"
            "    cmp ob {\n"
            "        fn create(name: Str): User = User(name)\n"
            "    }\n"
            "}"
        )
        expected = (
            "class User private constructor(val name: String) {\n"
            "    companion object {\n"
            "        fun create(name: String): User = User(name)\n"
            "    }\n"
            "}"
        )
        self.assertEqual(transpile(source), expected)

    def test_try_catch_finally(self):
        source = (
            "try {\n"
            "    vl result = riskyOperation()\n"
            "} ctch (e: Exception) {\n"
            "    pr(e.message ?? \"Unknown error\")\n"
            "} fnly {\n"
            "    cleanup()\n"
            "}"
        )
        expected = (
            "try {\n"
            "    val result = riskyOperation()\n"
            "} catch (e: Exception) {\n"
            "    println(e.message ?: \"Unknown error\")\n"
            "} finally {\n"
            "    cleanup()\n"
            "}"
        )
        self.assertEqual(transpile(source), expected)


class TestLexer(unittest.TestCase):
    """Direct tests for the lexer."""

    def test_empty_input(self):
        self.assertEqual(tokenize(""), [])

    def test_single_identifier(self):
        tokens = tokenize("fn")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].value, "fn")

    def test_string_token(self):
        tokens = tokenize('"hello"')
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, '"hello"')

    def test_line_comment_token(self):
        tokens = tokenize("// comment")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.COMMENT_LINE)

    def test_block_comment_token(self):
        tokens = tokenize("/* block */")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.COMMENT_BLOCK)

    def test_number_tokens(self):
        for num in ["42", "3.14", "0xFF", "0b1010", "1_000"]:
            with self.subTest(num=num):
                tokens = tokenize(num)
                self.assertEqual(tokens[0].type, TokenType.NUMBER, f"Failed for {num}")

    def test_operator_double_question(self):
        tokens = tokenize("??")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.OPERATOR)
        self.assertEqual(tokens[0].value, "??")


if __name__ == "__main__":
    unittest.main()
