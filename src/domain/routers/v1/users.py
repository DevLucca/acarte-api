from fastapi_pagination import Page

from domain.routers import BaseRouter
from domain.dtos.users import UserDTO as DTO
from domain.controllers.v1.users import UserController

router = BaseRouter()
controller = UserController()

router.get("/", 
        response_model=Page[DTO.UserResponseSchema],
        name="Get User",
        summary="Listar Usuários"
    )(controller.get)
router.get("/{uuid}",
        response_model=DTO.UserResponseSchema,
        name="Get User by UUID",
        summary="Buscar Usuário"
    )(controller.get_by_id)
router.post("/",
        response_model=DTO.UserResponseSchema,
        name="Create User",
        summary="Criar Usuário"
    )(controller.create)
router.post("/password",
        response_model=DTO.UserResponseSchema,
        name="Update User Password",
        summary="Atualizar Senha do Usuário"
    )(controller.update_password)
router.put("/{uuid}",
        response_model=DTO.UserResponseSchema,
        name="Update User",
        summary="Editar Usuário"
    )(controller.update)
router.delete("/{uuid}",
        response_model=None,
        name="Delete User",
        summary="Excluir Usuário [HARD Delete]"
    )(controller.delete)
