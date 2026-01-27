import json
import os
from PIL import Image


def generate_sprites(texture_path, name_prefix, images_per_row, rows_count, total_frames, path_id, output_folder):
    """
    根据用户输入的行数和列数切割图片，生成对应数量的 Sprite 文件。

    Args:
        texture_path (str): 纹理图片路径。
        name_prefix (str): Sprite 的名称前缀。
        images_per_row (int): 每行的图片数量。
        rows_count (int): 总行数。
        total_frames (int): 总帧数，由用户直接指定。
        path_id (int): 纹理文件的 Path ID。
        output_folder (str): 输出的目标文件夹。

    Returns:
        list: 生成的 Sprite 信息列表。
    """
    texture = Image.open(texture_path)
    texture_width, texture_height = texture.size
    frame_width = texture_width // images_per_row
    frame_height = texture_height // rows_count
    sprites = []
    os.makedirs(output_folder, exist_ok=True)

    print(f"纹理图片 '{texture_path}' 的总尺寸为宽 {texture_width}px, 高 {texture_height}px。")
    print(f"每行 {images_per_row} 张图片，共 {rows_count} 行，每帧宽度为 {frame_width}px，高度为 {frame_height}px。")
    print(f"根据输入的帧数，总计生成 {total_frames} 个 Sprite。")

    for i in range(total_frames):
        row = i // images_per_row
        col = i % images_per_row
        left = col * frame_width
        upper = row * frame_height

        sprite_name = f"{name_prefix}_{i:05d}"
        sprite = {
            "m_Name": sprite_name,
            "m_Rect": {
                "x": float(left),
                "y": float(upper),
                "width": float(frame_width),
                "height": float(frame_height),
            },
            "m_RD": {"texture": {"m_FileID": 0, "m_PathID": path_id}},
        }
        sprites.append(sprite)

        # 保存每帧 Sprite JSON
        sprite_path = os.path.join(output_folder, f"{sprite_name}.json")
        with open(sprite_path, "w", encoding="utf-8") as f:
            json.dump(sprite, f, ensure_ascii=False, indent=4)

    print(f"Sprite 数据生成完成，其文件保存在 '{output_folder}'，名称前缀为 '{name_prefix}'。")
    return sprites


def adjust_animation_clip(animation_clip, sprite_frames):
    """
    调整 AnimationClip 数据，并记录所有关键字段的改动提醒。

    Args:
        animation_clip (dict): 原始 AnimationClip 数据。
        sprite_frames (int): 总帧数。

    Returns:
        dict: 修改后的 AnimationClip 数据。
        dict: 提醒信息，包含动态调整的字段。
    """
    dense_clip = animation_clip.get("m_Clip", {}).get("data", {}).get("m_DenseClip", {})
    streamed_clip = animation_clip.get("m_Clip", {}).get("data", {}).get("m_StreamedClip", {}).get("data", {}).get("Array", [])
    pptr_curve_mapping = animation_clip.get("m_ClipBindingConstant", {}).get("pptrCurveMapping", {}).get("Array", [])

    # 动态调整帧数：原始帧数、帧率和停止时间
    original_frame_count = dense_clip.get("m_FrameCount", 0)
    original_sample_rate = dense_clip.get("m_SampleRate", 30.0)  # 默认帧率 30.0
    original_stop_time = dense_clip.get("m_BeginTime", 0.0) + (original_frame_count / original_sample_rate)  # 计算原始停止时间
    frame_count = sprite_frames
    updated_stop_time = frame_count / original_sample_rate

    # 修改 AnimationClip 的帧数信息
    dense_clip["m_FrameCount"] = frame_count
    dense_clip["m_BeginTime"] = 0.0
    animation_clip["m_StopTime"] = updated_stop_time

    # StreamedClip 修改情况
    original_streamedclip_count = len(streamed_clip)
    if original_streamedclip_count > sprite_frames:
        streamed_clip = streamed_clip[:sprite_frames * 7]  # 截取多余项
        streamedclip_message = (f"StreamedClip 原始数量为 {original_streamedclip_count}，"
                                 f"已截取至 {sprite_frames * 7} 项。")
    else:
        streamedclip_message = "StreamedClip 未调整数量。"

    # pptrCurveMapping 修改情况
    original_mapping_count = len(pptr_curve_mapping)
    if original_mapping_count > sprite_frames:
        pptr_curve_mapping = pptr_curve_mapping[:sprite_frames]
        pptr_curve_mapping_message = (f"pptrCurveMapping 原始数量为 {original_mapping_count}，"
                                       f"已截取至 {sprite_frames} 项。")
    elif original_mapping_count < sprite_frames:
        pptr_curve_mapping_message = (f"pptrCurveMapping 原始数量为 {original_mapping_count}，"
                                       "未补充，保持原样。")
    else:
        pptr_curve_mapping_message = "pptrCurveMapping 数量未变化。"

    # 更新提醒信息
    reminders = {
        "original_sample_rate": original_sample_rate,
        "original_frame_count": original_frame_count,
        "updated_frame_count": frame_count,
        "original_stop_time": round(original_stop_time, 6),
        "calculated_stop_time": round(updated_stop_time, 6),
        "streamedclip_message": streamedclip_message,
        "pptr_curve_mapping_message": pptr_curve_mapping_message,
    }

    # 返回修改后的 AnimationClip 和提醒信息
    animation_clip["m_Clip"]["data"]["m_StreamedClip"]["data"]["Array"] = streamed_clip
    animation_clip["m_ClipBindingConstant"]["pptrCurveMapping"]["Array"] = pptr_curve_mapping
    return animation_clip, reminders


