import re
import eyed3
from datetime import datetime
from schemas.adding_release import AddingRelease, AddingReleaseTrack

def Read(audio) -> AddingRelease:
    eyed3.log.setLevel("ERROR")
    audiofile = eyed3.load(audio)
    gbd = audiofile.tag.getBestDate()
    release_date = datetime(gbd.year, gbd.month, gbd.day).strftime('%Y-%m-%d') if gbd.month and gbd.day else str(gbd.year)
    genre_list = re.split('[,/]\s', audiofile.tag.genre.name)
    track = AddingReleaseTrack(
        track_num = audiofile.tag.track_num[0],
        track_title = audiofile.tag.title,
        genre = genre_list,
        bitrate = audiofile.info.bit_rate_str,
        file_size = int(audiofile.info.size_bytes),
        duration = int(audiofile.info.time_secs)
    )
    release = AddingRelease(
        artist = audiofile.tag.album_artist or audiofile.tag.artist, 
        album = audiofile.tag.album,
        release_date = release_date,
        tracks = [track]
    )
    return release

if __name__ == "__main__":
    print(Read("07 Feelin' Good.mp3"))
    print(Read("04 FIRE BIRD.mp3"))
