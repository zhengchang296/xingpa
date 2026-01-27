# -*- coding: utf-8 -*-
import os
import json
import random
from PIL import Image


def 生成SpriteJson(输出目录, 图片路径, 名称, 帧数, 行数, 每行数量):
    """生成 JSON 文件"""
    try:
        # 打开图片
        图片 = Image.open(图片路径)
        图片宽度, 图片高度 = 图片.size
        print(f"\n🎨 图片加载成功：{图片路径} ，尺寸：{图片宽度}x{图片高度}")
        
        # 校验帧数是否超出图片支持范围
        最大帧数 = 行数 * 每行数量
        if 帧数 > 最大帧数:
            print(f"⚠️ 警告：帧数 ({帧数}) 超出图片支持的最大帧数 ({最大帧数})。帧数将被裁剪为 {最大帧数}")
            帧数 = 最大帧数

        # 创建输出目录
        if not os.path.exists(输出目录):
            os.makedirs(输出目录)
            print(f"✅ 创建输出目录：{输出目录}")

        # 开始生成 JSON 文件
        for 索引 in range(帧数):
            行 = 索引 // 每行数量
            列 = 索引 % 每行数量
            小图宽度 = 图片宽度 / 每行数量
            小图高度 = 图片高度 / 行数

            # 确定小图的矩形区域
            矩形 = {
                "x": 列 * 小图宽度,
                "y": 行 * 小图高度,
                "width": 小图宽度,
                "height": 小图高度
            }

            # 创建唯一标识符 second
            while True:
                二级键 = random.randint(1, 2**63 - 1)
                if 二级键 not in {data['m_RenderDataKey']['second'] for data in []}:
                    break

            # 构建 JSON 数据
            sprite数据 = {
                "m_Name": f"{名称}_{索引:05d}",
                "m_Rect": 矩形,
                "textureRect": 矩形,
                "m_RenderDataKey": {
                    "second": 二级键
                }
            }

            # 写入 JSON 文件
            json路径 = os.path.join(输出目录, f"{sprite数据['m_Name']}.json")
            with open(json路径, 'w', encoding='utf-8') as 输出:
                json.dump(sprite数据, 输出, ensure_ascii=False, indent=4)
            print(f"✅ 已生成 JSON 文件：{json路径}")

        print(f"\n🎉 成功生成 {帧数} 个 JSON 文件，保存在：{输出目录}")

    except FileNotFoundError:
        print(f"❌ 图片路径无效或文件不存在：{图片路径}")
    except Exception as e:
        print(f"❌ 发生错误：{e}")


def 获取用户输入_无默认值(prompt, 类型=str):
    """
    要求用户输入信息，不提供默认值，必须输入有效值。
    """
    while True:
        输入值 = input(f"{prompt}: ").strip()
        if not 输入值:
            print("❌ 输入不能为空，请重新输入！")
            continue
        try:
            return 类型(输入值)
        except ValueError:
            print(f"❌ 无效的输入，请输入正确的 {类型.__name__} 类型值！")


def main():
    """主程序"""
    print("\n🎉 欢迎使用 Sprite JSON 生成器 🎉")
    print("=" * 60)

    while True:
        print("\n请根据提示输入所需的参数：")
        
        # 要求用户输入图片路径
        图片路径 = 获取用户输入_无默认值("请输入图片路径（支持拖动图片到终端中）")
        if not os.path.isfile(图片路径):
            print(f"❌ 图片路径无效！文件不存在：{图片路径}\n")
            continue

        # 要求用户输入输出目录
        输出目录 = 获取用户输入_无默认值("请输入输出目录路径（支持拖动文件夹到终端中）")
        if not os.path.isdir(输出目录):
            try:
                os.makedirs(输出目录)
                print(f"✅ 输出目录已自动创建：{输出目录}")
            except Exception as e:
                print(f"❌ 无法创建输出目录：{输出目录}")
                continue

        # 其他参数
        名称 = 获取用户输入_无默认值("请输入 JSON 文件名称前缀")
        帧数 = 获取用户输入_无默认值("请输入生成的 Sprite 总帧数", int)
        行数 = 获取用户输入_无默认值("请输入图像的行数", int)
        每行数量 = 获取用户输入_无默认值("请输入每行的图片数量", int)

        # 确认参数
        print("\n🔧 参数已经设置如下：")
        print(f"  图片路径       : {图片路径}")
        print(f"  输出目录       : {输出目录}")
        print(f"  JSON 名称前缀  : {名称}")
        print(f"  帧数           : {帧数}")
        print(f"  行数           : {行数}")
        print(f"  每行数量       : {每行数量}")
        
        确认 = input("是否确认生成 JSON 文件？ (输入 yes/no): ").strip().lower()
        if 确认 == "yes":
            生成SpriteJson(输出目录, 图片路径, 名称, 帧数, 行数, 每行数量)
        else:
            print("\n🚫 已取消操作，重新设置参数...\n")
            continue

        # 询问用户是否继续操作
        是否继续 = input("\n是否继续生成 JSON 文件？ (输入 yes/no): ").strip().lower()
        if 是否继续 != "yes":
            print("\n👋 感谢使用 Sprite JSON 生成器！程序退出。")
            break

        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    # 捕获 Ctrl+C 优雅退出
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已终止。感谢使用 Sprite JSON Generator！")
