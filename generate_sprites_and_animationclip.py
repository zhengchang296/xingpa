import json
import os
from PIL import Image


def adjust_animation_clip(animation_clip, sprite_frames):
    """
    调整 AnimationClip 数据，并根据输入的帧数更新字段。

    Args:
        animation_clip (dict): 原始 AnimationClip 数据。
        sprite_frames (int): 用户输入的总帧数。

    Returns:
        dict: 修改后的 AnimationClip 数据。
    """
    dense_clip = animation_clip.get("m_Clip", {}).get("data", {}).get("m_DenseClip", {})
    original_frame_count = dense_clip.get("m_FrameCount", 0)
    original_sample_rate = dense_clip.get("m_SampleRate", 30.0)
    original_stop_time = animation_clip.get("m_StopTime", 0.0)
    frame_count = sprite_frames
    stop_time = frame_count / original_sample_rate  # 动态计算停止时间

    # 动态调整 m_DenseClip
    dense_clip["m_FrameCount"] = frame_count
    dense_clip["m_BeginTime"] = 0.0
    animation_clip["m_StopTime"] = stop_time

    # 动态调整 StreamedClip 数据
    streamed_clip_array = animation_clip.get("m_StreamedClip", {}).get("data", {}).get("Array", [])
    original_streamed_length = len(streamed_clip_array)
    if original_streamed_length > frame_count:
        streamed_clip_array = streamed_clip_array[:frame_count]
    animation_clip["m_StreamedClip"]["data"]["Array"] = streamed_clip_array

    muscle_clip_size = animation_clip.get("m_MuscleClipSize", 0)

    # 提示信息
    message = (
        f"动态调整 AnimationClip 数据：\n"
        f"- 原始帧率 (m_SampleRate)：{original_sample_rate}（保持不变）\n"
        f"- 总帧数 (m_FrameCount)：\n"
        f"\t- 原始值：{original_frame_count}\n"
        f"\t- 修改后：{frame_count}\n"
        "\n"
        f"- 停止时间 (m_StopTime)：\n"
        f"\t- 原始值：{original_stop_time}\n"
        f"\t- 修改后：{stop_time}\n"
        "\n"
        f"- StreamedClip 数据总长度：\n"
        f"\t- 原始长度：{original_streamed_length}\n"
        f"\t- 调整后：{len(streamed_clip_array)}\n"
        "\n"
        f"- MuscleClipSize（未修改，当前值为 {muscle_clip_size}）\n"
        "请确认 MuscleClipSize 是否符合期望。\n"
        "\n"
        "⚠️ 提示：StreamedClip, FrameCount, SampleRate, StopTime, MuscleClipSize 的值可能需要进一步手动调整。\n"
    )
    print(message)
    return animation_clip


def adjust_pptr_curve_mapping(animation_clip, sprite_frames):
    """
    动态调整 AnimationClip 的 pptrCurveMapping 数据长度，并输出提醒信息。

    Args:
        animation_clip (dict): AnimationClip JSON 数据。
        sprite_frames (int): 总帧数。

    Returns:
        dict: 修改后的 AnimationClip 数据。
    """
    pptr_curve_array = animation_clip.get("m_ClipBindingConstant", {}).get("pptrCurveMapping", {}).get("Array", [])
    original_length = len(pptr_curve_array)

    if original_length > sprite_frames:
        pptr_curve_array = pptr_curve_array[:sprite_frames]
        message = (
            f"调整 pptrCurveMapping 数据：\n"
            f"- 原始长度：{original_length}\n"
            f"- 调整后长度：{len(pptr_curve_array)}\n"
            f"- 截断多余的 {original_length - len(pptr_curve_array)} 项。\n"
        )
    else:
        message = (
            f"调整 pptrCurveMapping 数据：\n"
            f"- 原始长度：{original_length}\n"
            f"- 调整后保持不变：{len(pptr_curve_array)}\n"
            "不足帧数或一致，无需修改。\n"
        )
    animation_clip["m_ClipBindingConstant"]["pptrCurveMapping"]["Array"] = pptr_curve_array
    print(message)
    return animation_clip


def main():
    # 用户输入
    texture_path = input("请输入纹理图片路径：").strip()
    clip_path = input("请输入 AnimationClip 文件路径：").strip()
    output_folder = input("请输入输出目录（默认：output）：").strip() or "output"
    total_frames = int(input("总帧数（例如：20）：").strip())
    name_prefix = input("新的 Sprite 和 AnimationClip 名称前缀（例如：Run）：").strip()

    # 加载 AnimationClip 的 JSON 文件
    with open(clip_path, "r", encoding="utf-8") as f:
        animation_clip = json.load(f)

    # 调整 AnimationClip 数据
    animation_clip["m_Name"] = name_prefix
    animation_clip = adjust_animation_clip(animation_clip, total_frames)
    animation_clip = adjust_pptr_curve_mapping(animation_clip, total_frames)

    # 保存结果
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{name_prefix}_adjusted_animation.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(animation_clip, f, ensure_ascii=False, indent=4)

    print(f"\n文件已生成，请检查：\n- 输出路径：{output_path}")


if __name__ == "__main__":
    main()
