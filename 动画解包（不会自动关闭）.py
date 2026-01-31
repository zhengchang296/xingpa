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
    从切片纹理还原完整图像
    
    Args:
        sprite_data: 精灵数据对象，包含以下属性:
            - Sprite.m_RD.m_VertexData._typelessdata: 顶点数据（字节数组）
            - Sprite.m_PixelsToUnits: 像素到单位的转换因子
            - Sprite.m_Rect: 精灵矩形，包含 x, y, width, height
        diced_texture: 切片纹理图像（PIL Image对象）
        
    Returns:
        还原后的图像（PIL Image对象）
        
    Raises:
        RoundError: 坐标舍入错误
    """
    # 获取数据
    data = sprite_data.m_RD.m_VertexData.m_DataSize
    ptu = sprite_data.m_PixelsToUnits
    sprite_rect = sprite_data.m_Rect
    
    # 将字节数据转换为 f32 数组
    data_as_f32 = []
    for i in range(0, len(data), 4):
        f32_value = struct.unpack('<f', data[i:i+4])[0]  # 小端序
        data_as_f32.append(f32_value)
    
    # 分割数据为 xy 和 uv（前 3/5 是 xy，后 2/5 是 uv）
    split_index = len(data_as_f32) // 5 * 3
    xy = data_as_f32[:split_index]
    uv = data_as_f32[split_index:]

    # 处理 xy 坐标（每12个元素为一个矩形，每个点3个坐标）
    xy_rects = []
    for i in range(0, len(xy), 12):
        rect_data = xy[i:i+12]
        if len(rect_data) < 12:
            break
            
        # 每个矩形有4个点，每个点3个坐标

        min_x, max_x = None, None

        points = []
        for j in range(0, 12, 3):
            x = round_coord(rect_data[j] * ptu - sprite_rect.x)
            y = round(sprite_rect.height - (rect_data[j+1] * ptu - sprite_rect.y))
            if not min_x or x < min_x:
                min_x = x
            if not max_x or x > max_x:
                max_x = x
            points.append(Point(x, y))
        
        if context.get('grid') is None and min_x and max_x:
            context['grid'] = True
            cell_size = max_x - min_x + 8
            grid_size = diced_texture.width / cell_size / 5
            if round(grid_size) == grid_size:
                grid_size = int(grid_size)
                print('网格大小: {}x{}'.format(grid_size, grid_size))
                generate_grid(diced_texture, grid_size, grid_size)
            else:
                print('网格大小计算失败')
            
        
        xy_rects.append(Rect(points))
    
    # 获取切片纹理尺寸
    diced_tex_size = Size(width=diced_texture.width, height=diced_texture.height)
    
    # 处理 uv 坐标（每8个元素为一个矩形，每个点2个坐标）
    uv_rects = []
    for i in range(0, len(uv), 8):
        rect_data = uv[i:i+8]
        if len(rect_data) < 8:
            break
            
        # 每个矩形有4个点，每个点2个坐标
        points = []
        for j in range(0, 8, 2):
            x = round_coord(rect_data[j] * diced_tex_size.width)
            y = round_coord((1.0 - rect_data[j+1]) * diced_tex_size.height)
            points.append(Point(x, y))
        
        uv_rects.append(Rect(points))
    
    # 创建要还原的图像
    image_to_restore = Image.new('RGBA', (round(sprite_rect.width), round(sprite_rect.height)))
    
    # 将切片粘贴到正确位置
    for uv_rect, xy_rect in zip(uv_rects, xy_rects):
        rect_map = RectMap(uv_rect, xy_rect)
        rect_map.crop_then_paste(diced_texture, image_to_restore)
    
    return image_to_restore


def strip_dquota(s):
    return s[1:-1] if len(s) > 1 and s[0] == '"' and s[-1] == '"' else s


def main():
    src_file = None
    while not src_file or not os.path.isfile(src_file):
        src_file = strip_dquota(input('输入解包文件路径 (.bundle): '))
        if src_file.find('.') == -1:
            src_file += '.bundle'

    env = UnityPy.load(src_file)

    sprites = []
    img = None
    for obj in env.objects:
        if obj.type.name in ["Sprite"]:
            data = obj.read()
            sprites.append(data)
        elif obj.type.name in ["Texture2D"]:
            data = obj.read()
            img = data.image
    
    if not img:
        print('未在bundle内找到贴图')
        return

    dst_dir = None
    while not dst_dir or os.path.isfile(dst_dir):
        dst_dir = strip_dquota(input('输入保存文件夹路径: '))

    os.makedirs(dst_dir, exist_ok=True)

    context = {}
    
    try:
        grid = int(input('输入生成网格数 (n x n, 留空自动计算, -1 不计算): '))
        if grid and grid > 0:
            generate_grid(img, grid, grid)
            context['grid'] = True
        elif grid == -1:
            context['grid'] = False
    except BaseException:
        pass

    for sprite in sprites:
        restore_image(sprite, img, context).save(os.path.join(dst_dir, '{}.png'.format(sprite.m_Name)))

    if context.get('grid'):
        img.save(os.path.join(dst_dir, '网格总览.png'))

if __name__ == '__main__':
    try:
        while True:  # 无限循环
            main()  # 调用主函数
    except BaseException as e:
        traceback.print_exc()  # 打印错误信息
        print(f"程序错误: {e}")  # 提示错误
        input('按回车键关闭程序...')
