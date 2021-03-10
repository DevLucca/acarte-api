from data import db_client
from core.settings import BASE_DIR
from importlib import import_module

for module in [
    module.name
    for module in (BASE_DIR / "data" / "entities").glob("*.py")
    if module.name != "__init__.py"
]:
    import_module(f'data.entities.{module.removesuffix(".py")}')

db_client.generate_mapping(create_tables=True)
