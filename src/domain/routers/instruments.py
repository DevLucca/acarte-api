from domain.controllers.instruments import InstrumentController
from domain.viewmodels.instruments import (
    RegisterInstrumentSchema,
    ResponseInstrumentSchema
)
from core.utils import CustomRouter, get_filters
from fastapi import (
    Query,
    Body,
    Path
)
from typing import List

router = CustomRouter()

descriptions = {
    "uuid": "Universally Unique Identifier.",
    "name": "Nome do Instrumento. Exemplo: Saxofone, Flauta, Trompete...",
    "instrument_id": "Numero do Instrumento. Exemplo: Saxofone 01, Saxofone 02, Flauta 01...",
    "repair": "Booleano para caso o instrumento esteja em reparo, portanto desabilitado para emprestimos.",
    "active": "Booleano para status de disponibilidade do instrumento."
}

@router.get("/", response_model=List[ResponseInstrumentSchema], summary="Listar Instrumentos")
async def get_instruments_filtered(
    instrument_id: str = Query(None, description=descriptions['instrument_id']),
    name: str = Query(None, description=descriptions['name']),
    repair: bool = Query(None, description=descriptions['repair']),
    active: bool = Query(None, description=descriptions['active'])
):
    """
    Lista os instrumentos que tenham todos os dados informados nos query params.
    """
    filters = get_filters(locals())
    return InstrumentController.get_filtered(filters)

@router.get("/{uuid}", response_model=ResponseInstrumentSchema, summary="Buscar Instrumento")
async def get_instrument(
    uuid: str = Path(..., description=descriptions['uuid'])
):
    """
    Retorna os dados do instrumento indicado pelo uuid passado como path param.
    """
    return InstrumentController.get_by_uuid(uuid)

@router.post("/", response_model=ResponseInstrumentSchema, summary="Criar Instrumento")
async def create_instrument(
    register_data: RegisterInstrumentSchema = Body(...)
):
    """
    Cria um novo registro de instrumento de acordo com os dados passados no body da request.
    """
    InstrumentController.create(register_data.dict())

@router.put("/{uuid}", response_model=ResponseInstrumentSchema, summary="Editar Instrumento")
async def update_instrument(
    uuid: str = Path(..., description=descriptions['uuid']),
    update_data: RegisterInstrumentSchema.EditValidator = Body(...)
):
    """
    Edita o resgistro do instrumento indicado pelo uuid passado como path param.
    """
    return InstrumentController.update(uuid, update_data.dict())

@router.delete("/{uuid}", response_model=None, summary="Excluir Instrumento [Soft Delete]")
async def delete_instrument(
    uuid: str = Path(..., description=descriptions['uuid'])
):
    """
    Apaga (SOFT) os dados do instrumento indicado pelo uuid passado como path param.
    """
    return InstrumentController.delete(uuid)
