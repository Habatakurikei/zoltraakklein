import os
import re
import sys
import time
from subprocess import DEVNULL
from subprocess import Popen
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config import EXT_YAML
from config import MARP_HEADER_TEMPLATE_BUSINESS_BOOK
from config import MARP_HEADER_TEMPLATE_PICTURE_BOOK
from config import MARP_HEADER_TEMPLATE_PRESENTATION
from config import MARP_HEADER_TEMPLATE_TECHNICAL_BOOK
from config import OS_WINDOWS
from config import PROMPT_FOR_BUSINESS_BOOK
from config import PROMPT_FOR_CODE
from config import PROMPT_FOR_IMAGE_PROMPT
from config import PROMPT_FOR_LITERATURE
from config import PROMPT_FOR_MARP
from config import PROMPT_FOR_PICTURE_BOOK
from config import PROMPT_FOR_SCRIPT
from config import PROMPT_FOR_TECHNICAL_BOOK
from config import PROMPT_FOR_VIRTUAL_CHARACTER
from config import PROMPT_FOR_WEB_ARTICLE
from config import WAIT_FOR_POLLING_PROCESS
from yaml_manager import YAMLManager


'''
アーキテクトリスト
'''
ARCHITECT_3D_MESHY = '3d_meshy'
ARCHITECT_EPUB = 'epub'
ARCHITECT_EPUB_PICTURE = 'epub_picture'
ARCHITECT_IMAGE_DALLE = 'image_dalle'
ARCHITECT_IMAGE_STABLE_DIFFUSION = 'image_stable_diffusion'
ARCHITECT_MARP_PRESENTATION = 'marp_presentation'
ARCHITECT_MARP_SCRIPT = 'marp_script'
ARCHITECT_MERMAID_CHART = 'mermaid_chart'
ARCHITECT_PIKAPIKAPIKA = 'video_pikapikapika'
ARCHITECT_VIRTUAL_CHARACTER = 'virtual_character'
ARCHITECT_VOICE_ELEVENLABS = 'voice_elevenlabs'
ARCHITECT_VOICE_VOICEVOX = 'voice_voicevox'
ARCHITECT_WRITER = 'writer'


'''
LLM共通設定
'''
ANTHROPIC = 'anthropic'
GOOGLE = 'google'
OPENAI = 'openai'
ANTHROPIC_MODEL = 'claude-3-5-sonnet-20240620'
GOOGLE_MODEL = 'gemini-1.5-pro'
OPENAI_MODEL = 'gpt-4o-2024-08-06'

MODEL = 'model'
PROVIDER = 'provider'


'''
要件定義書関連設定
'''
RD_CHARACTER_KEYWORD = '登場キャラクター'
RD_IMAGE_KEYWORD = '画像生成向けプロンプト'
RD_MESHY_3D_KEYWORD = '画像生成向けプロンプト'
RD_PIKAPIKAPIKA_KEYWORD = '画像生成向けプロンプト'
RD_VOICE_KEYWORD = 'キャラクター設定を反映したセリフ'

RD_LINE_FOR_CODE = ['file', 'headline']


'''
生成物別の詳細設定
  1. 文章生成AIプロバイダー
  2. 文章生成AIモデル
  3. 要件定義書ソース
  4. プロンプトテンプレート
  5. Marpヘッダー
  6. 縦書き／横書き指定
'''
VERTICAL_WRITING = 'vrtl'
HORIZONTAL_WRITING = 'hltr'
MARP_HEADER = 'marp_header'
SOURCE_RD = 'source_rd'
TEMPERATURE = 'temperature'
TEMPLATE = 'template'
VORH = 'vorh'

CONTENT_TYPE_BUSINESS_BOOK = 'business_book'
CONTENT_TYPE_CODE = 'code'
CONTENT_TYPE_IMAGE_PROMPT = 'image_prompt'
CONTENT_TYPE_LITERATURE = 'literature'
CONTENT_TYPE_MARP_PRESENTATION = 'presentation_marp'
CONTENT_TYPE_PICTURE_BOOK = 'picture_book'
CONTENT_TYPE_SCRIPT = 'script'
CONTENT_TYPE_TECHNICAL_BOOK = 'technical_book'
CONTENT_TYPE_VIRTUAL_CHARACTER = 'virtual_character'
CONTENT_TYPE_WEB_ARTICLE = 'web_article'

