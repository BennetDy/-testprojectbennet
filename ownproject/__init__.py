from otree.api import *
import random


doc = """
One-app social preferences experiment:
1. Altruism
2. Trust game
3. Truth-telling
4. Random payment selection
"""


class C(BaseConstants):
    NAME_IN_URL = 'preferences'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    ALTRUISM_ENDOWMENT = cu(300)
    TRUST_ENDOWMENT = cu(100)
    TRUST_MULTIPLIER = 3


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()


class Group(BaseGroup):
    trust_sent_amount = models.CurrencyField(initial=0)
    trust_sent_back_amount = models.CurrencyField(initial=0)


class Player(BasePlayer):
    donation = models.CurrencyField(
        min=0,
        max=C.ALTRUISM_ENDOWMENT,
        label=f'How many of your {C.ALTRUISM_ENDOWMENT} points do you want to donate?'
    )

    trust_send = models.CurrencyField(
        min=0,
        max=C.TRUST_ENDOWMENT,
        blank=True,
        label=f'How many of your {C.TRUST_ENDOWMENT} points do you want to send?'
    )

    trust_send_back = models.CurrencyField(
        min=0,
        blank=True,
        label='How many points do you want to send back?'
    )

    reported_number = models.IntegerField(
        min=0,
        max=6,
        label='Please report the number you obtained (0-6).'
    )

    altruism_payoff = models.CurrencyField(initial=0)
    trust_payoff = models.CurrencyField(initial=0)
    truth_payoff = models.CurrencyField(initial=0)

    selected_task = models.StringField()
    selected_task_payoff = models.CurrencyField(initial=0)


class Altruism(Page):
    form_model = 'player'
    form_fields = ['donation']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.altruism_payoff = C.ALTRUISM_ENDOWMENT - player.donation


class TrustSend(Page):
    form_model = 'player'
    form_fields = ['trust_send']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.group.trust_sent_amount = player.trust_send


class TrustSendWaitPage(WaitPage):
    pass


class TrustSendBack(Page):
    form_model = 'player'
    form_fields = ['trust_send_back']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player):
        sent = player.group.trust_sent_amount
        tripled = sent * C.TRUST_MULTIPLIER
        return dict(
            sent=sent,
            tripled=tripled,
        )

    @staticmethod
    def error_message(player, values):
        max_back = player.group.trust_sent_amount * C.TRUST_MULTIPLIER
        if values['trust_send_back'] > max_back:
            return f'You cannot send back more than {max_back}.'

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.group.trust_sent_back_amount = player.trust_send_back


class TrustResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        p1 = group.get_player_by_id(1)
        p2 = group.get_player_by_id(2)

        sent = group.trust_sent_amount
        sent_back = group.trust_sent_back_amount
        tripled = sent * C.TRUST_MULTIPLIER

        p1.trust_payoff = C.TRUST_ENDOWMENT - sent + sent_back
        p2.trust_payoff = tripled - sent_back


class TruthTelling(Page):
    form_model = 'player'
    form_fields = ['reported_number']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.truth_payoff = cu(player.reported_number)*50


class Payment(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            altruism_payoff=player.altruism_payoff,
            trust_payoff=player.trust_payoff,
            truth_payoff=player.truth_payoff,
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        task_map = {
            'Altruism': player.altruism_payoff,
            'Trust Game': player.trust_payoff,
            'Truth-telling': player.truth_payoff,
        }

        chosen_task = random.choice(list(task_map.keys()))
        chosen_payoff = task_map[chosen_task]

        player.selected_task = chosen_task
        player.selected_task_payoff = chosen_payoff
        player.payoff = chosen_payoff


class FinalResults(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            selected_task=player.selected_task,
            selected_task_payoff=player.selected_task_payoff,
            altruism_payoff=player.altruism_payoff,
            trust_payoff=player.trust_payoff,
            truth_payoff=player.truth_payoff,
        )


page_sequence = [
    Start,
    Altruism,
    TrustSend,
    TrustSendWaitPage,
    TrustSendBack,
    TrustResultsWaitPage,
    TruthTelling,
    Payment,
    FinalResults,
]
