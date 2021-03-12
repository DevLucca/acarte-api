from fastapi_pagination import Page

from domain.routers import BaseRouter
from domain.dtos.students import StudentDTO as DTO
from domain.controllers.v1.students import StudentController

router = BaseRouter()
controller = StudentController()

router.get("/", 
        response_model=Page[DTO.StudentResponseSchema],
        name="Get Students",
        summary="Listar Alunos"
    )(controller.get)
router.get("/{uuid}",
        response_model=DTO.StudentResponseSchema,
        name="Get Student by UUID",
        summary="Buscar Aluno"
    )(controller.get_by_id)
# router.get("/{uuid}/student", response_model=ResponseStudentSchema, summary="Buscar aluno no qual o instrumento esta emprestado")(controller.get_student_loan)
router.post("/",
        response_model=DTO.StudentResponseSchema,
        name="Create Student",
        summary="Criar Aluno"
    )(controller.create)
router.put("/{uuid}",
        response_model=DTO.StudentResponseSchema,
        name="Update Student",
        summary="Editar Aluno"
    )(controller.update)
router.delete("/{uuid}",
        response_model=None,
        name="Delete Student",
        summary="Excluir Aluno [HARD Delete]"
    )(controller.delete)
