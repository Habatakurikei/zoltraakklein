import yaml
from typing import Any
from typing import Dict
from typing import List


DUMMY_SECTION = 'dummy'


class YAMLManager:
    """
    This class is used to add and edit menu items in YAML.
    It is not intended for YAML as a configuration file:
    section1:
      subsection1:
        key1: value1
        key2: value2
      subsection2:
        key3: value3
    section2:
      subsection3:
        key4: value4
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.config: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """
        Load the specified file
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            self.config = {}

    def save(self) -> None:
        """
        Save to file
        """
        with open(self.filename, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True)

    def sum_of_sections(self) -> int:
        """
        Return the number of registered sections
        """
        return len(self.config)

    def sum_of_subsections(self, section: str) -> int:
        """
        Return the number of registered subsections in a given section
        """
        if section not in self.config:
            raise ValueError(f'Section {section} not exist')
        return len(self.config[section])

    def list_of_sections(self) -> List[str]:
        """
        Return a list of registered section names
        """
        return list(self.config.keys())

    def list_of_subsections(self, section: str) -> List[str]:
        """
        Return a list of registered subsection names for a given section
        """
        if section not in self.config:
            return []
        return list(self.config[section].keys())

    def sum_of_items(self) -> int:
        """
        Return the total number of registered configuration items
        """
        ans = 0
        for section in self.config.keys():
            if isinstance(self.config[section], dict):
                for subsection in self.config[section]:
                    if isinstance(self.config[section][subsection], dict):
                        ans += len(self.config[section][subsection].values())
                    else:
                        ans += 1
            else:
                ans += 1
        return ans

    def list_of_items(self) -> List[Any]:
        """
        Return a list of all values across all sections and subsections
        """
        ans = []
        for section in self.config.keys():
            if isinstance(self.config[section], dict):
                for subsection in self.config[section]:
                    if isinstance(self.config[section][subsection], dict):
                        ans += self.config[section][subsection].values()
                    else:
                        ans += [self.config[section][subsection]]
            else:
                ans += [self.config[section]]
        return list(ans)

    def get_all(self) -> Dict[str, Any]:
        """
        Return all section names and values as a dictionary
        """
        return self.config.copy()

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Return values for the specified section as a dictionary
        Return an empty dictionary if 'dummy' is specified
        """
        if section == DUMMY_SECTION:
            return {}
        elif section not in self.config:
            raise ValueError(f'Section {section} not exist')
        return self.config[section]

    def get_subsection(self, section: str, subsection: str) -> Dict[str, Any]:
        """
        Return values for the specified subsection as a dictionary
        """
        if section not in self.config:
            raise ValueError(f'Section {section} not exist')
        if subsection not in self.config[section]:
            msg = f'Subsection {subsection} not exist in section {section}'
            raise ValueError(msg)
        return self.config[section][subsection]

    def new_section(self, section: str) -> None:
        """
        Add a new section, ignore if it already exists
        """
        if section not in self.config:
            self.config[section] = {}

    def new_subsection(self, section: str, subsection: str) -> None:
        """
        Add a new subsection to a section, ignore if it already exists
        """
        if section not in self.config:
            self.config[section] = {}
        if subsection not in self.config[section]:
            self.config[section][subsection] = {}

    def set_section_item(self,
                         section: str,
                         key: str,
                         value: Any) -> None:
        """
        Add or update a value in the specified section
        """
        if section not in self.config:
            raise ValueError(f'Section {section} not exist')
        self.config[section][key] = value

    def set_subsection_item(self,
                            section: str,
                            subsection: str,
                            key: str,
                            value: Any) -> None:
        """
        Add or update a value in the specified section and subsection
        """
        if section not in self.config:
            raise Exception(f'Section {section} not exist')
        if subsection not in self.config[section]:
            msg = f'Subsection {subsection} not exist in section {section}'
            raise Exception(msg)
        self.config[section][subsection][key] = value

    def clear(self) -> None:
        """
        Clear all configuration values
        """
        self.config.clear()
