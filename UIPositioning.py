import os

import cv2
import numpy as np


def ui_positioning_pipe(pipe_conn_in, pipe_conn_out,
                        slot_headshot_dir, bar_template_path,
                        slot_region=None, bar_region=None,
                        threshold=0.8):
    """
    通过pipe实现的UI定位进程

    Args:
        pipe_conn_in (Pipe): 进程通信的输入端
        pipe_conn_out (Pipe): 进程通信的输出端
        slot_headshot_dir (str): ex槽头像模板目录路径
        bar_template_path (str): ex point bar模板路径
        slot_region (tuple, optional): ex槽头像识别区域. Defaults to None.
        bar_region (tuple, optional): ex point bar识别区域. Defaults to None.
        threshold (float, optional): 模板匹配的阈值. Defaults to 0.8.
    """
    TEMPLATE = 0
    SIFT = 1
    ex_pos_method = SIFT

    if ex_pos_method == SIFT:
        sift = cv2.SIFT_create()
        matcher = cv2.BFMatcher()
        # 创建FLANN匹配器
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        matcher = cv2.FlannBasedMatcher(index_params, search_params)
        features_dict = compute_sift_features(slot_headshot_dir, sift)

    screenshot = None
    bar_template_img = cv2.imread(bar_template_path, cv2.IMREAD_COLOR)
    while True:
        while not pipe_conn_in.poll():
            pass
        while pipe_conn_in.poll():
            screenshot = pipe_conn_in.recv()
        if screenshot is None:
            break  # 结束进程
        if ex_pos_method == TEMPLATE:
            slot_stat = ex_positioning_template(
                screenshot, slot_headshot_dir, slot_region, threshold)
        if ex_pos_method == SIFT:
            slot_stat = ex_positioning_sift(
                screenshot, features_dict, sift, matcher, slot_region)
        ex_point = ex_point_calc(
            screenshot, bar_template_img, bar_region, threshold)

        result = (slot_stat, ex_point)
        pipe_conn_out.send(result)


