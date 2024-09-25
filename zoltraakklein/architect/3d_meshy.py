import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import requests
from requests.models import Response

from llmmaster import LLMMaster
from llmmaster.config import REQUEST_OK

from architect_common import ArchitectBase
from architect_common import GEN_MESHY_3D_ADDITIONAL_PROMPT
from architect_common import GEN_MESHY_3D_NEGATIVE_PROMPT
from architect_common import GEN_MESHY_3D_PROVIDER
from architect_common import GEN_MESHY_3D_STYLE
from architect_common import RD_MESHY_3D_KEYWORD
from config import SEC_MESHY_3D_FIRST


MODEL_URLS = 'model_urls'
THUMBNAIL_URL = 'thumbnail_url'
VIDEO_URL = 'video_url'


class ArchitectMeshy3D(ArchitectBase):
    '''
    要件定義書から3Dモデルを生成するアーキテクトMeshy3D専用
    '''
    def __init__(self):
        super().__init__()

    def work(self):
        '''
        手順：
          1. 要件定義書を読み込む（全部）
          2. 要件定義書から3Dモデル生成向けプロンプトを抽出
          3. LLMMasterで3Dモデル生成し、生成結果を保存
            モデル生成結果にIDが含まれていればリファイン用にキープ
          4. LLMMasterで3Dモデルをリファインし、生成結果を保存
        '''
        super().work()

        master = LLMMaster()

        for key, value in self.source.items():
            prompt = self._find_image_prompt(value, RD_MESHY_3D_KEYWORD)
            prompt += GEN_MESHY_3D_ADDITIONAL_PROMPT
            params = master.pack_parameters(
                provider=GEN_MESHY_3D_PROVIDER,
                prompt=prompt,
                art_style=GEN_MESHY_3D_STYLE,
                negative_prompt=GEN_MESHY_3D_NEGATIVE_PROMPT)
            master.summon({key: params})

        master.run()

        for key, value in master.results.items():
            if not isinstance(value, Response):
                self._add_menu_items({f'{SEC_MESHY_3D_FIRST}_{key}':
                                      'Failed to generate 3D model.'})
            else:
                json_data = value.json()
                self._save_3d_models(json_data, key, SEC_MESHY_3D_FIRST)

        master.dismiss()

    def _save_3d_models(self, json_data: dict, tag: str, gen_type: str):
        '''
        3Dモデル生成結果のデータ保存とメニューへの追加
        主な保存データ：複数の3Dモデル形式*()、サムネイルPNG、プレビュー動画
        '''
        new_menu_items = {}

        for key, value in json_data[MODEL_URLS].items():
            if value:
                res = requests.get(value)
                if res.status_code == REQUEST_OK:
                    file_name = f'{gen_type}_{tag}.{key}'
                    new_menu_items[file_name] = self._save_bytes(
                        res.content, file_name)

        if THUMBNAIL_URL in json_data and json_data[THUMBNAIL_URL]:
            res = requests.get(json_data[THUMBNAIL_URL])
            if res.status_code == REQUEST_OK:
                file_name = f'{gen_type}_{tag}_thumbnail.png'
                new_menu_items[file_name] = self._save_bytes(
                    res.content, file_name)

        if VIDEO_URL in json_data and json_data[VIDEO_URL]:
            res = requests.get(json_data[VIDEO_URL])
            if res.status_code == REQUEST_OK:
                file_name = f'{gen_type}_{tag}_video.mp4'
                new_menu_items[file_name] = self._save_bytes(
                    res.content, file_name)

        self._add_menu_items(new_menu_items)


def main():
    architect = ArchitectMeshy3D()
    architect.work()


if __name__ == '__main__':
    main()
