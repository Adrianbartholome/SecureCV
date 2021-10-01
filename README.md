# SecureCV
My shitty security system.

Made using OpenCV, VLC, Twilio.

I needed a security system for my office, but didn't have the money to buy one. So I wrote this. It opens a viewer to align your webcam where you want it. 
Press 'C' when you're ready. That viewer will close and the Jeopardy theme song will play, giving you time to get out of the room. After the song ends, 
the security camera will kick in. It opens a viewer, and takes a picture every 5 seconds. It compares the current frame against that picture to detect
movement. If movement is detected, it plays a studpid warning sound that I made (Dummy.mp3), records the video, saving it to the hard drive, and sends a 
text message to me. Press 'Q' to quit the program.

There are some bugs. 1) Sometimes the sound plays twice almost simultaneously. 2) I get an error because the script tries to access the audio output 
even when it's already initiated. 3) I can't figure out what exception I need to impliment to avoid script failure in the event that the network is 
down (error happens because it is trying to reach twilio to send me a message).

That said, it all works 99% of the time. I'll work out the bugs when I have time (HAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHHAHAHAHAHAHAHAHAHAHAHHAHAHAHAH)
