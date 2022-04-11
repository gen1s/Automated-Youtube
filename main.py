import praw, os
import requests, datetime
from moviepy.editor import * 
import calendar

#           Pesonal Reddit Info
client_id = ""
client_secret = ""
user_agent = ""
username = ""
password = ""

folder = os.getcwd()    

#            Get The First Posts
reddit = praw.Reddit(client_id = client_id, client_secret = client_secret, user_agent = user_agent, username = username, password = password)
print(calendar.weekday(int(datetime.datetime.now().strftime('%Y')), int(datetime.datetime.now().strftime('%m')), int(datetime.datetime.now().strftime('%d'))))
weekday = calendar.weekday(int(datetime.datetime.now().strftime('%Y')), int(datetime.datetime.now().strftime('%m')), int(datetime.datetime.now().strftime('%d')))   

if 0 == weekday or 4 == weekday:    #
    subred = reddit.subreddit("ClashRoyale")
    new = subred.hot(limit = 50)
    game = "Clash Royale"

elif 1 == weekday or 5 == weekday:##
    subred = reddit.subreddit("MinecraftMemes") 
    new = subred.hot(limit = 50)
    game = "Minecraft"

elif 2 == weekday:
    subred = reddit.subreddit("WarzoneClips")
    new = subred.new(limit = 50)
    game = "Warzone"

elif 3 == weekday:
    subred = reddit.subreddit("GrandTheftAutoV")
    new = subred.new(limit = 50)
    game = "GTA"


elif 6 == weekday:
    subred = reddit.subreddit("ValorantMemes")
    new = subred.hot(limit = 70)
    game = "Valorant"



#            Get The Video Count
with open(folder+"/count.txt", "r") as f:
    count = int(f.read())


#           Create The Folders To Download The Memes
todayfolder = folder + "/memes" + "/{}".format(datetime.datetime.now().strftime('%Y')) + "/{}".format(datetime.datetime.now().strftime('%m')) + "/{}".format(datetime.datetime.now().strftime('%d'))
try:
    os.mkdir(folder +"/memes/{}".format(datetime.datetime.now().strftime('%Y')))
    os.mkdir(folder +"/memes/{}".format(datetime.datetime.now().strftime('%Y')) + "/{}".format(datetime.datetime.now().strftime('%m')))
    os.mkdir(todayfolder)
except OSError:
    try:
        os.mkdir(folder +"/memes/{}".format(datetime.datetime.now().strftime('%Y')) + "/{}".format(datetime.datetime.now().strftime('%m')))
        os.mkdir(todayfolder)
    except OSError:
        try:
            os.mkdir(todayfolder)
        except OSError:
            print("something went wrong while creating the memes folder")
            os._exit(0)

    

#        Make sure that the video Is Not already created
videos = []
try:
    output = VideoFileClip(folder +'/output/output{}.mp4'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
    print("video alredy created")
    os._exit(0)
except OSError:
    #                   Download all the videos
    for i in new:
        print(i.title,"\n" ,i.url, "\n")
        format = i.url.split(".")


        if format[-1] != "gif" and format[-1] != "png" and format[-1] != "jpg":
            req = requests.get(i.url)
            try:
                postURL = req.content.split(b'canonicalUrl":"')
                postURL = postURL[1].split(b'"')
                postURL = postURL[0]
                postURL = postURL.decode("utf-8")

                dowloadURL = "https://sd.redditsave.com/download.php?permalink=" + postURL + "&video_url=" + i.url + "/DASH_720.mp4?source=fallback&audio_url=" + i.url + "/DASH_audio.mp4?source=fallback"
                print(dowloadURL, "\n\n\n")

                reqDWN = requests.get(dowloadURL)
                videos.append(reqDWN.content)
                with open(todayfolder + "/{}.mp4".format(datetime.datetime.now().strftime('%H-%M-%S')), "wb") as f:
                    f.write(reqDWN.content)
            except IndexError:
                print("\nwrong URL skipping\n")


#           Merge all the clips into one video
clips = []
memes = os.listdir(todayfolder)

for meme in memes:
    try:
        #       Make sure the file is not corrupted
        print(todayfolder +"/" + meme)
        comp = concatenate_videoclips([VideoFileClip(folder +"/comp.mp4"), VideoFileClip(todayfolder + "/" + meme)], method= "compose")
        #clips.append(VideoFileClip(todayfolder + "/"  + meme))
        
    except OSError:
        os.remove(todayfolder + "/" + meme)
        print("\nRemoving Corrupt Clip ...\n")

memes = os.listdir(todayfolder)

for meme in memes:
    clips.append(VideoFileClip(todayfolder + "/"  + meme))

print("done selecting the clips ...")

allclips = []
for clip in clips:
    allclips.append(clip)

result_clip = concatenate_videoclips(allclips, method= "compose")
result_clip.write_videofile(folder+'/output/output{}.mp4'.format(datetime.datetime.now().strftime('%Y-%m-%d')))


#               Upload Video To Youtube
vidtitle = f"Memes/Funny Clips {game} #{count}"
description = f"Automated Memes/Funny Clips video #{count}\n\nContact Me: www.gen1s.tk"



os.system('python youtube.py --file="'+ 'output/output{}.mp4'.format(datetime.datetime.now().strftime('%Y-%m-%d'))  
            +'" --title="'+ vidtitle +'" --description="' + description + 
            '" --keywords="funny,funny videos,funny compilation,funny videos compilation,video copilation" --category="24" --privacyStatus="public"')

#           Adds 1 to the count
with open(folder+"/count.txt", "w") as f:    
    f.write(str(count + 1))

# Done
print("done")