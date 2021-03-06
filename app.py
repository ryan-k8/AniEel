from requests.api import request
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import eel

#lmao xD 
print(
'''
    _     _  _   ___   ___   ___   _    
   /_\   | \| | |_ _| | __| | __| | |   
  / _ \  | .` |  | |  | _|  | _|  | |__ 
 /_/ \_\ |_|\_| |___| |___| |___| |____|
              
               Author : Ryan K. 
                                            '''

)

class anime():
    def search_results(query):
        try:
            url1 = f"https://gogoanime.ai//search.html?keyword={query}"
            session = HTMLSession()
            response = session.get(url1)
            response_html = response.text
            soup = BeautifulSoup(response_html, 'html.parser')
            animes = soup.find("ul", {"class": "items"}).find_all("li")
            # print(animes)
            res_list_search = []
            for anime in animes:  # For every anime found
                tit = anime.a["title"]
                urll = anime.a["href"]
                r = urll.split('/')
                res_list_search.append({"name":f"{tit}","animeid":f"{r[2]}"})
            if res_list_search == []:
                return {"status":"204", "reason":"No search results found for the query"}
            else:
                return res_list_search
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}

    def anime_details(animeid):
        try:
            animelink = 'https://gogoanime.ai/category/{}'.format(animeid)
            response = requests.get(animelink)
            plainText = response.text
            soup = BeautifulSoup(plainText, "lxml")
            source_url = soup.find("div", {"class": "anime_info_body_bg"}).img
            imgg = source_url.get('src')
            tit_url = soup.find("div", {"class": "anime_info_body_bg"}).h1.string
            lis = soup.find_all('p', {"class": "type"})
            plot_sum = lis[1]
            pl = plot_sum.get_text().split(':')
            pl.remove(pl[0])
            sum = ""
            plot_summary = sum.join(pl)
            type_of_show = lis[0].a['title']
            ai = lis[2].find_all('a')  # .find_all('title')
            genres = []
            for link in ai:
                genres.append(link.get('title'))
            year1 = lis[3].get_text()
            year2 = year1.split(" ")
            year = year2[1]
            status = lis[4].a.get_text()
            oth_names = lis[5].get_text()
            lnk = soup.find(id="episode_page")
            ep_str = str(lnk.contents[-2])
            a_tag = ep_str.split("\n")[-2]
            a_tag_sliced = a_tag[:-4].split(">")
            last_ep_range = a_tag_sliced[-1]
            y = last_ep_range.split("-")
            ep_num = y[-1]
            res_detail_search = {"title":f"{tit_url}", "year":f"{year}", "other_names":f"{oth_names}", "type":f"{type_of_show}", "status":f"{status}", "genre":f"{genres}", "episodes":f"{ep_num}", "image_url":f"{imgg}","plot_summary":f"{plot_summary}"}
            return res_detail_search
        except AttributeError:
            return {"status":"400", "reason":"Invalid animeid"}
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}

    def episodes_link(animeid, episode_num):
        try:
            animelink = f'https://gogoanime.ai/category/{animeid}'
            response = requests.get(animelink)
            plainText = response.text
            soup = BeautifulSoup(plainText, "lxml")
            lnk = soup.find(id="episode_page")
            source_url = lnk.find("li").a
            tit_url = soup.find("div", {"class": "anime_info_body_bg"}).h1.string
            URL_PATTERN = 'https://gogoanime.ai/{}-episode-{}'
            url = URL_PATTERN.format(animeid, episode_num)
            srcCode = requests.get(url)
            plainText = srcCode.text
            soup = BeautifulSoup(plainText, "lxml")
            source_url = soup.find("li", {"class": "dowloads"}).a
            vidstream_link = source_url.get('href')
            # print(vidstream_link)
            URL = vidstream_link
            dowCode = requests.get(URL)
            data = dowCode.text
            soup = BeautifulSoup(data, "lxml")
            dow_url= soup.findAll('div',{'class':'dowload'})
            episode_res_link = {'title':f"{tit_url}"}
            for i in range(len(dow_url)):
                Url = dow_url[i].find('a')
                downlink = Url.get('href')
                str_= Url.string
                str_spl = str_.split()
                str_spl.remove(str_spl[0])
                str_original = ""
                quality_name = str_original.join(str_spl)
                episode_res_link.update({f"{quality_name}":f"{downlink}"})
            return episode_res_link
        except AttributeError:
            return {"status":"400", "reason":"Invalid animeid or episode_num"}
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}

    def by_genre(genre_name, page):
        try:
            url = f"https://gogoanime.ai/genre/{genre_name}?page={page}"
            response = requests.get(url)
            plainText = response.text
            soup = BeautifulSoup(plainText, "lxml")
            animes = soup.find("ul", {"class": "items"}).find_all("li")
            gen_ani_res = [{"genre":f"{genre_name}"}]
            gen_ani = []
            for anime in animes:  # For every anime found
                tits = anime.a["title"]
                urll = anime.a["href"]
                r = urll.split('/')
                gen_ani.append({"title":f"{tits}", "animeid":f"{r[2]}"})
            gen_ani_res.append(gen_ani)
            return gen_ani_res
        except AttributeError or KeyError:
            return {"status":"400", "reason":"Invalid genre_name or page_num"}
        except requests.exceptions.ConnectionError:
            return {"status": "404", "reason": "Check the host's network Connection"}
