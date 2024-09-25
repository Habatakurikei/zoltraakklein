import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from llmmaster import LLMMaster

from architect_common import ArchitectBase
from architect_common import MODEL
from architect_common import PROVIDER
from architect_common import CONTENT_ATTRIBUTES
from architect_common import CONTENT_TYPE_VIRTUAL_CHARACTER
from config import EXT_MARKDOWN
from config import PATH_TO_PROMPT
from config import PROMPT_FOR_VIRTUAL_CHARACTER
from config import SYSTEM_DIR


class ArchitectVirtualCharacter(ArchitectBase):
    '''
    要件定義書からバーチャルキャラクターの設定を生成するアーキテクト
    '''
    def __init__(self):
        super().__init__()

        self.provider = \
            CONTENT_ATTRIBUTES[CONTENT_TYPE_VIRTUAL_CHARACTER][PROVIDER]
        self.model = \
            CONTENT_ATTRIBUTES[CONTENT_TYPE_VIRTUAL_CHARACTER][MODEL]

    def work(self):
        '''
        手順：
          1. 要件定義書の読み込み
          2. 要件定義書からキャラクター設定を抽出
          3. LLMMasterでキャラクター設定生成
          4. 生成した設定を保存
          5. メニューに設定ファイルの保存先を記録
          6. メニューを保存
        '''
        super().work()

        master = LLMMaster()

        source = self._select_source(self.provider)
        source_content = Path(source).read_text(encoding='utf-8')

        character_list = self._find_character_definition(source)

        to_read = SYSTEM_DIR / PATH_TO_PROMPT / PROMPT_FOR_VIRTUAL_CHARACTER
        template = to_read.read_text(encoding='utf-8')

        for i, entry in enumerate(character_list, 1):
            prompt = template.format(prompt=entry, proposal=source_content)
            params = master.pack_parameters(provider=self.provider,
                                            model=self.model,
                                            prompt=prompt)
            master.summon({f"character_{i:02d}": params})

        master.run()

        new_menu_items = {}

        for key, value in master.results.items():
            if value:
                save_as = self.output_dir / f"{key}{EXT_MARKDOWN}"
                save_as.write_text(value, encoding='utf-8')
                new_menu_items[key] = str(save_as)
            else:
                new_menu_items[key] = "Failed to generate character settings"

        self._add_menu_items(new_menu_items)
        master.dismiss()

    def _find_character_definition(self, source: str):
        '''
        要件定義書からキャラクター設定を抽出する
        原則的にキャラ情報は1か所のみなので、最初に見つかったものを使う
        '''
        character_list = []
        candidates = []
        bracketed_content = self._list_bracketed_content(source)

        for entry in bracketed_content:
            if 'character' in entry[0]:
                candidates = entry[1].splitlines()
                break

        for line in candidates:
            character_list.append(line.strip().replace('- ', ''))

        return character_list


def main():
    architect = ArchitectVirtualCharacter()
    architect.work()


if __name__ == '__main__':
    main()
