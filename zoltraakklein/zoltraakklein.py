import os

from llmmaster import LLMMaster

from zoltraakklein.config import DEFAULT_MODEL
from zoltraakklein.config import DEFAULT_PROVIDER
from zoltraakklein.config import DEFAULT_TEMPERATURE
from zoltraakklein.config import FORMATTER
from zoltraakklein.config import PATH_TO_COMPILER
from zoltraakklein.config import PATH_TO_GENERATED
from zoltraakklein.config import PATH_TO_MAGIC
from zoltraakklein.config import PATH_TO_PROMPT
from zoltraakklein.config import PATH_TO_REQUIREMENT
from zoltraakklein.config import PROMPT_FOR_NAME
from zoltraakklein.utils import seek_compiler


class ZoltraakKlein:
    '''
    ゾルトラーク・クライン（小さいゾルトラーク）
    ゾルトラークのエッセンスを取り出してコンパクトなクラスにしました。
    ゾルトラークがどのように動いているのか学習できるように日本語解説付けました。
    '''
    def __init__(self, request='', compiler='', expand=False, **kwargs):
        '''
        初期化のための引数：
            request (str): リクエスト内容、いわゆるプロンプト
            compiler (str): コンパイラ名 (*.md)
            expand (bool): ディレクトリ展開を行うかどうか
            kwargs (dict): 使用するAI(LLM)情報
        【重要】
        LLMMasterの仕様に従って `kwargs` には複数のAIモデル情報を渡し並列処理することができます。
        ただし、領域展開はシステム固定のAIモデル単体で行います。
        複数のAIモデルを使った場合、要件定義書名と要件定義書本文はAIモデル数分生成されます。
        この場合、最初に指定したAIモデルの生成物だけ `self.file_name`, `self.requirement_path`
        に格納されます。
        全AIモデルの生成物にアクセスする場合は各LLMMasterの `results` にアクセスしてください。
        このクラスのインスタンスが残っており、次に生成関数が呼ばれるまで生成物は保持します。
        複数モデルを使う方法は上級者向けです。通常は単一モデルのみ指定してください。
        `kwargs` 変数にはプロンプト (`request`) 以外の情報を下記の形式で渡してください。
            kwargs = {
                "openai": {
                    provider="openai",
                    model="gpt-4o",
                    temperature=0.5
                },
                "anthropic": {
                    provider="anthropic",
                    model="claude-3-opus-20240229",
                    temperature=0.5
                },
            }
        '''
        if not request:
            raise ValueError('プロンプトが指定されていません')

        if not compiler:
            raise ValueError('コンパイラが指定されていません')

        if not any(kwargs):
            raise ValueError('AIモデルが指定されていません')

        self.system_dir = ''
        self.user_dir = ''
        self.request = request
        self.compiler = compiler
        self.expand = expand
        self.llm = kwargs
        self.master_naming = LLMMaster()
        self.master_requirement = LLMMaster()
        self.master_expand = LLMMaster()
        self.file_name = ''
        self.requirement_path = ''

        self._check_folders_exist()

    def cast_zoltraak(self):
        '''
        ゾルトラークを唱えます。
        手順：
          1. リクエスト内容を反映した要件定義書ファイル名を生成
          2. 要件定義書本文を生成してファイル保存
          3. 要件定義書から領域展開
        各手順を個別に呼び出し・実行することもできますが自己責任になります。
        '''
        self.name_for_requirement()
        self.generate_requirement()
        # self.expand_domain()

    def name_for_requirement(self):
        '''
        要件定義書ファイル名を生成します。
        生成されたファイル名は `self.file_name` に格納されます。
        手順：
          1. プロンプトを用意
          2. AIを召喚してプロンプト内容を実行
          3. 実行結果をファイル名として保存
        '''
        self.master_naming.dismiss()
        self.file_name = ''

        try:
            prompt = self._generate_naming_prompt()
            print(f'ファイル名生成プロンプト：\n{prompt}')

            entries = self.llm.copy()

            for _, parameters in entries.items():
                parameters['prompt'] = prompt

            print(f'AIを召喚します。')

            self.master_naming.summon(entries)
            self.master_naming.run()
            self.file_name = next(iter(self.master_naming.results.values()))

        except Exception as e:
            print(e)
            self.file_name = ''

        print(f'生成されたファイル名： {self.file_name}')

    def generate_requirement(self):
        '''
        要件定義書本文生成を行います。
        生成された要件定義書のファイル名をパス付きで `self.requirement_path` に格納します。
        手順：
          1. 保存先のフォルダとファイル名を確認
          2. プロンプトを用意
          3. AIを召喚してプロンプト内容を実行
          4. 実行結果として生成された要件定義書をファイル保存
          5. 要件定義書のパスを `self.requirement_path` に格納
        '''
        self.master_requirement.dismiss()

        if not self.file_name:
            self.file_name = 'hogehoge.md'

        self.requirement_path = os.path.join(self.user_dir,
                                             PATH_TO_REQUIREMENT,
                                             self.file_name)

        try:
            prompt = self._generate_requirement_prompt()
            print(f'要件定義書生成プロンプト：\n{prompt}')

            entries = self.llm.copy()

            for _, parameters in entries.items():
                parameters['prompt'] = prompt

            print(f'AIを召喚します。')

            self.master_requirement.summon(entries)
            self.master_requirement.run()

            candidate = next(iter(self.master_requirement.results.values()))

            with open(self.requirement_path, 'w', encoding='utf-8') as f:
                f.write(candidate)

            print(f'生成された要件定義書のパス： {self.requirement_path}')

        except Exception as e:
            print(e)
            self.requirement_path = ''

    def expand_domain(self):
        '''
        領域展開を行います。近日実装予定。
        '''
        if self.expand and self.requirement_path:
            # Do not forget to add checking if eligible compiler is selected
            self.master_expand.dismiss()
            # TODO: Implement domain expansion logic
            pass

    def _check_folders_exist(self):
        '''
        生成物保存先フォルダが存在するかを確認します。
        存在しない場合はフォルダを作成しておきます。
        初期化時のみ呼ばれます。
        '''
        self.system_dir = os.path.dirname(os.path.abspath(__file__))
        self.user_dir = os.getcwd()

        requirement_path = os.path.join(self.user_dir, PATH_TO_REQUIREMENT)
        generated_path = os.path.join(self.user_dir, PATH_TO_GENERATED)
        magic_path = os.path.join(self.user_dir, PATH_TO_MAGIC)

        if not os.path.exists(requirement_path):
            os.makedirs(requirement_path)
        if not os.path.exists(generated_path):
            os.makedirs(generated_path)
        if not os.path.exists(magic_path):
            os.makedirs(magic_path)

    def _generate_naming_prompt(self):
        '''
        ファイル名生成プロンプトを用意します。
        手順
          1. 既にある要件定義書のリストを取得
          2. プロンプトのテンプレートを読み込み
          3. プロンプトにあなたのリクエストを埋め込み
          4. 既にある要件定義書のリストをプロンプトに埋め込み
          5. プロンプトを返す
        '''
        prompt = ''

        existing_requirements = os.listdir(os.path.join(
            self.user_dir, PATH_TO_REQUIREMENT))
        existing_requirements = ', '.join(existing_requirements)

        to_open = os.path.join(self.system_dir, PATH_TO_PROMPT, PROMPT_FOR_NAME)
        with open(to_open, 'r', encoding='utf-8') as f:
            prompt = f.read()

        prompt = prompt.replace('{request}', self.request)
        prompt = prompt.replace('{existing_requirements}',
                                existing_requirements)

        return prompt

    def _generate_requirement_prompt(self):
        '''
        要件定義書本文生成プロンプトを用意します。
        手順：
          1. 指定コンパイラを探して読み込み
          2. コンパイラにあなたのリクエストを埋め込み
          3. コンパイラにフォーマットを追加（無くても本当は動く）
          4. コンパイラをプロンプトとして返す
        '''
        prompt = ''

        compiler_name = seek_compiler(self.compiler)
        if not compiler_name:
            raise ValueError(f'コンパイラ{self.compiler}が見つかりません')

        compiler_path = os.path.join(self.system_dir,
                                     PATH_TO_COMPILER,
                                     compiler_name)

        with open(compiler_path, 'r', encoding='utf-8') as f:
            prompt = f.read()

        prompt = prompt.replace('{prompt}', self.request)

        to_open = os.path.join(self.system_dir, PATH_TO_PROMPT, FORMATTER)
        with open(to_open, 'r', encoding='utf-8') as f:
            prompt += f.read()

        return prompt