c = True
while c:
    try:
        x = True
        Query = input("enter anime name : ")
        Search = anime.search_results(query=Query)
        n = 0
        for m in Search:
            try:
                print(f'<< {n} >>  {m.get("name")}')
                n +=1
            except AttributeError:
                x = False
        if x == True:
           Selection = int(input("enter selection : "))
           Animeid = Search[Selection].get("animeid")
           c = False
    except KeyError:
        print("no results were found from the search")
        c = True
Details = anime.anime_details(animeid=Animeid)
Title = Details.get("title")
Image = Details.get("image_url")
Status = Details.get("status")
Genre = Details.get("genre")
genres = ''
for i in eval(Genre):
    genres += i + ' , '
genres = genres[0:len(genres)-2]
OtherName = Details.get("other_names")
Released = Details.get("year")
Episodes = Details.get("episodes")
Summary = Details.get("plot_summary")
print ("please hold on .....")
print(f"{Title}  has {Episodes} no of Episodes ")
Ep_no = int(input('enter episode to watch : '))
Dw = anime.episodes_link(animeid=Animeid,episode_num=Ep_no)

@eel.expose
def name_link(msg):
    title = f'{Title}'    
    return title

@eel.expose
def img_link():
    img = Image
    return img

@eel.expose
def genre_link(g):
    genre = genres
    return genre

@eel.expose
def release_link(r):
    release = Released
    return release

@eel.expose
def status_link(s):
    status = Status
    return status


@eel.expose
def episodes_link(e):
    episodes_no = Episodes
    return episodes_no

@eel.expose
def othername_link(o):
    othername = OtherName[11:]
    return othername

@eel.expose
def plot_link():
    plot = Summary
    return plot

@eel.expose
def Src_link():
    c1 = 0 
    source_url=""
    for i in Dw.values():
        c1+=1
        if c1==2:
            source_url = source_url + i
            break
    if source_url[8] =="s":
        global GOOGLE_URL
        GOOGLE_URL = source_url
        return source_url

@eel.expose
def iframe_src_link(Msg):
    if "DoodStream" in Dw.keys():
        dood_str = Dw.get("DoodStream") 
        dood_lst = list(dood_str)
        dood_lst[16] ="e"  
        dood_src = "".join(dood_lst)
        try:
            requests.get(dood_src)
            return dood_src
        except:
            if "StreamTape" in Dw.keys():
                streamt_str = Dw.get("StreamTape")
                streamt_lst = list(streamt_str)
                streamt_lst[23] = "e"
                streamt_src = "".join(streamt_lst)
                return  streamt_src
            
            elif "MixdropSV" in Dw.keys():
                mxdrop_str = Dw.get("MixdropSV")
                mxdrop_lst = list(mxdrop_str)
                mxdrop_lst[19] ="e"
                mxdrop_src = "".join(mxdrop_lst)
                return mxdrop_src    
    elif "StreamTape" in Dw.keys():
        streamt_str = Dw.get("StreamTape")
        streamt_lst = list(streamt_str)
        streamt_lst[23] = "e"
        streamt_src = "".join(streamt_lst)
        return  streamt_src
            
    elif "MixdropSV" in Dw.keys():
        mxdrop_str = Dw.get("MixdropSV")
        mxdrop_lst = list(mxdrop_str)
        mxdrop_lst[19] ="e"
        mxdrop_src = "".join(mxdrop_lst)
        return mxdrop_src 


    else: 
        return "null"

@eel.expose
def check_js_vid(x):

    if GOOGLE_URL[20] != "l":  #check if the link's not from storage.googleapis.com
        return "null"
    else:
        pass 

if __name__ == "__main__":
    eel.init('web')
    eel.start('index.html',size=(853,873)) 
