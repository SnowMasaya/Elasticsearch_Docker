from slackclient import SlackClient
import yaml
from collections import namedtuple


class SlackModel():

    def __init__(self):
        """
        setting paramater Slack model
        :return:
        """
        self.Slack = namedtuple("slack", ["api_token", "channel", "user_name", "message", "icon_url"])
        self.config_file = "enviroment_slack.yml"
        self.slack_channel = ""
        self.chan = ""
        self.user_name = ""
        self.message = ""
        self.icon_url = ""

    def read_config(self):
        """
        read config file for slack
        """
        with open(self.config_file, encoding="utf-8") as cf:
           e = yaml.load(cf)
           slack = self.Slack(e["slack"]["api_token"], e["slack"]["channel"],
                              e["slack"]["user_name"], e["slack"]["message"],
                              e["slack"]["icon_url"])
           self.slack_channel = SlackClient(slack.api_token)
           self.chan = slack.channel
           self.user_name = slack.user_name
           self.message = slack.message
           self.icon_url = slack.icon_url
