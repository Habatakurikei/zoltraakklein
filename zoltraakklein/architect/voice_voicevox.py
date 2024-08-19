import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from requests.models import Response

from llmmaster import LLMMaster

from architect_common import ArchitectBase
from architect_common import GEN_VOICEVOX_DEFAULT_SPEAKER
from architect_common import GEN_VOICEVOX_INTERVAL
from architect_common import GEN_VOICEVOX_MAX_LINES
from architect_common import GEN_VOICEVOX_VOICE_PROVIDER
from architect_common import RD_VOICE_KEYWORD
from architect_common import VOICEVOX_CHARACTER_LIMIT
from architect_common import VOICEVOX_PREFIX
from config import EXT_WAV
from config import SEC_RD


class ArchitectVoicevox(ArchitectBase):
    '''
    要件定義書から音声を生成するアーキテクトVOICEVOX専用
    '''
    def __init__(self):
        super().__init__()

    def work(self):
        '''
        手順：
          1. 要件定義書は複数あるかもしれないので下記手順2-4を繰り返す
          2. 要件定義書からスピーカーIDを取得
          3. 要件定義書から音声生成テキストを抽出
          4. LLMMasterにて音声生成
          5. 音声ファイルを保存
          6. メニューに音声ファイルの保存先を記録
          7. メニューを保存
        補足：音声生成AIはVOICEVOXを使用
        '''
        super().work()

        master = LLMMaster(summon_limit=GEN_VOICEVOX_MAX_LINES,
                           wait_for_starting=GEN_VOICEVOX_INTERVAL)

        lines = {}
        for key, value in self.source.items():
            if SEC_RD in self.source_section:
                line_list = self._find_voice_text(value, RD_VOICE_KEYWORD)
                for i, line in enumerate(line_list, 1):
                    tag = VOICEVOX_PREFIX + f'{key}_{i:02d}'
                    lines[tag] = line
            else:
                text = Path(value).read_text(encoding='utf-8')
                if len(text.replace('\n', '')) < VOICEVOX_CHARACTER_LIMIT:
                    lines[VOICEVOX_PREFIX + key] = text.replace('\n', '')
                else:
                    lines.update(self._split_text(VOICEVOX_PREFIX + key, text))

        for key, value in lines.items():
            params = master.pack_parameters(
                provider=GEN_VOICEVOX_VOICE_PROVIDER,
                prompt=value,
                speaker=GEN_VOICEVOX_DEFAULT_SPEAKER)
            master.summon({key: params})

        master.run()
        new_menu_items = {}

        for key, value in master.results.items():
            to_write = ''

            if isinstance(value, Response):
                to_write = self._save_bytes(value.content, f'{key}{EXT_WAV}')
            elif isinstance(value, str):
                to_write = value
            else:
                msg = 'Content not found in the response from generative AI.'
                to_write = msg

            new_menu_items[key] = to_write

        self._add_menu_items(new_menu_items)
        master.dismiss()

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

    def _split_text(self, key: str, text: str):
        '''
        入力されたテキストを一行ずつ分解して読み上げ音声入力にする
        文字数が多すぎるとVocevoxが高負荷で落ちてしまうための対策
        '''
        ans = {}
        i = 1
        for sentence in text.splitlines():
            if sentence:
                tag = f'{key}_{i:02d}'
                ans[tag] = sentence
                i += 1

        return ans


def main():
    architect = ArchitectVoicevox()
    architect.work()


if __name__ == '__main__':
    main()
