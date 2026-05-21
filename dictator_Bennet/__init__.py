from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'dictator_Bennet'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    Payment_Start = cu(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    number_kept = models.IntegerField()
    min = 0
    max = C.Payment_Start
    label = "I will keep"
    currency_accepted = models.BooleanField(
        label="I accept the offer")


class Player(BasePlayer):
    pass

def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = group.number_kept
    p2.payoff = C.Payment_Start - group.number_kept
    
# PAGES
class MyPage(Page):
    form_model = "group"
    form_fields = ["number_kept"]


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return {
            "number_kept": group.number_kept,
            "number_sent": C.Payment_Start - group.number_kept
        }
    
class Results2(Page): # This page is only for the receiver, to accept or decline the offer
    form_model = "group"
    form_fields = ["currency_accepted"]
    @staticmethod
    def acceptDecline(player: Player):
        group = player.group
        return {
            "number_kept": group.number_kept,
            "number_sent": C.Payment_Start - group.number_kept
        }    


page_sequence = [MyPage, ResultsWaitPage , Results2]
