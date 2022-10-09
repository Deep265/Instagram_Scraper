import requests
import json
import csv
import os

# Used to write data in csv file
class Writer:

    def __init__(self,file_name,field_names):
        self.file_name = file_name
        self.field_names = field_names

    def write_data(self,dic):
        if os.path.isfile(os.path.join(os.getcwd(),self.file_name)):
            print(self.field_names)
            # Encoding utf-8-sig saves emojis
            with open(self.file_name+'.csv','a',encoding='utf-8-sig',newline='') as csvfile:
                wr = csv.DictWriter(csvfile,fieldnames=self.field_names)
                wr.writerows(dic)
        else:
            with open(self.file_name+'.csv','w',encoding='utf-8-sig',newline='') as csvfile:
                wr = csv.DictWriter(csvfile,fieldnames=self.field_names)
                wr.writeheader()
                wr.writerows(dic)
                print("Writing.....")


'''
Cookie csrf_token claim may expire once user logs out.
So in order to keep the scraper running we should change cookie csrf_token & claim.
A script can written to get this credentials but that would require a login.
'''


# this session id is of dummy account.
# Hence only open accounts or accounts followed by this account are extracted.
cookie = "sessionid=45441565726%3AOA3UHhq6wwRbul%3A13%3AAYfOdZEYEZG3KCn5tZeY28tJ96rbfMoO-Blk9wpyWg; "
csrf_token = "Mo5NZw1kDPGOqtoEi2lSKq9vhLaodWg5"
claim = "hmac.AR3nWtPSwNlZzN-L1cX4765UNzp3FR_2cLSYtB3vbUvHX9gc"


# Function to extract data
def followers_extracter(username,cookie,csrf_token,claim):

    w = Writer('edge_forex1', ['Primary_Key', 'Username', 'Full_Name', 'Profile_Pic'])
    # Headers
    headers = {
        "cookie": cookie,
        "Content-Type": "application/json",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://www.instagram.com",
        "referer": "https://www.instagram.com/",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "x-asbd-id": "198387",
        "x-csrftoken": csrf_token,
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": claim,
        "x-instagram-ajax": "1006355913"
    }

    # Getting username ID
    user_profile_id = requests.get(url=f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}', headers=headers)
    profile_id = json.loads(user_profile_id.text)['data']['user']['id']

    # Getting Followers 1st page
    first_follower_page = f'https://i.instagram.com/api/v1/friendships/{profile_id}/followers/?count=12&search_surface=follow_list_page'
    r2 = requests.get(
        url=first_follower_page,
        headers=headers)
    data=json.loads(r2.text)
    # next_max_id is to use to traverse new pages .
    next_max_id = data['next_max_id']

    # Stores all the 1st page information.
    users_data = []
    for i in range(len(data['users'])):
        users_info = dict()
        users_info['Primary_Key'] = data['users'][i]['pk']
        users_info['Username'] = data['users'][i]['username']
        users_info['Full_Name'] = data['users'][i]['full_name']
        users_info['Profile_Pic'] = data['users'][i]['profile_pic_url']
        users_data.append(users_info)


   # Stores the remaining pages.
    while True:
        # API Link of first page is different then others so written separately
        next_page_link = f'https://i.instagram.com/api/v1/friendships/{profile_id}/followers/?count=12&max_id={next_max_id}&search_surface=follow_list_page'
        response = requests.request("GET",
                                    next_page_link,
                                    headers=headers)
        data = json.loads(response.text)

        for i in range(len(data['users'])):
            users_info = dict()
            users_info['Primary_Key'] = data['users'][i]['pk']
            users_info['Username'] = data['users'][i]['username']
            users_info['Full_Name'] = data['users'][i]['full_name']
            users_info['Profile_Pic'] = data['users'][i]['profile_pic_url']
            w.write_data([users_info])
            # users_data.append(users_info)

        # w.write_data(users_data)
        try:
            next_max_id = data['next_max_id']
        except:
            break

followers_extracter('edge_forex1',cookie,csrf_token,claim)


# For Extracting users profile information
# user_profile = requests.get(url=profile_url,headers=headers)
# user_profile = json.loads(user_profile.text)
# total_followers = user_profile['data']['user']['edge_followed_by']['count']
# print(user_profile['data']['user']['edge_followed_by']['count'])