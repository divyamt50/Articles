from models_practice import User

# create function
async def create_user(session, email:str):
    user = User(email = email)
    session.add(user)
    await session.commit()
    await session.refresh()
    return user

async def get_user_by_id(session, user_id:int):
    user = await session.get(User, user_id)
    if user:
        return user
    else:
        return None