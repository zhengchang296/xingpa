# 生成 Sprite JSON 和调整 AnimationClip 的 JSON 文件的脚本

import json
import os

# 生成 Sprite JSON 的函数

def generate_sprite_json(sprite_data, output_file):
    """
    根据提供的精灵数据生成 JSON 文件。
    
    :param sprite_data: 包含精灵信息的字典。
    :param output_file: 输出的 JSON 文件名。
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sprite_data, f, ensure_ascii=False, indent=4)
    print(f'生成的精灵 JSON 文件: {output_file}')

# 调整 AnimationClip 的函数

def adjust_animation_clip(animation_data, output_file):
    """
    根据提供的动画剪辑数据调整并生成新的 JSON 文件。
    
    :param animation_data: 包含动画剪辑信息的字典。
    :param output_file: 输出的 JSON 文件名。
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(animation_data, f, ensure_ascii=False, indent=4)
    print(f'调整后的 animation clip JSON 文件: {output_file}')

# 示例数据
sprite_data = {
    "sprites": [
        {"name": "sprite1", "image": "sprite1.png", "x": 0, "y": 0},
        {"name": "sprite2", "image": "sprite2.png", "x": 32, "y": 0}
    ]
}

animation_data = {
    "animationClips": [
        {"name": "walk", "frames": [0, 1, 2, 3]},
        {"name": "jump", "frames": [4, 5, 6]}
    ]
}

# 运行示例
generate_sprite_json(sprite_data, 'sprites.json')
adjust_animation_clip(animation_data, 'animationClips.json')
