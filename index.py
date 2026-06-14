async def create_user(session, name:str, email:str):
    user = User(name = name, email = email)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(session, user_id:int):
    await session.get(User, user_id)

from sqlalchemy import select

async def get_user_by_email(session, user_email:str):
    result = await session.execute(select(User).where(User.email == user_email))
    return result.scalar_one_or_none()

async def user_update(session, user_id:int, new_name:str):
    user = await session.get(User, user_id)
    if not user:
        return None
    user.name = new_name
    await session.commit()
    await session.refresh(user)
    return user

async def delete_user(session, user_id:int):
    user = await session.get(User, user_id)
    if not user:
        return None
    await session.delete(user)
    await session.commit()
    return True