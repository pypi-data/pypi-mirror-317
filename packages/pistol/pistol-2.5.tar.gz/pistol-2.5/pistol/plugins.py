import json
from pathlib import Path
from typing import List, Dict
from .logging import info, warning, error

class PluginManager:
    def __init__(self, plugin_dir: Path, meta_file: Path):
        self.plugin_dir = plugin_dir
        self.meta_file = meta_file
        self.plugins: Dict[str, dict] = {}
        self._load_plugins_metadata()

    def _load_plugins_metadata(self):
        if not self.meta_file.exists():
            self.meta_file.write_text(json.dumps({}))
        with self.meta_file.open() as f:
            self.plugins = json.load(f)

    def _save_plugins_metadata(self):
        with self.meta_file.open("w") as f:
            json.dump(self.plugins, f, indent=4) # NOQA

    def list_plugins(self) -> List[tuple[str, dict]]:
        return list(self.plugins.items())

    def install_plugin(self, plugin_name: str, plugin_source: str):
        if plugin_name in self.plugins:
            warning(f"plugin {plugin_name} is already installed.")
            return

        plugin_path = self.plugin_dir / plugin_name
        try:
            if plugin_source.startswith("http://") or plugin_source.startswith("https://"):
                import requests
                response = requests.get(plugin_source)
                response.raise_for_status()
                plugin_path.mkdir(parents=True, exist_ok=True)
                with open(plugin_path / f"{plugin_name}.py", "w") as f:
                    f.write(response.text)
            else:
                source_path = Path(plugin_source)
                if not source_path.exists():
                    error(f"source path {plugin_source} does not exist.")
                    return
                plugin_path.mkdir(parents=True, exist_ok=True)
                import shutil
                shutil.copytree(source_path, plugin_path, dirs_exist_ok=True)
            self.plugins[plugin_name] = {"source": plugin_source, "enabled": True}
            self._save_plugins_metadata()
            info(f"plugin {plugin_name} installed successfully.")
        except Exception as e:
            error(f"failed to install plugin {plugin_name}: {str(e).lower()}")

    def uninstall_plugin(self, plugin_name: str):
        if plugin_name not in self.plugins:
            warning(f"plugin {plugin_name} is not installed.")
            return

        plugin_path = self.plugin_dir / plugin_name
        try:
            import shutil
            shutil.rmtree(plugin_path)

            del self.plugins[plugin_name]
            self._save_plugins_metadata()
            info(f"plugin {plugin_name} uninstalled successfully.")
        except Exception as e:
            error(f"failed to uninstall plugin {plugin_name}: {str(e).lower()}")

    def enable_plugin(self, plugin_name: str):
        if plugin_name not in self.plugins:
            error(f"plugin {plugin_name} is not installed.")
            return
        self.plugins[plugin_name]["enabled"] = True
        self._save_plugins_metadata()
        info(f"plugin {plugin_name} enabled.")

    def disable_plugin(self, plugin_name: str):
        if plugin_name not in self.plugins:
            error(f"plugin {plugin_name} is not installed.")
            return
        self.plugins[plugin_name]["enabled"] = False
        self._save_plugins_metadata()
        info(f"plugin {plugin_name} disabled.")
    def enable_all_plugins(self):
        info("enabling all plugins")
        for plugin_name in self.plugins:
            self.enable_plugin(plugin_name)
    def disable_all_plugins(self):
        info("disabling all plugins")
        for plugin_name in self.plugins:
            self.disable_plugin(plugin_name)
    def list_enabled_plugins(self) -> List[tuple[str, dict]]:
        return [(plugin_name, metadata) for plugin_name, metadata in self.list_plugins() if metadata.get("enabled", False)]