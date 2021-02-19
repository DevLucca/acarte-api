from fastapi_pagination import Page
from domain.routers import CustomRouter
from domain.controllers.v1.students import StudentController as v1Controller
from domain.viewmodels.students import ResponseStudentSchema
from domain.viewmodels.instruments import ResponseInstrumentSchema
from typing import List

router = CustomRouter()

router.get("/", response_model=Page[ResponseStudentSchema], summary="Listar Alunos")(v1Controller.get)
router.get("/{uuid}", response_model=ResponseStudentSchema, summary="Buscar Aluno")(v1Controller.get_by_uuid)
router.get("/{uuid}/instruments", response_model=List[ResponseInstrumentSchema], summary="Buscar Instrumento que emprestado pelo aluno")(v1Controller.get_lent_instrument)
router.post("/", response_model=ResponseStudentSchema, summary="Criar Aluno")(v1Controller.create)
router.put("/{uuid}", response_model=ResponseStudentSchema, summary="Editar Aluno")(v1Controller.update)
router.delete("/{uuid}", summary="Excluir Aluno [Soft Delete]")(v1Controller.delete)
