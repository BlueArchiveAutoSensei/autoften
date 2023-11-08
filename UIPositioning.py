import cv2
import numpy as np
import os


def ui_positioning_pipe(pipe_conn_in, pipe_conn_out,
                        slot_headshot_dir, bar_template_path,
                        slot_region=None, bar_region=None,
                        threshold=0.8):

    screenshot = None
    bar_template_img = cv2.imread(bar_template_path, cv2.IMREAD_COLOR)
    while True:
        while not pipe_conn_in.poll():
            pass
        while pipe_conn_in.poll():
            screenshot = pipe_conn_in.recv()
        if screenshot is None:
            break  # 结束进程
        slot_stat = ex_positioning(
            screenshot, slot_headshot_dir, slot_region, threshold)
        ex_point = ex_point_calc(
            screenshot, bar_template_img, bar_region, threshold)
        result = (slot_stat, ex_point)
        pipe_conn_out.send(result)


# TODO: EX Slot recognition currently iterates over all templates simply;
# optimization potential exists
def ex_positioning(main_img, templates_dir, region=None, threshold=0.8):

    original_main_img = main_img.copy()

    result = {}

    # 如果用户提供了范围，那么只在该范围内进行模板匹配
    if region:
        x1, y1, x2, y2 = region
        main_img = main_img[y1:y2, x1:x2]

        # 遍历模板目录下的所有图片
    for template_name in os.listdir(templates_dir):
        template_path = os.path.join(templates_dir, template_name)
        template_img = cv2.imread(template_path, cv2.IMREAD_COLOR)

        # 使用cv2的模板匹配方法
        match_result = cv2.matchTemplate(
            main_img, template_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_result)

        # 过滤阈值过低的匹配
        if max_val > threshold:
            if region:
                top_left = (max_loc[0] + x1, max_loc[1] + y1)
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + template_img.shape[1],
                            top_left[1] + template_img.shape[0])

            # 判断当前匹配在哪个ex槽
            center_x = (top_left[0] + bottom_right[0]) / 2
            relative_position = (center_x - x1) / (x2 - x1)
            filename_without_extension = os.path.splitext(template_name)[0]
            # print(center_x, relative_position)
            if relative_position >= 2/3:
                result[2] = filename_without_extension
            elif relative_position >= 1/3 and relative_position < 2/3:
                result[1] = filename_without_extension
            elif relative_position < 1/3:
                result[0] = filename_without_extension
            cv2.rectangle(original_main_img, top_left,
                          bottom_right, (0, 0, 255), 2)

    # print(result)
    # cv2.imshow('Templates Matched', original_main_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return result


def ex_point_calc(main_img, template_img, region=None, threshold=0.8):
    original_main_img = main_img.copy()

    # 如果用户提供了范围，那么只在该范围内进行模板匹配
    if region:
        x1, y1, x2, y2 = region
        main_img = main_img[y1:y2, x1:x2]

    # 使用cv2的模板匹配方法
    result = cv2.matchTemplate(main_img, template_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 如果最大值小于阈值，我们认为匹配失败
    if max_val < threshold:
        return -1

    top_left = max_loc
    bottom_right = (top_left[0] + template_img.shape[1],
                    top_left[1] + template_img.shape[0])

    # print(f"Top Left: {top_left}")
    # print(f"Bottom Right: {bottom_right}")
    center_x = (top_left[0] + bottom_right[0])//2
    if region:  # 如果没有提供区域，这会导致错误
        bar_length = region[2] - region[0]
    else:
        bar_length = original_main_img.shape[1]  # 使用原始图像宽度

    ratio = center_x/bar_length
    ratio = (center_x-int(ratio*10)*5-7)/(bar_length-9*5-15)
    if ratio >= 0.996:
        ratio = 1.0
    # print(center_x,bar_length)
    # print(ratio)

    # 在图像上写上ratio的值
    text = f"Ratio: {ratio*10:.2f}"  # 格式化文本保留两位小数
    position = (10, 30)  # 文本位置
    font = cv2.FONT_HERSHEY_SIMPLEX  # 字体
    font_scale = 1  # 字体缩放
    color = (0, 255, 0)  # 绿色文本
    thickness = 2  # 文本线条的粗细
    cv2.putText(main_img, text, position, font, font_scale, color, thickness)
    # 打印红色矩形的左上和右下坐标点
    cv2.rectangle(main_img, top_left, bottom_right, (0,0,255), 2)
    # 显示匹配结果
    cv2.imshow('Template Matched', main_img)
    cv2.waitKey(1)

    return ratio*10


if __name__ == "__main__":
    # 使用方法
    main_image_path = r"C:\Users\Vickko\Pictures\Image34.png"
    main_image_path = r"C:\Users\Vickko\Pictures\1.png"
    main_image_path = r"C:\Users\Vickko\Pictures\19_15_25.png"
    template_image_path = r"C:\Users\Vickko\Pictures\workspace"
    # 提供范围，如果不提供，删除这一行
    pos = (1660, 1020, 2280, 1250)  # 原始视频截图的坐标
    pos = (1640, 1110, 2300, 1340)  # 照片app全屏截图
    pos = (1660, 1110, 2310, 1340)  # win32带Mumu标题栏
    # pos = None
    # 读取主图片
    main_img = cv2.imread(main_image_path, cv2.IMREAD_COLOR)
    ex_positioning(main_img, template_image_path, pos, threshold=0.6)
