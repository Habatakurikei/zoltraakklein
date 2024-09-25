import shutil
import sys
from pathlib import Path
from string import Template

sys.path.append(str(Path(__file__).parent.parent))

from architect_common import ArchitectBase
from architect_common import CONTENT_ATTRIBUTES
from architect_common import CONTENT_TYPE_BUSINESS_BOOK
from architect_common import CONTENT_TYPE_PICTURE_BOOK
from architect_common import CONTENT_TYPE_MARP_PRESENTATION
from architect_common import CONTENT_TYPE_TECHNICAL_BOOK
from architect_common import SOURCE_RD
from architect_common import MARP_HEADER
from config import DEFAULT_IMAGE
from config import EXT_MARKDOWN
from config import EXT_PDF
from config import EXT_PNG
from config import EXT_PPTX
from config import MARP_BODY_TEMPLATE_BUSINESS_BOOK
from config import MARP_BODY_TEMPLATE_PICTURE_BOOK
from config import MARP_BODY_TEMPLATE_PRESENTATION
from config import MARP_BODY_TEMPLATE_TECHNICAL_BOOK
from config import PATH_TO_TEMPLATE
from config import SYSTEM_DIR


class ArchitectPresentationMarp(ArchitectBase):
    '''
    要件定義書とMarpコンテンツからプレゼン資料を生成するアーキテクト
    sys.argv[4]: 出力資料の種類
        business_book: ビジネス書／新書（文系本）
        technical_book: 科学／技術解説書（理系本）
        presentation_marp: プレゼンテーション資料
        script: 脚本書（未実装）
        literature: 小説（未実装）
        book_picture: 絵本
    sys.argv[5]: メニューから読み込む本文のパス一覧
    sys.argv[6]: メニューから読み込むカバー画像のパス
    sys.argv[7]: メニューから読み込む各ページ画像のパス一覧
    出力資料の種類によって本文、画像、見出しなど使用する素材が異なります。
    使用しない素材については `sys.argv` 引数に `dummy` を指定してください。
    【重要】
    MarpでMarkdownからPPTXとPDFを生成するために
    marp-cli を使用しています。事前にインストールしてください。
    https://github.com/marp-team/marp-cli
    '''
    def __init__(self):
        super().__init__()
        self.presentation_type = sys.argv[4]
        self.page_content = self._get_source_section(sys.argv[5])
        self.cover_image = self._get_source_section(sys.argv[6])
        self.page_image = self._get_source_section(sys.argv[7])

    def work(self):
        '''
        手順：
          1. 要件定義書の選択（一つのみ）
          2. 保存先情報の準備
          3. ヘッダーコンテンツの生成
          4. 各ページのコンテンツを結合
          5. ヘッダーと各ページが結合されたコンテンツをMarkdownとして保存
          6. MarkdownからPPTXとPDFを生成し保存
          7. Markdown、PPTX、PDFの各保存先をメニューに追記
        '''
        super().work()

        source = self._select_source(
            CONTENT_ATTRIBUTES[self.presentation_type][SOURCE_RD])
        cover_image = self._copy_cover_image()
        page_images = self._copy_page_images()
        total_pages = len(self.page_content) + 1

        full_content = self._merge_header(source, cover_image)
        full_content += self._merge_each_page(source, page_images)

        md_file = self.output_dir / f"{self.output_section}{EXT_MARKDOWN}"
        pdf_file = self.output_dir / f"{self.output_section}{EXT_PDF}"
        pptx_file = self.output_dir / f"{self.output_section}{EXT_PPTX}"

        md_file.write_text(full_content, encoding='utf-8')
        self._execute_marp(str(md_file), str(pdf_file))
        self._execute_marp(str(md_file), str(pptx_file))
        self._execute_marp(str(md_file), EXT_PNG)

        png_files = {}
        for i in range(total_pages):
            key_name = f"png_{i+1:03d}"
            png_name = f"{self.output_section}.{i+1:03d}{EXT_PNG}"
            png_files[key_name] = str(self.output_dir / png_name)

        new_menu_items = {
            "markdown": str(md_file),
            "pdf": str(pdf_file),
            "pptx": str(pptx_file)}
        new_menu_items.update(png_files)

        self._add_menu_items(new_menu_items)
        self._remove_images(cover_image, page_images)

    def _merge_header(self, source: str, cover_image: str):
        '''
        ヘッダーのテンプレートを読み込んでタイトルとカバー画像をセット
        source: 要件定義書のパス
        '''
        title = self._extract_title(source)

        header_template_path = SYSTEM_DIR / PATH_TO_TEMPLATE
        header_template_path /= \
            CONTENT_ATTRIBUTES[self.presentation_type][MARP_HEADER]

        marp_header = Template(
            header_template_path.read_text(encoding='utf-8'))

        header_content = marp_header.safe_substitute(
            title=title, cover_image_path=cover_image) + "\n\n"

        return header_content

    def _merge_each_page(self, source: str, page_images: list):
        '''
        各ページの見出し、本文、ページ画像を読み込む
        source: 要件定義書のパス
        【重要】
        出力資料の種類によって置き換える情報が異なります。
        '''
        full_body_content = ""
        body_template_path = SYSTEM_DIR / PATH_TO_TEMPLATE

        if (self.presentation_type == CONTENT_TYPE_BUSINESS_BOOK or
           self.presentation_type == CONTENT_TYPE_TECHNICAL_BOOK):

            if self.presentation_type == CONTENT_TYPE_BUSINESS_BOOK:
                body_template_path /= MARP_BODY_TEMPLATE_BUSINESS_BOOK
            else:
                body_template_path /= MARP_BODY_TEMPLATE_TECHNICAL_BOOK

            page_headers = self._load_page_headers(source)
            page_content = self._load_page_content()
            for headline, content in zip(page_headers, page_content):
                formatted_content = self._format_content(headline, content)
                body_template = Template(
                    body_template_path.read_text(encoding='utf-8'))
                full_body_content += body_template.safe_substitute(
                    headline=headline, content=formatted_content) + "\n\n"

        elif self.presentation_type == CONTENT_TYPE_PICTURE_BOOK:
            body_template_path /= MARP_BODY_TEMPLATE_PICTURE_BOOK
            page_content = self._load_page_content()
            for i in range(len(page_content)):
                body_template = Template(
                    body_template_path.read_text(encoding='utf-8'))
                full_body_content += body_template.safe_substitute(
                    page_image_path=page_images[i],
                    content=page_content[i]) + "\n\n"

        elif self.presentation_type == CONTENT_TYPE_MARP_PRESENTATION:
            body_template_path /= MARP_BODY_TEMPLATE_PRESENTATION
            page_content = []
            for entry in self.page_content.values():
                text = self._list_bracketed_content(entry)
                page_content.append(text[0][1])
            for entry in page_content:
                body_template = Template(
                    body_template_path.read_text(encoding='utf-8'))
                full_body_content += body_template.safe_substitute(
                    content=entry) + "\n\n"

        else:
            msg = f"Invalid presentation type: {self.presentation_type}"
            raise ValueError(msg)

        return full_body_content

    def _copy_cover_image(self):
        '''
        カバー画像をMarpに取り込むための処理
        手順：
          1. メニュー内の項目 (rd_image) からカバー画像のパスを取得
            強制的にひとつだけ採用
          2. カバー画像のファイル名を取得
          3. カバー画像をプレゼンテーション生成先フォルダにコピー
          4. カバー画像のファイル名を返す、表紙背景画像のリンク情報として必要
        ただしカバー画像が存在しない場合はシステムで用意した画像のパスを返す
        '''
        cover_name = ''
        source_rd = CONTENT_ATTRIBUTES[self.presentation_type][SOURCE_RD]
        cover_origin = next((Path(value) for key, value in
                             self.cover_image.items() if source_rd in key),
                            Path(next(iter(self.cover_image.values()))))
        if not cover_origin.is_file():
            cover_origin = SYSTEM_DIR / PATH_TO_TEMPLATE / DEFAULT_IMAGE
        cover_name = cover_origin.name
        shutil.copy2(cover_origin, self.output_dir / cover_name)
        return cover_name

    def _copy_page_images(self):
        '''
        各ページの画像を読み込む
        注意：
          パスがhttpから始まる場合はネット画像なのでパスをそのまま使用、
          ローカルファイルの場合はコピーして相対パスを指定、
          ただしパスにファイルが存在しなければシステムで用意したデフォルト画像を使用
        '''
        default_image = Path(SYSTEM_DIR / PATH_TO_TEMPLATE / DEFAULT_IMAGE)
        page_images = []
        for value in self.page_image.values():
            if value.startswith('http'):
                page_images.append(value)
            elif not Path(value).is_file():
                image_name = default_image.name
                shutil.copy2(default_image, self.output_dir / image_name)
                page_images.append(image_name)
            else:
                image_name = Path(value).name
                shutil.copy2(value, self.output_dir / image_name)
                page_images.append(image_name)
        return page_images

    def _load_page_headers(self, source: str):
        '''
        各ページのヘッダーを読み込む
        '''
        return self._list_code_lines(source)

    def _load_page_content(self):
        '''
        各ページの本文を読み込む
        '''
        page_body = []
        for value in self.page_content.values():
            page_body.append(Path(value).read_text(encoding='utf-8'))
        return page_body

    def _format_content(self, headlines: list, content: str):
        '''
        本文ページ作成のサポート：本文を整形
        '''
        result = ''
        for line in content.split('\n'):
            if line in headlines:
                continue
            elif line:
                result += f'{line}\n\n'
        return result

    def _execute_marp(self, md_file: str, output_path: str):
        '''
        MarpでMarkdownからPPTXとPDFを生成する
        md_file: 保存済みのMarp-Markdownファイルのパス
        output_path: 出力先ファイルのパス
        '''
        if EXT_PDF in output_path:
            options = ["-o", output_path, "--pdf"]
        elif EXT_PPTX in output_path:
            options = ["-o", output_path, "--pptx"]
        elif EXT_PNG in output_path:
            options = ["--images", "png"]
        else:
            raise ValueError(f"Invalid output file extension: {output_path}")

        command = ["marp", md_file, "--allow-local-files"] + options
        self._call_external_command(command)

    def _remove_images(self, cover_image: str, page_images: list):
        '''
        作業用でコピーしたカバー画像と各ページ画像を削除する
        '''
        for image in page_images + [cover_image]:
            img_path = self.output_dir / image
            if img_path.exists():
                img_path.unlink()


def main():
    architect = ArchitectPresentationMarp()
    architect.work()


if __name__ == '__main__':
    main()
