from otree.api import Currency as c, currency_range, safe_json
from ._builtin import Page, WaitPage
from .models import Constants, Player

#This is the pages.py file. Here we structure how our pages and pagesequence function.
#Each page has its own class where you always specify form_model = Player as we have players for each page
#and we have the form_fields in a list which indicate the variables we have on that page. There will be
#more functionality added here but this is a good start. 

from survey_example_appfolder.HelperFunctions import detect_screenout, detect_quota

class Welcome(Page):
    form_model = Player
    form_fields = ['device_type', 'operating_system', 'screen_height', 'screen_width', 'entry_question']


class DemoPage(Page):
    form_model = Player
    form_fields = ['age_question',
                    'gender_question', 'gender_popout', 'time_gender_popout', 
                    'has_travelled', 'travel_destination_popout', 'time_travel_popout']
        
    def vars_for_template(self):
        return {'participant_label': safe_json(self.participant.label),
                'screenout': safe_json(self.player.screenout),
                'quota': safe_json(self.player.quota),
                'info_quota': safe_json(self.session.vars), #display for debugging
                'available_genders': self.session.config['available_genders']  # Pass gender options
                }
    def before_next_page(self):
        detect_screenout(self)
        detect_quota(self)

class Screening(Page):
    form_model = Player
    def vars_for_template(self):
        return {'participant_label': safe_json(self.participant.label),
                'screenout': safe_json(self.player.screenout),
                'quota': safe_json(self.player.quota),
                'info_quota': safe_json(self.session.vars), #display for debugging
                'available_genders': self.session.config['available_genders']  # Pass gender options
                }

class CatsAndDogsPage(Page):
    form_model = Player
    form_fields = ['cats_or_dogs']

    def is_displayed(self):
        '''
        this otree function that regulates if a page is displayed or not
        '''
        #this will show the page to anybody who has the right assignment so in this case 
        return self.player.group_assignment == 1

class PineappleOnPizzaPage(Page):
    form_model = Player
    form_fields = ['pineapple_on_pizza']

    def is_displayed(self):
        '''
        this otree function that regulates if a page is displayed or not
        '''
        #this will show the page to anybody who has the right assignment so in this case 
        return self.player.group_assignment == 2

class MoneyPage(Page):
    form_model = Player
    form_fields = ['money_essay', 'money_question']

class EndPage(Page):
    def vars_for_template(self):
        '''this is another function by otree which allows you to "send" variables
        to html files if you need to access them from there'''
        return {"group_assignment": safe_json(self.player.group_assignment)}

class RedirectPage(Page):
    form_model = Player
    def vars_for_template(self):
        return {'participant_label': safe_json(self.participant.label)}

#Here we define in which ordering we want the pages to be shown. We always start with a Welcome page and end with an End page.
page_sequence = [Welcome,
                DemoPage,
                Screening,
                CatsAndDogsPage, 
                PineappleOnPizzaPage,
                MoneyPage,          
                EndPage,
                RedirectPage]