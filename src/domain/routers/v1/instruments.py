from fastapi_pagination import Page
from ..base import BaseRouter
from ...controllers.v1.instruments import InstrumentController as v1Controller
from ...dtos import (
    instruments,
)

router = BaseRouter()
controller = v1Controller()

router.get("/", response_model=Page[instruments.Instrument], summary="Listar Instrumentos")(controller.get)
router.get("/{uuid}", response_model=instruments.Instrument, summary="Buscar Instrumento")(controller.get_by_uuid)
# router.get("/{uuid}/student", response_model=ResponseStudentSchema, summary="Buscar aluno no qual o instrumento esta emprestado")(controller.get_student_loan)
router.post("/", response_model=instruments.Instrument, summary="Criar Instrumento")(controller.create)
router.put("/{uuid}", response_model=instruments.Instrument, summary="Editar Instrumento")(controller.update)
router.delete("/{uuid}", summary="Excluir Instrumento [Soft Delete]")(controller.delete)
