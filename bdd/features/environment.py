import sys
from pathlib import Path

# Каталог bdd/ с модулем player.py добавляется в путь поиска модулей
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
