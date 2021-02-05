from controllers.loans import LoanController
from viewmodels.loans import (
    RegisterLoanSchema,
    ResponseLoanSchema
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
    "lented_at": "Emprestado na data.",
    "returned_at": "Retornado na data."
}

@router.get("/", response_model=List[ResponseLoanSchema], summary="Listar Emprestimos")
async def get_loan_filtered(
    lented_at: str = Query(None, description=descriptions['lented_at']),
    returned_at: str = Query(None, description=descriptions['returned_at']),
    student_uuid: str = Query(None, description=descriptions['uuid']),
    instrument_uuid: str = Query(None, description=descriptions['uuid'])
):
    """
    Lista os emprestimos que tenham todos os dados informados nos query params.
    """
    filters = get_filters(locals())
    return LoanController.get_filtered(filters)

@router.post("/", response_model=ResponseLoanSchema, summary="Criar Emprestimo")
async def create_loan(
    register_data: RegisterLoanSchema = Body(...)
):
    """
    Cria um novo registro de emprestimo de acordo com os dados passados no body da request.
    """
    LoanController.create(register_data.dict())

@router.put("/{uuid}", response_model=ResponseLoanSchema, summary="Editar Emprestimo")
async def update_loan(
    uuid: str = Path(..., description=descriptions['uuid']),
    update_data: RegisterLoanSchema.EditValidator = Body(...)
):
    """
    Edita o resgistro do emprestimo indicado pelo uuid passado como path param.
    """
    return LoanController.update(uuid, update_data.dict())
