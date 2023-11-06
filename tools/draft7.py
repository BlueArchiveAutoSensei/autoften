import numpy as np
import copy
import timeit

# 创建一个2560x1440的BGR图像（3个通道，每个通道的值为0-255的uint8类型）
image = np.random.randint(0, 256, (2560, 1440, 3), dtype=np.uint8)

# 使用ndarray.copy进行拷贝的时间
def ndarray_copy_image():
    return image.copy()

# 使用copy.copy进行拷贝的时间
def shallow_copy_image():
    return copy.copy(image)

# 使用copy.deepcopy进行拷贝的时间
def deep_copy_image():
    return copy.deepcopy(image)

# 测量这三种方法的执行时间
ndarray_copy_time_image = timeit.timeit(ndarray_copy_image, number=1000)
shallow_copy_time_image = timeit.timeit(shallow_copy_image, number=1000)
deep_copy_time_image = timeit.timeit(deep_copy_image, number=1000)

print (ndarray_copy_time_image, shallow_copy_time_image, deep_copy_time_image)
