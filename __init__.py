import json
import os
from nonebot import get_bot
from hoshino import get_self_ids, logger

def get_config(filepath):
    with open(filepath, "r", encoding="UTF-8") as f:
        return json.load(f)
    

def savef(data, filepath):
    with open(filepath, mode= "w" , encoding="UTF-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

FILEPATH = os.path.join(os.path.dirname(__file__), "cache.json")
config = get_config(FILEPATH)
private_cache = config["private"]
group_cache = config["group"]

async def private_send(qid, msg):
    bots = get_self_ids()
    bot = get_bot()
    try:
        if len(bots) == 1:
            await bot.send_private_msg(user_id=int(qid), message = msg)
            return
        if not (bid:= private_cache.get(str(qid), 0)):
            for sid in bots:
                try:
                    await bot.send_private_msg(self_id = sid, user_id=int(qid), message = msg)
                    private_cache[str(qid)] = sid
                    savef(config, FILEPATH)
                    return
                except:
                    pass
            else:
                logger.error(f"QQ{qid}未找到")
        else:
            await bot.send_private_msg(self_id = bid, user_id=int(qid), message = msg)
    except:
        if len(bots) > 1:
            private_cache[str(qid)] = 0
            savef(config, FILEPATH)
        logger.error(f"QQ{qid}发送失败，可能已经更换bot")

async def group_send(group, msg):
    bots = get_self_ids()
    bot = get_bot()
    try:
        if len(bots) == 1:
            await bot.send_group_msg(group_id=int(group), message = msg)
            return
        if not (bid:= group_cache.get(str(group), 0)):
            for sid in bots:
                try:
                    await bot.send_group_msg(self_id = bid, group_id=int(group), message = msg)
                    group_cache[group] = sid
                    print(config)
                    savef(config, FILEPATH)
                    return
                except:
                    pass
            else:
                logger.error(f"群{group}未找到")
        else:
            await bot.send_group_msg(self_id = bid, group_id=int(group), message = msg)
    except:
        if len(bots) > 1:
            group_cache[group] = 0
            savef(config, FILEPATH)
        logger.error(f"群{group}发送失败，可能已经更换bot")

