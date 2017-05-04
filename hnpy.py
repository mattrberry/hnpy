import requests
import time

baseURL = "https://hacker-news.firebaseio.com/v0/"


# itemid is the string of the numerical id
def makeItem(itemid):
    itemjson = requests.get(baseURL + "item/" + itemid + ".json").json()
    itemtype = itemjson["type"]
    if "story" in itemtype:
        # Items of type "ask" say they are of type "story"
        if "text" not in itemjson:
            item = Story(itemjson)
        else:
            item = Ask(itemjson)
    elif "comment" in itemtype:
        item = Comment(itemjson)
    elif "job" in itemtype:
        item = Job(itemjson)
    elif "pollopt" in itemtype:
        item = PollOption(itemjson)
    elif "poll" in itemtype:
        item = Poll(itemjson)
    return item


class HackerNews(object):
    def getTop(self):
        self.top = requests.get(baseURL + "topstories.json").json()

    def getNew(self):
        self.new = requests.get(baseURL + "newstories.json").json()

    def getBest(self):
        self.best = requests.get(baseURL + "beststories.json").json()

    def getAskStories(self):
        self.ask = requests.get(baseURL + "askstories.json").json()

    def getShowStories(self):
        self.show = requests.get(baseURL + "showstories.json").json()

    def getJobStories(self):
        self.job = requests.get(baseURL + "jobstories.json").json()

    def load(self, ids, amount, start=0):
        self.loaded = []
        for index in range(start, start + amount):
            if index < len(ids):
                item = makeItem(str(ids[index]))
                self.loaded.append(item)


class Item(object):
    def __init__(self, itemjson):
        self.id = str(itemjson["id"])
        self.by = itemjson["by"]
        self.time = itemjson["time"]

    def age(self):
        return int(time.time()) - self.time

    def ageString(self):
        age = self.age()
        if age / (60 * 60 * 24) >= 1:
            return str(int(age / (60 * 60 * 24))) + " days"
        elif age / (60 * 60) >= 1:
            return str(int(age / (60 * 60))) + " hrs"
        elif age / 60 >= 1:
            return str(int(age / 60)) + " mins"
        else:
            return str(age) + " secs"


class Story(Item):
    def __init__(self, itemjson):
        Item.__init__(self, itemjson)
        self.title = itemjson["title"]
        self.url = itemjson["url"]
        self.descendants = itemjson["descendants"]
        if "kids" in itemjson:
            self.kids = itemjson["kids"]
        else:
            self.kids = []
        self.score = itemjson["score"]

    def loadKids(self):
        self.loadedkids = []
        for kid in self.kids:
            item = makeItem(str(kid))
            self.loadedkids.append(item)

    def infoString(self):
        return "{} points by {} {} ago | {} comments".format(
                self.score, self.by, self.ageString(), self.descendants)


class Comment(Item):
    def __init__(self, itemjson):
        Item.__init__(self, itemjson)
        self.text = itemjson["text"]
        if "kids" in itemjson:
            self.kids = itemjson["kids"]
        else:
            self.kids = []

    def loadKids(self):
        self.loadedkids = []
        for kid in self.kids:
            item = makeItem(str(kid))
            self.loadedkids.append(item)


class Ask(Item):
    def __init__(self, itemjson):
        Item.__init__(self, itemjson)
        self.title = itemjson["title"]
        self.text = itemjson["text"]
        self.descendants = itemjson["descendants"]
        if "kids" in itemjson:
            self.kids = itemjson["kids"]
        else:
            self.kids = []
        self.score = itemjson["score"]

    def loadKids(self):
        self.loadedkids = []
        for kid in self.kids:
            item = makeItem(str(kid))
            self.loadedkids.append(item)

    def infoString(self):
        return "{} points by {} {} ago | {} comments".format(
                self.score, self.by, self.ageString(), self.descendants)


class Job(Item):
    def __init__(self, itemjson):
        Item.__init__(self, itemjson)
        self.title = itemjson["title"]
        if "text" in itemjson:
            self.text = itemjson["text"]
        else:
            self.text = ""
        if "url" in itemjson:
            self.url = itemjson["url"]
        else:
            self.url = ""

    def infoString(self):
        return "{} ago".format(self.ageString())


class Poll(Item):
    def __init__(self, itemjson):
        Item.__init__(self, itemjson)
        self.title = itemjson["title"]
        self.text = itemjson["text"]
        self.descendants = itemjson["descendants"]
        if "kids" in itemjson:
            self.kids = itemjson["kids"]
        else:
            self.kids = []
        self.parts = itemjson["parts"]
        self.score = itemjson["score"]

    def loadKids(self):
        self.loadedkids = []
        for kid in self.kids:
            item = makeItem(str(kid))
            self.loadedkids.append(item)

    def infoString(self):
        return "{} points by {} {} ago | {} comments".format(
                self.score, self.by, self.ageString(), self.descendants)


class PollOption(Item):
    def __init__(self, itemjson):
        Item.__init__(self, itemjson)
        self.text = itemjson["text"]
        self.score = itemjson["score"]
