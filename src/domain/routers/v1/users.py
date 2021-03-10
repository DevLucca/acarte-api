from fastapi_pagination import Page
from domain.routers import BaseRouter
from domain.dtos.users import UserDTO
from domain.controllers.v1.users import UserController

router = BaseRouter()
controller = UserController()

router.get("/", 
        response_model=Page[UserDTO.UserResponseSchema],
        name="Get User",
        summary="Listar Usuários"
    )(controller.get)
router.get("/{uuid}",
        response_model=UserDTO.UserResponseSchema,
        name="Get User by UUID",
        summary="Buscar Usuário"
    )(controller.get_by_id)
router.post("/",
        response_model=UserDTO.UserResponseSchema,
        name="Create User",
        summary="Criar Usuário"
    )(controller.create)
router.put("/{uuid}",
        response_model=UserDTO.UserResponseSchema,
        name="Update Usuário",
        summary="Editar Usuário"
    )(controller.update)
router.delete("/{uuid}",
        response_model=None,
        name="Delete User",
        summary="Excluir Usuário [HARD Delete]"
    )(controller.delete)
