from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'multiply_app'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    factor = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    number_enterned = models.FloatField()


# PAGES
class MyPage(Page):
    form_model = "player"
    form_fields = ["number_enterned"]


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        result = player.number_enterned * C.factor
        return {
            "result": result
        }


page_sequence = [MyPage, Results]
