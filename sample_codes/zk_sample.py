import time
from pathlib import Path


from zoltraakklein import ZoltraakKlein

# Zoltraak Klein お試しプログラム
# リクエストとコンパイラを変更してからこのスクリプトをターミナルで実行してください。
# 実行するには OpenAI API key と Mermaid CLI が必要です。

# Sample program for Zoltraak Klein
# Run this script in your terminal after you change the request and compiler.
# Need OpenAI API key and Mermaid CLI installed on your system.

# 1. あなたのリクエスト内容に書き換えてください。
# 1. Change this for your request
REQUEST = 'Japanese foods festival to be held in London, in September.'

# 2. コンパイラを選択してください。使用しないコンパイラはコメントアウトしてください。
# 2. Comment/Uncomment to select a unique compiler
COMPILER = 'general_proposal'
# COMPILER = 'business_plan'
# COMPILER = 'strategic_consultant'
# COMPILER = 'marketing_research'
# COMPILER = 'business_negotiation'


def print_directory_tree(path: Path, level: int = 0):
    for item in path.iterdir():
        print("  " * level + "|-- " + item.name)
        if item.is_dir():
            print_directory_tree(item, level + 1)


zk = ZoltraakKlein(
    request=REQUEST,
    compiler=COMPILER,
    verbose=True
)

zk.name_for_requirement()
zk.generate_requirement()

while zk.is_expansion_capable():
    try:
        zk.expand_domain()
        while zk.expansion_in_progress:
            time.sleep(1)
    except Exception as e:
        print(e)
        break

print('領域展開完了！')
print('Domain expansion completed!')

if zk.project_menu.exists():
    print('----------------------------------')
    print('メニュー（生成物一覧）が生成されました。')
    print('Menu (list of generated items) is ready.')
    print(zk.project_menu.read_text(encoding="utf-8"))

    print('----------------------------------')
    print('生成ファイルとディレクトリ一覧')
    print('List of generated files and directories')
    print_directory_tree(zk.project_path)

else:
    print('----------------------------------')
    print('メニューが生成されませんでした。')
    print('Menu has not been generated.')

print('----------------------------------')
print(f'各ステップの実行時間（秒）：')
print(f'Elapsed time for each step (sec):')
for step, elapsed_time in zk.takt_time.items():
    print(f"    {step}: {elapsed_time}")
print('----------------------------------')
print(f'合計実行時間 (sec) = {sum(zk.takt_time.values())}')
print(f'Total elapsed time (sec) = {sum(zk.takt_time.values())}')
