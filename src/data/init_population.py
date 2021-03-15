import json

def get_database_file() -> dict:
    with open('database.json', 'r') as f:
        return json.load(f)

def check_population(table: str = None, record: dict = {}) -> bool:
    if table == 'users':
        pass
    elif table == 'settings':
        pass
    
def populate():
    database_config = get_database_file()
    if database_config.get('initiated', True):
        return
    
    for table in database_config.get('tables', []):
        for record in table.get('records', []):
            check_population(table=table.get('name', None), record=record)
    
populate()
