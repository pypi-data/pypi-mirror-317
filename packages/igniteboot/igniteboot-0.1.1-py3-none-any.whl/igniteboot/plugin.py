import importlib
import logging
import os
import sys
import shutil

logger = logging.getLogger("ignite")

class PluginManager:
    def __init__(self, plugins_folder: str = "plugins"):
        self.installed_plugins = {}
        self.plugins_folder = plugins_folder
        self.ensure_plugins_folder()

    def ensure_plugins_folder(self):
        if not os.path.exists(self.plugins_folder):
            os.makedirs(self.plugins_folder)
            logger.info("[PluginManager] Created plugins folder at '%s'", self.plugins_folder)

        if self.plugins_folder not in sys.path:
            sys.path.insert(0, self.plugins_folder)
            logger.debug("[PluginManager] Added '%s' to sys.path", self.plugins_folder)

    def install_plugin(self, plugin_name: str):
        plugin_path = os.path.join(self.plugins_folder, plugin_name)
        if os.path.exists(plugin_path):
            print(f"Plugin '{plugin_name}' already exists in '{self.plugins_folder}'.")
            return
        os.makedirs(plugin_path)
        with open(os.path.join(plugin_path, "plugin.py"), "w", encoding="utf-8") as f:
            f.write(f"""# {plugin_name}/plugin.py

def initialize_plugin():
    print("[{plugin_name}] Plugin initialized from '{self.plugins_folder}'")
""")
        print(f"[PluginManager] Installed plugin '{plugin_name}' in '{self.plugins_folder}'.")

    def remove_plugin(self, plugin_name: str):
        plugin_path = os.path.join(self.plugins_folder, plugin_name)
        if not os.path.exists(plugin_path):
            print(f"Plugin '{plugin_name}' does not exist in '{self.plugins_folder}'.")
            return
        shutil.rmtree(plugin_path)
        print(f"[PluginManager] Removed plugin '{plugin_name}' from '{self.plugins_folder}'.")

    def load_plugin(self, plugin_module_path: str):
        try:
            plugin_module = importlib.import_module(plugin_module_path)
            if hasattr(plugin_module, "initialize_plugin"):
                plugin_module.initialize_plugin()
            logger.info("[PluginManager] Loaded plugin from '%s'", plugin_module_path)
        except ImportError as e:
            logger.error("[PluginManager] Failed to load plugin '%s': %s", plugin_module_path, e)

    def load_all_plugins(self):
        if not os.path.isdir(self.plugins_folder):
            logger.warning("[PluginManager] Plugins folder '%s' does not exist.", self.plugins_folder)
            return

        for item in os.listdir(self.plugins_folder):
            item_path = os.path.join(self.plugins_folder, item)
            if os.path.isdir(item_path):
                plugin_module_path = f"{item}.plugin"
                self.load_plugin(plugin_module_path)
