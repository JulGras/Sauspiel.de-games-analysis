# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 15:22:06 2022

@author: UGrasJu
"""
# %% import txt data (3 html texts for 3 roles) and read into string 
# role: Spieler (bidder/declaring the contract)
with open('Sauspiel_Spieler.txt', 'r') as file:
    total_str_sp = file.read()
# role: Gegenspieler (playing against the bidder)
with open('Sauspiel_Gegenspieler.txt', 'r') as file:
    total_str_gs = file.read()
# role: Partner (playing with the bidder/holding the called ace)
with open('Sauspiel_Partner.txt', 'r') as file:
    total_str_pr = file.read()

# %% alternatively: scrape directly from URL
# import requests

# URL = "https://www.sauspiel.de/spiele"
# page = requests.get(URL)

# print(page.text)
    
# %% test: count ocurrences of '>HO<' (Herzober) and '>SO<' (Schellnober)
# HO_count = total_str.count('>HO<')
# print(HO_count)

# SO_count = total_str.count('>SO<')
# print(SO_count)

# %% split total string into substrings

# function: splitting string in list of substring; every substring corresponds to one game played

def split_games(total_string):
    
    # create list of individual words (blank as separator)
    list_of_words = total_string.split()
    # print(len(list_of_parts))
    # print(list_of_parts[0:100])
    
    # index of list where last game started 
    ind_last_game_start = 0
    
    list_substr = []
    
    for i in range(len(list_of_words)):
        if ' '.join(list_of_words[i:i+3]) == '<div class="card games-item">':
            list_substr.append(' '.join(list_of_words[ind_last_game_start:i-1]))
            ind_last_game_start=i
    list_substr.append(' '.join(list_of_words[ind_last_game_start:]))
    return list_substr


def split_str_regex(total_string, regul_expr):
    
    # create list of charcaters
    list_of_char = [*total_string]
    
    # index of list where last date started 
    ind_last_date = 0
    
    list_substr = []
    
    for i in range(len(list_of_char)-16):
        if re.match(regul_expr, ''.join(list_of_char[i:i+16])):
            list_substr.append(''.join(list_of_char[ind_last_date:i-1]))
            ind_last_date=i
    list_substr.append(''.join(list_of_char[ind_last_date:]))
    return list_substr

def split_str_regex_alt(total_string, regul_expr):
    
    # create list of charcaters
    list_of_parts = total_string.split()
    # print(len(list_of_parts))
    # print(list_of_parts[0:100])
    
    # index of list where last date started 
    ind_last_date = 0
    
    list_substr = []
    
    for i in range(len(list_of_parts)):
        if re.search(regul_expr, list_of_parts[i]):
            list_substr.append(' '.join(list_of_parts[ind_last_date:i-1]))
            ind_last_date=i
    list_substr.append(' '.join(list_of_parts[ind_last_date:]))
    return list_substr
    
# # test split_str_regex   
# list_of_substrings = split_str_regex(total_str, reg_ex)
# print(list_of_substrings[1])
# print(len(list_of_substrings))
# list_of_substrings = split_str_regex_alt(total_str, reg_ex_short)
# print(list_of_substrings[1])
# print(len(list_of_substrings))
# list_of_substrings = split_games(total_str)
# print(list_of_substrings[1])
# print(len(list_of_substrings))

# %% create lists of substrings (for the 3 string files)
list_substr_sp = split_games(total_str_sp) 
list_substr_gs = split_games(total_str_gs)
list_substr_pr = split_games(total_str_pr)
# remove first item each -> useless
list_substr_sp = list_substr_sp[1:]  
list_substr_gs = list_substr_gs[1:]
list_substr_pr = list_substr_pr[1:]
print(list_substr_sp[0])

# %% create lists of dictionaries with information for each game; turn into pandas DataFrame

# import pandas and NumPy
import pandas as pd
import numpy as np

# prep: create list of all card acronyms
possible_suits = ['E', 'G', 'H', 'S']
possible_ranks = ['O', 'U', 'A', 'X', 'K', '9', '8', '7']  # natural order of ranks in Schafkopf
possible_cards = []
for rank in possible_ranks:
    for suit in possible_suits:
        possible_cards.append(suit + rank)   # ordered from high to low in regular games (Sauspiel)

possible_contracts = ['sauspiel-auf-die-alte',
                      'sauspiel-auf-die-blaue',
                      'sauspiel-auf-die-hundsgfickte',
                      'eichel-farbwenz',
                      'gras-farbwenz',
                      'herz-farbwenz',
                      'schellen-farbwenz',
                      '-wenz',
                      '-geier',
                      'eichel-solo',
                      'gras-solo',
                      'herz-solo',
                      'schellen-solo',
                      'ramsch']
# # test
# print(possible_cards)

# useful regular expressions
# import re package for regular expressions
import re

# define regular expression matching a date+time in string
reg_ex = r'[0-3][0-9]\.[0-9][0-9]\.20[0-9][0-9]\s[0-2][0-9]:[0-5][0-9]'
reg_ex_res_tendency = r'(gewonnen|verloren)'
reg_ex_res_points = r'(?<=(gewonnen|verloren)\smit\s)([0-9]){1,3}'
reg_ex_pay = r'[0-9],[0-9]0'

# # test reg_ex
# print(re.match(reg_ex, '14.09.2022 12:01'))
# print(re.match(reg_ex, '34.09.2022 12:01'))
# print(re.match(reg_ex, '14.09.202212:01'))

# # test reg_ex_res_tendency
# print(re.match(reg_ex_res_tendency, 'gewonnen mit 23'))
# print(re.match(reg_ex_res_tendency, 'verloren mit 23'))
# print(re.match(reg_ex_res_tendency, 'gewonnen mit 1'))
# print(re.match(reg_ex_res_tendency, 'gewonnen mit 111'))
# print(re.match(reg_ex_res_tendency, 'gewonnen mit 0'))
# print(re.match(reg_ex_res_tendency, 'gewonnenmit 23'))
# print(re.match(reg_ex_res_tendency, 'gewonnen'))
# print(re.search(reg_ex_pay, list_substr[80]))


# now define function for creating
def create_list_dict(list_substr, role):
    '''
    list_substr: list of substrings as returned by function split_games()
    role: string; role in the game ('spieler', 'gegenspieler' or 'partner')
    returns list of dictionairy which can be converted into DataFrame
    '''
    list_of_dict = []
    for substr in list_substr:

        # fill dict with dates
        dict_game = {'date': re.search(reg_ex, substr)[0]}
        list_of_dict.append(dict_game)
        
        # fill dict with cards
        cards_list = []
        for card in possible_cards:
            if card in substr:
                cards_list.append(card)
        dict_cards = zip(['card' + str(i) for i in range(1,9)], cards_list)
        dict_game.update(dict_cards)
        
        # fill dict with role
        dict_game['role'] = role
        
        # fill dict with tendency of result (won/lost)
        dict_game['res_tendency'] = re.search(reg_ex_res_tendency, substr)[0]  
    
        # fill dict with result (points) 
        dict_game['res_points'] = re.search(reg_ex_res_points, substr)[0]  
    
        # fill dict with payment for game 
        if re.search(reg_ex_pay, substr)==None:
            dict_game['payment'] = np.nan
        else:
            dict_game['payment'] = re.search(reg_ex_pay, substr)[0] 
        
        # fill dict with type (contract) of game
        for contract in possible_contracts:
            if contract in substr:
                dict_game['contract'] = contract
    return list_of_dict


# create 3 lists
list_dict_sp = create_list_dict(list_substr_sp, 'spieler')
list_dict_gs = create_list_dict(list_substr_gs, 'gegenspieler')
list_dict_pr = create_list_dict(list_substr_pr, 'partner')
# print(list_dict_sp[0])


# turn list of dicts into DataFrame
df_games_sp = pd.DataFrame(list_dict_sp)
df_games_gs = pd.DataFrame(list_dict_gs)
df_games_pr = pd.DataFrame(list_dict_pr)

# print head
print(df_games_sp.head())
print(df_games_gs.head())
print(df_games_pr.head())
print(df_games_sp.info())
print(df_games_gs.info())
print(df_games_pr.info())    

# %% create DataFrame for all roles and convert date column into dtype datetime
# concatenate
df_games = pd.concat([df_games_sp, df_games_gs, df_games_pr])

# date column as datetime, then set as index and sort
df_games['date'] = pd.to_datetime(df_games['date'])
df_games = df_games.set_index('date')
df_games = df_games.sort_index()

# test
print(df_games.head())
print(df_games.info())

# %% filter: only the games in 2022
df_games_2022 = df_games[df_games.index >= '2022']

# test
print(df_games_2022.head())
print(df_games_2022.info())