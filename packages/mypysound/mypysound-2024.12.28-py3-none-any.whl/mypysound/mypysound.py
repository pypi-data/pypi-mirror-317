def play(file):
    import platform

    platform = platform.system().lower()
    if platform == "android":
        from android.media import MediaPlayer
        from os.path import dirname, join

        player = MediaPlayer()
        sound = file
        player.setDataSource(sound)
        player.prepare()
        player.start()
    if platform != "android" and platform != "ios":
        from playsound3 import playsound

        playsound(file)


if __name__ == "__main__":
    play(file="happy-birthday-whistled.wav")
