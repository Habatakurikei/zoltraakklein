import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from llmmaster import LLMMaster

from architect_common import ArchitectBase
from architect_common import CONTENT_ATTRIBUTES
from architect_common import CONTENT_TYPE_CODE
from architect_common import MODEL
from architect_common import PROVIDER
from architect_common import SOURCE_RD
from architect_common import TEMPERATURE
from architect_common import TEMPLATE
from config import EXT_TXT
from config import PATH_TO_PROMPT
from config import SYSTEM_DIR


class ArchitectWriter(ArchitectBase):
    '''
    要件定義書からプログラムコードまたは文章を生成するアーキテクト
    sys.argv[4]: 出力の種類
      code
      business_book
      image_prompt
      picture_book
      presentation_marp
      technical_book
      web_article
    '''
    def __init__(self):
        super().__init__()

        self.output_type = sys.argv[4]
        self.provider = CONTENT_ATTRIBUTES[self.output_type][PROVIDER]
        self.model = CONTENT_ATTRIBUTES[self.output_type][MODEL]
        self.temperature = CONTENT_ATTRIBUTES[self.output_type][TEMPERATURE]

    def work(self):
        '''
        手順：
          1. 要件定義書を読み込む（複数あっても一つだけ）
          2. 要件定義書から生成要求項目のリストを抽出
          3. リスト内の各生成要求項目に対して下記の動作を繰り返す
            3.1 プロンプト準備（生成タイプによってここが分岐）
            3.2 LLMMasterにセット
          4. LLMMasterでコード生成
          5. 生成したコードを保存
          6. メニューにコードファイルの保存先を記録
        '''
        super().work()

        master = LLMMaster()

        source = self._select_source(
            CONTENT_ATTRIBUTES[self.output_type][SOURCE_RD])

        markdown_content = Path(source).read_text(encoding='utf-8')
        files_list = self._list_code_lines(source)

        generated_files = {}

        for i, line in enumerate(files_list, 1):
            file_key = f"src_{i:02d}"
            file_name = self._cleanup_line(line)
            prompt = self._get_prompt(file_name, markdown_content)
            params = master.pack_parameters(provider=self.provider,
                                            model=self.model,
                                            prompt=prompt,
                                            temperature=self.temperature,
                                            max_tokens=4096)
            master.summon({file_key: params})

            if self.output_type == CONTENT_TYPE_CODE:
                generated_files[file_key] = file_name
            else:
                generated_files[file_key] = f'{file_key}{EXT_TXT}'

        master.run()

        new_menu_items = {}

        for key in generated_files.keys():
            if master.results[key]:
                save_as = self.output_dir / generated_files[key]
                save_as.parent.mkdir(parents=True, exist_ok=True)
                save_as.write_text(master.results[key], encoding='utf-8')
                new_menu_items[key] = str(save_as)
            else:
                msg = f'Failed to generate content for {generated_files[key]}.'
                new_menu_items[key] = msg

        self._add_menu_items(new_menu_items)
        master.dismiss()

    def _cleanup_line(self, line: str):
        '''
        要件定義書のファイル構成情報からファイル名または見出し情報のみ取り出す。
        特に先頭に'/'が付いているとルートフォルダに保存される恐れが
        あるため、そのような場合は除去する。
        例：
          file: /root/folder/file.py
          の場合は
          root/folder/file.py
          となる。
        '''
        return line[1:] if line.startswith('/') else line

    def _get_prompt(self, file_name: str, rd: str):
        '''
        コード生成プロンプトをここで整えて返す。
        file_name: 生成したいファイル名前（コード）または見出し（文章）
        rd: 読み込み済みの要件定義書の中身
        '''
        template = Path(SYSTEM_DIR) / PATH_TO_PROMPT
        template = template / CONTENT_ATTRIBUTES[self.output_type][TEMPLATE]
        base_prompt = template.read_text(encoding='utf-8')
        return base_prompt.format(file_name=file_name, rd=rd)


def main():
    architect = ArchitectWriter()
    architect.work()


if __name__ == '__main__':
    main()
