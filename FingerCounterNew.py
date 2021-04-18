import cv2
import time
import os
import numpy as np
import HandTrackingModule as htm


def checkSingleGesture(fingers_list, thumb):

    down_fingers =  (fingers_list["Ring"] is False) and (fingers_list["Middle"] is False)
    up_fingers = fingers_list["Index"] and fingers_list["Pinky"] and  thumb

    return down_fingers and up_fingers

def specialDetect():


    #multi_hand_landmarks
    #MULTI_HANDEDNESS

    num_of_hands = numOfHands_tmp


    if(num_of_hands>1):
        return "Both"
    else:

        hand_type = "Left"
        #TODO: Function that recognize hand type
            #Here function...

        hand_type = handType_tmp

        return hand_type

def countSingle(handType):

    fingers_list = {"Pinky":True,"Ring":False,
                    "Middle":False,"Index":True}

    thumb = False



    #TODO: Calculate number of all fingers except thumb
    #Your code

    num_of_fingers = numOfFingers_tmp




    #====THUMB CACLUALTION=====#

    if(handType=="Left"):
        #TODO: Function that calculates thumb of left hand
        #Your code here
        thumb = thumbLeft_tmp

    else:
        #TODO: Function that calcualtes thumb of right hand
        #Your code here...
        thumb = thumbRight_tmp







    return num_of_fingers, checkSingleGesture(fingers_list,thumb)



#REMOVE LATER
numOfHands_tmp = 1
handType_tmp = "Left"

thumbLeft_tmp, thumbRight_tmp = True, False
numOfFingers_tmp = 3
#==============


text_color_hands = (0,69,255)
text_color_count = (209,206,0)




#Determines if the program should continue or not
running, countLeft, countRight = True,0,0

detector = htm.handDetector(detectionCon=0.75)


#Video conf
cap = cv2.VideoCapture(0)


#TODO: Images store:
folderPath = "images"  # TODO:Change later to fingerImages
myList = os.listdir(folderPath)
myList.sort()



#Create a list of images
overlayList = []
img_space = 100
text_middle = 50


#Import images
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    print(f'{folderPath}/{imPath}')

    #print(myList)

    if imPath != ".DS_Store":
        overlayList.append(image)


while running:
    success, img =cap.read()
    img = detector.findHands(img)

    right_space = 920

    lmList_left = detector.findPosition(img, draw=False)

    handType,fingerCounter,running = detector.countSingle(lmList=lmList_left)

    if(fingerCounter==-2):
        cv2.putText(img, "NO HANDS", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    text_color_hands, 3)
    elif(fingerCounter==-1):
        cv2.putText(img, "TWO HANDS", (500, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    text_color_hands, 3)

        left_hand, right_hand = detector.findPositionMultiple(img)
        countLeft,countRight,running = detector.countTwo(left_hand,right_hand)


        #LEFT PICTURE
        w_img_left = overlayList[countLeft].shape[0]
        h_img_left = overlayList[countLeft].shape[1]

        img[img_space:w_img_left + img_space, img_space:h_img_left + img_space] = overlayList[countLeft]

        cv2.putText(img, str(countLeft), (200-text_middle, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    text_color_count, 3)
        #RIGHT PICTURE
        w_img_right = overlayList[countRight].shape[0]
        h_img_right = overlayList[countRight].shape[1]

        img[img_space:w_img_right + img_space, right_space+img_space:right_space+h_img_right + img_space] = overlayList[countRight]
        cv2.putText(img, str(countRight), (200+right_space-text_middle, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    text_color_count, 3)



        print("count left:", countLeft, "count right:", countRight ,"running:", running)
    else:
        w_img = overlayList[fingerCounter].shape[0]
        h_img = overlayList[fingerCounter].shape[1]

        img[img_space:w_img + img_space, img_space:h_img + img_space] = overlayList[fingerCounter]
        cv2.putText(img, str(fingerCounter), (200, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    text_color_count, 3)

        if handType=="Left":
            cv2.putText(img, "LEFT", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        text_color_hands, 3)

        else:
            cv2.putText(img, "RIGHT", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        text_color_hands, 3)





    cv2.imshow("Image", img)

    cv2.waitKey(1)

    #print(handType,fingerCounter,running)
    #detector.findPositionMultiple()



img[:,:] = text_color_count
img_close = cv2.imread("images_other/Close.png")
img[150:img_close.shape[0]+150,800:img_close.shape[1]+800]=img_close

cv2.putText(img, "GOODBYE!", (70, 400), cv2.FONT_HERSHEY_TRIPLEX, 4,
                text_color_hands, 10)
cv2.imshow("Image", img)

cv2.waitKey(2000)