import logging
import random
import azure.functions as func
import requests
from flask import Flask, render_template

def main(req: func.HttpRequest) -> func.HttpResponse:   
    def stat_roller(role,race):
        stats=[]
        for i in range(6):
            stat = []
            for i in range(4):
                stat.append(random.randint(1,6))
            stat.remove(min(stat))
            stats.append(sum(stat))
    
        primary_ability={
            'Barbarian':0,
            'Bard':5,
            'Cleric':4,
            'Driud':4,
            'Fighter':0,
            'Monk':1,
            'Paladin':0,
            'Ranger':1,
            'Rogue':1,
            'Sorcerer':5,
            'Warlock':5,
            'Wizard':3
            }
        if primary_ability[role] != stats.index(max(stats)):
            stats[primary_ability[role]], stats[stats.index(max(stats))] = stats[stats.index(max(stats))], stats[primary_ability[role]] #makes the primary ability the max stat

        ability_score={
            'Dwarf':[[2,2],[0,2]],
            'Elf':[[1,2],[4,1]],
            'Halfling':[[1,2],[2,1]],
            'Human':[[random.randint(0,5),1],[random.randint(0,5),1]],
            'Dragonborn':[[0,2],[5,1]],
            'Gnome':[[3,2],[2,1]],
            'Half-Elf':[[5,2],[random.randint(0,4),1],[random.randint(0,4),1]],
            'Half-Orc':[[0,2],[2,1]],
            'Teifling':[[3,1],[5,2]]
            } # [ability,increase]
        
        stat_increase=ability_score[race] #finds the stat increase based on the players race

        for i in range(len(stat_increase)):
            stats[stat_increase[i][0]] += stat_increase[i][1]
        
        ability={}
        ability_title = ('STR','DEX','CON','INT','WIS','CHA') 
        for i in range(6):
            ability[ability_title[i]]=stats[i]

        return ability
    
    player_class_response = requests.get('https://practical-project-dnd-stats.azurewebsites.net/api/class-gen?code=doMuGQczl/yzUKkEjAK0eCZf9A5IRRBpqeLrfgcVjOLZWHVz7TaeaA==')
    player_race_response = requests.get('https://practical-project-dnd-stats.azurewebsites.net/api/race-gen?code=Tt6pRkepWxZ/4pwivLl1sfmMXVUKXkaeY7Pj4pek51ffyIsWcOaL7Q==')
    player_class = player_class_response.text
    player_race = player_race_response.text

    player_ability=stat_roller(player_class,player_race)    

    ability_format=''

    for key, value in player_ability.items():
        if len(ability_format)!=0:
            ability_format+=', '
        ability_format += f'{key} {value}'

    
    
    return func.HttpResponse(f'Your are a {player_race} {player_class} with the stats of: {ability_format}')