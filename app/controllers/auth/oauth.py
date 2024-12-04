from ...dependencies.githubprovider import get_user
from ...dependencies.token import create_token
from ...utils.models import GitUser
from prisma import Prisma

prisma = Prisma()


async def github_login(code:str):
    await prisma.connect()
    auth_data = get_user(code)

    user = await prisma.user.find_first(where={"githubid":auth_data["id"]})

    if user != None and user.email != auth_data["email"]:
        user = await prisma.user.update(where={"id":user.id}, data={"email":auth_data["email"]})

    if not user or user == None:
        user = await prisma.user.create(data={
            "name":auth_data["name"],
            "email":auth_data["email"],
            "avatar":auth_data["avatar_url"],
            "githubid":auth_data["id"],
            "income":5000
        })

    token = create_token(user.id)
    await prisma.disconnect()

    return {"name":user.name, "success":True, "accessToken":token}