CONTENT_ATTRIBUTES = {
    CONTENT_TYPE_BUSINESS_BOOK: {
        PROVIDER: OPENAI,
        MODEL: OPENAI_MODEL,
        TEMPERATURE: 0.7,
        SOURCE_RD: OPENAI,
        TEMPLATE: PROMPT_FOR_BUSINESS_BOOK,
        MARP_HEADER: MARP_HEADER_TEMPLATE_BUSINESS_BOOK,
        VORH: VERTICAL_WRITING
    },
    CONTENT_TYPE_CODE: {
        PROVIDER: ANTHROPIC,
        MODEL: ANTHROPIC_MODEL,
        TEMPERATURE: 0.2,
        SOURCE_RD: ANTHROPIC,
        TEMPLATE: PROMPT_FOR_CODE,
        VORH: HORIZONTAL_WRITING
    },
    CONTENT_TYPE_IMAGE_PROMPT: {
        PROVIDER: OPENAI,
        MODEL: OPENAI_MODEL,
        TEMPERATURE: 0.7,
        SOURCE_RD: OPENAI,
        TEMPLATE: PROMPT_FOR_IMAGE_PROMPT,
        VORH: HORIZONTAL_WRITING
    },
    CONTENT_TYPE_LITERATURE: {
        PROVIDER: OPENAI,
        MODEL: OPENAI_MODEL,
        TEMPERATURE: 0.7,
        SOURCE_RD: OPENAI,
        TEMPLATE: PROMPT_FOR_LITERATURE,
        VORH: VERTICAL_WRITING
    },
    CONTENT_TYPE_MARP_PRESENTATION: {
        PROVIDER: ANTHROPIC,
        MODEL: ANTHROPIC_MODEL,
        TEMPERATURE: 0.2,
        SOURCE_RD: ANTHROPIC,
        TEMPLATE: PROMPT_FOR_MARP,
        MARP_HEADER: MARP_HEADER_TEMPLATE_PRESENTATION,
        VORH: HORIZONTAL_WRITING
    },
    CONTENT_TYPE_PICTURE_BOOK: {
        PROVIDER: OPENAI,
        MODEL: OPENAI_MODEL,
        TEMPERATURE: 0.7,
        SOURCE_RD: OPENAI,
        TEMPLATE: PROMPT_FOR_PICTURE_BOOK,
        MARP_HEADER: MARP_HEADER_TEMPLATE_PICTURE_BOOK,
        VORH: HORIZONTAL_WRITING
    },
    CONTENT_TYPE_SCRIPT: {
        PROVIDER: ANTHROPIC,
        MODEL: ANTHROPIC_MODEL,
        TEMPERATURE: 0.7,
        SOURCE_RD: ANTHROPIC,
        TEMPLATE: PROMPT_FOR_SCRIPT,
        VORH: VERTICAL_WRITING
    },
    CONTENT_TYPE_TECHNICAL_BOOK: {
        PROVIDER: ANTHROPIC,
        MODEL: ANTHROPIC_MODEL,
        TEMPERATURE: 0.2,
        SOURCE_RD: ANTHROPIC,
        TEMPLATE: PROMPT_FOR_TECHNICAL_BOOK,
        MARP_HEADER: MARP_HEADER_TEMPLATE_TECHNICAL_BOOK,
        VORH: HORIZONTAL_WRITING
    },
    CONTENT_TYPE_VIRTUAL_CHARACTER: {
        PROVIDER: OPENAI,
        MODEL: OPENAI_MODEL,
        TEMPERATURE: 0.7,
        SOURCE_RD: OPENAI,
        TEMPLATE: PROMPT_FOR_VIRTUAL_CHARACTER,
        VORH: HORIZONTAL_WRITING
    },
    CONTENT_TYPE_WEB_ARTICLE: {
        PROVIDER: ANTHROPIC,
        MODEL: ANTHROPIC_MODEL,
        TEMPERATURE: 0.7,
        SOURCE_RD: ANTHROPIC,
        TEMPLATE: PROMPT_FOR_WEB_ARTICLE,
        VORH: HORIZONTAL_WRITING
    },
}


'''
EPUB 生成設定
'''
EPUB_TEMPLATES = ['META-INF', 'OEBPS']
EPUB_TEMPLATE_MIME_TYPE = 'mimetype'

EPUB_WORK_PATH = 'epub_work'

EPUB_OEBPS_PATH = Path('OEBPS')
EPUB_IMAGE_PATH = EPUB_OEBPS_PATH / 'Images'
EPUB_TEXT_PATH = EPUB_OEBPS_PATH / 'Text'

EPUB_OPF_PATH = EPUB_OEBPS_PATH / 'content.opf'
EPUB_NCX_PATH = EPUB_OEBPS_PATH / 'toc.ncx'

