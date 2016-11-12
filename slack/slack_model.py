from slackclient import SlackClient
import yaml
from collections import namedtuple


class SlackModel():

    def __init__(self):
        """
        setting paramater Slack model
        :return:
        """
        self.Slack = namedtuple("Slack", ["api_token", "channel", "user", "message"])
        self.config_file = "enviroment_slack.yml"
        self.slack_channel = ""
        self.chan = ""
        self.user = ""
        self.message = ""

    def read_config(self):
        """
        read config file for slack
        """
        with open(self.config_file, encoding="utf-8") as cf:
           e = yaml.load(cf)
           slack = self.Slack(e["slack"]["api_token"], e["slack"]["channel"],
                              e["slack"]["user"], e["slack"]["message"])
           self.slack_channel = SlackClient(slack.api_token)
           self.chan = slack.channel
           self.user = slack.user
           self.message = slack.message