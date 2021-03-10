from fastapi_pagination import Page
from domain.routers import BaseRouter
from domain.dtos.instruments import InstrumentDTO
from domain.controllers.v1.instruments import InstrumentController

router = BaseRouter()
controller = InstrumentController()

router.get("/", 
        response_model=Page[InstrumentDTO.InstrumentResponseSchema],
        name="Get Instruments",
        summary="Listar Instrumentos"
    )(controller.get)
router.get("/{uuid}",
        response_model=InstrumentDTO.InstrumentResponseSchema,
        name="Get Instrument by UUID",
        summary="Buscar Instrumento"
    )(controller.get_by_id)
# router.get("/{uuid}/student", response_model=ResponseStudentSchema, summary="Buscar aluno no qual o instrumento esta emprestado")(controller.get_student_loan)
router.post("/",
        response_model=InstrumentDTO.InstrumentResponseSchema,
        name="Create Instrument",
        summary="Criar Instrumento"
    )(controller.create)
router.put("/{uuid}",
        response_model=InstrumentDTO.InstrumentResponseSchema,
        name="Update Instrument",
        summary="Editar Instrumento"
    )(controller.update)
router.delete("/{uuid}",
        response_model=None,
        name="Delete Instrument",
        summary="Excluir Instrumento [HARD Delete]"
    )(controller.delete)
