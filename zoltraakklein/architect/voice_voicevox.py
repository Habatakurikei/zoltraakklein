import re
import sys
import wave
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
        self.master = LLMMaster(summon_limit=GEN_VOICEVOX_MAX_LINES,
                                wait_for_starting=GEN_VOICEVOX_INTERVAL)

    def work(self):
        '''
        キャラクター要件定義書からセリフ音声を合成する場合と
        読み上げ原稿から音声を合成する場合で処理を分ける
        '''
        super().work()

        if SEC_RD in self.source_section:
            self._voice_from_rd()
        else:
            self._voice_from_document()

    def _set_llmmaster_parameters(self, prompt: str):
        '''
        LLMMasterに渡すパラメータを整えて返す
        単純処理だがこのクラスで繰り返し呼ばれるので
        ひとまとめにしてコードを見やすくした
        '''
        return self.master.pack_parameters(
            provider=GEN_VOICEVOX_VOICE_PROVIDER,
            prompt=prompt,
            speaker=GEN_VOICEVOX_DEFAULT_SPEAKER)

    def _voice_from_rd(self):
        '''
        キャラクター要件定義書のセリフ音声を合成
        各セリフは短いので並列処理で一気に作る
        '''
        for key, value in self.source.items():
            line_list = self._find_voice_text(value, RD_VOICE_KEYWORD)
            for i, line in enumerate(line_list, 1):
                tag = VOICEVOX_PREFIX + f'{key}_{i:02d}'
                self.master.summon({tag: self._set_llmmaster_parameters(line)})

        self.master.run()

        new_menu_items = {}
        for key, response in self.master.results.items():
            new_menu_items[key] = self._save_voice(response, f'{key}{EXT_WAV}')
        self._add_menu_items(new_menu_items)

        self.master.dismiss()

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

    def _voice_from_document(self):
        '''
        読み上げ原稿から音声を合成する
        原稿が短い場合は1原稿=1音声で合成
        原稿が長い場合は分割してそれぞれの音声を合成した後組み合わせる
        '''
        new_menu_items = {}

        for key, value in self.source.items():

            tag = VOICEVOX_PREFIX + key
            text = Path(value).read_text(encoding='utf-8')

            if len(text.replace('\n', '')) < VOICEVOX_CHARACTER_LIMIT:
                params = self._set_llmmaster_parameters(text.replace('\n', ''))
                self.master.summon({tag: params})
                self.master.run()
                new_menu_items[tag] = self._save_voice(
                    self.master.results[tag], f'{tag}{EXT_WAV}')

            else:
                lines = self._split_text(tag, text)
                for line_name, text_to_read in lines.items():
                    params = self._set_llmmaster_parameters(text_to_read)
                    self.master.summon({line_name: params})

                self.master.run()

                file_list = []
                for line_name, response in self.master.results.items():
                    if isinstance(response, Response):
                        entry = self._save_bytes(response.content,
                                                 f'{line_name}{EXT_WAV}')
                        file_list.append(entry)

                new_menu_items[tag] = self._concat_files(file_list, tag)

            self.master.dismiss()

        self._add_menu_items(new_menu_items)

    def _split_text(self, tag: str, text: str):
        '''
        入力されたテキストを一行ずつ分解して読み上げ音声入力にする
        文字数が多すぎるとVocevoxが高負荷で落ちてしまうための対策
        '''
        ans = {}
        i = 1
        for sentence in text.splitlines():
            if sentence:
                ans[f'{tag}_{i:02d}'] = sentence
                i += 1
        return ans

    def _concat_files(self, file_list: list, file_name: str):
        '''
        分割された音声ファイルを結合する
        '''
        save_as = str(self.output_dir / f'{file_name}{EXT_WAV}')
        output = wave.open(save_as, 'wb')
        for i, path in enumerate(file_list):
            with wave.open(path, 'rb') as wav_file:
                params = wav_file.getparams()
                frames = wav_file.readframes(wav_file.getnframes())
            if i == 0:
                output.setparams(params)
            output.writeframes(frames)
            Path(path).unlink()
        output.close()
        return save_as

    def _save_voice(self, response: Response, file_name: str):
        '''
        合成した音声を保存し、メニュー記載用にファイル名を返す
        引数のresponseは音声合成が成功したと仮定してResponseを受け取りたい
        '''
        to_write = ''
        if isinstance(response, Response):
            to_write = self._save_bytes(response.content, file_name)
        elif isinstance(response, str):
            to_write = response
        else:
            msg = 'Content not found in the response from generative AI.'
            to_write = msg
        return to_write


def main():
    architect = ArchitectVoicevox()
    architect.work()


if __name__ == '__main__':
    main()