def show_reminders(reminders):
    """
    输出脚本执行后的提醒信息，按需求精细分组，并空一行区分。

    Args:
        reminders (dict): 包含所有提醒字段的字典。
    """
    print("\n=== 脚本运行结束，以下是本次操作的重要提醒信息 ===\n")

    # 第一组：帧率信息
    print("- 原始帧率 (m_SampleRate)：{:.1f}（保持不变）".format(reminders["original_sample_rate"]))
    print("\n")  # 空一行

    # 第二组：帧数信息
    print("- 原始帧数 (m_FrameCount)：{}".format(reminders["original_frame_count"]))
    print("- 新帧数 (updated_frame_count)：{}".format(reminders["updated_frame_count"]))
    print("\n")  # 空一行

    # 第三组：停止时间信息
    print("- 原始停止时间 (original_stop_time)：{:.6f}".format(reminders["original_stop_time"]))
    print("- 新停止时间 (updated_stop_time)：{:.6f}".format(reminders["calculated_stop_time"]))
    print("\n")  # 空一行

    # 第四组：StreamedClip 修改情况
    print("- StreamedClip 修改情况：{}".format(reminders["streamedclip_message"]))
    print("\n")  # 仅空一行

    # 第五组：pptrCurveMapping 修改情况
    print("- pptrCurveMapping 修改情况：{}".format(reminders["pptr_curve_mapping_message"]))
    print("\n")

    print("请检查以上字段是否符合预期！")


def main():
    while True:
        try:
            # 用户输入基础参数
            texture_path = input("请输入纹理图片路径：").strip()
            if not os.path.isfile(texture_path):
                print("错误：纹理图片路径不存在！")
                continue

            clip_path = input("请输入 AnimationClip JSON 文件路径：").strip()
            if not os.path.isfile(clip_path):
                print("错误：AnimationClip JSON 文件路径不存在！")
                continue

            output_folder = input("请输入输出目录（默认: output）：").strip() or "output"
            images_per_row = int(input("请输入每行的图片数量（例如 5）：").strip())
            rows_count = int(input("请输入总行数（例如 4）：").strip())
            total_frames = int(input("请输入需要生成的帧数（例如 20）：").strip())
            path_id = int(input("请输入纹理文件的 Path ID（例如 123456789）：").strip())
            name_prefix = input("请输入 Sprite 和 AnimationClip 的新名称前缀（例如 'Run'）：").strip()

            # 加载 AnimationClip JSON 数据
            with open(clip_path, "r", encoding="utf-8") as f:
                animation_clip = json.load(f)

            # 生成 Sprite JSON 数据
            generate_sprites(texture_path, name_prefix, images_per_row, rows_count, total_frames, path_id, output_folder)

            # 调整 AnimationClip JSON 数据
            animation_clip["m_Name"] = name_prefix  # 修改 AnimationClip 名称
            adjusted_clip, reminders = adjust_animation_clip(animation_clip, total_frames)

            # 保存调整后的 AnimationClip JSON
            output_clip_path = os.path.join(output_folder, f"{name_prefix}_adjusted_animation.json")
            os.makedirs(output_folder, exist_ok=True)
            with open(output_clip_path, "w", encoding="utf-8") as f:
                json.dump(adjusted_clip, f, ensure_ascii=False, indent=4)

            print(f"\nAnimationClip 文件已保存到：{output_clip_path}")

            # 显示提醒信息
            show_reminders(reminders)

        except Exception as e:
            print(f"程序发生错误：{e}")

        # 提示是否继续运行
        user_input = input("是否继续运行？输入 'n' 或 'no' 退出，按回车继续：").strip().lower()
        if user_input in ('n', 'no'):
            print("程序已退出。")
            break
