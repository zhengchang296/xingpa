import struct
import traceback
from PIL import Image
from typing import Tuple, List
from dataclasses import dataclass

from PIL.ImageOps import pad
import UnityPy
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
    
    def width(self) -> int:
        x_min = min(p.x for p in self.points)
        x_max = max(p.x for p in self.points)
        return x_max - x_min

    def height(self) -> int:
        y_min = min(p.y for p in self.points)
        y_max = max(p.y for p in self.points)
        return y_max - y_min
    
    def pos(self) -> Point:
        x_min = min(p.x for p in self.points)
        y_min = min(p.y for p in self.points)
        return Point(x_min, y_min)
    
    def pad(self, value=1):
        x_min = min(p.x for p in self.points)
        y_min = min(p.y for p in self.points)
        x_max = max(p.x for p in self.points)
        y_max = max(p.y for p in self.points)
        
        self.points = [
            Point(x_min, y_min),
            Point(x_max + value, y_min),
            Point(x_max + value, y_max + value),
            Point(x_min, y_max + value),
        ]

    def offset(self, x, y):
        for p in self.points:
            p.x += x
            p.y += y


class RectMap:
    """矩形映射"""
    def __init__(self, uv_rect: Rect, xy_rect: Rect):
        self.uv_rect = uv_rect
        self.xy_rect = xy_rect
    
    def pad(self, value=2):
        """填充一个像素"""
        if self.xy_rect.pos().x == 0 or self.xy_rect.pos().y == 0:
            value = value // 2
            self.xy_rect.pad(value)
            self.uv_rect.pad(value)
        else:
            self.xy_rect.pad(value)
            self.uv_rect.pad(value)
            value = value // 2
            self.xy_rect.offset(-value, -value)
            self.uv_rect.offset(-value, -value)
    
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


def restore_image(sprite_data, diced_texture: Image.Image, save_img: Image.Image):
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
        points = []
        for j in range(0, 12, 3):
            x = round_coord(rect_data[j] * ptu - sprite_rect.x)
            y = round(sprite_rect.height - round_coord(rect_data[j+1] * ptu - sprite_rect.y))
            points.append(Point(x, y))

        xy_rects.append(Rect(points))
    
    # 获取切片纹理尺寸
    diced_tex_size = Size(width=save_img.width, height=save_img.height)
    
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
        
        rect = Rect(points)

        uv_rects.append(rect)
    
    # 创建要还原的图像
    
    # 将切片粘贴到正确位置
    for uv_rect, xy_rect in zip(xy_rects, uv_rects):
        rect_map = RectMap(uv_rect, xy_rect)
        rect_map.pad(8)
        rect_map.crop_then_paste(diced_texture, save_img)


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

    img_obj = None
    img_data = None
    img_origin = None

    for obj in env.objects:
        if obj.type.name in ["Sprite"]:
            data = obj.parse_as_object()
            sprites.append(data)
        elif obj.type.name in ["Texture2D"]:
            data = obj.parse_as_object()
            img_origin = data.image
            img_obj = obj
            img_data = data

    if not img_origin:
        print('未在bundle内找到贴图')
        return

    dst_dir = None
    while not dst_dir or not os.path.isdir(dst_dir):
        dst_dir = strip_dquota(input('输入图片文件夹路径: '))

    new_img = Image.new('RGBA', (img_origin.width, img_origin.height))

    for sprite in sprites:
        img_file = os.path.join(dst_dir, '{}.png'.format(sprite.m_Name))
        if not os.path.isfile(img_file):
            print('未找到图片文件: {}'.format(os.path.basename(img_file)))
            continue
        restore_image(sprite, Image.open(img_file), new_img)

    img_data.image = new_img
    img_data.save()
    # img_obj.patch(img_data)

    with open(src_file, 'wb') as f:
        f.write(env.file.save())

    print('图片已写入 .bundle 文件')
    # dst_file = None
    # while not dst_file or os.path.isdir(dst_file):
    #     dst_file = strip_dquota(input('输入保存文件路径 (.png): '))
    # if not dst_file.endswith('.png'):
    #     dst_file += '.png'
    # if not os.path.exists(os.path.dirname(dst_file)):
    #     os.makedirs(os.path.dirname(dst_file), exist_ok=True)
    # print('保存文件: {}'.format(dst_file))
    # new_img.save(dst_file)



if __name__ == '__main__':
    try:
        while True:  # 无限循环
            main()  # 调用主函数
    except BaseException as e:
        traceback.print_exc()  # 打印错误信息
        print(f"程序错误: {e}")  # 提示错误
        input('按回车键关闭程序...')
