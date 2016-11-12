import time
from slack_model import SlackModel
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))


class SlackApp():
    """
    Slack Call app
    You preapre the chainer model, You execute the bellow command, you can play the dialogue app
    Example
        python app.py
    """

    def __init__(self, data_paramater):
        """
        Iniital Setting
        :param data_model: Setting Slack Model. Slack Model has the a lot of paramater
        """
        self.slack_channel = data_paramater.slack_channel
        """
        We confirm channel number
        https://api.slack.com/methods/channels.list
        """
        self.chan = data_paramater.chan
        self.usr = data_paramater.user
        self.message = data_paramater.message

    def call_method(self):
        """
        Slack api call
        1: read sentence
        2: return the sentence
        """
        if self.slack_channel.rtm_connect():
            while True:
                self.data = self.slack_channel.rtm_read()
                self.__judge_call()
                time.sleep(1)
        else:
            print("connection Fail")

    def __judge_call(self):
        """
        judge slack call for Slack
        Example:
            search_bot:{your sentence}
                return the sentence
        """
        if len(self.data) >= 1 and "text" in self.data[0]:
            if "search_bot:" in self.data[0]["text"]:
                word = self.message
                print(self.slack_channel.api_call("chat.postMessage", user=self.usr, channel=self.chan, text=word))

if __name__ == '__main__':
    data_paramater = SlackModel()
    data_paramater.read_config()
    slack = SlackApp(data_paramater)
    slack.call_method()