def compute_sift_features(template_dir, sift):
    # 初始化存放结果的字典
    features_dict = {}

    # 遍历指定目录中的所有文件
    for filename in os.listdir(template_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
            # 构建完整的文件路径
            file_path = os.path.join(template_dir, filename)

            # 读取图片
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

            # 检查图片是否正确加载
            if image is not None:
                # 使用SIFT算法检测关键点和计算描述符
                keypoints, descriptors = sift.detectAndCompute(image, None)

                # 获取无后缀的文件名作为字典的键
                file_key = os.path.splitext(filename)[0]

                # 将结果存储在字典中
                features_dict[file_key] = (keypoints, descriptors, image.shape[:2])
            else:
                print(f"Warning: Unable to load image {filename}")

    return features_dict


def ex_positioning_sift(main_img, templates_dict, sift, matcher, region=None):
    original_main_img = main_img.copy()

    result = {}

    # 如果用户提供了范围，那么只在该范围内进行模板匹配
    if region:
        x1, y1, x2, y2 = region
        main_img = main_img[y1:y2, x1:x2]
    else:
        x1, y1 = 0, 0
        y2, x2 = main_img.shape[:2]

    # 计算关键点和描述符
    keypoints_main, descriptors_main = sift.detectAndCompute(main_img, None)

    for template_name, (keypoints_template, descriptors_template, shape) in templates_dict.items():
        matches = matcher.knnMatch(descriptors_template, descriptors_main, k=2)

        # 应用Lowe's比率测试
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)

        # 至少需要4个匹配来计算单应性，这里的场景下经过实验，误报一般在4个以下，正确的匹配点一般在40个以上，取中间值>16个是比较稳定的参数
        if len(good) > 16:
            # 获取关键点的坐标
            src_pts = np.float32([keypoints_template[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints_main[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            # 计算单应性
            H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            if H is not None:
                # 获取模板图片的尺寸
                h, w = shape

                # 使用单应性变换计算模板图片的矩形在主图片中的位置
                pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, H)

                # 计算矩形中心点坐标
                center_x = np.mean(dst[:, 0, 0])
                # center_y = np.mean(dst[:, 0, 1])
                relative_position = (center_x - x1) / (x2 - x1)
                if relative_position >= 2 / 3:
                    result[2] = template_name
                elif 1 / 3 <= relative_position < 2 / 3:
                    result[1] = template_name
                elif relative_position < 1 / 3:
                    result[0] = template_name

                print(template_name)

                # 绘制矩形
                main_image = cv2.polylines(main_img, [np.int32(dst)], True, (255, 0, 0), 3, cv2.LINE_AA)
    cv2.imshow('Detected Subimage', main_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return result


# TODO: EX Slot recognition currently iterates over all templates simply;
# optimization potential exists
def ex_positioning_template(main_img, templates_dir, region=None, threshold=0.8):

    original_main_img = main_img.copy()

    result = {}

    # 如果用户提供了范围，那么只在该范围内进行模板匹配
    if region:
        x1, y1, x2, y2 = region
        main_img = main_img[y1:y2, x1:x2]
    else:
        x1, y1 = 0, 0
        y2, x2 = main_img.shape[:2]

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
            if relative_position >= 2 / 3:
                result[2] = filename_without_extension
            elif 1 / 3 <= relative_position < 2 / 3:
                result[1] = filename_without_extension
            elif relative_position < 1 / 3:
                result[0] = filename_without_extension
    #         cv2.rectangle(original_main_img, top_left,
    #                       bottom_right, (0, 0, 255), 2)
    #
    # # print(result)
    # cv2.imshow('Templates Matched', original_main_img)
    # cv2.waitKey(1)
    # # cv2.destroyAllWindows()
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
    center_x = (top_left[0] + bottom_right[0]) // 2
    if region:  # 如果没有提供区域，这会导致错误
        bar_length = region[2] - region[0]
    else:
        bar_length = original_main_img.shape[1]  # 使用原始图像宽度

    ratio = center_x / bar_length
    # ex point bar 每格之间间距的距离（像素值）。
    # 目前720p为3， 1440p为5
    barCap = 3
    # 截取时由于ex point bar两侧多余的像素值而使用的修正值
    # 目前720P为2，1440p为7
    reviceValue = 2
    ratio = (center_x - int(ratio * 10) * barCap - reviceValue) / (bar_length - 9 * barCap - 2 * reviceValue - 1)
    if ratio >= 0.99:
        ratio = 1.0
    # print(center_x,bar_length)
    # print(ratio)

    # # 在图像上写上ratio的值
    # text = f"Ratio: {ratio*10:.2f}"  # 格式化文本保留两位小数
    # position = (10, 30)  # 文本位置
    # font = cv2.FONT_HERSHEY_SIMPLEX  # 字体
    # font_scale = 1  # 字体缩放
    # color = (0, 255, 0)  # 绿色文本
    # thickness = 2  # 文本线条的粗细
    # cv2.putText(main_img, text, position, font, font_scale, color, thickness)
    # # 打印红色矩形的左上和右下坐标点
    # cv2.rectangle(main_img, top_left, bottom_right, (0,0,255), 2)
    # # 显示匹配结果
    # cv2.imshow('Template Matched', main_img)
    # cv2.waitKey(1)

    return ratio * 10


if __name__ == "__main__":
    # 使用方法
    main_image_path = r"C:\Users\Vickko\Pictures\Image34.png"
    main_image_path = r"C:\Users\Vickko\Pictures\1.png"
    main_image_path = r"C:\Users\Vickko\Pictures\19_15_25.png"
    template_image_path = r"C:\Users\Vickko\Pictures\workspace\720p"
    # 提供范围，如果不提供，删除这一行
    pos = (1660, 1020, 2280, 1250)  # 原始视频截图的坐标
    pos = (1640, 1110, 2300, 1340)  # 照片app全屏截图
    pos = (1660, 1110, 2310, 1340)  # win32带MuMu标题栏
    # pos = None
    # 读取主图片
    main_img = cv2.imread(main_image_path, cv2.IMREAD_COLOR)

    sift = cv2.SIFT_create()
    matcher = cv2.BFMatcher()
    # # 创建FLANN匹配器
    # FLANN_INDEX_KDTREE = 1
    # index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    # search_params = dict(checks=50)
    # matcher = cv2.FlannBasedMatcher(index_params, search_params)
    features_dict = compute_sift_features(template_image_path, sift)
    ex_positioning_sift(main_img, features_dict, sift, matcher, pos)
