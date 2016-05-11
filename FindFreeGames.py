#author: https://github.com/metedagsuyu

import praw, datetime

#fileName = the file name to open and read
def readlinesFile(fileName):
    with open("{}.txt".format(fileName),"r") as myFile:
        allLines = myFile.readlines()
        return allLines
    
#fileName = the file name to open and append to
#oneLine = one line worth of info, ids
def appendToFile(fileName, oneLine):
    with open("{}.txt".format(fileName), "a") as myFile:
        myFile.write("{}".format(oneLine)) 
        myFile.write("\n")
        
#fileName = the file name to split     
#splitThis = split the file with this str     
def splitFile(fileName, splitThis):
    with open("{}.txt".format(fileName),"r") as myFile:
        all_post_info =  myFile.read().split(splitThis)
        return all_post_info
    
def run_bot(): 
    
    #create an object
    r = praw.Reddit(user_agent = "free game finder by Mete Dagsuyu /u/__code-code__")
            
    #login to reddit
    username = readlinesFile("login")[0]
    password = readlinesFile("login")[1]
    r.login(username, password, disable_warning=True)  
    
    #get subreddit
    subreddit = r.get_subreddit("GameDeals")  
    
    #get the latest 1000 submissions on that sub
    submissions = subreddit.get_new(limit = 1000)        
    
    for each in submissions: 
        #100 usually implies 100% off, if over_18 is true: the post has expired
        if "100" in each.title and not each.over_18: 
            
            #change from unix time to datetime
            unix_time_created = each.created
            proper_datetime = datetime.datetime.fromtimestamp(int(unix_time_created)).strftime('%d-%m-%Y ')  
            
            #change month number to month name
            time_split = proper_datetime.split("-")
            month_number = time_split[1]
            number_name = {"01":"January",
                           "02":"February",
                           "03":"March",
                           "04":"April",
                           "05":"May",
                           "06":"June",
                           "07":"July",
                           "08":"August",
                           "09":"September",
                           "10":"October", 
                           "11":"November",
                           "12":"December"}
            month_name = number_name[month_number]
            proper_time = "{}-{}-{}".format(time_split[0],month_name,time_split[2])
            
            #get the game info ready: title, date post was created, link to post
            free_game_info = "Title:   {}\n\tDate:   {}\n\tLink:   [https://reddit.com/{}]\
            \n\n-----<<<<<>>>>>-----".format(each.title, proper_time, each.id)
            #print(free_game_info)
            
            #add these to the file
            appendToFile("nonExpiredGames", free_game_info)  
         
            
            #split the entries in newFreeOutOf1000.txt
            all_posts_with_100_in_it = set(splitFile("nonExpiredGames","-----<<<<<>>>>>-----"))
            
            
            good_pc_words = set(["indiegla","indiegala","pc","steam","gleam","itch.io","humble"])
            shouldnt_be_in_title = ["$","£","€ "]
            
            #get rid of all non-pc games
            is_match = set()
            no_match = all_posts_with_100_in_it - is_match
            for current_post_info in all_posts_with_100_in_it:
                for good_word in good_pc_words:
                    if good_word in current_post_info.lower():
                        for bad_word in shouldnt_be_in_title:
                            if bad_word in current_post_info:
                                break 
                            else:
                                is_match.add(current_post_info)
                                break
            
    for each in is_match:
        appendToFile("actuallyFreeGame",each) 

run_bot()