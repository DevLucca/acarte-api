from .. import db_client
from src.core.settings import BASE_DIR
from importlib import import_module

n = 0
for module in [
    module.name
    for module in (BASE_DIR / "data" / "entities").glob("*.py")
    if module.name != "__init__.py"
]:
    print(f'{n}: data.entities.{module.removesuffix(".py")}')
    n +=1
    import_module(f'src.data.entities.{module.removesuffix(".py")}')

print(BASE_DIR)
# print((BASE_DIR / "data" / "entities").glob("*.py"))
# print("trying to map")
db_client.generate_mapping(create_tables=True)
