import pyaudio, wave
import threading
import cv2
import time
import numpy as np
import ffmpeg
import subprocess

def rec_sound():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    def record() :
        p = pyaudio.PyAudio()

        stream = p.open( format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE,
                         input=True,
                         frames_per_buffer=CHUNK )

        print( "Start recording" )
        frames = []

        global stop_sound
        #r = sr.Recognizer()
        try :
            while True and stop_sound == False :
                data = stream.read( CHUNK )
                frames.append( data )
                """
                try :
                    with sr.Microphone() as source2 :
                        r.adjust_for_ambient_noise( source2, duration=0.2 )
                        audio2 = r.listen( source2 )
                        MyText = r.recognize_google( audio2 )
                        MyText = MyText.lower()
                        print( "YOU SAID:  ", MyText )

                except sr.RequestError as e :
                    print( "Could not request results; {0}".format( e ) )

                except sr.UnknownValueError :
                    print( "ERROR" )
                """

        except KeyboardInterrupt :
            print( "Done recording" )


        except Exception as e :
            print( str( e ) )

        sample_width = p.get_sample_size( FORMAT )
        stream.stop_stream()
        stream.close()
        p.terminate()
        print( "Done recording" )

        return sample_width, frames


    def record_to_file(file_path) :
        wf = wave.open( file_path, 'wb' )
        wf.setnchannels( CHANNELS )
        sample_width, frames = record()
        wf.setsampwidth( sample_width )
        wf.setframerate( RATE )
        wf.writeframes( b''.join( frames ) )
        wf.close()


    if __name__ == '__main__' :
        record_to_file( 'CONFIDENTIAL_SOUND.wav' )


def rec_video():
    cap = cv2.VideoCapture( 0 )

    width = int( cap.get( cv2.CAP_PROP_FRAME_WIDTH ) )
    height = int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT ) )
    writer = cv2.VideoWriter( 'CONFIDENTIAL_VIDEO.mp4', cv2.VideoWriter_fourcc( *'DIVX' ), 20, (width, height) )
    face_cascade = cv2.CascadeClassifier( 'haarcascade_frontalface_default.xml' )
    cap = cv2.VideoCapture( 0 )
    rec = False
    time.sleep(3)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY )
        faces = face_cascade.detectMultiScale( gray, 1.3, 5 )
        for (x, y, w, h) in faces :
            # To draw a rectangle in a face
            cv2.rectangle( frame, (x-20, y-20), (x + w + 20, y + h + 20), (255, 255, 0), 2 )
            frame[y-20:y+h+20, x-20:x+w+20] = cv2.blur(frame[y-20:y+h+20, x-20:x+w+20] ,(50,50))

        writer.write( frame )
        frame = mirror_this(frame, False, False)
        if rec == False:
            t_sound = threading.Thread( target=rec_sound )
            t_sound.start()
            rec = True
        cv2.imshow( 'CONFIDENTIAL', frame )
        if cv2.waitKey( 1 ) & 0xFF == 27 :
            break

    cap.release()
    writer.release()
    cv2.destroyAllWindows()


def mirror_this(image_file, gray_scale=False, with_plot=False) :
    image_rgb = image_file
    image_mirror = np.fliplr( image_rgb )
    if with_plot :
        fig = plt.figure( figsize=(10, 20) )
        ax1 = fig.add_subplot( 2, 2, 1 )
        ax1.axis( "off" )
        ax1.title.set_text( 'Original' )
        ax2 = fig.add_subplot( 2, 2, 2 )
        ax2.axis( "off" )
        ax2.title.set_text( "Mirrored" )
        if not gray_scale :
            ax1.imshow( image_rgb )
            ax2.imshow( image_mirror )
        else :
            ax1.imshow( image_rgb, cmap='gray' )
            ax2.imshow( image_mirror, cmap='gray' )
        return True
    return image_mirror


def finalize():


    cmd_audio = '@echo off | echo y | ffmpeg.exe -i CONFIDENTIAL_SOUND.wav -af asetrate=44100*0.7,aresample=44100,atempo=1.70 output.mp3 >nul 2>&1'
    subprocess.call( cmd_audio, shell=True )

    cmd = '@echo off | ffmpeg.exe  -y -i output.mp3  -r 30 -i CONFIDENTIAL_VIDEO.mp4  -filter:a aresample=async=1 -c:a flac -c:v copy CONF_FINAL.mkv >nul 2>&1'
    subprocess.call( cmd, shell=True )

    print( 'VIDEO READY' )



stop_sound = False
rec_video()
stop_sound = True
finalize()



