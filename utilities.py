from linkedin_scraper import Person, actions
from selenium import webdriver
import re
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import time
import time
import requests
from PIL import Image
import matplotlib.pyplot as plt
import openai
from tqdm import tqdm
from iteration_utilities import unique_everseen

openai.api_key = "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"

def login(driver, email = "botbotshukriya@gmail.com", password = "gj04dl5539"):
    actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal

def improve_content(content):
    des = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": content},
            ])['choices'][0]['message']['content']
    time.sleep(7)
    return des

def get_loc_des(exp_list, loc_len):
    if len(exp_list)<4:
        return None, None
    loc = None
    des = None
    print('length of exp: ',len(exp_list))
    if len(exp_list)==4:
        print('length of loc: ',len(exp_list[3]))
        if len(exp_list[3])<=loc_len:
            loc = exp_list[3].split('·')[0]
            if loc in ['On-site', 'Hybrid', 'Remote']:
                loc = None
        else:
            des = exp_list[3]
    elif len(exp_list)==7:
        loc = exp_list[3].split('·')[0]
        if loc in ['On-site', 'Hybrid', 'Remote']:
            loc = None
        des = exp_list[4]
    else:
        if len(exp_list[3])>len(exp_list[4]):
            des = exp_list[3]
        else:
            des = exp_list[4]
            loc = exp_list[3].split('·')[0]
            if loc in ['On-site', 'Hybrid', 'Remote']:
                loc = None
    return loc, des

def clean_exp(exps, loc_len=51):
    exp_lists = []
    for exp in exps:
        exp_lists.append(list(exp.values()))
    exp_lists = list(unique_everseen(exp_lists))
    res=[]
    i=0
    while(i<len(exp_lists)):
        print(i)
        exp_list=exp_lists[i]
        print(exp_list)
        # exp_list = list(exp.values())
        single = True
        try:
            second = exp_list[1]
            third = exp_list[2]
            if second[4:8].isnumeric() or third[4:8].isnumeric():
                pass
            else:
                single = False
        except Exception as ex:
            single = False
        temp={}
        if single:
            print('single')
            temp['company'] = exp_list[1]
            temp['date'] = exp_list[2].split('·')[0]
            temp['position'] = exp_list[0]
            loc, des = get_loc_des(exp_list, loc_len)
            if loc:
                temp['location'] = loc
            if des:
                temp['description'] = des
            i=i+1
            try:
                exp_list=exp_lists[i]
                # exp_list = list(exp.values())
            except:
                break
        else:
            print('multiple')
            temp['company'] = exp_list[0]
            if len(exp_list)>2:
                temp['location'] = exp_list[2].split('·')[0]
            temp['experiences'] = []
            i=i+1
            exp_list=exp_lists[i]
            # exp_list = list(exp.values())
            etype = ['Full-time', 'Part-time', 'Self-employed', 'Freelance', 'Internship', 'Trainee']
            print(exp_list[1])
            while(i<len(exps) and (exp_list[1][4:8].isnumeric() or (exp_list[1] in etype))):
                print(i)
                temp1 = {}
                if exp_list[1][4:8].isnumeric():
                    temp1['date'] = exp_list[1].split('·')[0]
                else:
                    temp1['date'] = exp_list[2].split('·')[0]
                temp1['position'] = exp_list[0]
                loc, des = get_loc_des(exp_list, loc_len)
                if loc:
                    temp1['location'] = loc
                if des:
                    temp1['description'] = des
                temp['experiences'].append(temp1)
                i=i+1
                try:
                    exp_list=exp_lists[i]
                    # exp_list = list(exp.values())
                except:
                    break
        res.append(temp)
    return res

def clean_projects(projects):
    project_lists = []
    for project in projects:
        project_lists.append(list(project.values()))
    project_lists = list(unique_everseen(project_lists))
    res=[]
    for project in project_lists:
        temp={}
        temp['name'] = project[0]
        i=1
        while(i<len(project)):
            if i<=1 and project[i][4:8].isnumeric():
                temp['date'] = project[i]
                i=i+1
                continue
            if i<=2 and  project[i][:10]=='Associated':
                temp['location'] = project[i][16:]
                i=i+1
                continue
            if i<=3 and  project[i]=='Other creators':
                temp['description'] = ''
                break
            else:
                temp['description'] = project[i]
                break
        res.append(temp)
    return res
            
def extract_section(driver, soup, name = 'Experience'):
    print(name)
    sections = soup.find_all('section')
    for section in sections:
        #print(section)
        try:
            heading = section.find('div', {'class':'pvs-header__container'}).find('span').get_text().strip()
            if(heading==name):
                break
        except:
            continue
    if(heading!=name):
        print('AAND KE NA GAAND KE, GYAAN CHODE BRAHMAND KE')
        return
    if(name=='About'):
        return section.find('div', {'class':'display-flex'}).find('span').get_text()
    try:
        url_exp = section.find('a',{'id':re.compile('navigation-index-.*')})['href']
        print(name, url_exp)
        driver.get(url_exp) 
        time.sleep(3)
        src = driver.page_source

        # Now using beautiful soup
        soup_exp = BeautifulSoup(src, 'lxml')
        section = soup_exp.find('section',{'class':'artdeco-card ember-view pb3'})
    except:
        print('BHOSDIKE THODA AUR KAAM KARO')
        pass
    pvs_list = section.find_all("li")#, {"class": "pvs-list__outer-container"}
    res=[]
    temp={}

    for pvs in pvs_list:
        spans = pvs.find_all('span')
        for span in spans:
            try:
                c = span['class'][0]
                if c=='mr1':
                    temp1 = {val : key for key, val in temp.items()}
                    temp = {val : key for key, val in temp1.items()}
                    res.append(temp.copy())
                    temp={}
                    i=0
            except:
                i=i+1
                temp[i] = span.get_text()
    temp1 = {val : key for key, val in temp.items()}
    temp = {val : key for key, val in temp1.items()}
    res.append(temp.copy())
    if name == 'Experience':
        return clean_exp(res[1:])
    if name == 'Projects':
        return clean_projects(res[1:])
    return res[1:]

