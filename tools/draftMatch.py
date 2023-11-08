import cv2
import numpy as np

def template_matching_within_range(main_image_path, template_image_path, region=None):
    # 读取主图片和模板图片
    main_img = cv2.imread(main_image_path, cv2.IMREAD_COLOR)
    main_copy = main_img.copy()
    template_img = cv2.imread(template_image_path, cv2.IMREAD_COLOR)

    # 如果用户提供了范围，那么只在该范围内进行模板匹配
    if region:
        x1, y1, x2, y2 = region
        main_img = main_img[y1:y2, x1:x2]

    # 使用cv2的模板匹配方法
    result = cv2.matchTemplate(main_img, template_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)


    top_left = max_loc
    bottom_right = (top_left[0] + template_img.shape[1], top_left[1] + template_img.shape[0])
    
    # 打印红色矩形的左上和右下坐标点
    print(f"Top Left: {top_left}")
    print(f"Bottom Right: {bottom_right}")
    center_x = (top_left[0] + bottom_right[0])//2
    bar_length = region[2]-region[0]
    # center_x -= 50
    # bar_length -= 55
    ratio = center_x/bar_length
    ratio = (center_x-int(ratio*10)*3-2)/(bar_length-9*3-5)
    print(center_x,bar_length)
    print((center_x-int(ratio*10)*3-2),(bar_length-9*3-5))
    print(ratio)


    cv2.rectangle(main_img, top_left, bottom_right, (0,0,255), 2)

    # 显示匹配结果
    cv2.imshow('Template Matched', main_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 使用方法
main_image_path = r"C:\Users\Vickko\Pictures\20_15_51.png"
template_image_path = r"c:\Users\Vickko\Pictures\line720p.png"
region = (1640, 1250, 2285, 1316)  # 原始视频截图的坐标
region = (1648, 1345, 2298, 1400)  # 照片app全屏截图
region = (1640, 1350, 2285, 1400)  # 照片app全屏win32
region = (1648, 1345, 2298, 1400)  # win32带Mumu标题栏
region = (895, 740, 1248, 770)  # win32带Mumu标题栏720p
# template_matching_within_range(main_image_path, template_image_path, region)
template_matching_within_range(main_image_path, template_image_path, region)