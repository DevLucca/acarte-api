from fastapi_pagination import Page

from domain.routers import BaseRouter
from domain.dtos.loans import LoanDTO as DTO
from domain.controllers.v1.loans import LoanController

router = BaseRouter()
controller = LoanController()

router.get("/", 
        response_model=Page[DTO.LoanResponseSchema],
        name="Get Loans",
        summary="Listar Empréstimos"
    )(controller.get)
router.get("/{uuid}",
        response_model=DTO.LoanResponseSchema,
        name="Get Loan by UUID",
        summary="Buscar Empréstimo"
    )(controller.get_by_id)
router.post("/",
        response_model=DTO.LoanResponseSchema,
        name="Create Loan",
        summary="Criar Empréstimo"
    )(controller.create)
router.put("/{uuid}",
        response_model=DTO.LoanResponseSchema,
        name="Update Loan",
        summary="Editar Empréstimo"
    )(controller.update)
