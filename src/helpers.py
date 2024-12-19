import imutils
import cv2
def crop_ct101_bb(image, bb, padding=10, dstSize=(32, 32)):
    # unpack the bounding box, extract the ROI from teh image, while taking into account
    # the supplied offset
    (y1, y2, x1, x2) = bb
    y1, y2, x1, x2 = int(y1), int(y2), int(x1), int(x2)
    (x1, y1) = (max(x1 - padding, 0), max(y1 - padding, 0))
    roi = image[y1:y2 + padding, x1:x2 + padding]
    # resize the ROI to the desired destination size
    try:
        roi = cv2.resize(roi, dstSize, interpolation=cv2.INTER_AREA)
    except:
        pass
    # return the ROI
    return roi

def pyramid(image, scale=1.5, minSize=(30, 30)):
    # yield the original image
    yield image
    # keep looping over the pyramid
    while True:
    # compute the new dimensions of the image and resize it
        w = int(image.shape[1] / scale)
        image = imutils.resize(image, width=w)
        # if the resized image does not meet the supplied minimum
        # size, then stop constructing the pyramid
        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break
        # yield the next image in the pyramid
        yield image
def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])
def yolo_to_bbox(yolo_annotation, image_width, image_height):
    """
    將 YOLO 標註格式轉換為邊界框 (bounding box) 格式 (y, h, x, w)。
    :param yolo_annotation: YOLO 標註格式的單行，例如 [class_id, x_center, y_center, width, height]
    :param image_width: 圖片的寬度
    :param image_height: 圖片的高度
    :return: (y, h, x, w) 邊界框格式
    """
    class_id, x_center, y_center, width, height = yolo_annotation
    
    # 計算邊界框的像素座標
    x_center = x_center * image_width
    y_center = y_center * image_height
    width = width * image_width
    height = height * image_height
    
    # 計算左上角和右下角的坐標
    x = int(x_center - width / 2)
    y = int(y_center - height / 2)
    
    # 返回 (y, h, x, w) 格式，這是裁剪所需要的格式
    return (y, y + height, x, x + width)
