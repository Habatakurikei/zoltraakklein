import time
from pathlib import Path
from threading import Thread

from llmmaster import LLMMaster

from zoltraakklein.config import DEFAULT_MODEL
from zoltraakklein.config import DEFAULT_PROVIDER
from zoltraakklein.config import EXT_MARKDOWN
from zoltraakklein.config import EXT_YAML
from zoltraakklein.config import KEYWORD_EXPANSION_STARTED
from zoltraakklein.config import PATH_TO_COMPILER
from zoltraakklein.config import PATH_TO_INSTRUCTION
from zoltraakklein.config import SEC_RD
from zoltraakklein.config import TAKT_TIME_DOMAIN_EXPANSION
from zoltraakklein.config import TAKT_TIME_NAME
from zoltraakklein.config import TAKT_TIME_RD_GENERATION
from zoltraakklein.config import WAIT_FOR_POLLING_PROCESS
from zoltraakklein.utils import check_output_folder
from zoltraakklein.utils import create_menu
from zoltraakklein.utils import fetch_instruction_content
from zoltraakklein.utils import generate_naming_prompt
from zoltraakklein.utils import generate_requirement_prompt
from zoltraakklein.utils import order_to_architect
from zoltraakklein.utils import seek_document
from zoltraakklein.utils import set_expansion_limit
from zoltraakklein.yaml_manager import YAMLManager


