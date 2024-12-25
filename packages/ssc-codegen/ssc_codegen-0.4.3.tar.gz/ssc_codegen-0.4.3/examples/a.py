from ssc_codegen.ast_builder import build_ast_module
from ssc_codegen.converters.py_parsel import converter

a = build_ast_module('schemas/animego.py')
print(converter.convert_program(a))