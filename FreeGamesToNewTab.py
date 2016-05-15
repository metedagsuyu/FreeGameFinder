#author: https://github.com/metedagsuyu
#check out the master script first, this script only has the new lines commented

import praw, datetime, webbrowser

def readlinesFile(fileName):
    with open("{}.txt".format(fileName),"r") as myFile:
        allLines = myFile.readlines()
        return allLines
    
def run_bot(): 
    
    r = praw.Reddit(user_agent = "free game finder by Mete Dagsuyu /u/__code-code__")
            
    username = readlinesFile("login")[0]
    password = readlinesFile("login")[1]
    r.login(username, password, disable_warning=True)  
    
    subreddit = r.get_subreddit("GameDeals")  
    submissions = subreddit.get_new(limit = 1000)    
    
    is_match = set()
    good_pc_words = set(["indiegla","indiegala","pc","steam","gleam","itch.io","humble"])
    shouldnt_be_in_title = ["$","£","€ "]  
    
    for each in submissions: 
        if "100" in each.title and not each.over_18: 
            for good_word in good_pc_words:
                if good_word in each.title.lower():
                    for bad_word in shouldnt_be_in_title:
                        if bad_word in each.title.lower():
                            break 
                        else:
                            #create url as a string
                            chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
                            #use the webbrowser library to open up that url in a new tab
                            webbrowser.open_new_tab("https://reddit.com/{}".format(each.id)) 
                            break
                           
run_bot()