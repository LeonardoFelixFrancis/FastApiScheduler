from fastapi.exceptions import HTTPException
from fastapi import status

duplicate_email = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="A User with this e-mail already exists"
    )

ambiguous_permission = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="A user need to be a adm or a teacher"
)

unauthorized_action = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Ação proíbida."
)

user_does_not_exist_forgot_password = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='E-mail informado não é associado a nenhum usuário.'
)

teacher_does_not_exist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="The informed user does not exists."
)

teacher_cannot_be_adm = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="A Teacher account cannot be a admin user."
)

informed_user_is_not_teacher = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The informed user is not a teacher."
)

lesson_does_not_exist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="The informed lesson does not exist."
)

lesson_schedule_does_not_exist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='The informed lesson schedule does not exist.'
)

password_reset_does_not_exists = HTTPException(
    status_code = status.HTTP_404_NOT_FOUND,
    detail='O token informado não é associado nenhum processo de alteração de senha.'
)

password_and_confirm_password_are_not_equal = HTTPException(
    status_code = status.HTTP_400_BAD_REQUEST,
    detail='As senhas informadas são diferentes.'
)

expired_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='O token está expirado.'
)

email_already_taken = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='E-mail já cadastrado.'
)

username_already_taken = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Nome de usuário já cadastrado.'
)

student_doest_not_exists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Estudante informado não existe.'
)