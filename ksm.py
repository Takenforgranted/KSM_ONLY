import os
import math
from PIL import Image

# 配置参数
BACKGROUND_COLOR = (238, 204, 238)  # 淡紫色背景
LOGO_WIDTH = 120  # 团徽统一缩放宽度（高度按原图比例自动计算，避免拉伸变形）
NUM_LOGOS = 12  # 邦多利十二个团
RADIUS = 300  # 旋转半径
ROTATION_SPEED = 5  # 每帧旋转的角度增量
FRAMES = 72  # 动画帧数（72 × 5° = 360°，恰好一整圈，保证 GIF 循环无缝衔接）
OUTPUT_FILE = "bandori_gif.gif"  # 输出文件名
LOGO_DIR = "compressed"  # 团徽所在文件夹（logo1.png ~ logo12.png）

# 加载中心的大头照
center_image = Image.open("ksm.jpg").convert("RGBA")
center_image = center_image.resize((400, 400))  # 放大中心图片

# 创建背景图并贴上中心图片
background = Image.new("RGBA", (800, 800), BACKGROUND_COLOR)
background.paste(center_image, (200, 200))

# 加载十二个团的团徽（logo1.png ~ logo12.png），按原图宽高比等比缩放
logos = []
for i in range(1, NUM_LOGOS + 1):
    path = os.path.join(LOGO_DIR, f"logo{i}.png")
    logo = Image.open(path).convert("RGBA")
    logo_height = round(LOGO_WIDTH * logo.height / logo.width)
    logo = logo.resize((LOGO_WIDTH, logo_height))
    logos.append(logo)

# 创建动画帧
frames = []
for frame_index in range(FRAMES):
    # 复制背景图
    frame = background.copy()

    # 计算每个团徽的位置并粘贴
    for i, logo in enumerate(logos):
        angle_deg = frame_index * ROTATION_SPEED + i * 360 / NUM_LOGOS
        angle_rad = math.radians(angle_deg)
        x = int(400 + RADIUS * math.cos(angle_rad) - logo.width / 2)
        y = int(400 + RADIUS * math.sin(angle_rad) - logo.height / 2)
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
