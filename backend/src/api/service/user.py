import logging

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from api.database.repository.user import UserRepository
from api.database.table_models import User
from api.models.user import UserOut, UserIn
from api.shared.password_helper import hash_password

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db=db)

    async def get_all_users(self) -> list[UserOut]:
        try:
            users = await self.repo.get_all()
            return [self.map_to_response_model(user=user) for user in users]
        except Exception as e:
            logger.error(f"Error getting all {self.repo.model.__name__}: {e}")
            return []

    async def create_user(self, user_in: UserIn) -> UserOut:
        try:
            existing_user = await self.repo.get_first_by_field(field_name="username", field_value=user_in.username)
            if existing_user:
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Username already taken")

            new_user = await self.repo.create(
                instance=User(
                    username=user_in.username,
                    password=hash_password(user_in.password),
                )
            )
            return self.map_to_response_model(user=new_user)
        except HTTPException:
            raise  # Re-raise HTTP exceptions for FastAPI to handle
        except Exception as e:
            logger.error(f"Error creating {self.repo.model.__name__}: {e}")
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    @staticmethod
    def map_to_response_model(user: User) -> UserOut:
        return UserOut(
            id=user.id,
            username=user.username,
        )
