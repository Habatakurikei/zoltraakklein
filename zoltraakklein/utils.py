import os

from zoltraakklein.config import PATH_TO_COMPILER


def seek_compiler(name=''):
    """
    指定したコンパイラが存在するかを調べる。
    あれば拡張子を含むコンパイラファイル名を返す。
    なければ空の文字を返す。
    """
    compiler = ''

    compiler_list = os.listdir(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        PATH_TO_COMPILER))

    if '.md' not in name:
        name += '.md'

    if name in compiler_list:
        compiler = compiler_list[compiler_list.index(name)]

    return compiler
