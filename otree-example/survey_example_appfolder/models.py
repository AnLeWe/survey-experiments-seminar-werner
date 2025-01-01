from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import random  # for random group assignment

author = 'Anna Werner'
doc = 'This a very small survey to learn the basics, consisting of 3 pages and different types of questions.'

class Constants(BaseConstants):
    name_in_url = 'survey-example'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
     def creating_session(self):
        """ 
        otree function that
        creates new subsession
        Any variables that need to be custom are created here
        """
        if 'gender_quotas' not in self.session.vars:
             #this for quota you wish to fill:
            self.session.vars['gender_quotas'] = {1: 20, 2: 20, 3: 20, 4: 20, 5:20, 6:20}
        # Create gender group counts
        # this will also be displayed in the data you download
        for gender in self.session.vars['gender_quotas'].keys():
            if f"completed_gender_{gender}" not in self.session.vars:
                self.session.vars[f"completed_gender_{gender}"] = 0

        for p in self.get_players(): # every player in player
            # is assigned to either group 1 or 2  randomly.
            p.group_assignment = random.Random().randint(1, 2)

class Group(BaseGroup):
   counter = models.IntegerField(initial = 0)

class Player(BasePlayer):
    # this is the most important feature of this file. 
    # We can collect all the variables used on the html pages here
    
    # Variables on the HelperFunctions.py
    screenout = models.BooleanField(initial=0)
    quota = models.BooleanField(initial=0)

    # Assigning each player to either group 1 or 2 in the beginning
    group_assignment = models.IntegerField()

    # Welcome
    device_type = models.IntegerField()
    operating_system = models.IntegerField()
    screen_height = models.IntegerField(initial=-999)
    screen_width = models.IntegerField(initial=-999)
    entry_question = models.StringField(
        blank=True, 
        initial=-999, 
        widget=widgets.TextInput(),  # Standard text input
        label = "<b>Have you ever participated in an online survey before?</b>"
        )
    # DemoPage
    age_question = models.IntegerField(
        max=110, min=1,
        label = "<b>How old are you?</b>" #we can also have max and min guidelines
        )
    time_gender_popout = models.StringField(initial=-999, blank=True)
    gender_question = models.IntegerField(choices=[(1, 'Female'), (2, 'Male'), (3, 'Non-binary'), (4, 'Agender'), (5, 'Other'), (6, 'Prefer not to say')], 
                                              initial=-999, label="<b>Which is your gender?</b>")
    gender_popout = models.StringField(
        blank=True,
        label = '<b>How do you identify?</b>'
        )
    time_travel_popout = models.StringField(initial=-999, blank=True)
    has_travelled = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No']]
            )
    travel_destination_popout = models.LongStringField(
        blank=True,
        label="<b>Where did you go?</b>"
        )
    # CatsAndDogsPage
    cats_or_dogs = models.IntegerField(label="<b>Do you prefer cats or dogs?</b>") 
    # PineappleOnPizzaPage
    pineapple_on_pizza = models.IntegerField(
        label = "<b>How much do you like pineapple on pizza?</b>",
        choices=[
          [5, 'Heaven on earth'],
          [4, 'Like it'],
          [3, 'Neither'],
          [2, 'Don\'t like it'],
          [1, 'Not at all']],
          widget=widgets.RadioSelectHorizontal
          )
    # MoneyPage
    money_essay = models.LongStringField(
        blank=True,
        label="<b>Please write a short argumentative essay about why it is a moral duty to gift money to students:</b>"
        )
    money_question = models.CurrencyField(
        label="<b>How much do you want to gift me?</b>"
    )

    #custom error message
        #has to: 
        #1) be in the class Player (important to indent the right way)
        #2) have a specific name "variablename"_error_message

    def money_question_error_message(player, value):
        if value < 20:
            return 'Aren\'t you a generous person? Value should be 20 or higher!'  
