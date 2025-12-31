import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def create_record_csv_poke(name_of_csv):
    """
    Creates a new CSV file with the specified name containing an empty Pokémon card DataFrame 
    with the following columns: 'pokemon_name', 'nat_dex_num', 'set', 'foil_flag', 'full_art_flag', 'url'
    Keep a record of cards needed to keep a national dex of all the Pokemon
    NOTE: We exclude Mega Evolutions and special variants for the sake of simplicity. Any form changes are also
    counted as just one Pokemon

    Args:
        name_of_csv (str): The base name (without .csv extension) to use for the new CSV file.

    Returns:
        None (saves a csv file to your computer)
    """
    record_df = pd.DataFrame(columns = ['nat_dex_num', 'pokemon_name', 'set_name', 'foil_flag', 'full_art_flag', 'url'])
    record_df.to_csv('{}.csv'.format(name_of_csv), index=False)
    return None

def num_to_position(num):
    """
    Convert a board position number (1–9) to a (row, col) tuple.
    Positions are numbered left-to-right, top-to-bottom:
        1 2 3
        4 5 6
        7 8 9
    Args:
        num (int): The board position number (1–9)
    Returns:
        tuple: (row, col) corresponding to the board coordinates.
    Raises:
        ValueError: If num is not between 1 and 9.
    """
    #Convert 1–9 to (row, col) position, reading left to right, top to bottom
    if not (1 <= num <= 9):
        raise ValueError("Number must be between 1 and 9.")
    row = (num - 1) // 3
    col = (num - 1) % 3
    return row, col

