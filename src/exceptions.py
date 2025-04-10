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
    detail="This action is forbiden."
)

teacher_does_not_exist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="The informed user does not exists."
)

informed_user_is_not_teacher = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The informed user is not a teacher."
)

lesson_does_not_exist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="The informed lesson does not exist."
)