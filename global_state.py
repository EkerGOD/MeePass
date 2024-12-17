import configparser
import logging
import os

logger = logging.getLogger(__name__)
class GlobalState:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._init_state()
        return cls._instance

    def _init_state(self):
        # 配置文件路径
        self.config_file = os.path.join(os.getcwd(), 'config.ini')
        self.config = configparser.ConfigParser()

        # 加载配置文件，如果不存在则创建一个空的
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding='utf-8')
        else:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)

        # 初始化临时属性和允许存储的键集合
        self._temp_data = {}
        self._allowed_temp_keys = {
            "master_password",
            "cryption_code",
            "group_id",
            "tree_rows",
            "db_path"
        }  # 定义允许存储的临时键

    # 持久化属性操作
    def get_config(self, section, key, default=None):
        """获取持久化配置的值"""
        if self.config.has_section(section) and self.config.has_option(section, key):
            return self.config.get(section, key)
        return default

    def set_config(self, section, key, value):
        """设置持久化配置的值"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        self._save_config()

    def remove_config(self, section, key=None):
        """删除持久化配置的值"""
        if key:
            if self.config.has_section(section) and self.config.has_option(section, key):
                self.config.remove_option(section, key)
        else:
            if self.config.has_section(section):
                self.config.remove_section(section)
        self._save_config()

    def _save_config(self):
        """保存持久化配置到文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)

    # 临时属性操作
    def get_temp(self, key):
        """获取临时属性的值"""
        return self._temp_data.get(key)

    def set_temp(self, key, value):
        """设置临时属性的值，限定键必须在允许范围内"""
        if key not in self._allowed_temp_keys:
            logger.critical(f"不允许将键 '{key}' 用于临时存储。")
            raise KeyError(f"Key '{key}' is not allowed for temporary storage.")
        logger.info(f"更改临时数据键 {key} 为 {value}")
        self._temp_data[key] = value

    def remove_temp(self, key):
        """移除临时属性的值"""
        if key in self._temp_data:
            del self._temp_data[key]

    def list_temp_keys(self):
        """列出当前所有的临时属性键"""
        return list(self._temp_data.keys())

    def clear_temp(self):
        """清空所有临时属性"""
        self._temp_data.clear()

# 创建全局状态实例
global_state = GlobalState()
