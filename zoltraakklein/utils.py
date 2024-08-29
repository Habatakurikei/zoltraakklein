import shutil
from pathlib import Path
from subprocess import Popen

from zoltraakklein.config import EXT_MARKDOWN
from zoltraakklein.config import EXT_PYTHON
from zoltraakklein.config import EXT_YAML
from zoltraakklein.config import MENU_FORMAT
from zoltraakklein.config import MENU_TEMPLATE
from zoltraakklein.config import PATH_TO_ARCHITECT
from zoltraakklein.config import PATH_TO_COMPILER
from zoltraakklein.config import PATH_TO_INSTRUCTION
from zoltraakklein.config import PATH_TO_OUTPUT
from zoltraakklein.config import PATH_TO_PROMPT
from zoltraakklein.config import PATH_TO_TEMPLATE
from zoltraakklein.config import PROMPT_FOR_NAME
from zoltraakklein.config import PYTHON_COMMAND
from zoltraakklein.config import SYSTEM_DIR
from zoltraakklein.yaml_manager import YAMLManager


def check_output_folder(work_dir: Path):
    '''
    生成物保存先フォルダが存在するかを確認します。
    存在しない場合はフォルダを作成しておきます。
    '''
    output_path = work_dir / PATH_TO_OUTPUT
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def generate_naming_prompt(request: str, work_dir: Path):
    '''
    プロジェクト名生成プロンプトを用意します。
    （旧ファイル名生成プロンプト）
    手順
        1. 既にあるプロジェクト名の一覧を取得
        2. プロンプトのテンプレートを読み込み
        3. リクエスト内容と既にあるプロジェクト名リストをプロンプトに埋め込み
        4. プロンプトを返す
    '''
    prompt = ''

    existing_projects = [p.name for p in work_dir.iterdir() if p.is_dir()]
    existing_projects = ', '.join(existing_projects)

    prompt_path = SYSTEM_DIR / PATH_TO_PROMPT / PROMPT_FOR_NAME
    prompt = prompt_path.read_text(encoding='utf-8')
    prompt = prompt.format(request=request,
                           existing_projects=existing_projects)
    return prompt


def generate_requirement_prompt(request: str, compiler: str):
    '''
    要件定義書生成プロンプトを用意します。
    手順：
      1. 指定コンパイラを読み込み
      2. コンパイラにあなたのリクエストを埋め込み
      3. 整形済みコンパイラをプロンプトとして返す
    2024-08-10: フォーマッタ追加処理を試験的にコメントアウト
    2024-08-16: 問題なかったのでフォーマッタ処理を削除
    '''
    prompt = ''
    compiler_path = SYSTEM_DIR / PATH_TO_COMPILER / compiler
    prompt = compiler_path.read_text(encoding='utf-8')
    return prompt.format(prompt=request)


def create_menu(project_path: Path, project_name: str):
    '''
    新規プロジェクトに対して空のメニュー（生成物リスト）を作成します。
    出力先フォルダ＋ファイル名を含む Path クラスを返します。
    '''
    menu_template = SYSTEM_DIR / PATH_TO_TEMPLATE / MENU_TEMPLATE
    new_menu = project_path / f"{project_name}{MENU_FORMAT}"
    shutil.copy2(menu_template, new_menu)
    return new_menu


def seek_document(name: str, path: Path):
    """
    コンパイラや指示書を探すための関数。
    指定したパスにあるドキュメント名を調べます。
    あれば拡張子を含むファイル名を文字列で返します。
    (e.g. outfit_idea.md, outfit_idea.yaml)
    なければ空の文字列を返します。
    """
    document = ''
    document_path = SYSTEM_DIR / path
    document_list = list(document_path.iterdir())

    if path == PATH_TO_COMPILER and not name.endswith(EXT_MARKDOWN):
        name += EXT_MARKDOWN
    elif path == PATH_TO_INSTRUCTION and not name.endswith(EXT_YAML):
        name += EXT_YAML

    for doc in document_list:
        if doc.name == name:
            document = doc.name
            break

    return document


def fetch_instruction_content(instruction: str):
    '''
    領域展開指示書を読み込みます。
    引数の文字列は拡張子を含むファイル名です。(e.g. outfit_idea.yaml)
    '''
    to_open = SYSTEM_DIR / PATH_TO_INSTRUCTION / instruction
    return YAMLManager(str(to_open))


def set_expansion_limit(compiler: str):
    '''
    領域展開の最大ステップ数を設定します。
    引数のコンパイラ名により設定値が異なります。
    '''
    instruction = fetch_instruction_content(
        seek_document(compiler, PATH_TO_INSTRUCTION))
    return instruction.sum_of_sections()


def order_to_architect(project_path: str, output: str, function: str):
    '''
    領域展開するために指定のアーキテクトを呼び出します。
    アーキテクトは別プロセス（つまり非同期）で実行されます。
    引数：
    project_path: プロジェクトフォルダのパス
    output: 生成物の保存先フォルダのパス
    function: アーキテクトの関数名と引数
    YAML形式の指示書と引数の関係はこのようになっています。
      output: function(key_in_menu)
      (Example) rd_mermaid: generate_mermaid_graph(rd)
    意味： `generate_mermaid_graph.py` スクリプトを実行してグラフを生成せよ。
    入力はメニューに書かれている要件定義書(rd)、生成物保存先は `rd_mermaid` フォルダ。
    '''
    buff = function.split('(')
    architect = SYSTEM_DIR / PATH_TO_ARCHITECT / f"{buff[0]}{EXT_PYTHON}"
    args = buff[1].replace(')', '').replace(' ', '').split(',')
    to_call = [PYTHON_COMMAND, str(architect), project_path, output] + args
    return Popen(to_call)
