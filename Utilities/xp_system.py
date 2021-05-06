async def update_data(xp_data, author, server):
    if f"{server}_{server.id}" not in xp_data:
        xp_data[f"{server}_{server.id}"] = {}
    if str(author).replace("#", "_") not in xp_data[f"{server}_{server.id}"]:
        xp_data[f"{server}_{server.id}"][str(author).replace("#", "_")] = {}
        xp_data[f"{server}_{server.id}"][str(author).replace("#", "_")]["experience"] = 0
        xp_data[f"{server}_{server.id}"][str(author).replace("#", "_")]["level"] = 1
    return xp_data


async def add_experience(xp_data, author, server, value=5):
    xp_data[f"{server}_{server.id}"][str(author).replace("#", "_")]["experience"] += value
    return xp_data


async def level_up(xp_data, author, channel, server):
    experience = xp_data[f"{server}_{server.id}"][str(author).replace("#", "_")]["experience"]
    current_level = xp_data[f"{server}_{server.id}"][str(author).replace("#", "_")]["level"]
    new_level = int(((0.3 * (experience ** 0.5)) + 1) // 1)
    if current_level < new_level:
        xp_data[f"{server}_{server.id}"][str(author).replace("#", "_")]["level"] = new_level
        await channel.send(f"{author.mention} has just leveled up to Level {new_level}!")

    return xp_data


def sort_xp_data(data):
    return {k: v for k, v in sorted(data.items(), key=lambda item: item[1]["experience"], reverse=True)}


def ratelimit_check(cooldown, message):
    bucket = cooldown.get_bucket(message)
    return bucket.update_rate_limit()
