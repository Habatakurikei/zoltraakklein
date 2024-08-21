import shutil
import sys
import uuid
from pathlib import Path
from string import Template

sys.path.append(str(Path(__file__).parent.parent))

from architect_common import ArchitectBase
from architect_common import CONTENT_ATTRIBUTES
from architect_common import EPUB_AUTO_PATH
from architect_common import EPUB_BODY_PATH
from architect_common import EPUB_COLO_PATH
from architect_common import EPUB_COVER_PATH
from architect_common import EPUB_IMAGE_PATH
from architect_common import EPUB_NAV_PATH
from architect_common import EPUB_NCX_PATH
from architect_common import EPUB_OPF_PATH
from architect_common import SOURCE_RD
from architect_common import EPUB_TEMPLATES
from architect_common import EPUB_TEMPLATE_MIME_TYPE
from architect_common import EPUB_TEXT_PATH
from architect_common import EPUB_TITLE_PATH
from architect_common import EPUB_TOC_PATH
from architect_common import EPUB_WORK_PATH
from architect_common import VORH
from config import DEFAULT_IMAGE
from config import EXT_EPUB
from config import EXT_XHTML
from config import EXT_ZIP
from config import PATH_TO_TEMPLATE
from config import SYSTEM_DIR


class ArchitectEPUB(ArchitectBase):
    '''
    要件定義書からEPUB形式の電子書籍を生成するアーキテクト
    sys.argv[4]: 出力資料の種類
        picture_book: 写真集`
    sys.argv[5]: メニューから読み込む本文のパス一覧
    sys.argv[6]: メニューから読み込むカバー画像のパス
    sys.argv[7]: メニューから読み込む各ページ画像のパス一覧
    '''
    def __init__(self):
        super().__init__()
        self.book_type = sys.argv[4]
        self.page_body = self._get_source_section(sys.argv[5])
        self.cover_image = self._get_source_section(sys.argv[6])
        self.page_image = self._get_source_section(sys.argv[7])

        self.work_dir = self.project_path / EPUB_WORK_PATH

    def work(self):
        '''
        手順：
          1. 要件定義書の選択（一つのみ）
          2. 保存先情報の準備
          3. UUIDコードを生成
          4. 各EPUB形式ファイルを整形
          5. EPUBファイルとしてZIP化、保存
          6. EPUBファイルの保存先をメニューに追記
          7. 作業ファイル一式を削除
        '''
        super().work()

        source = self._select_source(
            CONTENT_ATTRIBUTES[self.book_type][SOURCE_RD])

        save_as = self.output_dir / f'{self.output_section}'

        uuid_code = uuid.uuid4()

        self._copy_epub_templates()

        title = self._extract_title(source)
        headlines = self._list_code_lines(source)
        cover_image = self._set_cover_image()
        content = self._load_page_content()
        vorh = CONTENT_ATTRIBUTES[self.book_type][VORH]

        self._set_simple_pages(title, vorh)
        self._set_cover_page(title, vorh, cover_image)
        file_list = self._set_body_pages(title, vorh, headlines, content)
        self._set_toc_page(title, vorh, headlines, file_list)
        self._set_navigation(title, headlines, file_list)

        self._set_opf(title, uuid_code, cover_image, file_list)
        self._set_ncx(title, uuid_code)

        self._pack_epub(save_as)

        new_menu_items = {"epub": str(save_as) + EXT_EPUB}
        self._add_menu_items(new_menu_items)

        self._remove_epub_templates()

    def _copy_epub_templates(self):
        '''
        EPUB形式テンプレートのフォルダとファイル一式を
        作業ファイルとして出力フォルダにコピー
        '''
        source_path = SYSTEM_DIR / PATH_TO_TEMPLATE / self.output_section
        for entry in EPUB_TEMPLATES:
            copy_from = source_path / entry
            copy_to = self.work_dir / entry
            shutil.copytree(copy_from, copy_to, dirs_exist_ok=True)
        shutil.copy2(source_path / EPUB_TEMPLATE_MIME_TYPE,
                     self.work_dir / EPUB_TEMPLATE_MIME_TYPE)

    def _remove_epub_templates(self):
        '''
        EPUB生成後、作業ファイル一式を削除
        '''
        shutil.rmtree(self.work_dir)

    def _set_cover_image(self):
        '''
        カバー画像をEPUBに取り込むための処理
        手順：
          1. メニュー内の項目 (rd_image) からカバー画像のパスを取得
            強制的にひとつだけ採用
          2. カバー画像のファイル名を取得
          3. カバー画像をEPUB生成先フォルダにコピー
          4. カバー画像のファイル名を返す、表紙のリンク情報として必要
        ただしカバー画像が存在しない場合はシステムで用意した画像のパスを返す
        '''
        cover_name = ''
        source_rd = CONTENT_ATTRIBUTES[self.book_type][SOURCE_RD]
        cover_origin = next((Path(value) for key, value in
                             self.cover_image.items() if source_rd in key),
                            Path(next(iter(self.cover_image.values()))))
        if not cover_origin.is_file():
            cover_origin = SYSTEM_DIR / PATH_TO_TEMPLATE / DEFAULT_IMAGE
        cover_name = cover_origin.name
        shutil.copy(cover_origin,
                    self.work_dir / EPUB_IMAGE_PATH / cover_name)
        return cover_name

    def _load_page_content(self):
        '''
        各ページの本文を読み込む
        '''
        page_body = []
        for value in self.page_body.values():
            page_body.append(Path(value).read_text(encoding='utf-8'))
        return page_body

    def _set_simple_pages(self, title: str, vorh: str):
        '''
        タイトル・著者紹介・奥付ページを作成
        '''
        file_list = [self.work_dir / EPUB_TITLE_PATH,
                     self.work_dir / EPUB_AUTO_PATH,
                     self.work_dir / EPUB_COLO_PATH]
        for file in file_list:
            page = Template(file.read_text(encoding='utf-8'))
            page = page.safe_substitute(title=title, vorh=vorh)
            file.write_text(page, encoding='utf-8')

    def _set_cover_page(self, title: str, vorh: str, cover_image: str):
        '''
        カバーページを作成
        '''
        file = self.work_dir / EPUB_COVER_PATH
        page = Template(file.read_text(encoding='utf-8'))
        page = page.safe_substitute(title=title,
                                    vorh=vorh,
                                    cover_image=cover_image)
        file.write_text(page, encoding='utf-8')

    def _set_body_pages(self,
                        title: str,
                        vorh: str,
                        headlines: list,
                        contents: list):
        '''
        本文ページを作成
        作成されたページのリストを返して目次生成に活用する
        '''
        file_list = []
        template = self.work_dir / EPUB_BODY_PATH
        for i, (headline, content) in enumerate(zip(headlines, contents)):
            save_as = f'chapter-{i:02d}{EXT_XHTML}'
            formatted_content = self._format_content(headlines, content)
            page = Template(template.read_text(encoding='utf-8'))
            page = page.safe_substitute(title=title,
                                        vorh=vorh,
                                        headline=headline,
                                        content=formatted_content)
            file = self.work_dir / EPUB_TEXT_PATH / save_as
            file.write_text(page, encoding='utf-8')
            file_list.append(save_as)
        return file_list

    def _set_toc_page(self,
                      title: str,
                      vorh: str,
                      headlines: list,
                      file_list: list):
        '''
        目次ページを作成
        '''
        file = self.work_dir / EPUB_TOC_PATH
        line = Template('<p><a href="../Text/$file">$headline</a></p>\n')
        formatted_lines = [line.safe_substitute(file=file, headline=headline)
                           for file, headline in zip(file_list, headlines)]
        page = Template(file.read_text(encoding='utf-8'))
        page = page.safe_substitute(title=title,
                                    vorh=vorh,
                                    content=''.join(formatted_lines))
        file.write_text(page, encoding='utf-8')

    def _set_navigation(self, title: str, headlines: list, file_list: list):
        '''
        ナビゲーションページを作成
        '''
        file = self.work_dir / EPUB_NAV_PATH
        line = Template('<li><a href="../Text/$file">$headline</a></li>\n')
        formatted_lines = [line.safe_substitute(file=file, headline=headline)
                           for file, headline in zip(file_list, headlines)]
        page = Template(file.read_text(encoding='utf-8'))
        page = page.safe_substitute(title=title,
                                    content=''.join(formatted_lines))
        file.write_text(page, encoding='utf-8')

    def _set_opf(self,
                 title: str,
                 uuid_code: str,
                 cover_image: str,
                 file_list: list):
        '''
        OPFファイルを作成
        '''
        file = self.work_dir / EPUB_OPF_PATH

        cover_image = self._get_opf_image(cover_image)
        content_manifest = self._get_opf_content_manifest(file_list)
        content_spine = self._get_opf_content_spine(file_list)

        page = Template(file.read_text(encoding='utf-8'))
        page = page.safe_substitute(title=title,
                                    uuid_code=uuid_code,
                                    cover_image=cover_image,
                                    content_manifest=content_manifest,
                                    content_spine=content_spine)
        file.write_text(page, encoding='utf-8')

    def _set_ncx(self, title: str, uuid_code: str):
        '''
        NCXファイルを作成
        '''
        file = self.work_dir / EPUB_NCX_PATH
        page = Template(file.read_text(encoding='utf-8'))
        page = page.safe_substitute(title=title, uuid_code=uuid_code)
        file.write_text(page, encoding='utf-8')

    def _format_content(self, headlines: list, content: str):
        '''
        本文ページ作成のサポート：本文を整形
        '''
        result = ''
        for line in content.split('\n'):
            if line in headlines:
                continue
            elif line:
                result += f'<p>{line}</p>\n'
        return result

    def _get_opf_image(self, cover_image: str):
        '''
        OPFファイル作成のサポート：カバー画像のリンク情報を返す
        '''
        suffix = cover_image.split('.')[-1]
        href = f'href="Images/{cover_image}"'
        id = f'id="{cover_image}"'
        media_type = f'media-type="image/{suffix}"'
        return f'<item {href} {id} {media_type} />'

    def _get_opf_content_manifest(self, file_list: list):
        '''
        OPFファイル作成のサポート：コンテンツマニフェストを返す
        '''
        result = ''
        for file in file_list:
            result += f'<item href="Text/{file}" id="{file}" '
            result += 'media-type="application/xhtml+xml" />\n'
        return result

    def _get_opf_content_spine(self, file_list: list):
        '''
        OPFファイル作成のサポート：コンテンツスピナーを返す
        '''
        result = ''
        for file in file_list:
            result += f'<itemref idref="{file}" linear="yes" '
            result += 'properties="rendition:page-spread-right" />\n'
        return result

    def _pack_epub(self, save_as: Path):
        '''
        EPUBファイルをZIP化して保存
        '''
        shutil.make_archive(save_as,
                            format=EXT_ZIP[1:],
                            root_dir=self.work_dir)
        current_file = Path(str(save_as)+EXT_ZIP)
        new_file = current_file.with_suffix(EXT_EPUB)
        current_file.rename(new_file)


def main():
    architect = ArchitectEPUB()
    architect.work()


if __name__ == '__main__':
    main()
