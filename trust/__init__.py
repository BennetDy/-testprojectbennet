from otree.api import *




doc = """
This is a standard 2-player trust game where the amount sent by player 1 gets
tripled. The trust game was first proposed by
<a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" target="_blank">
    Berg, Dickhaut, and McCabe (1995)
</a>.
"""


class C(BaseConstants):
    NAME_IN_URL = 'trust'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    # Initial amount allocated to each player
    ENDOWMENT = cu(500)
    MULTIPLIER = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        choices=[0,50,100,150,200, 250, 300, 350, 400, 450, 500],
        doc="""Amount sent by P1""",
        label="Please enter an amount from 0 to 500, in steps of 50:",
    )
    sent_back_amount_000 = models.CurrencyField(label='', doc="""Amount sent back by P2""", min=cu(0), max=cu(0))
    sent_back_amount_050 = models.CurrencyField(label='', doc="""Amount sent back by P2""", min=cu(0), max=cu(150))
    sent_back_amount_100 = models.CurrencyField(label='', doc="""Amount sent back by P2""", min=cu(0), max=cu(300))
    sent_back_amount_150 = models.CurrencyField(label='', doc="""Amount sent back by P2""", min=cu(0), max=cu(450))
    sent_back_amount_200 = models.CurrencyField(label='', doc="""Amount sent back by P2""", min=cu(0), max=cu(600))
    sent_back_amount_250 = models.CurrencyField(label='', doc="""Amount sent back by P2""", min=cu(0), max=cu(750))
    sent_back_amount_300 = models.CurrencyField(label='', doc="""Amount sent back by P2""", min=cu(0), max=cu(900))
    sent_back_amount_350 = models.CurrencyField(label='', doc="""Amount sent back by P2""", min=cu(0), max=cu(1050))
    sent_back_amount_400 = models.CurrencyField(label='', doc="""Amount sent back by P2""", min=cu(0), max=cu(1200))
    sent_back_amount_450 = models.CurrencyField(label='', doc="""Amount sent back by P2""", min=cu(0), max=cu(1350))
    sent_back_amount_500 = models.CurrencyField(label='', doc="""Amount sent back by P2""", min=cu(0), max=cu(1500))


class Player(BasePlayer):
    pass


# FUNCTIONS
def sent_back_amount_max(group: Group):
    return group.sent_amount * C.MULTIPLIER


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    if group.sent_amount == cu(0):
        p1.payoff = C.ENDOWMENT -group.sent_amount + group.sent_back_amount_000
        p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount_000
    elif group.sent_amount == cu(50):
        p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount_050
        p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount_050
    elif group.sent_amount == cu(100):
        p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount_100
        p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount_100
    elif group.sent_amount == cu(150):
        p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount_150
        p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount_150
    elif group.sent_amount == cu(200):
        p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount_200
        p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount_200
    elif group.sent_amount == cu(250):
        p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount_250
        p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount_250
    elif group.sent_amount == cu(300):
        p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount_300
        p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount_300
    elif group.sent_amount == cu(350):
        p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount_350
        p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount_350
    elif group.sent_amount == cu(400):
        p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount_400
        p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount_400
    elif group.sent_amount == cu(450):
        p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount_450
        p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount_450
    elif group.sent_amount == cu(500):
        p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount_500
        p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount_500
# PAGES
class Introduction(Page):
    pass


class Send(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = 'group'
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class SendBackWaitPage(WaitPage):
    pass


class SendBack(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = 'group'
    form_fields = [
    'sent_back_amount_000',
    'sent_back_amount_050',
    'sent_back_amount_100',
    'sent_back_amount_150',
    'sent_back_amount_200',
    'sent_back_amount_250',
    'sent_back_amount_300',
    'sent_back_amount_350',
    'sent_back_amount_400',
    'sent_back_amount_450',
    'sent_back_amount_500',
]


    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        tripled_amount = group.sent_amount * C.MULTIPLIER
        return dict(tripled_amount=tripled_amount)


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    """This page displays the earnings of each player"""

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(tripled_amount=group.sent_amount * C.MULTIPLIER)


page_sequence = [
    Introduction,
    Send,
    SendBackWaitPage,
    SendBack,
    ResultsWaitPage,
    Results,
]
