import cv2
import vlc
import time
import datetime
import threading
import schedule
import webbrowser

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# twilio stuff for sms
account_sid = '###############################'
auth_token = '###############################'
client = Client(account_sid, auth_token)

action = False
played = True
end = time.time()
pp = vlc.MediaPlayer('Jeopardy.mp3')

preview = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while preview:
    on, frame = preview.read()
    # insert timestamp
    if on:
        font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        dt = str(datetime.datetime.now())
        frame = cv2.putText(frame, dt, (325, 20), font, 0.6, (255, 255, 255), 0, cv2.LINE_8)
    # show preview
    cv2.imshow('Preview', frame)
    pkill = cv2.waitKey(1)
    if pkill == ord('c'):
        break
preview.release()
cv2.destroyWindow('Preview')
vlc.MediaPlayer('Jeopardy.mp3').play()
time.sleep(35)

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
out = cv2.VideoWriter("C://Path-to-where-you-want-your-video-saved",
                          cv2.VideoWriter_fourcc(*'XVID'), 30, (640, 480))


def run_continuously(interval=60):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def background_job():
    global played
    played = True


schedule.every().minute.do(background_job)

stop_run_continuously = run_continuously()

while video:
    on, frame = video.read()

    # timestamp
    if on:
        font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        dt = str(datetime.datetime.now())
        frame = cv2.putText(frame, dt, (325, 20), font, 0.6, (255, 255, 255), 0, cv2.LINE_8)

    # show video
    cv2.imshow('Action', frame)

    # take comparison picture every 5 seconds
    if time.time() > end:
        background = cv2.imwrite(filename="C://Path-to-where-you-want-to-save-comparison-image", img=frame)
        background = cv2.imread("C://Same-as-previous-path")
        background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        background = cv2.GaussianBlur(background, (21, 21), 0)
        end = time.time() + 5

    # set video interpreter stream that simplifies video for comparison purposes
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    diff = cv2.absdiff(background, gray)
    thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    cont, check = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # if movement is detected, records video and checks if sound has been played
    if action:
        # print(message.sid)
        out.write(frame)

        # plays sound and starts timer
        if played:
            # send sms
            try:
                message = client.messages \
                    .create(
                        body="movement detected.",
                        # your twilio number
                        from_='+15555555555',
                        # your actual number
                        to='+15555555555'
                    )
            # TODO TEST THESE
            except TwilioRestException as e:
                print("Something's fucked. " + repr(e.msg))
            else:
                print("Message ID: %s", message.sid)

            # play sound
            if not vlc.MediaPlayer('Dummy.mp3').play():
                try:
                    vlc.MediaPlayer('Dummy.mp3').play()
                # TODO FIND THE RIGHT EXCEPTION
                # TODO MMDEVICE AUDIO OUTPUT ERROR: CANNOT INITIALIZE
                except Exception as e:
                    print(e)
                    pass
            played = False

    # checks for big movement
    for contour in cont:
        if cv2.contourArea(contour) > 10000:
            action = True
        else:
            action = False

    kill = cv2.waitKey(1)
    if kill == ord('q'):
        break

# kill everything when exiting and open folder location
stop_run_continuously.set()
webbrowser.open("C://Path-to-wherever-you-saved-video")

out.release()
video.release()
cv2.destroyAllWindows()
