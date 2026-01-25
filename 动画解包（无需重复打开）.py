import struct
import traceback
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import argparse
from typing import Tuple, List
from dataclasses import dataclass
import UnityPy
import decimal
import os


class RoundError(Exception):
    """坐标舍入错误"""
    pass


class CoordNotPositive(RoundError):
    """坐标不为正数"""
    pass


class CoordNotInteger(RoundError):
    """坐标不接近整数"""
    pass


@dataclass
class Point:
    """二维点"""
    x: int
    y: int


@dataclass
class Size:
    """尺寸"""
    width: int
    height: int


@dataclass
class Rect:
    """矩形（由4个点组成）"""
    points: List[Point]
    
    def __init__(self, points: List[Point]):
        if len(points) != 4:
            raise ValueError("矩形必须有4个点")
        self.points = points


class RectMap:
    """矩形映射"""
    def __init__(self, uv_rect: Rect, xy_rect: Rect):
        self.uv_rect = uv_rect
        self.xy_rect = xy_rect
    
    def crop_then_paste(self, source_image: Image.Image, target_image: Image.Image):
        """从源图像裁剪然后粘贴到目标图像"""
        # 获取UV矩形的边界
        uv_points = self.uv_rect.points
        uv_x_min = min(p.x for p in uv_points)
        uv_y_min = min(p.y for p in uv_points)
        uv_x_max = max(p.x for p in uv_points)
        uv_y_max = max(p.y for p in uv_points)
        
        # 获取XY矩形的边界
        xy_points = self.xy_rect.points
        xy_x_min = min(p.x for p in xy_points)
        xy_y_min = min(p.y for p in xy_points)
        xy_x_max = max(p.x for p in xy_points)
        xy_y_max = max(p.y for p in xy_points)
        
        # 裁剪源图像
        cropped = source_image.crop((uv_x_min, uv_y_min, uv_x_max, uv_y_max))
        
        # 粘贴到目标图像
        target_image.paste(cropped, (xy_x_min, xy_y_min))


def round_coord(f: float) -> int:
    """
    对坐标进行四舍五入
    
    Args:
        f: 浮点数坐标
        
    Returns:
        舍入后的整数坐标
        
    Raises:
        CoordNotPositive: 如果坐标为负数
        CoordNotInteger: 如果坐标不接近整数
    """
    if f < -0.5:
        raise CoordNotPositive(f"坐标不为正数: {f}")
    
    round_diff = abs(f - round(f))
    if round_diff < 0.1:
        return int(round(f))
    else:
        raise CoordNotInteger(f"坐标不接近整数: {f}, 差值: {round_diff}")


def generate_grid(image, rows, cols):# 计算图片总大小
    draw = ImageDraw.Draw(image)
    
    cell_size = image.width // rows

    # 尝试加载字体，如果失败则使用默认字体
    try:
        # 尝试使用系统字体
        font_size = cell_size // 3
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            # Windows 中文字体
            font_size = cell_size // 3
            font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", font_size)
        except:
            # 使用默认字体
            font = ImageFont.load_default()
    
    # 绘制网格线
    for i in range(rows + 1):
        y = i * cell_size
        draw.line([(0, y), (image.width, y)], 
                 fill=None, width=1)
    
    for j in range(cols + 1):
        x = j * cell_size
        draw.line([(x, 0), (x, image.height)], 
                 fill=None, width=1)
    
    # 填充序号
    index = 1
    for i in range(rows):
        for j in range(cols):
            # 计算单元格中心位置
            x = j * cell_size + cell_size // 2
            y = i * cell_size + cell_size // 2
            
            # 绘制序号
            text = str(index)
            
            # 获取文本边界框来居中显示
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            text_x = x - text_width // 2
            text_y = y - text_height // 2
            
            draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
            
            index += 1
    

def restore_image(sprite_data, diced_texture: Image.Image, context: dict) -> Image.Image:
    """
    从切片纹理还原完整图像。
    提供遗漏的详细描述。
    """
    # 获取数据
    data = sprite_data.m_RD.m_VertexData.m_DataSize
    ptu = sprite_data.m_PixelsToUnits
    sprite_rect = sprite_data.m_Rect
    
    data_as_f32 = []
    for i in range(0, len(data), 4):
        f32_value = struct.unpack('<f', data[i:i+4])[0]  # 小端序
        data_as_f32.append(f32_value)
    
    split_index = len(data_as_f32) // 5 * 3
    xy = data_as_f32[:split_index]
    uv = data_as_f32[split_index:]

    xy_rects = []
    for i in range(0, len(xy), 12):
        rect_data = xy[i:i+12]
        if len(rect_data) < 12:
            break
        min_x, max_x = None, None
        points = []
        for j in range(0, 12, 3):
            x, y = (round_coord(rect_data[j] * ptu), round(0))
            points.append(Point(x, y))
        
        xy_rects.append(Rect(points))
    
    uv_rects = []
    for i in range(0, len(uv), 8):
        rect_data = uv[i:i+8]
