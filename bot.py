# -*- coding: utf-8 -*-
import vk_api.vk_api
from unix_time import *
import time

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

class Bot:

    def __init__(self, token_app, token_group, group_id, server_name = "Empty"):

        self.server_name = server_name

        self.vkGroup = vk_api.VkApi(token=token_group,api_version='5.126')
        self.vkApp = vk_api.VkApi(token=token_app)

        self.long_poll = VkBotLongPoll(self.vkGroup, group_id)

        self.app = self.vkApp.get_api()
        self.group = self.vkGroup.get_api()


    def sendMsg(self, message, send_id):
        self.group.messages.send(peer_id=send_id, message=message, random_id=0)


    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.object.message.get('id') == 0:
                id_discuss = int(event.object.message.get('peer_id'))
                if event.object.message.get('text') == "/инфа":
                    self.sendInfoPosts(id_discuss)
                    self.output(event)
                    print(event)
                    with open(f'log.txt', 'a') as file:
                        file.write(str(event) + "\n")

                if event.object.message.get('text') == "/простите":
                    self.sendMsg("Чел выше зря быканул, извините его :/", id_discuss)

                if event.object.message.get('text') == "/fff":
                    a = 0 / 0

                if event.object.message.get('text') == "/мемы":
                    self.sendMsg(str(self.group.users.get(user_ids=event.object.message.get('from_id'), fields='first_name')[0]['first_name']) + " - добавил новые мемасики", id_discuss)

        print("OK " + str(ts_now()) + '\n')

        if ts_now() >= 61200 and ts_now() <= 61240:
            ID_DISCUSS_MATH_AND_PYSH = 2000000005
            self.sendInfoPosts(ID_DISCUSS_MATH_AND_PYSH)
            time.sleep(20)
        if ts_now()%3600 >= 0 and ts_now()%3600 <= 40:
            self.sendMsg("OK " + str(ts_now()) + '\n', 178985832)



    def getUserName(self, user_id):
        FIRST_FOUND = 0
        NEEDS_FIELDS = 'first_name'
        return self.group.users.get(user_id=user_id)[FIRST_FOUND][NEEDS_FIELDS]

    def getUserCity(self, user_id):
        NEED_RETURN = 'city'
        FIRST_FOUND = 0
        SET_CITY = 'city'
        NAME_CITY = 'title'
        return self.group.users.get(user_id=user_id, fields=NEED_RETURN)[FIRST_FOUND][SET_CITY][NAME_CITY]

    def getTop3PostsThreeDaysAgo(self):
        lastsPost = []
        timePeriod = ts_tomorrow()
        MAX_COUNT_POST_IN_DAY = 50
        NAME_GROUP = "math_and_physics"

        for item in (self.app.wall.get(domain=NAME_GROUP, count=MAX_COUNT_POST_IN_DAY)['items']):
            if item['date'] < timePeriod - 2*86400-10800 and item['date'] > timePeriod - 3*86400-10800:
                lastsPost.append((item['id'], item['likes']['count']))

        lastsPost.sort(key=lambda v: v[1], reverse=True)
        return lastsPost[0:3]

        #ПОСМОТРЕТЬ КАК ПРАВИЛЬНО СОРТИРОВАТЬ
        #ПОСМОТРЕТЬ ЧТО ТАКОЕ РАЗРЕЗ СПИСКА



    def sendInfoPosts(self, id_discuss):
        data = self.getTop3PostsThreeDaysAgo()
        post_ids = []
        post_views = []
        for item in data:
            post_ids.append(str(item[0]))
            post_views.append(str(item[1]))

        try:
            self.sendMsg('Первое место - ' + str(post_views[0]) +'\n'+'https://vk.com/math_and_physics?w=wall-61817535_'+post_ids[0], id_discuss)
        except:
            print("Today was no one post")
        else:
            try:
                self.sendMsg('Второе место - ' + post_views[1] +'\n'+'https://vk.com/math_and_physics?w=wall-61817535_'+post_ids[1], id_discuss)
            except:
                print("Today was only one posts")
            else:
                try:
                    self.sendMsg('Третье место - ' + post_views[2] +'\n'+'https://vk.com/math_and_physics?w=wall-61817535_'+post_ids[2], id_discuss)
                except:
                    print("Today was only two posts")


    def output(self, event):
        print("Username: " + self.getUserName(event.object.message.get('from_id')))
        print("From: " + self.getUserCity(event.object.message.get('from_id')))
        print("Text: " + event.object.message.get('text'))
        print("Type: ")


        if event.object.message.get('id') > 0:
            print("private message")
        else:
            print("group message")
        print(" --- ")

