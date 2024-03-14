import eyed3
from datetime import datetime

eyed3.log.setLevel("ERROR")

audiofile = eyed3.load("07 Feelin' Good.mp3")
# audiofile = eyed3.load("04 FIRE BIRD.mp3")


if audiofile.tag.getBestDate().month and audiofile.tag.getBestDate().day:
    release_date = str(audiofile.tag.getBestDate().year)+'-'+str(audiofile.tag.getBestDate().month)+'-'+str(audiofile.tag.getBestDate().day)
else:
    release_date = str(audiofile.tag.getBestDate().year)
release_date = datetime.strptime(release_date, '%Y-%m-%d')
json = {
    "artist": audiofile.tag.album_artist or audiofile.tag.artist,
    "album": audiofile.tag.album,
    "release_date": release_date,
    "tracks": {
        "track_num": audiofile.tag.track_num[0],
        "track_title": audiofile.tag.title,
        "genre": audiofile.tag.genre.name,
        "bitrate": audiofile.info.bit_rate_str,
        "file_size": audiofile.info.size_bytes,
        "duration": audiofile.info.time_secs,
    },
}

print(json)
