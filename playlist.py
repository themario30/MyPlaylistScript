#!/usr/bin/python3
import sys, os
import httplib2
import urllib.request as urllib

def appendToFile(message, filepath):
    message = str(message)
    file = open(filepath, 'a')
    if(file != None):
        print("Appending [" + message + "]")
        file.write(str(message))
        file.close()
        
    
    
def grabTitle(url):

    h = httplib2.Http()
    
    resp, content = h.request(url)
    
    assert int(resp['status']) < 400
    
    start_tag = str(content).find("<title>")
    end_tag = str(content).find("</title>")
    name = str(content)[start_tag + 7:end_tag]
    if(name == "Youtube"):
        content = content[end_tag:]
        start_tag = str(content).find("<title>")
        end_tag = str(content).find("</title>")
        name = str(content)[start_tag + 7:end_tag]
    
    return name
    
def list(file,option = 1):
    
    videos = [] #init the video list
    with open(file, 'r') as f: #open the file
        lines = f.readlines()
    
    f.close()
    
    offset = 0; #offset used incase there are any sudden new lines added into the data file
    
    #loop to check each line
    for i in range(0, len(lines)):
        #if line is a new line, add an offset and continue the loop
        if(lines[i] == "\n"):
            offset = offset + 1;
            continue
        #if the line has text, and matches 0 in the modulus division, then display text
        if((i+offset) % 2 == 0):
            if(option == 1):
                print("%i. %s" %(((i-offset)/2) + 1, lines[i]))
            #if the function is used to return a list, we add the links to the list
            if(option == 2):
                videos.append([lines[i], lines[i+1]])
                #links.append(lines[i+1])
    
    return videos
                
def play(file,index):
    
    links = list(file, 2)
    
    if(len(links) < index):
        print("Error. Index #%i not found. Please use `list` to receive a list of the playlist" % (index))
    else:
        playVideo(links[index-1][0], links[index-1][1])
        
            
def playVideo(title,url):
    print ("Playing [%s]..." % (title.rstrip()))
    os.system("mpv --no-video %s" % (url))
     
def main():

    

    if(len(sys.argv) <= 1):
        message = ""
        message += "Welcome to my Playlist script. This script is designed to add and store youtube links so that you can\n"
        message += "play them via MPV. Below are the commands in which you can use for the program.\n"
        message += "\n"
        message += "list - Shows a list of all the songs in the playlist.\n"
        message += "add <link> - Adds a youtube link into the playlist. It will automatically check to see if the link\n"
        message += "             is valid or not, and grabs the title to save to the playlist data.\n"
        message += "play <number> - plays the video via \'Meme Video Player \' using the index in the list.\n"
        message += "<number> also functions the same as play <number>"
        print(message)
    else:
        
        dir = os.path.dirname(__file__)
        
        if(not os.path.exists(os.path.join(dir, "playlist"))):
            os.makedirs(os.path.join(dir,"playlist"))
        
        filepath = os.path.join(dir,"playlist","playlist.data")
        
        if(not os.path.isfile(filepath)):
            f = open(filepath, 'w')
            f.close()
        
        
        option = sys.argv[1]
        
        if(option.isdigit()):
            arg = int(option)
            option = 'play'
        
        if (len(sys.argv) >= 3):
            arg = sys.argv[2]
        
        if(option == 'add'):
            titleName = grabTitle(arg)
            appendToFile(titleName + "\n" + arg + "\n", filepath)
        if(option == 'list'):
            list(filepath)
        if(option == 'play'):
            play(filepath,int(arg))
    

main()