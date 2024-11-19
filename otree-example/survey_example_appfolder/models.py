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

author = 'Anna Werner'
doc = 'This a very small survey to learn the basics, sonsisting of 3 pages and different types of questions.'

class Constants(BaseConstants):
    name_in_url = 'survey-example'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    #we will only come to the group class when we look at advanced methods
    pass


class Player(BasePlayer):
    #this is the most important feature of this file. We can collect all the variables used on the html pages here
    
#The Variables are structured on the base of pages
    #The Variables are structured on the base of pages
    entry_question = models.StringField(blank = True) #this is an optional field through blank = True
    age_question = models.IntegerField(max=110, min=1)  #we can also have max and min guidelines
    cats_or_dogs = models.IntegerField(initial=-999) 
    pineapple_on_pizza = models.IntegerField(
    widget=widgets.RadioSelectHorizontal,
    choices=[
        [5, 'Heaven on earth'],
        [4, 'Like it'],
        [3, 'Neither'],
        [2, 'Don\'t like it'],
        [1, 'Not at all']],
        label = ''
        )


    #custom error message
        #has to: 
        #1) be in the class Player (important to indent the right way)
        #2) have a specific name "variablename"_error_message
    def age_question_error_message(player, value):
        if value < 18:
            return 'I highly doubt that you are under 18. Please be honest.'
        if value > 30:
            return 'I highly doubt that you are over 30. Please be honest.'
                                                