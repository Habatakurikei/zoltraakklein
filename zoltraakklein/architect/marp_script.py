import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from llmmaster import LLMMaster

from architect_common import ArchitectBase
from architect_common import CONTENT_ATTRIBUTES
from architect_common import CONTENT_TYPE_SCRIPT
from architect_common import PROVIDER
from architect_common import MODEL
from config import EXT_PLAINTEXT
from config import PATH_TO_PROMPT
from config import PROMPT_FOR_SCRIPT
from config import SYSTEM_DIR


class MarpScriptGenerator(ArchitectBase):
    '''
    Marpプレゼンテーション本文から読み上げ用スクリプトを生成するアーキテクト
    '''
    def __init__(self):
        super().__init__()

        self.provider = CONTENT_ATTRIBUTES[CONTENT_TYPE_SCRIPT][PROVIDER]
        self.model = CONTENT_ATTRIBUTES[CONTENT_TYPE_SCRIPT][MODEL]

    def work(self):
        '''
        手順：
          1. LLMMasterで見出しを生成
          2. 生成物をそれぞれ保存
          4. メニューに生成物の保存先を記録
          5. メニューを保存
        '''
        super().work()

        template = SYSTEM_DIR / PATH_TO_PROMPT / PROMPT_FOR_SCRIPT
        base_prompt = template.read_text(encoding='utf-8')

        master = LLMMaster()

        for key, content_file in self.source.items():
            content = Path(content_file).read_text(encoding='utf-8')

            prompt = base_prompt.format(content=content)
            params = master.pack_parameters(
                provider=self.provider,
                model=self.model,
                prompt=prompt,
                max_tokens=4096)
            master.summon({key: params})

        master.run()

        new_menu_items = {}

        for key, value in master.results.items():
            menu_key = f'script_{key}'
            if value:
                save_as = self.output_dir / f'{menu_key}{EXT_PLAINTEXT}'
                save_as.write_text(value, encoding='utf-8')
                msg = str(save_as)
            else:
                msg = f'Failed to generate speech for {key}.'
            new_menu_items[menu_key] = msg

        self._add_menu_items(new_menu_items)
        master.dismiss()


def main():
    generator = MarpScriptGenerator()
    generator.work()


if __name__ == '__main__':
    main()
