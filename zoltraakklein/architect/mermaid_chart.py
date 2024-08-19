import subprocess
import sys
from pathlib import Path
from subprocess import DEVNULL

sys.path.append(str(Path(__file__).parent.parent))

from architect_common import ArchitectBase
from config import EXT_PNG


class ArchitectMermaidGraphGenerator(ArchitectBase):
    '''
    要件定義書からMermaid記法の部分を探してグラフ化するアーキテクト
    【重要】
    マーメイド記法をグラフにするために別のコマンドラインアプリ
    mermaid-cli を使用しています。事前にインストールしてください。
    https://github.com/mermaid-js/mermaid-cli
    '''
    def __init__(self):
        super().__init__()

    def work(self):
        '''
        手順：
          1. 要件定義書は複数あるかもしれないので下記手順2-5を繰り返す
          2. 要件定義書の読み込み
          3. 要件定義書からマーメイド記法の部分をすべて抽出
            （ひとつとは限らない）
          4. 抽出したマーメイド記法の部分を画像化
          5. 画像化したファイルを保存
          6. メニューに画像ファイルの保存先を記録
        '''
        super().work()

        new_menu_items = {}

        i = 1
        for key, value in self.source.items():
            diagrams = self._list_bracketed_content(value)
            for entry in diagrams:
                if entry[0] == 'mermaid':
                    menu_key = f'{self.output_section}_{key}_{i:02}'
                    save_as = self.output_dir / f'{menu_key}{EXT_PNG}'
                    self._save_diagram(entry[1].strip(), save_as)
                    new_menu_items[menu_key] = str(save_as)
                    i += 1

        self._add_menu_items(new_menu_items)

    def _save_diagram(self, mermaid_text: str, save_as: Path):
        '''
        一部のマーメイド記法グラフにて中黒点がエラーになる
        仮の対処法として置換、問題なければ削除予定
        '''
        to_write = mermaid_text.replace('・', 'と')

        temporary_file = Path('temp.mmd')
        temporary_file.write_text(to_write, encoding='utf-8')

        command = ['mmdc', '-i', str(temporary_file), '-o', str(save_as)]
        subprocess.run(command, shell=True, stdout=DEVNULL, stderr=DEVNULL)

        temporary_file.unlink()


def main():
    architect = ArchitectMermaidGraphGenerator()
    architect.work()


if __name__ == '__main__':
    main()
