async def update_data(xp_data, author, server):
    if f"{server}#{server.id}" not in xp_data:
        xp_data[f"{server}#{server.id}"] = {}

    if str(author) not in xp_data[f"{server}#{server.id}"]:
        xp_data[f"{server}#{server.id}"][str(author)] = {}
        xp_data[f"{server}#{server.id}"][str(author)]["experience"] = 0
        xp_data[f"{server}#{server.id}"][str(author)]["level"] = 1

    return xp_data


async def add_experience(xp_data, author, server, value=5):
    xp_data[f"{server}#{server.id}"][str(author)]["experience"] += value
    return xp_data


async def level_up(xp_data, author, channel, server):
    experience = xp_data[f"{server}#{server.id}"][str(author)]["experience"]
    current_level = xp_data[f"{server}#{server.id}"][str(author)]["level"]
    new_level = int(((0.3 * (experience ** 0.5)) + 1) // 1)
    if current_level < new_level:
        xp_data[f"{server}#{server.id}"][str(author)]["level"] = new_level
        await channel.send(f"{author.mention} has just leveled up to Level {new_level}!")

    return xp_data


def sort_xp_data(data):
    return {k: v for k, v in sorted(data.items(), key=lambda item: item[1]["experience"], reverse=True)}


def ratelimit_check(cooldown, message):
    bucket = cooldown.get_bucket(message)
    return bucket.update_rate_limit()
