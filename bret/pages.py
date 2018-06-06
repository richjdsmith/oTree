from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player
import random


# ******************************************************************************************************************** #
# *** Welcome and Gender Choice *** #
# ******************************************************************************************************************** #
class Questions(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = 'player'
    form_fields = ['gender','age','amazon_turk_id']

# ******************************************************************************************************************** #
# *** CLASS GAME *** #
# ******************************************************************************************************************** #
class Gamedescription(Page):

    # only display instruction in round 1
    def is_displayed(self):
        return self.subsession.round_number == 1

    # variables for use in template
    def vars_for_template(self):
        return {

        }


# ******************************************************************************************************************** #
# *** CLASS BOMB RISK ELICITATION TASK *** #
# ******************************************************************************************************************** #

# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class Instructions(Page):

    # only display instruction in round 1
    def is_displayed(self):
        return self.subsession.round_number == 1

    # variables for use in template
    def vars_for_template(self):
        return {
            'num_rows':             Constants.num_rows,
            'num_cols':             Constants.num_cols,
            'num_boxes':            Constants.num_rows * Constants.num_cols,
            'num_nobomb':           Constants.num_rows * Constants.num_cols - 1,
            'box_value':            Constants.box_value,
            'time_interval':        Constants.time_interval,
        }


# ******************************************************************************************************************** #
# *** CLASS BOMB RISK ELICITATION TASK *** #
# ******************************************************************************************************************** #
class Decision(Page):

    # form fields on player level
    form_model = 'player'
    form_fields = [
        'bomb',
        'boxes_collected',
        'bomb_row',
        'bomb_col',
    ]

    def current_round_number(self):
        return self.subsession.round_number

    # BRET settings for Javascript application
    def vars_for_template(self):
        reset = self.participant.vars.get('reset',False)
        if reset:
            del self.participant.vars['reset']

        input = not Constants.devils_game if not Constants.dynamic else False

        otree_vars = {
            'reset':            reset,
            'input':            input,
            'random':           Constants.random,
            'dynamic':          Constants.dynamic,
            'num_rows':         Constants.num_rows,
            'num_cols':         Constants.num_cols,
            'feedback':         Constants.feedback,
            'undoable':         Constants.undoable,
            'box_width':        Constants.box_width,
            'box_height':       Constants.box_height,
            'time_interval':    Constants.time_interval,
        }

        return {
            'otree_vars':       otree_vars
        }

    def before_next_page(self):
        self.participant.vars['reset'] = True
        self.player.set_payoff()


# ******************************************************************************************************************** #
# *** CLASS RESULTS *** #
# ******************************************************************************************************************** #
class Results(Page):

    # only display results after all rounds have been played
    def is_displayed(self):
        return self.subsession.round_number == 6

    # variables for use in template
    def vars_for_template(self):
        payoff_round = random.randint(3,6)
        total_payoff = ([p.payoff for p in self.player.in_all_rounds()])
        self.participant.vars['bret_payoff'] = total_payoff

        return {
            'player_in_all_rounds':   self.player.in_all_rounds(),
            'box_value':              Constants.box_value,
            'boxes_total':            Constants.num_rows * Constants.num_cols,
            'boxes_collected':        self.player.boxes_collected,
            'bomb':                   self.player.bomb,
            'bomb_row':               self.player.bomb_row,
            'bomb_col':               self.player.bomb_col,
            'round_result':           self.player.round_result,
            'round_to_pay':           payoff_round,
            'payoff':                 self.player.payoff,
            'total_payoff':           total_payoff,
        }


# ******************************************************************************************************************** #
# *** COMPETITIVE *** #
# ******************************************************************************************************************** #
class Competitive(Page):
    def is_displayed(self):
        return self.subsession.round_number == 7

    def vars_for_template(self):
        return {
            'treatment': self.participant.vars['treatment'],
           
        }



# ******************************************************************************************************************** #
# *** FINAL *** #
# ******************************************************************************************************************** #
class ResultsFinal(Page):
    def is_displayed(self):
        return self.subsession.round_number == 7

    def vars_for_template(self):
        payoff_round = random.randint(2,5)
        total_payoff = ([p.payoff for p in self.player.in_all_rounds()])
        self.participant.vars['bret_payoff'] = total_payoff

        return {
            'player_in_all_rounds':   self.player.in_all_rounds(),
            'box_value':              Constants.box_value,
            'boxes_total':            Constants.num_rows * Constants.num_cols,
            'boxes_collected':        self.player.boxes_collected,
            'bomb':                   self.player.bomb,
            'bomb_row':               self.player.bomb_row,
            'bomb_col':               self.player.bomb_col,
            'round_result':           self.player.round_result,
            'round_to_pay':           payoff_round,
            'payoff':                 self.player.payoff,
            'total_payoff':           total_payoff,
            'naw': self.participant.code,
        }


# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Questions,Gamedescription, Instructions,Competitive,Decision,Results,ResultsFinal]


