import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import requests
from requests.models import Response

from llmmaster import LLMMaster
from llmmaster.config import REQUEST_OK

from architect_common import ArchitectBase
from architect_common import GEN_PIKAPIKAPIKA_DEFAULT_STYLE
from architect_common import GEN_PIKAPIKAPIKA_PARAMS
from architect_common import GEN_PIKAPIKAPIKA_PROVIDER
from architect_common import GEN_PIKAPIKAPIKA_SOURCE_RD
from architect_common import RD_PIKAPIKAPIKA_KEYWORD
from config import EXT_MP4
from config import EXT_PNG


class ArchitectPikaPikaPika(ArchitectBase):
    '''
    要件定義書から画像を生成するアーキテクトPikaPikaPika専用
    sys.argv[4]: 生成したい動画のスタイル ('Anime', '3D', 'Natural',etc) オプション
    '''
    def __init__(self):
        super().__init__()

        if self.args == 5:
            self.style = sys.argv[4]
        else:
            self.style = GEN_PIKAPIKAPIKA_DEFAULT_STYLE

    def work(self):
        '''
        手順：
          1. 要件定義書の読み込み
          2. 要件定義書から画像生成プロンプトを抽出
          3. LLMMasterにて動画生成
          4. 生成した動画を保存
          5. メニューに動画ファイルの保存先を記録
          6. メニューを保存
        補足：動画生成AIはPikaPikaPikaTTVModelを使用、HD品質のものを1枚生成
              動画の保存方法が生成AIにより異なるためハードコーディングせざるを得ない
        '''
        super().work()

        master = LLMMaster()

        source = self._select_source(GEN_PIKAPIKAPIKA_SOURCE_RD)

        prompt = self._find_image_prompt(source, RD_PIKAPIKAPIKA_KEYWORD)
        params = master.pack_parameters(provider=GEN_PIKAPIKAPIKA_PROVIDER,
                                        prompt=prompt,
                                        style=self.style,
                                        sfx=False,
                                        aspect_ratio='16:9',
                                        parameters=GEN_PIKAPIKAPIKA_PARAMS)
        master.summon({f"pikapikapika_{self.source_section}": params})

        master.run()
        new_menu_items = {}

        for key, value in master.results.items():
            if isinstance(value, Response):
                new_menu_items.update(self._save_contents(key, value))
            else:
                msg = 'Contents not found in the response from generative AI.'
                new_menu_items[key] = msg

        self._add_menu_items(new_menu_items)
        master.dismiss()

    def _save_contents(self, key: str, value: Response):
        '''
        HTTPレスポンスから生成物の情報を探して保存、メニューに記載して返す
        '''
        json_result = value.json()
        menu_items = {}

        if 'resultUrl' in json_result['videos'][0]:
            res = requests.get(json_result['videos'][0]['resultUrl'])
            if res.status_code == REQUEST_OK:
                msg = self._save_bytes(res.content, f'{key}{EXT_MP4}')
            else:
                msg = 'Failed to download the video file.'
            menu_items[key] = msg

        if 'imageThumb' in json_result['videos'][0]:
            menu_key = f'{key}_thumb'
            res = requests.get(json_result['videos'][0]['imageThumb'])
            if res.status_code == REQUEST_OK:
                msg = self._save_bytes(res.content,
                                       f'{menu_key}{EXT_PNG}')
            else:
                msg = 'Failed to download the thumbnail image.'
            menu_items[menu_key] = msg

        if 'videoPoster' in json_result['videos'][0]:
            menu_key = f'{key}_poster'
            res = requests.get(json_result['videos'][0]['videoPoster'])
            if res.status_code == REQUEST_OK:
                msg = self._save_bytes(res.content,
                                       f'{menu_key}{EXT_PNG}')
            else:
                msg = 'Failed to download the poster image.'
            menu_items[menu_key] = msg

        return menu_items


def main():
    architect = ArchitectPikaPikaPika()
    architect.work()


if __name__ == '__main__':
    main()
