from otree.api import *


doc = """
Altruism task: participants receive 300 points and decide how many points
to donate to a charitable organization.
"""


class C(BaseConstants):
    NAME_IN_URL = 'altruism'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    ENDOWMENT = cu(300)

    CHARITY_CHOICES = [
        'Brot für die Welt',
        'Kindernothilfe',
        'German Red Cross',
        'Welthungerhilfe',
        'Bund für Umwelt und Naturschutz Deutschland',
        'Greenpeace',
        'Terre des Hommes',
        'Aktion Mensch',
        'Other',
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    donation = models.CurrencyField(
        min=0,
        max=C.ENDOWMENT,
        label=f'How many of your {C.ENDOWMENT} points do you want to donate?',
    )

    charity = models.StringField(
        choices=C.CHARITY_CHOICES,
        widget=widgets.RadioSelect,
        label='Which charitable organization should receive your donation?',
    )

    other_charity = models.StringField(
        blank=True,
        label='If other, please name the charitable organization:',
    )


# PAGES
class Decision(Page):
    form_model = 'player'
    form_fields = ['donation', 'charity', 'other_charity']

    @staticmethod
    def error_message(player: Player, values):
        if values['charity'] == 'Other' and not values['other_charity']:
            return 'Please specify the name of the charitable organization.'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.payoff = C.ENDOWMENT - player.donation


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        selected_charity = player.other_charity if player.charity == 'Other' else player.charity
        return dict(
            selected_charity=selected_charity,
            donation=player.donation,
            kept_amount=C.ENDOWMENT - player.donation,
        )


page_sequence = [Decision, Results]