def get_dp_bg(soup, name):
    images = {}
    try:
        bg_url = soup.find('div', {'class':'profile-background-image__image-container'}).find('img')['src']
        images['bg'] = Image.open(requests.get(bg_url, stream = True).raw)
    except:
        images['bg'] = None
    try:
        dp_url = soup.find('img', {'title': name})['src']
        if not dp_url:
            dp_url = soup.find('img', {'alt': name})['src']
        images['dp'] = Image.open(requests.get(dp_url, stream = True).raw)
    except:
        try:
            dp_url = soup.find('img', {'title': name+', #OPEN_TO_WORK'})['src']
            if not dp_url:
                dp_url = soup.find('img', {'alt': name+', #OPEN_TO_WORK'})['src']
            images['dp'] = Image.open(requests.get(dp_url, stream = True).raw)
        except:
            try:
                dp_url = soup.find('img', {'title': name+', #HIRING'})['src']
                if not dp_url:
                    dp_url = soup.find('img', {'alt': name+', #HIRING'})['src']
                images['dp'] = Image.open(requests.get(dp_url, stream = True).raw)
            except:
                images['dp'] = None
    return images

def get_basic_info(driver, soup):
    res = {}
    # In case of an error, try changing the tags used here.
    intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
    name_loc = intro.find("h1")

    # Extracting the Name
    res['name'] = name_loc.get_text().strip()
    # strip() is used to remove any extra blank spaces

    works_at_loc = intro.find("div", {'class': 'text-body-medium'})

    # this gives us the HTML of the tag in which the Company Name is present
    # Extracting the Company Name
    res['headline'] = works_at_loc.get_text().strip()


    intro = soup.find('div', {'class': 'pv-text-details__left-panel mt2'})
    location_loc = intro.find_all("span", {'class': 'text-body-small'})
    res['location'] = location_loc[0].get_text().strip()
    
    cons = soup.find('ul', {'class':'pv-top-card--list-bullet'}).find_all('span')
    res['followers'] = cons[0].get_text().strip()
    res['connections'] = cons[1].get_text().strip()
    
    driver.get('https://www.linkedin.com'+intro.find('a')['href'])
    time.sleep(3)
    con_info_src = BeautifulSoup(driver.page_source, 'lxml')
    con_infos = con_info_src.find_all('section', {'class':'pv-contact-info__contact-type'})
    con_info = {}
    for c in con_infos:
        try:
            con_info[c.find('h3').get_text().strip().split()[-1]] = c.find('span',{'class':'t-14'}).get_text().strip()
        except:
            temp = c.find('a')
            con_info[c.find('h3').get_text().strip().split()[-1]] = temp.get_text().strip()
            con_info[c.find('h3').get_text().strip().split()[-1]+'_link'] = temp['href']
            
    res['contact_info'] = con_info
    res['images'] = get_dp_bg(soup, res['name'])
    return res

def basic_improvements(basic_info):
    imp = {}
    for n in basic_info['name'].split():
        if n.lower() not in basic_info['contact_info']['Profile']:
            imp['URL'] = '{} not in profile. Change the profile link and try to add your name on the link which makes it easier to search.'.format(n)
            break

    if not basic_info['images']['dp']:
        imp['Profile picture'] = """Add a profession profile picture. 
Best Practice: 
        1) a high-resolution image
        2) Use a headshot, not a full-body photo
        3) Choose a background that isn’t distracting
        4) Make sure you’re the only person in the photo"""
        
    if not basic_info['images']['bg']:
        imp['Background image'] = """Add a background image.
Best Practices:
        1) Photograph your workspace.
        2) Showcase your tools of trade.
        3) Brand it.
        4) Feature awards and accomplishments.
        5) Display your professional community.
        6) Add a personal touch.
        7) Make the most of the city skyline.
        8) Use inspirational quotes."""
        
    if basic_info['connections'].split()[0]!='500+':
        imp['Connections'] = """Increase your connections upto atleast 500. With 500+ connections on LinkedIn, you have a greater chance of click throughs to your blog or website. that means profile, reach, presence and influence. It's also likely that you'll appear more often in search results and be higher in the search rankings if you are more connected."""
        
    if all(contact not in basic_info['contact_info'] for contact in ['Email', 'Phone']):
        imp['Contact info'] = """Atleast add your email id in your contact info so that a recruiter might be able to reach you in case they like your profile."""
    # basic_info['improvements'] = imp
    return imp

def improve_section(section):
    if not section:
        return
    for ex in tqdm(section):
        time.sleep(10)
        if len(list(ex.values())[-1])<150:
            des = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "generate my project description for my linkedin profile in bullet points - " + '. '.join(list(ex.values()))},
            ])['choices'][0]['message']['content']
        else:
            des = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "improve my project description for my linkedin profile in bullet points - " + list(ex.values())[-1]},
            ])['choices'][0]['message']['content']
        ex['improved_description'] = des
    return section
