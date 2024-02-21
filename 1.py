import configparser
import re
from io import StringIO

class NestedConfigParser(configparser.ConfigParser):
    def __init__(self):
        super().__init__()

    def read_file(self, filename, encoding=None):
        with open(filename, encoding=encoding) as f:
            content = f.read()
        super().read_string(content)

    def read_str(self, config_str):
        super().read_string(config_str)
        
    def get_nested(self, section, option):
        value = self.get(section, option)
        return self._parse_nested(value)
    
    def set_nested(self, section, option, value):
        if isinstance(value, dict):
            value = str(value)
            value = value.replace('{', '(').replace('}', ')').replace('\'','')
        self.set(section, option, value)

    def delete_section(self, section):
        super().remove_section(section)

    def delete_option(self, section, option):
        super().remove_option(section, option)
        
    def delete_option_attr(self, section, option):
        super().remove_option(section, option)
        
    def save(self, filename):
        with open(filename, 'w') as config_file:
            super().write(config_file)

    def _parse_nested(self, value):
        # 使用正则表达式解析INI文件中的嵌套结构
        match = re.match(r'\((.+)\)', value)
        if match:
            nested_str = match.group(1)
            value = {}
            node_list = nested_str.split(',')
            for node in node_list:
                node_data = node.split('=')
                if len(node_data) > 0:
                    value.update({
                        node_data[0]: node_data[1]
                    })
        return value

# 示例用法
config = NestedConfigParser()
config.read_file('new_config.ini')

# 获取原始属性和值
nested_value = config.get_nested('/Script/Pal.PalGameLocalSettings', 'audiosettings')

print(nested_value)

# 修改属性
if isinstance(nested_value, dict):  # 二级属性
    nested_value['BGM'] = '0.8'
else:  # 一级属性
    nested_value = '0.8'

config.set_nested('/Script/Pal.PalGameLocalSettings', 'audiosettings', nested_value)

# 保存修改
config.save('new_config_modified.ini')

# 删除节点和属性
config.delete_section('/Script/Pal.PalGameLocalSettings')
config.delete_option('/Script/Pal.PalGameLocalSettings', 'audiosettings')

# 保存删除后的结果
config.save('new_config_after_deletion.ini')
