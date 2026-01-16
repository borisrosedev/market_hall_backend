from sqlmodel import Session, select

from app.models.db_models import __all_models__
import uuid
from app.api.crud.users import create_user
from app.core.config import settings
from app.models.db_models.user import User
from app.models.non_db_models.user import UserCreate, UserRoles


def init_db(session: Session) -> User:
    """
    return super user
    """

    user = session.exec(select(User).where(User.email == settings.FIRST_SUPERUSER)).first()
    if user:
        return user

    user_in = UserCreate(
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        role=UserRoles.admin.value,
        firstname="Admin",
        lastname="User",
        # is_banned=False,
    )
    user = create_user(session=session, user_create=user_in)

    from app.models.db_models.cart import Cart  # avoid cycles

    existing_cart = session.exec(select(Cart).where(Cart.user_id == user.id)).first()

    if not existing_cart:
        session.add(Cart(user_id=user.id))
        # commit at the end
        session.commit()
    else:
        # no unnecessary re-commit
        session.flush()

    return user
