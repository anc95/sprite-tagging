# coding=utf-8
import cv2

def main():
    tagging = SpritesTagging('./icon.png')
    tagging.gen_tagging()

class SpritesTagging():
    def __init__(self, img_source):
        self.img_source = img_source
    
    def gen_tagging(self):
        pic = self.gen_gray_img()
        self.find_contours_on_bw_img(pic)
    
    # only black and white img
    def gen_gray_img(self):
        origin_image = cv2.imread(self.img_source, cv2.IMREAD_UNCHANGED)
        origin_image = self.transprent_px_to_balck(origin_image)
        origin_image = cv2.cvtColor(origin_image, cv2.COLOR_RGB2GRAY)
        _, pic = cv2.threshold(src=origin_image, thresh=1, maxval=255, type=0)
        pic = cv2.medianBlur(pic, 5)
        return pic

    # tansform the px width 100% alpha to black
    def transprent_px_to_balck(self, img):
        if (img.shape[2] != 4):
            raise Exception, 'png image is needed' 

        for i in xrange(img.shape[0]):  
            for j in xrange(img.shape[1]):  
                alpha = img[i][j][3]
                if alpha == 0:
                    img[i][j] = [0, 0, 0, 0]
        return img

    # find contours of black and white image
    def find_contours_on_bw_img(self, img):
        _1, contours, _2 = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        pic = cv2.imread(self.img_source)
        print(len(contours))
        for i in xrange(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            origin_pic = cv2.rectangle(pic, (x, y), (x+w, y+h), (255, 0, 0), 1)
        cv2.imshow('', origin_pic)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
                
if (__name__ == '__main__'):
    main()




# origin_pic = cv2.imread('./icon.png')

# pic = cv2.cvtColor(origin_pic, cv2.COLOR_BGR2GRAY)
# # 阈值处理，将前景全填充为白色，背景全填充为黑色
# _, pic = cv2.threshold(src=pic, thresh=254, maxval=255, type=1)
# # 中值滤波，去除椒盐噪声
# pic = cv2.medianBlur(pic, 5)
# # 边缘检测，得到的轮廓列表
# _1, contours, _2 = cv2.findContours(pic, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# # 根据轮廓列表，循环在原始图像上绘制矩形边界
# for i in range(len(contours)):
#     cnt = contours[i]
#     x, y, w, h = cv2.boundingRect(cnt)
#     origin_pic = cv2.rectangle(origin_pic, (x, y), (x+w, y+h), (255, 0, 0), 2)

# cv2.imwrite('./rectangle.jpg', origin_pic)

# cv2.imshow('', origin_pic)
# cv2.waitKey(0)
# cv2.destroyAllWindows()