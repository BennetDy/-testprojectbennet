from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'prisoners_dilemma_simple'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    payoff_both_cooperate = -1
    payoff_both_defect = -3
    payoff_coopered_defect_high = 0
    payoff_coopered_defect_low = -4


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    defect = models.BooleanField(
        label="Please choose if you want to cooperate or defect",
        choices=[
            [True, "Defect"],
            [False, "Cooperate"]
        ]
    )


# PAGES
class MyPage(Page):
    form_model = "player"
    form_fields = ["defect"]


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        player_lists = group.get_players()
        player_1 = player_lists[0]
        player_2 = player_lists[1] 
        if player_1.defect:
            if player_2.defect:
                player_1.payoff = C.payoff_both_defect
                player_2.payoff = C.payoff_both_defect
            else:
                player_1.payoff = C.payoff_coopered_defect_high
                player_2.payoff = C.payoff_coopered_defect_low
        else:
            if player_2.defect:
                player_1.payoff = C.payoff_coopered_defect_low
                player_2.payoff = C.payoff_coopered_defect_high
            else:
                player_1.payoff = C.payoff_both_cooperate
                player_2.payoff = C.payoff_both_cooperate


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
