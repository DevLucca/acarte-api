from fastapi_pagination import Page
from domain.routers import CustomRouter
from domain.controllers.v1.loans import LoanController as v1Controller
from domain.viewmodels.loans import ResponseLoanSchema

router = CustomRouter()

router.get("/", response_model=Page[ResponseLoanSchema], summary="Listar Emprestimos")(v1Controller.get)
router.get("/{uuid}", response_model=ResponseLoanSchema, summary="Buscar Emprestimo")(v1Controller.get_by_uuid)
router.post("/", response_model=ResponseLoanSchema, summary="Criar Emprestimo")(v1Controller.create)
router.put("/{uuid}", response_model=ResponseLoanSchema, summary="Editar Emprestimo")(v1Controller.update)
