import re
import eyed3
from datetime import datetime
from schemas.adding_release import AddingRelease, AddingReleaseTrack

def Read(audio) -> AddingRelease:
    eyed3.log.setLevel("ERROR")
    audiofile = eyed3.load(audio)
    audio_tag = audiofile.tag
    audio_info = audiofile.info
    audio_date = audio_tag.getBestDate()
    release_date = datetime(audio_date.year, audio_date.month, audio_date.day).strftime('%Y-%m-%d') if audio_date.month and audio_date.day else str(audio_date.year)
    genre_list = re.split('[,/]\s', audio_tag.genre.name)
    track = AddingReleaseTrack(
        track_num = audio_tag.track_num[0],
        track_title = audio_tag.title,
        genre = genre_list,
        bitrate = audio_info.bit_rate_str,
        file_size = int(audio_info.size_bytes),
        duration = int(audio_info.time_secs)
    )
    release = AddingRelease(
        artist = audio_tag.album_artist or audio_tag.artist, 
        album = audio_tag.album,
        release_date = release_date,
        tracks = [track]
    )
    return release

if __name__ == "__main__":
    print(Read("07 Feelin' Good.mp3"))
    print(Read("04 FIRE BIRD.mp3"))
