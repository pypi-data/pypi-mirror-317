import boozelib
from . import *

class AlcoholConsumption:
    def alcohol_consumption_help(self,print_only=True):
        msg=f''''''
        for i in self.options:
            msg+=f"\n{self.options[i]['cmds']} - {self.options[i]['desc']}"
        if not print_only:
            return msg
        print(msg)

    def bac_usa(self):
        weight_pounds=Prompt.__init2__(None,func=FormBuilderMkText,ptext="How much is your weight in pounds?",helpText="pounds",data="float")
        if weight_pounds in [None,'d']:
            return
        height_inches=Prompt.__init2__(None,func=FormBuilderMkText,ptext="How tall are you in inches?",helpText="inches",data="integer")
        if height_inches in [None,'d']:
            return
        cm_ht=pint.UnitRegistry().convert(height_inches,"inches","centimeters")
        kg_wt=pint.UnitRegistry().convert(weight_pounds,"pounds","kilograms")
        #True for female

        sex=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Male[False] or Female[True]",helpText="DONT TYPE MALE or FEMALE, you will be FEMALE. true values are female",data="boolean")
        if sex in [None,]:
            return
        elif sex in ['d',]:
            sex=False
        #mL
        volume=Prompt.__init2__(None,func=FormBuilderMkText,ptext="How Much Volume in mL?",helpText="milliters",data="float")
        if volume in [None,]:
            return
        #% of total valume alcohol
        #percent=(((0.09*568)+(0.095*568))/volume)*100
        percent=Prompt.__init2__(None,func=FormBuilderMkText,ptext="What is the % ABV?",helpText="% abv",data="float")
        if percent in [None,]:
            return
        age=Prompt.__init2__(None,func=FormBuilderMkText,ptext="What is date of birth?",helpText="date",data="datetime")
        if age in ['d',None]:
            return
        age=pint.UnitRegistry().convert((age-datetime.now()).total_seconds(),"seconds","years")
        value=boozelib.get_blood_alcohol_content(age=age,weight=kg_wt,height=cm_ht,sex=sex,volume=volume,percent=percent)
        
        deg=0
        minutes=0
        while deg <= value:
            deg=boozelib.get_blood_alcohol_degradation(age=age,weight=kg_wt,height=cm_ht,sex=sex,minutes=minutes)
            minutes+=1
            print(deg,minutes,value)
        msg=f'''
BAC:{value}
Volume:{volume}
% ABC:{percent}
SEX:{sex}
WEIGHT(KG):{kg_wt}
HEIGHT(CM):{cm_ht}
Time To BAC(0) in Minutes: {timedelta(seconds=minutes*60)}
        '''
        print(msg)

    def __init__(self):
        self.options={
            'help':{
                'cmds':['alcohol consumption help','ach'],
                'exec':self.alcohol_consumption_help,
                'desc':"helpful info for this tool"
                },
            'bac usa':{
                'cmds':['bac usa','blood alcohol content estimate usa'],
                'exec':self.bac_usa,
                'desc':'blood alcohol content estimate usa',
            },
            }
        while True:
            command=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f'{Fore.grey_70}[{Fore.light_steel_blue}AlcoholConsumption{Fore.grey_70}] {Fore.light_yellow}Menu[help/??/?]',helpText=self.alcohol_consumption_help(print_only=False),data="string")
            print(command)
            if command in [None,]:
                break
            elif command in ['','d']:
                self.alcohol_consumption_help(print_only=True)
            for option in self.options:
                if self.options[option]['exec'] != None and (command.lower() in self.options[option]['cmds'] or command in self.options[option]['cmds']):
                    self.options[option]['exec']()
                elif self.options[option]['exec'] == None and (command.lower() in self.options[option]['cmds'] or command in self.options[option]['cmds']):
                    return