def show_board_with_star(star_position, page_num):
    """
    Display a 3x3 board with a single yellow star at the given position.
    Each cell also shows its position number faintly for reference.

    Args:
        star_position (int): The board position (1–9) where the star should appear.
        page_num (int): The page number the card should be in, for reference.
    """

    #First set up board
    fig, ax = plt.subplots()
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_aspect('equal')

    #Draw grid lines
    ax.set_xticks(np.arange(-0.5, 3, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 3, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle="-", linewidth=2)

    #Remove axis labels
    ax.set_xticks([])
    ax.set_yticks([])

    #Add faint numbers 1-9 in all cells
    num = 1
    for r in range(3):
        for c in range(3):
            ax.text(c, r, str(num), ha='center', va='center',
                    fontsize=16, color='gray', alpha=0.4)
            num += 1

    #Draw star for the given position 1-9
    row, col = num_to_position(star_position)
    ax.scatter(col, row, marker='*', s=800, color='gold', edgecolors='black')

    plt.gca().invert_yaxis()  #Make row 0 at the top
    plt.title("Page Number:{}".format(page_num))
    plt.show()

def plot_page_pos(poke_national_dex_num):
    #Since a standard page is 3x3, 9 cards are on one page
    #We use the symbols instead of divmod since theses are "small" numbers.
    quotient_page = poke_national_dex_num // 9
    remainder_ind = poke_national_dex_num % 9
    
    #For numbers not divisble by 9, we need to add one to the quotient for the accurate page.
    #For numbers divisible by 9, the quoitient is the right page but now the individual position (remainder) is wrong. It should be 9.
    if remainder_ind == 0:
        remainder_ind = 9
    else:
        quotient_page += 1

    show_board_with_star(remainder_ind, quotient_page)

def add_card_record(national_dex_num, name_of_pokemon, record_df, csv_name):
    """
    Adds a new Pokémon card to the DataFrame and updates the CSV file if the card is not already present.
    Prompts the user for further card info.
    
    Args:
        national_dex_num (pd.int): The National Dex number of the Pokemon being added.
        name_of_pokemon (str): The name of the Pokemon.
        record_df (pd.DataFrame: The df of your record of cards.
        csv_name (str): The filename of the CSV file to update (including '.csv').

    Returns:
        pd.DataFrame: The updated DataFrame, with a new card added.
    """
    clean_set_name_input, clean_foil_check, clean_full_art_check, clean_url_input = ask_card_details()

    #Row to append as a dictionary
    new_row = {'nat_dex_num': national_dex_num,'pokemon_name': name_of_pokemon, 'set_name': clean_set_name_input,\
               'foil_flag': clean_foil_check, 'full_art_flag': clean_full_art_check, 'url': clean_url_input}
    
    # Append the row (returns a new DataFrame)
    record_df.loc[len(record_df)] = new_row
    record_df.to_csv(csv_name, index=False) #resave new dataframe

    #Now physically add it to your binder based on numerical order
    print('Add it to your binder now according to our predicted position and page number:')
    plot_page_pos(national_dex_num)

    return record_df

def replace_card_record(national_dex_num, name_of_pokemon, record_df, csv_name):
    #Get info of the row in the records_df
    set_name_info = record_df.loc[(record_df['pokemon_name'] == name_of_pokemon), 'set_name'].values[0]
    foil_flag_info = record_df.loc[(record_df['pokemon_name'] == name_of_pokemon), 'foil_flag'].values[0]
    full_art_flag_info = record_df.loc[(record_df['pokemon_name'] == name_of_pokemon), 'full_art_flag'].values[0]
    url_info = record_df.loc[(record_df['pokemon_name'] == name_of_pokemon), 'url'].values[0]

    # Display results
    print("{} #{} is currently in your collection. It has the following details: ".format(name_of_pokemon, national_dex_num))
    print(f"Set Name: {set_name_info}")
    print(f"Is it a foil?: {foil_flag_info}")
    print(f"Is it full art?: {full_art_flag_info}")
    print(f"URL: {url_info}")

    print("Additonally, it resides in your binder at the following page and position: ")
    plot_page_pos(national_dex_num)

    replace_check = input("Would you like to replace your card?: ")
    clean_replace_check = replace_check.strip()
    acceptable_yes_arr = ["y", "yes", "Yes", 'yup']

    if clean_replace_check in acceptable_yes_arr:
        clean_set_name_input, clean_foil_check, clean_full_art_check, clean_url_input = ask_card_details()
        
        #Update df
        record_df.loc[(record_df['pokemon_name'] == name_of_pokemon), 'set_name'] = clean_set_name_input
        record_df.loc[(record_df['pokemon_name'] == name_of_pokemon), 'foil_flag'] = clean_foil_check
        record_df.loc[(record_df['pokemon_name'] == name_of_pokemon), 'full_art_flag'] = clean_full_art_check
        record_df.loc[(record_df['pokemon_name'] == name_of_pokemon), 'url'] = clean_url_input
        
        record_df.to_csv(csv_name, index=False) #resave new dataframe

        #Now physically add it to your binder based on numerical order
        print('Add it to your binder now according to our predicted position and page number:')
        plot_page_pos(national_dex_num)
    else: 
        print('Kept same card.')
        
    return record_df

def card_recording(record_csv_name):
    init_poke_record_df = pd.read_csv(record_csv_name)

    national_dex_df = pd.read_csv('pokemon_dex_num.csv')
    user_poke_name_check = input("Enter the name of the Pokemon: ")
    
    #First calpitalize the words. Then, clean the result of leading and trailing whitespace of user input
    cap_name_check = user_poke_name_check.title()
    poke_name_check = cap_name_check.strip()
    
    #Check if the name of the pokemon is in the National Dex
    if (national_dex_df['NAME'] == poke_name_check).any():
        print('Pokemon does exist in the National Dex. Taking the National Dex Number.')
        
        #The following line will always take the first instance (values[0]),
        #which really doesn't matter for this since we ignore special variants
        dex_num = national_dex_df.loc[(national_dex_df['NAME'] == poke_name_check), 'national_dex_num'].values[0]
        print('National Dex number is #{}'.format(dex_num))
        print('----------------------------------------------------------------------- \n')
    
        #Check if card is already documented
        #Either you add it for the first time, or you can replace it
        existence_check = (init_poke_record_df['pokemon_name'] == poke_name_check).any()
        if existence_check == 0:
            print('Pokemon does not exists in your records. Going into add_card_record function: ')
            poke_record_df = add_card_record(dex_num, poke_name_check, init_poke_record_df, record_csv_name)
    
            return poke_record_df
            
        elif existence_check == 1:
            print('Pokemon does exist in your records! Going into replace_card_record function: ')
            poke_record_df = replace_card_record(dex_num, poke_name_check, init_poke_record_df, record_csv_name)
            
            return poke_record_df
    else:
        print("Pokemon name is incorrect or does not exist in the National Dex. Please check National Dex csv file.")

        return init_poke_record_df

def check_existence_in_record(record_csv_name):
    poke_record_df = pd.read_csv(record_csv_name)
    name_or_dex_num = input("Enter the Pokemon name or National Dex Number: ")
    clean_name_or_dex_num = name_or_dex_num.strip()
    
    #Try to interpret the input as an integer first
    try:
        dex_num_to_find = np.int64(clean_name_or_dex_num) #make it the same type as in the csv file
        #Find any matches
        dex_num_match = poke_record_df[poke_record_df['nat_dex_num'] == dex_num_to_find]
        
        if dex_num_match.empty:
            print(f"No card found with National Dex Number {dex_num_to_find}.")
        else:
            #Give url for easy reference
            url_info = poke_record_df.loc[(poke_record_df['nat_dex_num'] == dex_num_to_find), 'url'].values[0]
            print('Card exists in your records! Giving position in binder now: ')
            print(f"Pokemon Card URL: {url_info}")
            plot_page_pos(dex_num_to_find)
            
    except ValueError:
        #Treat input as a card name
        card_name_match = poke_record_df[poke_record_df['pokemon_name'] == clean_name_or_dex_num]

        if card_name_match.empty:
            print(f"No card found with name {clean_name_or_dex_num} found.")
        else:
            dex_num_info = poke_record_df.loc[(poke_record_df['pokemon_name'] == clean_name_or_dex_num), 'nat_dex_num'].values[0]
            url_info = poke_record_df.loc[(poke_record_df['pokemon_name'] == clean_name_or_dex_num), 'url'].values[0]
            print('Card exists in your records! Giving position in binder now: ')
            print(f"Pokemon Card URL: {url_info}")
            plot_page_pos(dex_num_info)
    return None

def find_dex_num_or_pokemon_name():
    national_dex_df = pd.read_csv('pokemon_dex_num.csv') #Read in csv of national dex numbers for pokemon
    
    nat_dex_num_or_name = input("Enter the Pokemon name or National Dex Number to find it in the national dex: ")
    clean_name_or_dex_num = nat_dex_num_or_name.strip() #clean name from any superfluous spaces
    
    #Try to interpret the input as an integer first
    try:
        dex_num_to_find = np.int64(clean_name_or_dex_num) #make it the same type as in the csv file
        #Find any matches
        poke_name_match = national_dex_df.loc[(national_dex_df['national_dex_num'] == dex_num_to_find), 'NAME']
        
        if poke_name_match.empty:
            print(f"No Pokemon found with National Dex Number {dex_num_to_find}.")
        else:
            first_poke_name_match = national_dex_df.loc[(national_dex_df['national_dex_num'] == dex_num_to_find), 'NAME'].values[0]
            print('\nVia dex num. match: {} has the national dex number #{}'.format(first_poke_name_match, dex_num_to_find))
            
    except ValueError:
        #Treat input as a Pokemon name
        dex_num_match =  national_dex_df.loc[(national_dex_df['NAME'] == clean_name_or_dex_num), 'national_dex_num']
        
        if dex_num_match.empty:
            print(f"{clean_name_or_dex_num} doesn't seem to have a National Dex Number. Double check spelling or csv file.")
        else:
            first_dex_num_match =  national_dex_df.loc[(national_dex_df['NAME'] == clean_name_or_dex_num), 'national_dex_num'].values[0]
            print('\nVia name match: {} has the national dex number #{}'.format(clean_name_or_dex_num, first_dex_num_match))
    return None

def ask_card_details():
    
    print('Please provide additional info to replace card:\n')
    stripped_set_name_input = get_list_of_poke_sets()
    foil_check = input("Is this card a foil? (Any foil): ") #valid responses are yes, Yes, y, yup
    stripped_foil_check = foil_check.strip()

    #If a card is not foil, no point in asking next question, just autofill
    acceptable_yes_arr_2 = ["y", "Y", "yes", "Yes", 'yup']

    if stripped_foil_check in acceptable_yes_arr_2:
        stripped_foil_check = 'yes'
        full_art_check = input("Is this card full art? (IR or higher rarity): ") #valid responses are yes, Yes, y
        stripped_full_art_check = full_art_check.strip()
    else:
        stripped_full_art_check = 'no'
    
    url_input = input("Provide url of the card for reference: ") #can either be from TCGplayer or PriceCharting. It's just for quick reference.
    stripped_url_input = url_input.strip()

    return stripped_set_name_input, stripped_foil_check, stripped_full_art_check, stripped_url_input

def get_list_of_poke_sets():
    """
    Prompt the user to select a recent Pokémon TCG set name.

    This function displays a numbered list of the most recent Scarlet & Violet-era 
    Pokémon TCG expansion sets (from Obsidian Flames up to Phantasmal Forces).
    The user can select a set in 2 ways:
      1. Enter the corresponding number from the list.
      2. Type the full set name (case-insensitive).

    If the user selects "Other" or provides an unrecognized input, the function
    will prompt them to manually enter the set name.

    Returns:
        str: The selected or manually entered set name (stripped of leading/trailing spaces).
    """
    #Recent Scarlet & Violet-era sets to Mega Evolution
    recent_sets = [
        "Ascended Heroes",
        "Phantasmal Flames",
        "Mega Evolution",
        "White Flare",
        "Black Bolt",
        "Destined Rivals",
        "Journey Together",
        "Prismatic Evolutions",
        "Surging Sparks",
        "Stellar Crown",
        "Shrouded Fable",
        "Twilight Masquerade",
        "Temporal Forces",
        "Paldean Fates",
        "Paradox Rift",
        "151"
    ]

    #Print set names and enumerate them
    print("Select the set name:")
    for i, name in enumerate(recent_sets, 1):
        print(f"{i}. {name}")
    print(f"{len(recent_sets) + 1}. Other") #Have an 'Other' option for manual input

    choice = input("Enter number: ").strip() #Have the user enter just the number

    if choice.isdigit() and 1 <= int(choice) <= len(recent_sets):
        return recent_sets[int(choice) - 1]
    else:
        return input("Enter the set name of the card: ").strip()