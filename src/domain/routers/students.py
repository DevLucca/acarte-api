from domain.controllers.students import StudentController
from domain.viewmodels.students import (
    RegisterStudentSchema,
    ResponseStudentSchema
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
    "name": "Nome do Aluno.",
    "surname": "Sobrenome do Aluno.",
    "ra": "Registro do Aluno."
}

@router.get("/", response_model=List[ResponseStudentSchema], summary="Listar Alunos")
async def get_student_filtered(
    name: str = Query(None, description=descriptions['name']),
    surname: str = Query(None, description=descriptions['surname']),
    ra: int = Query(None, description=descriptions['ra'])
):
    """
    Lista os alunos que tenham todos os dados informados nos query params.
    """
    filters = get_filters(locals())
    return StudentController.get_filtered(filters)

@router.get("/{uuid}", response_model=ResponseStudentSchema, summary="Buscar Aluno")
async def get_student(
    uuid: str = Path(..., description=descriptions['uuid'])
):
    """
    Retorna os dados do aluno indicado pelo uuid passado como path param.
    """
    return StudentController.get_by_uuid(uuid)

@router.post("/", response_model=ResponseStudentSchema, summary="Criar Aluno")
async def create_student(
    register_data: RegisterStudentSchema = Body(...)
):
    """
    Cria um novo registro de aluno de acordo com os dados passados no body da request.
    """
    StudentController.create(register_data.dict())

@router.put("/{uuid}", response_model=ResponseStudentSchema, summary="Editar Aluno")
async def update_student(
    uuid: str = Path(..., description=descriptions['uuid']),
    update_data: RegisterStudentSchema.EditValidator = Body(...)
):
    """
    Edita o resgistro do aluno indicado pelo uuid passado como path param.
    """
    return StudentController.update(uuid, update_data.dict())

@router.delete("/{uuid}", response_model=None, summary="Excluir Aluno [Soft Delete]")
async def delete_student(
    uuid: str = Path(..., description=descriptions['uuid'])
):
    """
    Apaga (SOFT) os dados do aluno indicado pelo uuid passado como path param.
    """
    return StudentController.delete(uuid)
