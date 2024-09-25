import sys
from pathlib import Path
from requests.models import Response

sys.path.append(str(Path(__file__).parent.parent))

from llmmaster import LLMMaster

from architect_common import ArchitectBase
from architect_common import GEN_IMAGE_NEGATIVE_PROMPT
from architect_common import RD_IMAGE_KEYWORD
from config import EXT_MARKDOWN
from config import EXT_PNG


class ArchitectStableDiffusion(ArchitectBase):
    '''
    要件定義書から画像を生成するアーキテクトStable Diffusion専用
    sys.argv[4]: 生成したい画像サイズ ("square" or "landscape")
    '''
    def __init__(self):
        super().__init__()

        self.size = '1:1'

        if self.args == 5 and sys.argv[4] == 'landscape':
            self.size = '16:9'

    def work(self):
        '''
        手順：
          1. 要求内容は複数あるかもしれないので下記手順2-3を繰り返す
          2. 要求内容の読み込み
            a. 要求内容が要件定義書(.md)の場合はプロンプトを抽出
            b. 要求内容がテキストファイル(.txt)の場合はそのままプロンプトとする
          3. LLMMasterにAIインスタンスを召喚
          4. LLMMasterにて画像一括生成
          5. 画像化したファイルを保存
          6. メニューに画像ファイルの保存先を記録
        補足：画像生成AIはStable Diffusionを使用
              画像の保存方法が生成AIにより異なるためハードコーディングせざるを得ない
        '''
        super().work()

        master = LLMMaster(wait_for_starting=1.5)

        new_menu_items = {}

        for key, value in self.source.items():
            if value.endswith(EXT_MARKDOWN):
                prompt = self._find_image_prompt(value, RD_IMAGE_KEYWORD)
            else:
                prompt = Path(value).read_text(encoding='utf-8').strip()

            if prompt:
                params = master.pack_parameters(
                    provider='stable_diffusion_tti',
                    model='core',
                    prompt=prompt,
                    aspect_ratio=self.size,
                    negative_prompt=GEN_IMAGE_NEGATIVE_PROMPT)
                master.summon({key: params})
            else:
                msg = 'No prompt found or Japanese keywords might be included.'
                new_menu_items[key] = msg

        master.run()

        for key, value in master.results.items():
            to_write = ''

            if isinstance(value, Response):
                to_write = self._save_bytes(value.content,
                                            f'image_{key}{EXT_PNG}')
            elif isinstance(value, str):
                to_write = value
            else:
                msg = 'Content not found in the response from generative AI.'
                to_write = msg

            new_menu_items[key] = to_write

        self._add_menu_items(new_menu_items)
        master.dismiss()


def main():
    architect = ArchitectStableDiffusion()
    architect.work()


if __name__ == '__main__':
    main()
