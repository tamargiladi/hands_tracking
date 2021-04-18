"""
Hand Tracing Module
By: Murtaza Hassan
Youtube: http://www.youtube.com/c/MurtazasWorkshopRoboticsandAI
Website: https://www.murtazahassan.com/
"""

import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):

        lmList = []

        #Chooses the correct hand
        if self.results.multi_hand_landmarks:
            handsNum = len(self.results.multi_hand_landmarks)

            if(handsNum==1):
                #print(self.results.multi_hand_landmarks[0])
                #print(self.results.multi_handedness[0].classification[0].label)
                #print(len(self.results.multi_handedness))

                statement = self.results.multi_handedness[0].classification[0].label=="Left"
                #print(self.results.multi_handedness[0].classification[0].label)

                myHand = self.results.multi_hand_landmarks[0]
            else:
                #print(len(self.results.multi_handedness),self.results.multi_handedness[0])

                if(self.results.multi_handedness[0].classification[0].label=="Left"):
                    myHand = self.results.multi_hand_landmarks[0]
                else:
                    myHand = self.results.multi_hand_landmarks[1]


            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList

    def findPositionMultiple(self,img):
        label = "N"
        lmList_left = []
        lmList_right = []
        if self.results.multi_handedness and len(self.results.multi_handedness)==2:
            if (self.results.multi_handedness[0].classification[0].label == "Left"):
                left = self.results.multi_hand_landmarks[0]
                right = self.results.multi_hand_landmarks[1]
            else:
                left = self.results.multi_hand_landmarks[1]
                right = self.results.multi_hand_landmarks[0]

            for id, lm in enumerate(left.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList_left.append([id, cx, cy])

            for id, lm in enumerate(right.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList_right.append([id, cx, cy])


        return lmList_left,lmList_right




    def countSingle(self,lmList):
        hand_type, count_fingers = "No detection", -2

        fingerState = {"Thumb":False,"Index":False,"Middle":False,"Ring":False, "Pinky":False}
        if self.results.multi_hand_landmarks:
            # ====HAND TYPE====
            if len(self.results.multi_hand_landmarks)==1:
                count_fingers = 0
                #print(self.results.multi_handedness)
                hand_label = self.results.multi_handedness[0].classification[0].label
                if hand_label =="Left":
                    hand_type="Left"
                else:
                    hand_type="Right"

                #====FINGERS COUNT====
                fingerArr = [["Pinky", 20, 18], ["Ring", 16, 14], ["Middle", 12, 10], ["Index", 8, 6], ["Thumb", 4, 5]]

                for finger in fingerArr:
                    fingerName, fingerUp, fingerLow = finger[0], finger[1], finger[2]

                    if fingerName != "Thumb":
                        statement = lmList[fingerUp][2] < lmList[fingerLow][2]

                        if statement:
                            count_fingers = count_fingers + 1
                            fingerState[fingerName] = True

                if hand_type == "Right":
                    statement = (lmList[fingerUp][1] < lmList[fingerLow][1] or  (lmList[fingerUp][1] < lmList[5][1]))
                else:
                    statement = (lmList[fingerUp][1] > lmList[fingerLow][1] or (lmList[fingerUp][1] > lmList[5][1]))

                if statement:
                    count_fingers = count_fingers + 1
                    fingerState["Thumb"] = True


            else:
                hand_type="BOTH"
                count_fingers=-1

        if hand_type == "Left":
            hand_type="Right"
        elif hand_type== "Right":
            hand_type = "Left"

        running_state_down = fingerState["Middle"] is False and fingerState["Ring"] is False
        running_state_up = fingerState["Thumb"] and fingerState["Pinky"] and fingerState["Index"]




        return hand_type, count_fingers, not (running_state_down and running_state_up)

    def countTwo(self,lmList_left,lmList_right):
        fingerArr_left = [["Pinky", 20, 18], ["Ring", 16, 14], ["Middle", 12, 10], ["Index", 8, 6], ["Thumb", 4, 5]]
        fingerArr_right = [["Pinky", 20, 18], ["Ring", 16, 14], ["Middle", 12, 10], ["Index", 8, 6], ["Thumb", 4, 5]]

        fingerState_left = {"Thumb":False,"Index":False,"Middle":False,"Ring":False, "Pinky":False}
        fingerState_right = {"Thumb":False,"Index":False,"Middle":False,"Ring":False, "Pinky":False}

        count_fingers_left =0
        count_fingers_right = 0
        for finger in fingerArr_left:
            fingerName, fingerUp, fingerLow = finger[0], finger[1], finger[2]

            statement = True
            if fingerName != "Thumb":
                statement = lmList_left[fingerUp][2] < lmList_left[fingerLow][2]
            else:
                statement = lmList_left[fingerUp][1] > lmList_left[fingerLow][1]

            fingerState_left[fingerName] = statement

            if statement:
                count_fingers_left = count_fingers_left + 1
                fingerState_left[fingerName] = True


        for finger in fingerArr_right:
            fingerName, fingerUp, fingerLow = finger[0], finger[1], finger[2]

            statement = True

            if fingerName != "Thumb":
                statement = lmList_right[fingerUp][2] < lmList_right[fingerLow][2]
            else:
                statement = lmList_right[fingerUp][1] < lmList_right[fingerLow][1]


            fingerState_right[fingerName] = statement

            if statement:
                count_fingers_right = count_fingers_right + 1
                fingerState_right[fingerName] = True


        state_left_down = fingerState_left["Ring"] is False and fingerState_left["Middle"] is False
        state_left_up = fingerState_left["Pinky"] and fingerState_left["Thumb"] and fingerState_left["Index"]

        state_right_down = fingerState_right["Ring"] is False and fingerState_right["Middle"] is False
        state_right_up = fingerState_right["Pinky"] and fingerState_right["Thumb"] and fingerState_right["Index"]

        final_state = (state_left_down and state_left_up) or (state_right_down and state_right_up)

        return count_fingers_right, count_fingers_left, not final_state

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()