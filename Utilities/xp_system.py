from math import ceil


async def update_data(data, user):
  if not str(user) in data:
    data[str(user)] = {}
    data[str(user)]["xp"] = 0
    data[str(user)]["level"] = 1


async def add_xp(data, user, value):
  data[str(user)]["xp"] += value


async def level_up(data, user):
  xp = data[str(user)]["xp"]
  level = data[str(user)]["level"]
  new_level = int(ceil(0.3 * (xp ** 0.5)))

  if new_level > level:
    data[str(user)]["level"] = new_level
