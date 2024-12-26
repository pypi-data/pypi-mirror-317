import cv2
import numpy as np
from PIL import Image
import os

def crop_rect(img: cv2.typing.MatLike, points):

    rotated = cv2.minAreaRect(points)
    angle = rotated[2]

    # 有些矩形长度方向是竖着的，需要扶正
    if abs(angle - 90) < 15:
        angle = rotated[2] - 90

    h, w, _ = img.shape
    center = (w / 2, h / 2)
    m = cv2.getRotationMatrix2D(center, angle, 1.0)
    rect = cv2.RotatedRect(center, (w, h), angle)
    newimg_points = cv2.boundingRect(rect.points())
    new_size = newimg_points[2:]
    m[:, 2] -= newimg_points[:2]

    new_points = []
    for p in points:
        new_points.append((np.matmul(m[:, :2], p) + m[:, 2]).astype("int32"))

    new_img = cv2.warpAffine(img, m, new_size)
    points = np.asarray(new_points)
    x0, y0 = points.min(axis=0)
    x1, y1 = points.max(axis=0)
    res = new_img[y0 : y1 + 1, x0 : x1 + 1]
    return res

def generate_gif_from_dir(dir, tar_path, duration=200, loop=0, tar_size=None):
    """
    duration=200 表示每帧之间的延迟时间为200毫秒  
    loop=0 表示无限循环  
    """
    images = []
    files = os.listdir(dir)
    for file in files:
        img = Image.open(os.path.join(dir, file))
        if tar_size is not None:
            img = img.resize(tar_size)
        images.append(img)
        print(f"已读取完成 {len(images)} / {len(files)}， 读取 {file}")

    print(f"正在组合成gif")
    images[0].save(tar_path, save_all=True, append_images=images[1:], duration=duration, loop=loop)
    print(f"成功生成:{tar_path}")

