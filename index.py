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
        contours = self.get_reliable_contours(pic)
        pic = self.add_tag_on_img(cv2.imread(self.img_source), contours)
        cv2.imshow('', pic)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    # only black and white img
    def gen_gray_img(self):
        origin_image = cv2.imread(self.img_source, cv2.IMREAD_UNCHANGED)
        origin_image = self.transprent_px_to_balck(origin_image)
        origin_image = cv2.cvtColor(origin_image, cv2.COLOR_RGB2GRAY)
        _, pic = cv2.threshold(src=origin_image, thresh=100, maxval=255, type=0)
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
    
    def add_tag_on_img(self, img, contours):
        for i in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            text = 'pos:({}, {})'.format(x, y)
            print text
            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
        
        return img

                
if (__name__ == '__main__'):
    main()