EPUB_TITLE_PATH = EPUB_TEXT_PATH / 'title.xhtml'
EPUB_COVER_PATH = EPUB_TEXT_PATH / 'cover.xhtml'
EPUB_TOC_PATH = EPUB_TEXT_PATH / 'toc.xhtml'
EPUB_NAV_PATH = EPUB_TEXT_PATH / 'navigation.xhtml'
EPUB_BODY_PATH = EPUB_TEXT_PATH / 'body.xhtml'
EPUB_AUTO_PATH = EPUB_TEXT_PATH / 'about-author.xhtml'
EPUB_COLO_PATH = EPUB_TEXT_PATH / 'colophon.xhtml'


'''
画像生成設定
'''
GEN_IMAGE_NEGATIVE_PROMPT = 'ugly, low-quality, low-resolution'


'''
ElevenLabs音声ID設定 (2024-08-04)
  Female: Charlotte
  Male: Callum
  Neutral: Charlie
'''
GEN_ELEVENLABS_FEMALE_VOICE_ID = 'XB0fDUnXU5powFXDhCwa'
GEN_ELEVENLABS_MALE_VOICE_ID = 'N2lVS1w4EtoT3dr4eOWO'
GEN_ELEVENLABS_NEUTRAL_VOICE_ID = 'IKne3meq5aSn9XLyUdCD'
GEN_ELEVENLABS_VOICE_PROVIDER = 'elevenlabs_tts'


'''
Voicevox 設定
'''
GEN_VOICEVOX_DEFAULT_SPEAKER = 1
GEN_VOICEVOX_VOICE_PROVIDER = 'voicevox_tts'
GEN_VOICEVOX_INTERVAL = 2.5
GEN_VOICEVOX_MAX_LINES = 1000
VOICEVOX_CHARACTER_LIMIT = 300
VOICEVOX_PREFIX = 'voicevox_'


'''
Meshy 3Dモデル設定
'''
GEN_MESHY_3D_ADDITIONAL_PROMPT =\
    ', full-body, japanese-anime-style'
GEN_MESHY_3D_NEGATIVE_PROMPT = 'ugly, low resolution'
GEN_MESHY_3D_PROVIDER = 'meshy_tt3d'
GEN_MESHY_3D_STYLE = 'cartoon'
REFINE_MESHY_3D_PROVIDER = 'meshy_tt3d_refine'


'''
Pikapikapika 動画生成設定
'''
GEN_PIKAPIKAPIKA_DEFAULT_STYLE = 'Anime'
GEN_PIKAPIKAPIKA_PARAMS = {
    "guidanceScale": 25,
    "motion": 4,
    "negativePrompt": "ugly, low-quality, low-resolution"
}
GEN_PIKAPIKAPIKA_PROVIDER = 'pikapikapika_ttv'
GEN_PIKAPIKAPIKA_SOURCE_RD = OPENAI


'''
プレゼン動画生成設定
'''
COVER_DISPLAY_TIME = 3


