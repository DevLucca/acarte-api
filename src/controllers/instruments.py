from fastapi import HTTPException
from repository.instruments import InstrumentsRepository
class InstrumentController():
    
    def get_filtered(filters):
        return InstrumentsRepository.get(filters)

    def get_by_uuid(uuid):
        print(uuid)

    def create(data):
        data = validate(data)
        return InstrumentsRepository.create(data)

    def update(uuid, data):
        validate(data)
        print(uuid, data)

    def delete(uuid):
        print(uuid)

def validate(data):
    name = data['name']
    instr_id = data['instrument_id']
    instr_type = data['instrument_type']
    active = data['active']
    repair = data['repair']

    if name is None or name == '':
        raise HTTPException(401, detail=f"Attribute name empty or missing.")

    if instr_id is None or instr_id == '':
        raise HTTPException(401, detail=f"Attribute instrument_id empty or missing.")
    
    if instr_type is None or instr_type == '':
        raise HTTPException(401, detail=f"Attribute instrument_type empty or missing.")

    if active is None:
        data['active'] = True
    
    if repair is None:
        data['repair'] = False

    return data
    
