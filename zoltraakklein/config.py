import sys
from pathlib import Path


# システムのPythonコマンド
PYTHON_COMMAND = sys.executable

# OSタイプ
OS_WINDOWS = "nt"
OS_LINUX = "posix"
OS_MACOS = "posix"

# デフォルト言語モデルとパラメータ
DEFAULT_PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o"

# 各種パス設定
SYSTEM_DIR = Path(__file__).parent.resolve()

PATH_TO_ARCHITECT = "architect"
PATH_TO_COMPILER = "compilers"
PATH_TO_INSTRUCTION = "instructions"
PATH_TO_OUTPUT = "projects"
PATH_TO_PROMPT = "prompts"
PATH_TO_TEMPLATE = "templates"

# 各種ファイルの指定
EXT_EPUB = ".epub"
EXT_MARKDOWN = ".md"
EXT_MP3 = ".mp3"
EXT_MP4 = ".mp4"
EXT_PDF = ".pdf"
EXT_PLAINTEXT = ".txt"
EXT_PNG = ".png"
EXT_PPTX = ".pptx"
EXT_PYTHON = ".py"
EXT_TXT = ".txt"
EXT_WAV = ".wav"
EXT_XHTML = ".xhtml"
EXT_YAML = ".yaml"
EXT_ZIP = ".zip"

DEFAULT_IMAGE = "zk_image.jpg"

FORMATTER = "md_comment.md"

MENU_FORMAT = ".yaml"
MENU_TEMPLATE = "menu_template.yaml"

PROMPT_FOR_CODE = "code_generation_prompt.md"
PROMPT_FOR_BUSINESS_BOOK = "text_generation_prompt.md"
PROMPT_FOR_IMAGE_PROMPT = "image_description_generation_prompt.md"
PROMPT_FOR_IMAGE_SEARCH = "image_search_prompt.md"
PROMPT_FOR_LITERATURE = "text_generation_prompt.md"
PROMPT_FOR_MARP = "marp_generation_prompt_code.md"
PROMPT_FOR_NAME = "name_for_requirement_prompt.md"
PROMPT_FOR_PICTURE_BOOK = "book_picture_generation_prompt.md"
PROMPT_FOR_TECHNICAL_BOOK = "text_generation_prompt.md"
PROMPT_FOR_SPEECH = "speech_generation_prompt.md"
PROMPT_FOR_SCRIPT = "script_conversion_prompt.md"
PROMPT_FOR_VIRTUAL_CHARACTER = "virtual_character_generation_prompt.md"
PROMPT_FOR_WEB_ARTICLE = "web_article_generation_prompt.md"

MARP_BODY_TEMPLATE_GENERAL = "marp_body_template_general.md"
MARP_BODY_TEMPLATE_BUSINESS_BOOK = "marp_body_template_general.md"
MARP_BODY_TEMPLATE_PICTURE_BOOK = "marp_body_template_picture_book.md"
MARP_BODY_TEMPLATE_PRESENTATION = "marp_body_template_presentation_code.md"
MARP_BODY_TEMPLATE_TECHNICAL_BOOK = "marp_body_template_general.md"

MARP_HEADER_TEMPLATE_BUSINESS_BOOK = "marp_header_template_business_book.md"
MARP_HEADER_TEMPLATE_PICTURE_BOOK = "marp_header_template_picture_book.md"
MARP_HEADER_TEMPLATE_PRESENTATION = "marp_header_template_presentation.md"
MARP_HEADER_TEMPLATE_TECHNICAL_BOOK = "marp_header_template_technical_book.md"

# メニューファイルのセクション名設定
SEC_RD = "rd"
SEC_SRC = "src"
SEC_MESHY_3D_COMMON = "meshy_3d"
SEC_MESHY_3D_FIRST = "first_gen"
SEC_MESHY_3D_REFINE = "refine"

# 領域展開開始時のキーワード
KEYWORD_EXPANSION_STARTED = "領域展開開始"

# 領域展開・外部処理コマンドが終わったかどうか確認する間隔（秒）
WAIT_FOR_POLLING_PROCESS = 1

# 2024-08-21 追加タクトタイムのラベル
TAKT_TIME_NAME = 'naming'
TAKT_TIME_RD_GENERATION = 'rd_generation'
TAKT_TIME_DOMAIN_EXPANSION = 'domain_expansion'