class ArchitectBase:
    '''
    アーキテクトの基底クラス
    【共通引数】
    sys.argv[0]: 呼ばれたスクリプトファイル名
    sys.argv[1]: プロジェクトのパス
    sys.argv[2]: メニューに記載する保存先の新規セクション名(e.g. mermaid)
    sys.argv[3:]: 各アーキテクト固有の引数を位置引数で受け取る
    【共通メンバー】
    self.args: コマンドライン引数の総数
    self.architect: アーキテクトの名前（呼ばれたプログラム名）
    self.project_path: プロジェクトのパス
    self.output_section: メニューに記載する保存先の新規セクション名
    self.output_dir: アーキテクトが生成したファイルの保存先ディレクトリ
    self.source_section: メニューから入力として読み込むセクション名
    self.source: メニューから読み込まれた要件定義書または入力ファイルの辞書型リスト
    '''
    def __init__(self):

        self.args = len(sys.argv)
        if self.args < 4:
            msg = f'アーキテクトへの引数が足りません: {self.args-1}, '
            msg += '最低3以上必要です。'
            raise ValueError(msg)

        self.architect = Path(sys.argv[0]).stem

        self.project_path = Path(sys.argv[1])

        self.output_section = sys.argv[2]
        self.output_dir = self.project_path / self.output_section
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.source_section = sys.argv[3]
        self.source = self._get_source_section(self.source_section)
        if not self.source:
            msg = 'List of files to process is not found in the menu. '
            msg += f'Section: {self.source_section}'
            self._add_menu_items({'error': msg})
            raise ValueError(msg)

    def work(self):
        '''
        メインの処理は各派生クラスで実装する
        '''
        pass

    def _get_source_section(self, source_section: str):
        '''
        メニューから入力として読み込むセクション名を受け取り、
        そのセクションの内容を `YAMLManager` オブジェクトとして返す
        主に要件定義書の一覧を取得するために使用する
        '''
        menu = self._menu_from_project_path()
        return menu.get_section(source_section)

    def _select_source(self, keyword: str):
        '''
        複数のソースがある場合に指定されたキーワード `keyword` を含む
        要件定義書ソースを返すない場合はリストの最初の項目を返す
        主に複数の要件定義書からどれかひとつだけを選択するために使用する
        （領域展開で大量のコンテンツ生成を防ぐため）
        '''
        if self.source is None:
            raise ValueError('ソースが読み込まれていません')

        buff = next((file for file in self.source if keyword in file), None)
        if buff:
            to_load = self.source[buff]
        else:
            to_load = next(iter(self.source.values()))
        return to_load

    def _menu_from_project_path(self):
        '''
        プロジェクトパスからメニューの内容をすべて読み込んでオブジェクトで返す
        '''
        file_base = self.project_path.name
        to_load = self.project_path / f"{file_base}{EXT_YAML}"
        return YAMLManager(str(to_load))

    def _add_menu_items(self, items: dict):
        '''
        生成物の保存先情報をメニューに追記する
        '''
        menu = self._menu_from_project_path()
        menu.new_section(self.output_section)

        for key, value in items.items():
            menu.set_item(self.output_section, key, str(value))

        menu.save()

    def _extract_title(self, source: str):
        '''
        要件定義書からタイトルを抽出する
        引数：
          source: 要件定義書のパス
        '''
        title = 'タイトルが見つかりませんでした'

        lines = Path(source).read_text(encoding='utf-8').splitlines()

        i = 0
        while i < len(lines):
            if (lines[i].startswith('#') and 'タイトル' not in lines[i] and
               'たいとる' not in lines[i]):
                title = re.sub(r'^[^\w]+', '', lines[i]).strip()
                break
            elif 'タイトル' in lines[i] or 'たいとる' in lines[i]:
                title = re.sub(r'^[^\w]+', '', lines[i+1]).strip()
                break
            i += 1

        return title

    def _list_bracketed_content(self, source: str):
        '''
        要件定義書内にあるブラケットで囲まれたコードを抽出して返す
        ブラケットに囲まれた箇所を全て拾うので要件定義書内に複数箇所あれば全部返す
        引数：
          source: 要件定義書のパス
        戻り値：
          該当するコンテンツをリストで返す
          リスト内の要素はタプル (header, content)
        '''
        markdown_content = Path(source).read_text(encoding='utf-8')
        pattern = r'^\s*```(\w+)\n(.*?)\n\s*```'
        matches = re.findall(pattern,
                             markdown_content,
                             re.DOTALL | re.MULTILINE)
        return matches

    def _find_image_prompt(self, source: str, keyword: str):
        '''
        要件定義書から画像生成プロンプトを抽出する
        手順：
          1. 要件定義書 `source` を読み込む
          2. 要件定義書を逆から追って画像生成プロンプトの行を見つける
             その際、正規表現で不要なスペースや記号を除去してプロンプトを見つける
          3. 見つけた画像生成プロンプトを返す
        補足：逆から読み込んで指定のキーワード `keyword` の行に到達した場合
              プロンプトは見つからなかったと判断する
        '''
        ans = ''

        markdown = Path(source).read_text(encoding='utf-8').splitlines()

        for entry in reversed(markdown):
            line = entry.strip()
            line = re.sub(r'[^\w\s,]', '', line)
            line = re.sub(r'^\s*(?=[a-zA-Z0-9])', '', line)

            if keyword in line:
                break
            elif re.match(r'^[a-zA-Z0-9]', line):
                ans = line
                break

        return ans

    def _list_code_lines(self, source: str):
        '''
        要件定義書`source`からコードまたは見出しの行を抽出してリストとして返す
        '''
        entries = []

        document = Path(source).read_text(encoding='utf-8').splitlines()

        for line in document:
            items = line.strip().split(':')
            if items[0] in RD_LINE_FOR_CODE:
                entries.append(re.sub(r'^\s+', '', items[1]))

        return entries

    def _save_bytes(self, data: bytes, file_name: str):
        '''
        主に外部URLから取得してきたバイナリデータ(画像/3D)をファイルに保存
        メニュー記録用に保存先ファイルパス情報を返す
        '''
        save_as = self.output_dir / file_name
        save_as.write_bytes(data)
        return str(save_as)

    def _call_external_command(self, command: list[str]):
        '''
        外部コマンドを呼び出してコンテンツ生成する
        Mermaid-CLI, Marp-CLI など
        '''
        if OS_WINDOWS in os.name:
            pid = Popen(command, shell=True, stdout=DEVNULL, stderr=DEVNULL)
        else:
            pid = Popen(command,
                        shell=False,
                        start_new_session=False,
                        stdout=DEVNULL,
                        stderr=DEVNULL)
        while pid.poll() is None:
            time.sleep(WAIT_FOR_POLLING_PROCESS)
