import json
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parent / "app_config.json"


DEFAULT_CONFIG = {
    "first_run": True,
    "attract_shortcut": "",
    "repel_shortcut": "",
    "delay_seconds": 4.0,
    "storage_path": ""
}


def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(cfg: dict) -> None:
    data = DEFAULT_CONFIG.copy()
    data.update(cfg or {})
    CONFIG_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def is_first_run() -> bool:
    cfg = load_config()
    return bool(cfg.get("first_run", True))


def set_first_run(value: bool):
    cfg = load_config()
    cfg["first_run"] = bool(value)
    save_config(cfg)
