from fastapi_pagination import Page
from domain.routers import CustomRouter
from domain.controllers.v1.instruments import InstrumentController as v1Controller
from domain.viewmodels.instruments import ResponseInstrumentSchema
from domain.viewmodels.students import ResponseStudentSchema

router = CustomRouter()

router.get("/", response_model=Page[ResponseInstrumentSchema], summary="Listar Instrumentos")(v1Controller.get)
router.get("/{uuid}", response_model=ResponseInstrumentSchema, summary="Buscar Instrumento")(v1Controller.get_by_uuid)
router.get("/{uuid}/student", response_model=ResponseStudentSchema, summary="Buscar aluno no qual o instrumento esta emprestado")(v1Controller.get_student_loan)
router.post("/", response_model=ResponseInstrumentSchema, summary="Criar Instrumento")(v1Controller.create)
router.put("/{uuid}", response_model=ResponseInstrumentSchema, summary="Editar Instrumento")(v1Controller.update)
router.delete("/{uuid}", summary="Excluir Instrumento [Soft Delete]")(v1Controller.delete)
