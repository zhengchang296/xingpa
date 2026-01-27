import json
import os
import uuid
from PIL import Image

def generate_sprites_json(texture_path, name_prefix, images_per_row, rows_count, path_id, output_folder):
    """
    自动切割纹理图片为小矩形区域，并为每个矩形生成 Sprite 的 JSON 数据。

    Args:
        texture_path (str): 纹理图片路径。
        name_prefix (str): 每帧 JSON 的名称前缀。
        images_per_row (int): 每行的图片数量。
        rows_count (int): 图片的总行数。
        path_id (int): 纹理的 m_PathID 值。
        output_folder (str): JSON 文件的输出目录。
    """
    try:
        # 打开纹理图片并获取宽度、高度
        texture = Image.open(texture_path)
        texture_width, texture_height = texture.size
        print(f"纹理图片大小：{texture_width}x{texture_height}")

        # 计算单帧宽高
        frame_width = texture_width // images_per_row
        frame_height = texture_height // rows_count
        print(f"每帧大小：{frame_width}x{frame_height}")

        os.makedirs(output_folder, exist_ok=True)
        frame_index = 0
        sprites = []

        # 遍历行和列，切割图片并生成对应的 JSON 信息
        for row in range(rows_count):
            for col in range(images_per_row):
                left = col * frame_width
                upper = row * frame_height

                # 生成随机的 `second` 字段值
                second_id = int(uuid.uuid4().int % (10**18))

                # 生成单帧 JSON 数据
                sprite = {
                    "m_Name": f"{name_prefix}_{frame_index:05d}",
                    "m_Rect": {  # 当前帧在图片的裁剪区域
                        "x": float(left),
                        "y": float(upper),
                        "width": float(frame_width),
                        "height": float(frame_height)
                    },
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
                            "data[2]": frame_index,
                            "data[3]": 0
                        },
                        "second": second_id  # 使用UUID随机生成唯一值
                    },
                    "m_AtlasTags": {
                        "Array": []
                    },
                    "m_SpriteAtlas": {
                        "m_FileID": 0,
                        "m_PathID": 0
                    },
                    "m_RD": {
                        "texture": {
                            "m_FileID": 0,
                            "m_PathID": path_id  # 用户输入的 path_id
                        },
                        "alphaTexture": {
                            "m_FileID": 0,
                            "m_PathID": 0
                        },
                        "secondaryTextures": {
                            "Array": []
                        },
                        "m_IndexBuffer": {
                            "Array": []
                        },
                        "m_VertexData": {
                            "m_VertexCount": 4,
                            "m_Channels": {
                                "Array": [
                                    { "stream": 0, "offset": 0, "format": 0, "dimension": 3 },
                                    { "stream": 1, "offset": 0, "format": 0, "dimension": 2 }
                                ]
                            },
                            "m_DataSize": []
                        },
                        "m_SubMeshes": {
                            "Array": []
                        },
                        "textureRect": {
                            "x": float(left),
                            "y": float(upper),
                            "width": float(frame_width),
                            "height": float(frame_height)
                        },
                        "textureRectOffset": { "x": 0.0, "y": 0.0 },
                        "atlasRectOffset": { "x": 0.0, "y": 0.0 },
                        "settingsRaw": 128,
                        "uvTransform": {
                            "x": 1.0,
                            "y": 1.0,
                            "z": 1.0,
                            "w": 1.0
                        },
                        "downscaleMultiplier": 1.0
                    },
                    "m_PhysicsShape": { "Array": [] },
                    "m_Bones": { "Array": [] }
                }

                # 保存每帧 JSON 文件
                frame_output_path = os.path.join(output_folder, f"{name_prefix}_{frame_index:05d}.json")
                with open(frame_output_path, 'w', encoding='utf-8') as f:
                    json.dump(sprite, f, ensure_ascii=False, indent=4)

                print(f"生成 JSON 文件：{frame_output_path}")
                sprites.append(sprite)
                frame_index += 1

        # 保存整合的合并 JSON 文件
        all_sprites_path = os.path.join(output_folder, f"{name_prefix}_all_sprites.json")
        with open(all_sprites_path, 'w', encoding='utf-8') as f:
            json.dump({"Sprites": sprites}, f, ensure_ascii=False, indent=4)

        print(f"生成完成！合并后的 JSON 保存到：{all_sprites_path}\n")

        # 测试输出前 3 个结果以供预览
        print("====== 示例 JSON 输出 (前3帧) ======")
        print(json.dumps(sprites[:3], ensure_ascii=False, indent=4))

    except Exception as e:
        print(f"生成 JSON 失败！错误信息：{e}")

def main():
    print("\n=== 自动生成 Sprite JSON 文件 ===")
    # 获取用户输入
    try:
        texture_path = input("请输入纹理图片路径：").strip()
        if not os.path.isfile(texture_path):
            print("纹理文件路径无效，请重新输入！")
            return

        name_prefix = input("请输入 Sprite 前缀名称（如 Walk、Run 等）：").strip()
        path_id = int(input("请输入纹理的 m_PathID 值（例如 -1234567890）：").strip())
        images_per_row = int(input("请输入每行的图片数量：").strip())
        rows_count = int(input("请输入图片的总行数：").strip())
        output_folder = input("请输入 JSON 输出目录（默认：generated_sprites）：").strip() or "generated_sprites"

        # 调用生成 JSON 的函数
        generate_sprites_json(texture_path, name_prefix, images_per_row, rows_count, path_id, output_folder)

    except Exception as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    main()