# coding: utf-8

from os.path import join, dirname
from textx.metamodel import metamodel_from_file
from textx.export import metamodel_export, model_export

from pyccel.parser.syntax.core import ImportFromStmt, ImportAsNames
from pyccel.parser.syntax.core import clean_namespace

__all__ = ['find_imports']

def find_imports(filename=None, stmts=None, debug=False):
    """
    Finds all import statements in the file.

    filename: str
        name of the file to parse
    stmts: str
        instructions to parse
    debug: bool
        use debug mode if True
    """
    this_folder = dirname(__file__)

    # Get meta-model from language description
    grammar = join(this_folder, 'grammar/imports.tx')
    meta = metamodel_from_file(grammar, debug=debug, \
                               classes=[ImportFromStmt, ImportAsNames])

    # Instantiate model
    if filename:
        model = meta.model_from_file(filename)
    elif stmts:
        model = meta.model_from_str(stmts)
    else:
        raise ValueError('Expecting a filename or a string')

    d = {}
    for stmt in model.statements:
        if isinstance(stmt, ImportFromStmt):
            expr = stmt.expr
            module = str(expr.fil)
            names  = str(expr.funcs)

            # ...
            txt = names
            txt = txt.replace('\'', '')
            txt = txt.replace('(', '')
            txt = txt.replace(')', '')
            txt = txt.replace('[', '')
            txt = txt.replace(']', '')
            txt = txt.split(',')

            names = [s.strip() for s in txt if len(s) > 0]
            # ...

            # ...
            if not(module in d):
                d[module] = []

            d[module] += names
            # ...

    clean_namespace()

    return d
