import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import elevenlabs
from llmmaster import LLMMaster

from architect_common import ArchitectBase
from architect_common import GEN_ELEVENLABS_FEMALE_VOICE_ID
from architect_common import GEN_ELEVENLABS_MALE_VOICE_ID
from architect_common import GEN_ELEVENLABS_NEUTRAL_VOICE_ID
from architect_common import GEN_ELEVENLABS_VOICE_PROVIDER
from architect_common import RD_VOICE_KEYWORD
from config import EXT_MP3
from config import SEC_RD


class ArchitectElevelLabs(ArchitectBase):
    '''
    要件定義書から音声を生成するアーキテクトElevenLabs専用
    sys.argv[4]: 希望する音声の性別(male, female or neutral) 非必須
    '''
    def __init__(self):
        super().__init__()

        if self.args == 5:
            self.voice_gender = sys.argv[4].lower()
        else:
            self.voice_gender = None

    def work(self):
        '''
        手順：
          1. 要件定義書は複数あるかもしれないので下記手順2-4を繰り返す
          2. 要件定義書から性別を取得、声の生成に必須
          3. 要件定義書から音声生成テキストを抽出
          4. LLMMasterにて音声生成
          5. 音声ファイルを保存
          6. メニューに音声ファイルの保存先を記録
          7. メニューを保存
        補足：音声生成AIはElevenLabsを使用
        '''
        super().work()

        master = LLMMaster()

        lines = {}
        voice_ids = {}
        for key, value in self.source.items():
            if self.source_section == SEC_RD:
                voice_id = self._get_voice_id(value)
                line_list = self._find_voice_text(value, RD_VOICE_KEYWORD)
                i = 1
                for line in line_list:
                    tag = f'{key}_{i:02}'
                    lines[tag] = line
                    voice_ids[tag] = voice_id
                    i += 1
            else:
                tag = f'elevenlabs_{key}'
                voice_ids[tag] = self._gender_to_voice_id(self.voice_gender)
                lines[tag] = Path(value).read_text(encoding='utf-8')

        for key, value in lines.items():
            params = master.pack_parameters(
                provider=GEN_ELEVENLABS_VOICE_PROVIDER,
                prompt=value,
                voice_id=voice_ids[key])
            master.summon({key: params})

        master.run()
        new_menu_items = {}

        for key, value in master.results.items():

            to_write = ''

            if value:
                save_as = self.output_dir / f'{key}{EXT_MP3}'
                to_write = str(save_as)
                elevenlabs.save(value, to_write)
            else:
                to_write = 'Failed to generate speech voice.'

            new_menu_items[key] = to_write

        self._add_menu_items(new_menu_items)
        master.dismiss()

    def _get_voice_id(self, source: str):
        '''
        要件定義書から性別を取得し `voice_id` を選定
        手順：
          1. 要件定義書 `source` を読み込む
          2. 要件定義書を順に追って性別の行を見つける
          3. 男性の場合は `GEN_ELEVENLABS_MALE_VOICE_ID` を返す
          4. 女性の場合は `GEN_ELEVENLABS_FEMALE_VOICE_ID` を返す
        '''
        voice_id = None
        markdown = Path(source).read_text(encoding='utf-8').splitlines()

        for line in markdown:
            line = line.strip().lower()
            if '性別' in line:
                if '男性' in line:
                    voice_id = self._gender_to_voice_id('male')
                    break
                elif '女性' in line:
                    voice_id = self._gender_to_voice_id('female')
                    break
                else:
                    voice_id = self._gender_to_voice_id('neutral')
                    break

        return voice_id

    def _gender_to_voice_id(self, gender: str):
        '''
        希望する音声の性別を `voice_id` に変換
        '''
        if gender == 'male':
            return GEN_ELEVENLABS_MALE_VOICE_ID
        elif gender == 'female':
            return GEN_ELEVENLABS_FEMALE_VOICE_ID
        else:
            return GEN_ELEVENLABS_NEUTRAL_VOICE_ID

    def _find_voice_text(self, source: str, keyword: str):
        '''
        要件定義書から音声合成するセリフを一覧で抽出する
        手順：
          1. 要件定義書 `source` を読み込む
          2. 要件定義書を順に追って音声合成するセリフの行を見つける
          3. 見つけたセリフを返す
          4. 次のセクションが見つかるまで3.を繰り返す
        '''
        ans = []
        found_keyword = False

        markdown = Path(source).read_text(encoding='utf-8').splitlines()

        for line in markdown:
            line = line.strip()
            if line.startswith('#') and found_keyword:
                break
            if keyword in line:
                found_keyword = True
                continue
            if found_keyword and line:
                buff = line.split(':')[-1]
                buff = re.sub(r'[「」\s]', '', buff)
                ans.append(buff)

        return ans


def main():
    architect = ArchitectElevelLabs()
    architect.work()


if __name__ == '__main__':
    main()
