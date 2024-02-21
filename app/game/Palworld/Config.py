import configparser
import re,os,platform
os_name = platform.system()

class NestedConfigParser(configparser.ConfigParser):
    def __init__(self):
        super().__init__()

    def read_file_config(self, filename):
        super().read_file(filename)

    def read_str(self, config_str):
        super().read_string(config_str)
        
    def get_all_nested(self):
        pass
        
    def get_nested(self, section, option):
        value = self.get(section, option)
        return self._parse_nested(value)
    
    def set_nested(self, section, option, value):
        if isinstance(value, dict):
            data = ""
            for key in value:
                data += str(key) + '=' + str(value[key]) + ','
            if len(value) > 0:
                data = '(' + data[0:-1] + ')'
            value = data
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
    def _dict_to_config_string(d):
        items = []
        for key, value in d.items():
            if value is None:
                items.append(f'{key}=None')
            elif isinstance(value, bool):
                items.append(f'{key}={str(value)}')
            else:
                items.append(f'{key}={value:.6f}')

        return ','.join(items)
#login anonymous 匿名登录
#app_update 343050 validate 激活服务器
# steamcmd +login anonymous +app_update 2394010 validate +quit

class Config():
    def __init__(self) -> None:
        if os_name == "Windows":
            self.configPath = os.path.join(os.getcwd(), 'steamcmd/steamapps/common/PalServer/Pal/Saved/Config/WindowsServer')
        elif os_name == "Linux":
            self.configPath = os.path.join(os.getcwd(), 'steamcmd/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer')
        self.configFiles = []
        if os.path.isdir(self.configPath):
            files_in_current_directory = os.listdir(self.configPath)

            # 打印文件列表
            for file_name in files_in_current_directory:
                self.configFiles.append(file_name)
            
        pass
    
    def setConfigOption(self, file, text):
        path = os.path.join(self.configPath, file)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        
    def getConfigOption(self, file):
        path = os.path.join(self.configPath, file)
        text = ''
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
        return text
    
    def getPalWorldSettings(self):
        text = self.getConfigOption('PalWorldSettings.ini')
        if text == '':
            default_config = os.path.join(os.getcwd(), 'steamcmd/steamapps/common/PalServer/DefaultPalWorldSettings.ini')
            if os.path.isfile(default_config):
                with open(default_config, 'r', encoding='utf-8') as f:
                    text = f.read()
                self.setConfigOption('PalWorldSettings.ini', text)
        return text
    
    def getPalWorldSettingsPath(self):
        path = os.path.join(os.getcwd(), 'steamcmd/steamapps/common/PalServer/Pal/Saved/Config/WindowsServer/PalWorldSettings.ini')
        text = self.getConfigOption('PalWorldSettings.ini')
        if text == '':
            default_config = os.path.join(os.getcwd(), 'steamcmd/steamapps/common/PalServer/DefaultPalWorldSettings.ini')
            if os.path.isfile(default_config):
                with open(default_config, 'r', encoding='utf-8') as f:
                    text = f.read()
                self.setConfigOption('PalWorldSettings.ini', text)
        return path
    
    