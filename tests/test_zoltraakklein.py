import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../zoltraakklein'))

import pytest

from zoltraakklein import ZoltraakKlein
from zoltraakklein.yaml_manager import YAMLManager


REQUEST = '冬の北海道、札幌雪祭りの会場で開催するクラシック音楽イベント'
COMPILER = 'general_proposal'


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def show_results(zk: ZoltraakKlein):
    print(f'project_name = {zk.project_name}')
    print(f'project_path = {zk.project_path}')
    print(f'menu = {zk.project_menu}')
    menu = YAMLManager(str(zk.project_menu))
    print('Menu (list of generated items) is ready.')
    print(zk.project_menu.read_text(encoding="utf-8"))
    print(f'Total {menu.sum_of_items()} files generated.')
    print(f'Elapsed time for each step (sec):')
    for step, elapsed_time in zk.takt_time.items():
        print(f"    {step}: {elapsed_time}")
    print(f'Total elapsed time (sec) = {sum(zk.takt_time.values())}')


def test_no_prompt():
    with pytest.raises(ValueError, match='リクエストが指定されていません'):
        ZoltraakKlein(compiler='general_proposal')


def test_no_compiler():
    with pytest.raises(ValueError, match='コンパイラが指定されていません'):
        ZoltraakKlein(request='テストプロジェクト')


def test_wrong_compiler():
    with pytest.raises(ValueError):
        ZoltraakKlein(request=REQUEST, compiler='wrong_compiler')


def test_default_setting(run_api):

    judgment = True

    zk = ZoltraakKlein(request=REQUEST, compiler=COMPILER, verbose=True)

    if not isinstance(zk, ZoltraakKlein):
        pytest.fail('ZoltraakKlein インスタンスが生成されていません')

    print(f'compiler = {zk.compiler}, request = {zk.request}, verbose = {zk.verbose}')
    print(f'Default LLM: {zk.llm}')

    if run_api:
        print('Cast Zoltraak!')

        zk.cast_zoltraak()

        if not zk.project_menu.exists():
            pytest.fail('メニューが生成されていません')

        show_results(zk)

    assert judgment


def test_multiple_llm(run_api):

    judgment = True

    single_llm = {
        "naming": {
            "provider": "anthropic",
            "model": "claude-3-haiku-20240307",
            "max_tokens": 100,
            "temperature": 0.9
        }
    }

    multiple_llm = {
        "openai": {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "max_tokens": 10000,
            "temperature": 0.7
        },
        "anthropic": {
            "provider": "anthropic",
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 4096,
            "temperature": 0.2
        },
        "google": {
            "provider": "google",
            "model": "gemini-1.5-flash",
            "max_tokens": 10000,
            "temperature": 0.5
        }
    }

    zk = ZoltraakKlein(request=REQUEST, compiler=COMPILER, verbose=True)

    if not isinstance(zk, ZoltraakKlein):
        pytest.fail('ZoltraakKlein インスタンスが生成されていません')

    print(f'compiler = {zk.compiler}, request = {zk.request}, verbose = {zk.verbose}')
    print(f'Default LLM: {zk.llm}')

    if run_api:

        print("Cast Zoltraak!")

        zk.name_for_requirement(**single_llm)
        zk.generate_requirement(**multiple_llm)

        while zk.is_expansion_capable():
            try:
                zk.expand_domain()
                while zk.expansion_in_progress:
                    time.sleep(1)
            except Exception as e:
                print(e)
                break

        if not zk.project_menu.exists():
            pytest.fail('メニューが生成されていません')

        show_results(zk)

    assert judgment
