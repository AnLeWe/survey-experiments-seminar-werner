import random

def random_number(x, y):
    '''
    method for random integers
    '''  
    rng = random.Random()
    number = rng.randint(x, y)
    return number



'''
we also want to implement some functions to help with the quota checking and 
to have an overwview (counting) who is taking part in our survey.

Generally when it comes to redirecting we distinguish between people who: 
1. took part in the whole survey (and get redirected as success to the provider)
2. people who get screened-out (meaning they did not fulfill a characteristic one agreed upon previously)
3. people who get redirected because the quota is already full

We encode those three different events in three different variables (booleans) to use for redirecting

'''

def detect_screenout(self):
    '''
    this function will check for characteristics a participant needs to 
    take part in the survey, (f.e. a certain age or being eligible to vote)
    '''

    if self.player.age_question > 40: # screen out anybody that is not eligible
        self.player.screenout = 1

#screenout if quota is already full 
def detect_quota(self):
    
    if self.player.screenout == 0 and self.player.quota == 0:

        # Acces gender quotas dict
        gender_quotas = self.session.vars['gender_quotas']
        # Store the selected gender 
        selected_gender = self.player.gender_question 

        # Get the current completed count for the selected gender
        current_count = self.session.vars[f"completed_gender_{selected_gender}"]
        max_quota = gender_quotas[selected_gender]

        # Apply quota logic
        if current_count >= max_quota:
             self.player.quota = True  # Mark as screened out
        else:
            # Increment the quota counter for the selected gender
            self.session.vars[f"completed_gender_{selected_gender}"] += 1
            self.player.quota = False


# def participant_count(self):
#     '''if we want to count different things we might also implement a function here.
#     For now we are just using the counter we implemented before'''
#     return None