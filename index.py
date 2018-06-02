# coding=utf-8
import cv2

def main():
    tagging = SpritesTagging('./icon.png')
    tagging.gen_tagging()

class SpritesTagging():
    def __init__(self, img_source):
        self.__contours_number = 0
        self.__tried_times = 0
        self.img_source = img_source
    
    def gen_tagging(self):
        pic = self.gen_gray_img()
        self.get_reliable_contours(pic)
    
    # only black and white img
    def gen_gray_img(self):
        origin_image = cv2.imread(self.img_source, cv2.IMREAD_UNCHANGED)
        origin_image = self.transprent_px_to_balck(origin_image)
        origin_image = cv2.cvtColor(origin_image, cv2.COLOR_RGB2GRAY)
        _, pic = cv2.threshold(src=origin_image, thresh=100, maxval=255, type=0)
        # pic = cv2.medianBlur(pic, 5)
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
    # def find_contours_on_bw_img(self, img):
    #     contours = self.get_reliable_contours(img)
    #     pic = cv2.imread(self.img_source, cv2.IMREAD_UNCHANGED)
    #     for i in range(len(contours)):
    #         x, y, w, h = cv2.boundingRect(contours[i])
    #         origin_pic = cv2.rectangle(pic, (x, y), (x+w, y+h), (255, 0, 0), 1)

    def fill_content_inner_gray_img_contours_255(self, img, contours):
        for i in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            print(x, y, w, h)
            xIndex = 0
            yIndex = 0
            while yIndex <= h:
                while xIndex <= w:
                    img[y + yIndex][x + xIndex] = 255
                    xIndex += 1
                xIndex = 0
                yIndex += 1
        
        return img
    
    def get_reliable_contours(self, gray_img):
        _1, contours, _2 = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_number = len(contours)
        if contours_number == self.__contours_number or self.__tried_times == 10:
            # 消除边缘的一些误差
            for i in range(len(contours)):
                contours[i][1][0][1] -= self.__tried_times
                contours[i][2][0][1] -= self.__tried_times
                contours[i][2][0][0] -= self.__tried_times
                contours[i][3][0][0] -= self.__tried_times

            return contours
        
        self.__tried_times += 1
        self.__contours_number = contours_number

        gray_img = self.fill_content_inner_gray_img_contours_255(gray_img, contours)
        
        return self.get_reliable_contours(gray_img)

                
if (__name__ == '__main__'):
    main()
# [
#     [
#         [394 116]
#     ]

#     [
#      [394 132]
#     ]

#  [
#      [411 132]]

#  [[411 116]]]



# origin_pic = cv2.imread('./icon.png')

# pic = cv2.cvtColor(origin_pic, cv2.COLOR_BGR2GRAY)
# # 阈值处理，将前景全填充为白色，背景全填充为黑色
# _, pic = cv2.threshold(src=pic, thresh=254, maxval=255, type=1)
# # 中值滤波，去除椒盐噪声
# pic = cv2.medianBlur(pic, 5)
# # 边缘检测，得到的轮廓列表
# _1, contours, _2 = cv2.findContours(pic, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# # 根据轮廓列表，循环在原始图像上绘制矩形边界
# print len(contours)
# for i in range(len(contours)):
#     cnt = contours[i]
#     x, y, w, h = cv2.boundingRect(cnt)
#     origin_pic = cv2.rectangle(origin_pic, (x, y), (x+w, y+h), (255, 0, 0), 2)

# cv2.imwrite('./rectangle.jpg', origin_pic)

# cv2.imshow('', origin_pic)
# cv2.waitKey(0)
# cv2.destroyAllWindows()