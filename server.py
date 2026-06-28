from fastmcp import FastMCP
from market_engine import MarketGame
import json
import os

mcp = FastMCP("ShangzhuoChiFan")

# 全局游戏对象
game = MarketGame()

SAVE_FILE = "savegame.json"

@mcp.tool()
def new_game() -> str:
    """开始新游戏"""
    global game
    game = MarketGame()
    return game.cmd("新局")

@mcp.tool()
def command(text: str) -> str:
    """向游戏发送指令，例如：菜场、去 veg_1、买 番茄、回家"""
    try:
        return game.cmd(text)
    except Exception as e:
        return f"执行失败：{str(e)}"

@mcp.tool()
def get_status() -> str:
    """查看当前游戏状态"""
    try:
        basket = getattr(game, "basket", {})
        fridge = getattr(game, "fridge", {})
        budget = getattr(game, "budget", 0)
        spent = getattr(game, "spent", 0)
        day = getattr(game, "day", 1)

        basket_text = "\n".join(
            [f"- {k} x{v}" for k, v in basket.items()]
        ) or "（空）"

        fridge_text = "\n".join(
            [f"- {k} x{v}" for k, v in fridge.items()]
        ) or "（空）"

        return f"""
第 {day} 天

预算：{budget} 元
已花费：{spent} 元

菜篮：
{basket_text}

冰箱：
{fridge_text}
"""
    except Exception as e:
        return f"读取状态失败：{str(e)}"

@mcp.tool()
def save_game() -> str:
    """保存游戏"""
    try:
        state = {
            "basket": getattr(game, "basket", {}),
            "fridge": getattr(game, "fridge", {}),
            "budget": getattr(game, "budget", 0),
            "spent": getattr(game, "spent", 0),
            "day": getattr(game, "day", 1),
            "affection": getattr(game, "affection", {}),
        }

        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

        return "游戏已保存。"
    except Exception as e:
        return f"保存失败：{str(e)}"

@mcp.tool()
def load_game() -> str:
    """读取游戏"""
    global game

    if not os.path.exists(SAVE_FILE):
        return "没有找到存档。"

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)

        game = MarketGame()

        game.basket = state.get("basket", {})
        game.fridge = state.get("fridge", {})
        game.budget = state.get("budget", 0)
        game.spent = state.get("spent", 0)
        game.day = state.get("day", 1)
        game.affection = state.get("affection", {})

        return "游戏已读取。"
    except Exception as e:
        return f"读取失败：{str(e)}"

@mcp.tool()
def help() -> str:
    """显示可用命令"""
    return """
常用指令：

新局
菜场
去 veg_1
去 egg_1
去 meat_1
看看
买 番茄
买 鸡蛋
回家
做法 番茄切块，鸡蛋打散...
她说 挺好吃的
"""

if __name__ == "__main__":
    mcp.run()