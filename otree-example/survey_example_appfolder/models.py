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
        for p in self.get_players(): # every player in player
            # is assigned to either group 1 or 2  randomly.
            p.group_assignment = random.Random().randint(1, 2)

class Group(BaseGroup):
   pass

class Player(BasePlayer):
    #this is the most important feature of this file. We can collect all the variables used on the html pages here
    
    # Assigning each player to either group 1 or 2 in the beginning
    group_assignment = models.IntegerField()

    # Welcome
    device_type = models.IntegerField()
    operating_system = models.IntegerField()
    screen_height = models.IntegerField(initial=-999)
    screen_width = models.IntegerField(initial=-999)
    entry_question = models.StringField(
        blank=True, 
        initial=-999, #this is an optional field through blank = True
        abel = "<b>Have you ever participated in an online survey before?</b>")
    # DemoPage
    age_question = models.IntegerField(
        max=110, min=1,
        label = "<b>How old are you?</b>")  #we can also have max and min guidelines
    gender_question = models.StringField(
        label = "<b>Which is your gender?</b>")
    # CatsAndDogsPage
    cats_or_dogs = models.IntegerField(label="<b>Do you prefer cats or dogs?</b>") 
    # PineappleOnPizzaPage
    pineapple_on_pizza = models.IntegerField(
        label = "<b>How much do you like pineapple on pizza?</b>",
        widget=widgets.RadioSelectHorizontal,
        choices=[
          [5, 'Heaven on earth'],
          [4, 'Like it'],
          [3, 'Neither'],
          [2, 'Don\'t like it'],
          [1, 'Not at all']])
    # PopoutPage
    has_travelled = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No']]
    )
    travel_destination_popout = models.LongStringField(
        blank=True,
        label="<b>Where did you go?</b>")
    time_popout = models.StringField(initial=-999)
    # MoneyPage
    money_essay = models.LongStringField(
        blank=True,
        label="<b>Please write a short argumentative essay about why it is a moral duty to gift money to students:</b>")
    money_question = models.CurrencyField(
        label="<b>How much do you want to gift me?</b>"
    )
    # EndPage
    group_assignment = models.IntegerField()  # Why do we assign the group on the last page?
                                              # Also, not everyone completes the survey, bu we might still be interested in
                                              # whether the person would have belonged to a certain group?

    #custom error message
        #has to: 
        #1) be in the class Player (important to indent the right way)
        #2) have a specific name "variablename"_error_message
    def age_question_error_message(player, value):
        if value < 18:
            return 'I highly doubt that you are under 18. Please be honest.'
        if value > 30:
            return 'I highly doubt that you are over 30. Please be honest.'
        
    def money_question_error_message(player, value):
        if value < 20:
            return 'Aren\'t you a generous person? Value should be 20 or higher!'

                                                