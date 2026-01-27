# -*- coding: utf-8 -*-
import os
import json
import random
import argparse
from PIL import Image

def 生成SpriteJson(输出目录, 图片路径, 名称, 帧数, 行数, 每行数量, texture_m_PathID):
    # 打开纹理图片
    图片 = Image.open(图片路径)
    图片宽度, 图片高度 = 图片.size

    # 计算切割矩形的宽度和高度
    小图宽度 = 图片宽度 / 每行数量
    小图高度 = 图片高度 / 行数

    # 确保输出目录存在
    if not os.path.exists(输出目录):
        os.makedirs(输出目录)

    索引 = 0
    生成的JSON列表 = []
    已用随机值 = set()  # 用于存储唯一的随机值

    for 行 in range(行数):
        for 列 in range(每行数量):
            if 索引 >= 帧数:  # 达到所需帧数后停止
                break

            # 计算每个Sprite的矩形区域
            X = 列 * 小图宽度
            Y = 行 * 小图高度

            矩形 = {
                "x": X,
                "y": Y,
                "width": 小图宽度,
                "height": 小图高度
            }

            # 随机生成唯一RenderDataKey->second值
            while True:
                second = random.randint(1, 2**63 - 1)
                if second not in 已用随机值:
                    已用随机值.add(second)
                    break

            # 构建Sprite JSON 结构
            sprite数据 = {
                "m_Name": f"{名称}_{索引:05d}",
                "m_Rect": 矩形,
                "m_Offset": {
                    "x": 0.0,
                    "y": 0.0
                },
                "m_Border": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0,
                    "w": 0.0
                },
                "m_PixelsToUnits": 100.0,
                "m_Pivot": {
                    "x": 0.5,
                    "y": 0.5
                },
                "m_Extrude": 0,
                "m_IsPolygon": False,
                "m_RenderDataKey": {
                    "first": {
                        "data[0]": 0,
                        "data[1]": 0,
                        "data[2]": 0,
                        "data[3]": 0
                    },
                    "second": second
                },
                "m_Bindpose": {
                    "Array": []
                },
                "textureRect": 矩形,
                "textureRectOffset": {
                    "x": 0.0,
                    "y": 0.0
                },
                "atlasRectOffset": {
                    "x": -1.0,
                    "y": -1.0
                },
                "settingsRaw": 128,  # 保留字段，默认值
                "uvTransform": {  # 清空为默认值
                    "x": 0.0,
                    "y": 0.0,
                    "z": 1.0,
                    "w": 1.0
                },
                "downscaleMultiplier": 1.0,
                "m_PhysicsShape": {
                    "Array": []
                },
                "m_Bones": {
                    "Array": []
                }
            }

            # 保存JSON文件
            json文件路径 = os.path.join(输出目录, f"{sprite数据['m_Name']}.json")
            with open(json文件路径, 'w', encoding='utf-8') as json文件:
                json.dump(sprite数据, json文件, ensure_ascii=False, indent=2)

            生成的JSON列表.append(sprite数据)
            索引 += 1

        if 索引 >= 帧数:
            break

    print(f"✅ 成功生成 {帧数} 个 JSON Sprite 文件，保存到 {输出目录}")
    return 生成的JSON列表

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成 JSON Sprite 文件。")
    parser.add_argument("--输出目录", type=str, required=True, help="存储 JSON 文件的输出目录。")
    parser.add_argument("--图片路径", type=str, required=True, help="输入图片的路径。")
    parser.add_argument("--名称", type=str, required=True, help="JSON 文件的名称前缀。")
    parser.add_argument("--帧数", type=int, required=True, help="生成的 Sprite 数量（帧数）。")
    parser.add_argument("--行数", type=int, required=True, help="图像的行数。")
    parser.add_argument("--每行数量", type=int, required=True, help="每行的图片数量。")
    parser.add_argument("--texture_m_PathID", type=int, default=0, help="纹理的 Path ID（备用参数）。")

    args = parser.parse_args()

    生成SpriteJson(
        输出目录=args.输出目录,
        图片路径=args.图片路径,
        名称=args.名称,
        帧数=args.帧数,
        行数=args.行数,
        每行数量=args.每行数量,
        texture_m_PathID=args.texture_m_PathID
    )
