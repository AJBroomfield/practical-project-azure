import logging
import random
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    player_class=random.choice(['Barbarian','Bard','Cleric','Driud','Fighter','Monk','Paladin','Ranger','Rogue','Sorcerer','Warlock','Wizard'])

    return func.HttpResponse(player_class)