class ZoltraakKlein:
    '''
    ゾルトラーク・クライン（小さいゾルトラーク）
    ゾルトラークのエッセンスを取り出してコンパクトなクラスにしました。
    ゾルトラークがどのように動いているのか学習できるように日本語解説付き。
    '''
    def __init__(self,
                 request='',
                 compiler='',
                 verbose=False,
                 work_dir=Path.cwd(),
                 **kwargs):
        '''
        初期化のための引数：
            request (str): リクエスト内容、いわゆるプロンプト
            compiler (str): コンパイラ識別子 (e.g. outfit_idea)
              拡張子不要、なぜならコンパイラ(.md)と指示書(.yaml)の指定で共有するため
            verbose (bool): 途中の処理経過を `print` 表示するかどうか
            work_dir (Path/str): 作業ディレクトリのパス、この下に `projects` フォルダを作る
            kwargs (dict): 使用する AI (LLM) 情報
        【上級者向け情報】
        LLMMasterの仕様に従って `kwargs` には複数のAIモデル情報を渡し並列処理することができます。
        ただし、領域展開はシステム固定のAIモデル単体で行います。
        複数のAIモデルを使った場合、要件定義書名と要件定義書本文はAIモデル数分生成されます。
        各AIモデルの生成物にアクセスする場合は `self.master.results` メンバーにアクセスしてください。
        このクラスのインスタンスが残っており、次に生成関数が呼ばれるまで生成物は保持します。
        複数モデルを使う方法は上級者向けです。通常は単一モデルのみ指定してください。
        `kwargs` 変数にはプロンプト (`request`) 以外の情報を下記の形式で渡してください。
            kwargs = {
                "openai": {
                    'provider': "openai",
                    'model': "gpt-4o",
                    'max_tokens': 1000,
                    'temperature': 0.9
                },
                "anthropic": {
                    'provider': "anthropic",
                    'model': "claude-3-opus-20240229",
                    'max_tokens': 4096,
                    'temperature': 0.2
                }
            }
        呼び出すときは zk.name_for_requirement(**kwargs) のようにしてください。
        '''
        if not request:
            raise ValueError('リクエストが指定されていません')

        if not compiler:
            raise ValueError('コンパイラが指定されていません')
        elif not seek_document(compiler, PATH_TO_COMPILER):
            raise ValueError(f'コンパイラが見つかりません： {compiler}')

        if not isinstance(work_dir, Path):
            work_dir = Path(work_dir)

        self.request = request
        self.compiler = compiler.split('.')[0]
        self.verbose = verbose
        self.work_dir = check_output_folder(work_dir)

        '''
        初期化以外のメンバー変数
          llm (dict): 使用するAIモデル情報
          limit (int): 領域展開の最大ステップ数、コンパイラにより異なる
          (0: 要件定義書のみ, 1: 要件定義書＋領域1, 2: 要件定義書＋領域2まで, ...)
          master (LLMMaster): 生成AIのハンドラ
          project_name (str): プロジェクト名
          project_path (Path): プロジェクトフォルダのパス
          project_menu (Path): メニュー（生成物リスト）ファイルのパス
          current_power (int): 現在の領域展開ステップ
          expansion_in_progress (bool): 領域展開中かどうか
          takt_time (list): 各処理の実行時間
        '''
        if any(kwargs):
            self.llm = kwargs
        else:
            self.llm = {DEFAULT_PROVIDER: {'provider': DEFAULT_PROVIDER,
                                           'model': DEFAULT_MODEL}}

        self.limit = set_expansion_limit(self.compiler)
        self.master = LLMMaster()
        self.project_name = ''
        self.project_path = None
        self.project_menu = None
        self.current_power = 1
        self.expansion_in_progress = False
        self.takt_time = {}

    def cast_zoltraak(self):
        '''
        ゾルトラークを唱えます。
        手順：
          1. リクエスト内容を反映した要件定義書ファイル名を命名
          2. 要件定義書本文を生成してファイル保存
          3. 要件定義書から領域展開(1回のみ)
        各手順を個別に呼び出し・実行することもできますが自己責任になります。
        '''
        try:
            self.name_for_requirement()
            self.generate_requirement()
            self.expand_domain()

        except Exception as e:
            msg = f'ゾルトラークの実行中にエラーが発生しました：\n{e}'
            raise Exception(msg)

    def name_for_requirement(self, **kwargs):
        '''
        （旧）要件定義書のファイル名を生成します。
        （新）要件定義書名＝プロジェクト名となる新規フォルダを用意します。
        手順：
          1. プロンプトを用意
          2. AIを召喚してプロンプト内容を実行、プロジェクト名を生成
          3. 新規プロジェクトの生成物保存先フォルダと空のメニューファイルを用意
        **kwargs 引数はこのプロジェクト名生成にだけ適用したい生成AIモデルがあれば渡します。
        なければ初期設定 `llm` のモデルを使用します。
        '''
        if self.project_path:
            msg = f'プロジェクトを既に保持しています：{self.project_path}\n'
            msg += '命名処理を開始できません。インスタンスを新しく作ってください。'
            raise ValueError(msg)

        self.master.dismiss()

        time_start = time.time()

        try:
            prompt = generate_naming_prompt(self.request, self.work_dir)

            if self.verbose:
                msg = 'プロジェクト名の新規命名プロンプト：\n'
                msg += prompt + '\n'
                msg += '※生成AIを召喚します。'
                print(msg)

            entries = self._set_prompt(prompt, **kwargs)

            self.master.summon(entries)
            self.master.run()

            self.project_name = next(iter(self.master.results.values()))
            self.project_path = self.work_dir / self.project_name

            if self.project_path.is_dir():
                msg = f'プロジェクトフォルダは既に存在しています： {self.project_path}\n'
                msg += '命名に失敗しました。再度この関数を呼び命名してください。'
                self.project_path = None
                raise ValueError(msg)

            else:
                if self.verbose:
                    msg = f'新規生成されたプロジェクト名：{self.project_name}\n'
                    msg += f'プロジェクトフォルダを作成します： {self.project_path}'
                    print(msg)

                self.project_path.mkdir(parents=True, exist_ok=True)
                self.project_menu = create_menu(self.project_path,
                                                self.project_name)

                time_end = time.time()
                takt_time = round(time_end - time_start, 3)
                self.takt_time[TAKT_TIME_NAME] = takt_time

                if self.verbose:
                    msg = 'メニュー（生成物リスト）ファイル名を生成しました： '
                    msg += str(self.project_menu)
                    print(msg)

        except Exception as e:
            msg = f'プロジェクトフォルダ生成中にエラーが発生しました：\n{e}'
            msg += 'やり直してください。'
            raise Exception(msg)

    def generate_requirement(self, **kwargs):
        '''
        要件定義書の中身を生成します。
        手順：
          1. 保存先のフォルダとファイル名を確認
          2. 指定コンパイラからプロンプトを用意
          3. AIを召喚してプロンプト内容を実行
          4. 実行結果として生成された要件定義書をファイル保存
          5. 要件定義書のパスを `self.menu_name` のYAMLファイルに記録
        **kwargs 引数はこのプロジェクト名生成にだけ適用したい生成AIモデルがあれば渡します。
        なければ初期設定 `llm` のモデルを使用します。
        '''
        if not self.project_path:
            msg = f'プロジェクトフォルダが存在しません：{self.project_path}\n'
            msg += '要件定義書生成を開始できません。'
            raise ValueError(msg)

        elif not self.project_menu:
            msg = 'メニュー（生成物リスト）を保持していません。'
            msg += '要件定義書生成を開始できません。'
            raise ValueError(msg)

        self.master.dismiss()

        time_start = time.time()

        try:
            prompt = generate_requirement_prompt(
                self.request, seek_document(self.compiler, PATH_TO_COMPILER))

            if self.verbose:
                msg = '要件定義書生成プロンプト：\n'
                msg += prompt + '\n'
                msg += '※生成AIを召喚します。'
                print(msg)

            entries = self._set_prompt(prompt, **kwargs)

            self.master.summon(entries)
            self.master.run()

            menu = YAMLManager(str(self.project_menu))
            for key, value in self.master.results.items():
                save_as = self.project_path / \
                    f'{self.project_name}_{key}{EXT_MARKDOWN}'
                save_as.write_text(value, encoding='utf-8')
                menu.set_item(SEC_RD, key, str(save_as))
            menu.save()

            time_end = time.time()
            takt_time = round(time_end - time_start, 3)
            self.takt_time[TAKT_TIME_RD_GENERATION] = takt_time

            if self.verbose:
                for key, value in self.master.results.items():
                    print(f'生成された要件定義書 ({key}):\n{value}')

        except Exception as e:
            msg = f'要件定義書生成に失敗しました：\n{e}'
            msg += 'やり直してください。'
            raise Exception(msg)

    def expand_domain(self):
        '''
        領域展開（ディレクトリ・ファイル生成）を行います。
        一気に大量のファイル生成処理は生成AIサーバーへの負担と
        セキュリティ懸念があります。そのためこの関数が呼ばれる
        たびに指示書にある1ステップだけ展開するように制御されています。
        手順：
          1. 領域展開してもよいか厳正にチェック
          2. 領域展開指示書を探して読み込み
          3. 指定されたステップのみ指示展開を実行
          4. 次のステップを呼ばれるために待機(+1)
        ヒント：指示書YAMLの関数キーに"#"が入っている処理は呼び出ししません。
        '''
        msg = self._pre_expansion_inspection()

        if not msg:
            to_do = fetch_instruction_content(
                seek_document(self.compiler, PATH_TO_INSTRUCTION))

            if self.current_power in to_do.list_of_sections():
                function_list = to_do.get_section(self.current_power).items()
                process_list = {}
                for key, value in function_list:
                    msg += f'{key}:{value}: '
                    if '#' in key:
                        msg += '処理をスキップします。\n'
                    else:
                        process_list[key] = order_to_architect(
                            str(self.project_path), key, value)
                        msg += '処理を開始します。\n'

                process_monitor = Thread(
                    target=self._monitor_process,
                    args=(process_list, self.current_power, ),
                    daemon=True)
                process_monitor.start()

                msg = f'{KEYWORD_EXPANSION_STARTED}:'
                msg += f'指示番号({self.current_power})\n'
                msg += f'呼び出し作業リスト = {function_list}'

            else:
                msg = f'指示番号({self.current_power})が見つかりません。'
                msg += '領域展開できません。'

            self.current_power += 1

        if self.verbose:
            print(msg)

        if KEYWORD_EXPANSION_STARTED not in msg:
            raise Exception(msg)

    def _pre_expansion_inspection(self):
        '''
        領域展開前の点検処理。
        下記の処理の1つでもNGなら領域展開を行いません。
          1. 前工程の領域展開が完了していること
          2. プロジェクトフォルダが存在すること
          3. 指示書が存在すること
          4. メニュー（生成物リスト）が存在すること
          5. 最大火力が適切に設定されていること
          6. 領域展開できる火力が残っていること
        '''
        msg = ''
        instruction = seek_document(self.compiler, PATH_TO_INSTRUCTION)
        if self.expansion_in_progress:
            msg += '領域展開中です。終わるまで新規に領域展開を開始できません。'
        elif not self.project_path:
            msg += f'プロジェクトフォルダが存在しません：{self.project_path}\n'
            msg += '領域展開を開始できません。'
        elif not instruction:
            msg += f'領域展開指示書が見つかりません：{self.compiler}\n'
            msg += '領域展開を開始できません。'
        elif not self.project_menu:
            msg += 'メニュー（生成物リスト）を保持していません。'
            msg += '領域展開を開始できません。'
        elif self.limit < 1:
            msg += f'最大火力が1未満です: {self.limit}\n'
            msg += '領域展開を開始できません。'
        elif not self.is_expansion_capable():
            msg += f'最大火力オーバーです: MAX {self.limit} < {self.current_power}\n'
            msg += '領域展開を開始できません。'
        return msg

    def _set_prompt(self, prompt: str, **kwargs):
        '''
        生成AIにプロンプトを渡します。
        複雑なポイントが2つあります。
          1. kwargs に言語モデル情報があればそれを使用、なければ `llm` の情報を使う。
            これはプロジェクト名生成と要件定義書生成で別々の生成AIを使えるようにするため。
          2. 複数の生成AIモデルを指定された場合は複数分インスタンスを
            LLMMaster 内部で作る。そのため for 文が使われている。
            1種類の生成AIモデルのみ指定の場合でも動く。
        '''
        if any(kwargs):
            entries = kwargs.copy()
        else:
            entries = self.llm.copy()

        for _, parameters in entries.items():
            parameters['prompt'] = prompt

        return entries

    def load_project(self, project_name: str, current_power: int = 1):
        '''
        生成中のプロジェクトフォルダを読み込みます。
        既に要件定義書ができているプロジェクトに対して
        領域展開を再開するために使用します。
        プロジェクトフォルダが存在しない場合はエラーを返します。
        引数：
        project_name (str): プロジェクト名、パス不要
        current_power (int): 再開したい領域展開番号を指定
        '''
        self.project_path = self.work_dir / project_name
        if not self.project_path.is_dir():
            msg = f'プロジェクトフォルダが存在しません: {self.project_path}'
            raise ValueError(msg)

        self.project_name = project_name
        self.project_menu = self.project_path / f'{project_name}{EXT_YAML}'
        if not self.project_menu.is_file():
            msg = f'メニュー（生成物リスト）が存在しません: {self.project_menu}'
            raise ValueError(msg)

        self.current_power = int(current_power)

    def is_expansion_capable(self):
        '''
        現在の領域展開ステップが最大ステップ数以下かどうかを判定します。
        それによりまだ領域展開できるか判定します。
        この処理がないと指示書に書かれていない展開を始めようとします。
        暴走を食い止めなければいけません。
        '''
        return True if self.current_power <= self.limit else False

    def _monitor_process(self, process_list: dict, step: int):
        '''
        領域展開中かどうかプロセスを監視します。
        独立したスレッドで動かすため、
        領域展開中でもユーザーにとって操作待ちにはなりません。
        ただし現領域展開中に次の展開操作は許可しません。
        '''
        if process_list:

            self.expansion_in_progress = True

            time_start = time.time()

            while process_list:
                completed_processes = []

                for key, entry in process_list.items():
                    if self.verbose:
                        msg = f'プロセスの状態 {key}: {str(entry.poll())}'
                        print(msg)
                    if entry.poll() is not None:
                        completed_processes.append(key)

                for key in completed_processes:
                    process_list.pop(key)

                time.sleep(WAIT_FOR_POLLING_PROCESS)

            time_end = time.time()
            takt_time = round(time_end - time_start, 3)
            label = TAKT_TIME_DOMAIN_EXPANSION + f'_{step:02d}'
            self.takt_time[label] = takt_time

        self.expansion_in_progress = False
