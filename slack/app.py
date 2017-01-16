import time
from slack_model import SlackModel
import sys
import os
import re
from get_answer import GetAnswer
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
        self.user_name = data_paramater.user_name
        self.message = data_paramater.message
        self.icon_url = data_paramater.icon_url
        self.elastic_search = GetAnswer()

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
            input_text = self.data[0]["text"]
            if "search_bot:" in input_text:
                if "?" in input_text or "？" in input_text:
                    word = self.__search_word(input_text)
                    self.__slack_call(word)
                else:
                    word = self.message
                    self.__slack_call(word)

    def __search_word(self, input_text):
        """
        Search word by the Elasticsearch Docker
        :param input_text(string): input the search word
        :return(string): search result
        """
        replace_input = re.sub("search_bot:|\?|\？", "", input_text.strip())
        self.elastic_search.search_data(replace_input)
        if len(self.elastic_search.search_result) > 0:
            hyp_batch = self.elastic_search.search_result[0]
            word = hyp_batch["title"] + "\n" + hyp_batch["abstract"] + "\n" + hyp_batch["url"]
        else:
            word = "No match"
        return word

    def __slack_call(self, word):
        """
        Post Message Slack app
        :param word(string): post message
        """
        print(self.slack_channel.api_call("chat.postMessage", username=self.user_name, channel=self.chan, text=word, \
                                          icon_url=self.icon_url))

if __name__ == '__main__':
    data_paramater = SlackModel()
    data_paramater.read_config()
    slack = SlackApp(data_paramater)
    slack.call_method()
