from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from api.routers.dependencies import db_dependency
from api.models.user import UserIn, UserOut
from api.service.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    path="/",
    operation_id="createUser",
    status_code=HTTP_201_CREATED,
    response_model=UserOut,
)
async def create_user(
        user_in: UserIn,
        db: AsyncSession = Depends(db_dependency),
):
    user_service = UserService(db=db)
    return await user_service.create_user(user_in=user_in)


@router.get(
    path="/",
    operation_id="getUsers",
    status_code=HTTP_200_OK,
    response_model=list[UserOut],
)
async def get_users(
        db: AsyncSession = Depends(db_dependency),
):
    user_service = UserService(db=db)
    return await user_service.get_all_users()
