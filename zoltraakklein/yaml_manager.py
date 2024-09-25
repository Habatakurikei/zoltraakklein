import yaml
from typing import Any
from typing import Dict
from typing import List


DUMMY_SECTION = 'dummy'


class YAMLManager:
    """
    このクラスはYAMLで記載したゾルトラーク関連の
    レコードファイルを追加編集するためのクラスです。
    主にこれらのファイルの操作を簡単にするために使用します。
      1. メニュー（生成物一覧）ファイル
      2. 領域展開指示ファイル
    いわゆる設定ファイルとしてのYAMLについては想定しません。
    ゾルトラーク本体の設定は `config.py` で行います。
    このようなYAMLフォーマットを想定して追加編集します。
    key, value の組み合わせを1アイテム（項目）とします。
    section1:
      key1: value1
      key2: value2
    section2:
      key3: value3
      key4: value4
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.config: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """
        指定ファイルを読み込む
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.config = yaml.safe_load(file) or {}

            for entry, value in self.config.items():
                if value is None:
                    self.config[entry] = {}

        except FileNotFoundError:
            self.config = {}

    def save(self) -> None:
        """
        ファイル保存
        """
        with open(self.filename, 'w', encoding='utf-8') as file:
            yaml.dump(self.config, file)

    def sum_of_sections(self) -> int:
        """
        登録されているセクション数を返す
        """
        return len(self.config.keys())

    def list_of_sections(self) -> List[str]:
        """
        登録されているセクション名をリスト型で返す
        """
        return list(self.config.keys())

    def sum_of_items(self) -> int:
        """
        登録されている設定項目数を返す
        """
        return sum(len(self.config[key]) for key in self.config.keys())

    def list_of_items(self) -> List[str]:
        """
        全セクションに登録されている項目の値だけをリスト型で返す
        """
        items = []
        for _, value in self.config.items():
            items.extend(value.values())
        return items

    def get_all(self) -> Dict[str, Any]:
        """
        全てのセクション名と設定値を辞書型で返す
        """
        return self.config.copy()

    def get_section(self, section: str) -> Dict:
        """
        指定セクションの設定値を辞書型で返す
        'dummy' が指定された場合は空の辞書を返す
        """
        if section == DUMMY_SECTION:
            return {}
        elif section not in self.config:
            msg = f'Section {section} がありません'
            raise Exception(msg)
        return self.config[section]

    def new_section(self, section: str) -> None:
        """
        新しいセクションを追加する、すでにあれば無視
        """
        if section not in self.config:
            self.config[section] = {}

    def set_item(self, section: str, key: str, value: Any) -> None:
        """
        指定セクションに設定値を追加または更新する
        """
        if section not in self.config:
            msg = f'Section {section} がありません'
            raise Exception(msg)
        self.config[section][key] = value

    def remove_item(self, section: str, key: str) -> None:
        """
        指定セクションの設定値を削除する
        """
        if section not in self.config:
            msg = f'Section {section} がありません'
            raise Exception(msg)
        del self.config[section][key]

    def clear(self) -> None:
        """
        全ての設定値をクリアする
        """
        self.config.clear()
