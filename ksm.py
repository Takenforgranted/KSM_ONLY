import os
import math
from PIL import Image, ImageDraw, ImageFont
import emoji

# 配置参数
BACKGROUND_COLOR = (238, 204, 238)  # 淡紫色背景
LOGO_SIZE = (100, 41)  # 团徽大小
NUM_LOGOS = 10  # 邦多利十个团
RADIUS = 300  # 旋转半径
ROTATION_SPEED = 5  # 每帧旋转的角度增量
FRAMES = 72  # 动画帧数
OUTPUT_FILE = "bandori_gif.gif"  # 输出文件名

# 加载户山香橙的大头照（替换为实际图片路径）
kotoko_image = Image.open("ksm.jpg").convert("RGBA")
kotoko_image = kotoko_image.resize((400, 400))  # 放大中心图片

# 创建一个更大的背景图
background = Image.new("RGBA", (800, 800), BACKGROUND_COLOR)
background.paste(kotoko_image, (200, 200))  # 将户山香橙的照片粘贴到背景中央

# 加载邦多利十个团的团徽（假设团徽图片名为 logo1.png 到 logo10.png）
logos = []
for i in range(1, NUM_LOGOS + 1):
    logo = Image.open(f"logo{i}.png").convert("RGBA")
    logo = logo.resize(LOGO_SIZE)
    logos.append(logo)

# 创建动画帧
frames = []
for frame_index in range(FRAMES):
    # 复制背景图
    frame = background.copy()
    draw = ImageDraw.Draw(frame)

    # 计算每个团徽的位置并粘贴
    for i, logo in enumerate(logos):
        angle_deg = frame_index * ROTATION_SPEED + i * 360 / NUM_LOGOS
        angle_rad = math.radians(angle_deg)
        x = int(400 + RADIUS * math.cos(angle_rad) - LOGO_SIZE[0] / 2)
        y = int(400 + RADIUS * math.sin(angle_rad) - LOGO_SIZE[1] / 2)
        frame.paste(logo, (x, y), logo)

    frames.append(frame)

# 保存为GIF
frames[0].save(
    OUTPUT_FILE,
    save_all=True,
    append_images=frames[1:],
    duration=50,  # 每帧显示时间
    loop=0,  # 无限循环
    transparency=0,
    disposal=2,
)

print(f"GIF动画已保存为 {OUTPUT_FILE}")
