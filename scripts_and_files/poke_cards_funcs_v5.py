import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random

def new_pokemon_df(name_of_csv):
    """
    Creates a new CSV file with the specified name containing an empty Pokémon card DataFrame 
    with the following columns: 'Card_Name', 'Set_Name', 'url', 'ungraded_price', 'PSA10_price', 'grade_yn', 'quantity'
    Meant for tracking card details and prices using Price Charting website (https://www.pricecharting.com/)

    Args:
        name_of_csv (str): The base name (without .csv extension) to use for the new CSV file.

    Returns:
        None (saves a csv file to your computer)
    """
    poke_df = pd.DataFrame(columns = ['Card_Name', 'Set_Name', 'url', 'ungraded_price', 'PSA10_price', 'grade_yn', 'quantity'])
    poke_df.to_csv('{}.csv'.format(name_of_csv), index=False)
    return None

def extract_price(url, label):
    """
    Scrapes the given URL to extract the price corresponding to a specified label 
    (e.g., 'PSA 10', 'Ungraded') from a PriceCharting page.

    Args:
        url (str): The URL of the PriceCharting page for a specific Pokémon card.
        label (str): The text label used to identify the desired price row 
                     (e.g., 'PSA 10', 'Ungraded').

    Returns:
        float: The extracted price as a float if found and valid.
        np.nan: If the label or price is not found or conversion to float fails.
    """
    #Header might change based on browser
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    label_td = soup.find('td', string=label)
    if label_td:
        price_td = label_td.find_next_sibling('td')
        if price_td:
            price_text = price_td.text.strip().replace('$', '').replace(',', '')
            try:
                return float(price_text)
            except ValueError:
                print(f"Couldn't convert {label} price to float.")
                return np.nan
    else:
        print(f"Could not find {label} label.")
        return np.nan

def extract_card_name_set(url):
    """
    Scrapes the given PriceCharting card URL to extract the card name and set name.

    Args:
        url (str): The URL of the PriceCharting page for a specific Pokémon card.

    Returns:
        tuple:
            - card_name_only (str or np.nan): The name of the card (e.g., "Cynthia's Garchomp ex #104").
            - set_name_only (str or np.nan): The set name the card belongs to 
                                             (e.g., "Pokemon Destined Rivals").
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the card name — it's usually in the <h1> tag
    card_name_tag = soup.find('h1')
    if card_name_tag:
        card_name_and_set = card_name_tag.text.strip()
        
        # Split by newline and strip each part
        parts = [part.strip() for part in card_name_and_set.split('\n') if part.strip()]
        
        # Assign to separate variables
        card_name_only = parts[0] if len(parts) > 0 else None
        set_name_only = parts[1] if len(parts) > 1 else None
    else:
        print("Card name not found.")
        card_name_only = np.nan
        set_name_only = np.nan
    return card_name_only, set_name_only

def add_card(df_poke_cards, url, poke_csv_name):
    """
    Adds a single new Pokémon card to the DataFrame and updates the CSV file if the card is not already present.
    If the card is already in the DataFrame, prompts the user to optionally update its price instead.

    Args:
        df_poke_cards (pd.DataFrame): The existing DataFrame containing Pokémon card data.
        url (str): The PriceCharting URL for the Pokémon card to add.
        poke_csv_name (str): The filename of the CSV file to update (including '.csv').

    Returns:
        pd.DataFrame: The updated DataFrame, either with a new card added or with prices optionally updated.
    """
    # Get the card name and set name
    check_card_name, set_name_only = extract_card_name_set(url)
    
    if ((df_poke_cards['Card_Name'] == check_card_name) & (df_poke_cards['Set_Name'] == set_name_only)).any():
        print(f"{check_card_name} from {set_name_only} is present in spreadsheet.")
        
        #Ask to update quantity or price
        choice_input = input("Would you like to:\n1. Update price? \n2. Update quantity?\n").strip()
        while not (choice_input.isdigit() and (int(choice_input) == 1 or int(choice_input) == 2)):
            choice_input = input("Not a valid choice! Choose 1 or 2!:\n").strip()
        #Call diff. function based on choice above
        if int(choice_input) == 1:
            df_poke_cards_output = update_price(df_poke_cards, check_card_name, set_name_only, poke_csv_name, call_flag = 1)
        elif int(choice_input) == 2:
            df_poke_cards_output = update_quantity_cards(df_poke_cards, check_card_name, set_name_only, poke_csv_name)
        else:
            print('No new card added nor price updated.')
    else:
        print(f"{check_card_name} from {set_name_only} is not present in the 'Card_Names' column. Adding card:")
        
        # Extract prices and determine if we should grade it
        ungraded_price = extract_price(url, 'Ungraded')
        psa10_price = extract_price(url, 'PSA 10')
        grade_choice = determine_psa_worth(psa10_price)

        #Since it's new, assume quantity is 1
        quantity_new = 1
            
        # Display results
        print(f"Card Name: {check_card_name}")
        print(f"Set Name: {set_name_only}")
        print(f"Url: {url}")
        print(f"Ungraded Price: ${ungraded_price}")
        print(f"PSA 10 Price: ${psa10_price}")
        
        #Row to append as a dictionary
        new_row = {'Card_Name': check_card_name, 'Set_Name': set_name_only, 'url': url, \
                   'ungraded_price':ungraded_price, 'PSA10_price':psa10_price, 'grade_yn':grade_choice, 'quantity': quantity_new}
        
        # Append the row (returns a new DataFrame)
        df_poke_cards.loc[len(df_poke_cards)] = new_row
        df_poke_cards.to_csv(poke_csv_name, index=False) #resave new dataframe
        
    return df_poke_cards

def remove_card(poke_csv_name):
    """
    Prompts the user to input a card name or row index to remove from the DataFrame.
    Deletes the matching row and updates the CSV file.

    Args:
        df_poke_cards (pd.DataFrame): The DataFrame containing Pokémon card data.
        poke_csv_name (str): The filename of the CSV file to update after deletion.

    Returns:
        pd.DataFrame: The updated DataFrame with the specified row removed.
    """
    df_poke_cards = pd.read_csv(poke_csv_name)
    user_input = input("Enter the card name or row index to delete: ").strip()

    #Try to interpret the input as an integer index
    try:
        #If it was an integer, we then drop the column
        index_to_drop = int(user_input)
        #Check if that integer value is actually a row value in the df
        if index_to_drop in df_poke_cards.index:
            print(f"Dropping card '{df_poke_cards['Card_Name'][index_to_drop]}' at index {index_to_drop}")
            df_poke_cards = df_poke_cards.drop(index=index_to_drop).reset_index(drop=True)
        else:
            print(f"Index {index_to_drop} not found in DataFrame")
            return df_poke_cards
    except ValueError:
        #Treat input as a card name
        card_name_matches = df_poke_cards[df_poke_cards['Card_Name'] == user_input]
        if card_name_matches.empty:
            print(f"No card found with name '{user_input}'. No row removed")
            return df_poke_cards
        elif len(card_name_matches) > 1:
            print(f"Multiple entries found for card name '{user_input}'. Use the index:")
            print(card_name_matches)
            return df_poke_cards
        else:
            index_to_drop = card_name_matches.index[0]
            print(f"Dropping card '{user_input}' at index {index_to_drop}.")
            df_poke_cards = df_poke_cards.drop(index=index_to_drop).reset_index(drop=True)

    # Save updated DataFrame
    print('Saving csv file.')
    df_poke_cards.to_csv(poke_csv_name, index=False) #resave new dataframe
    return df_poke_cards

def update_price(df_poke_cards, card_name, set_name, poke_csv_name, call_flag):
    """
    Updates the ungraded and PSA 10 prices for a specific Pokémon card in the DataFrame,
    recalculates whether it's worth grading, and saves the updated DataFrame to CSV.

    Args:
        df_poke_cards (pd.DataFrame): The existing DataFrame containing Pokémon card data.
        card_name (str): The name of the card to update.
        set_name (str): The set name the card belongs to.
        poke_csv_name (str): The filename of the CSV file to save the updated DataFrame to.
        call_flag (int): Flag to see where the function is being called from. It helps determine whether
                         card details are printed or not.

    Returns:
        pd.DataFrame: The updated DataFrame with revised price and grading information for the specified card.
    """
    #Extract url
    url = df_poke_cards.loc[(df_poke_cards['Card_Name'] == card_name) & (df_poke_cards['Set_Name'] == set_name), 'url'].values[0]
    
    # Extract prices and determine if we should grade it
    ungraded_price = extract_price(url, 'Ungraded')
    psa10_price = extract_price(url, 'PSA 10')
    grade_choice = determine_psa_worth(psa10_price)
        
    # Display results
    if call_flag == 1:
        print(f"Card Name: {card_name}")
        print(f"Url: {url}")
        print(f"Updated Ungraded Price: ${ungraded_price}")
        print(f"Updated PSA 10 Price: ${psa10_price}")
    elif call_flag == 2:
        print(f"Card Name: {card_name}")
        print(f"Url: {url} \n")
        # print('-------------')
    
    #Update df
    df_poke_cards.loc[(df_poke_cards['Card_Name'] == card_name) & (df_poke_cards['Set_Name'] == set_name), 'ungraded_price'] = ungraded_price
    df_poke_cards.loc[(df_poke_cards['Card_Name'] == card_name) & (df_poke_cards['Set_Name'] == set_name), 'PSA10_price'] = psa10_price
    df_poke_cards.loc[(df_poke_cards['Card_Name'] == card_name) & (df_poke_cards['Set_Name'] == set_name), 'grade_yn'] = grade_choice
    
    df_poke_cards.to_csv(poke_csv_name, index=False) #resave new dataframe
        
    return df_poke_cards

def update_quantity_cards(df_poke_cards, card_name, set_name, poke_csv_name):
    """
    Updates the quantity for a specific Pokémon card in the DataFrame,
    recalculates whether it's worth grading, and saves the updated DataFrame to CSV.

    Args:
        df_poke_cards (pd.DataFrame): The existing DataFrame containing Pokémon card data.
        card_name (str): The name of the card to update.
        set_name (str): The set name the card belongs to.
        poke_csv_name (str): The filename of the CSV file to save the updated DataFrame to.

    Returns:
        pd.DataFrame: The updated DataFrame with quantity for the specified card.
    """
    #First it prints how many you own right now. You can either update it by adding one or manually tell how many you have now.
    quant_owned = df_poke_cards.loc[(df_poke_cards['Card_Name'] == card_name) & (df_poke_cards['Set_Name'] == set_name), 'quantity'].values[0]
    print(f"You currently have {quant_owned} of these cards.")

    #Next we have an input choice for quantity
    quant_input = input("Would you like to:\n1.Add one? \n2.Update manually?\n").strip()
    while not (quant_input.isdigit() and (int(quant_input) == 1 or int(quant_input) == 2)):
        quant_input = input("Not a valid choice! Choose 1 or 2!:\n").strip()
    
    if quant_input == '1':
        df_poke_cards.loc[(df_poke_cards['Card_Name'] == card_name) & (df_poke_cards['Set_Name'] == set_name), 'quantity'] = quant_owned + 1
    elif quant_input == '2':
        quant_choice = input("How many of the card do you own?: ").strip()
        while not (quant_choice.isdigit()):
            quant_choice = input("Not a valid choice! Input only an integer: ").strip()
        df_poke_cards.loc[(df_poke_cards['Card_Name'] == card_name) & (df_poke_cards['Set_Name'] == set_name), 'quantity'] = int(quant_choice)
    
    df_poke_cards.to_csv(poke_csv_name, index=False) #resave new dataframe
        
    return df_poke_cards

def determine_psa_worth(price_of_card_psa10):
    """
    Determines whether a card is worth grading based on its PSA 10 price. Determination is based on
    current Gamestop pricing to send in a single card plus shipping cost.

    Args:
        price_of_card_psa10 (float): The market price of the card in PSA 10 condition.

    Returns:
        str: 'Yes' if the PSA 10 price exceeds the minimum grading threshold; otherwise, 'No'.
    """
    min_price_grade = 22 * 2.2
    worth_grading_check = price_of_card_psa10 > min_price_grade
    if worth_grading_check == True:
        grade_decision = 'Yes'
    else:
        grade_decision = 'No'
    return grade_decision

def update_poke_df(poke_csv_name):
    """
    Prompts the user to either input a URL to add a single new Pokémon card or a card name to update an existing one.
    Based on the input, the function updates the Pokémon card DataFrame and the associated CSV file.

    Args:
        poke_csv_name (str): The file name (including path if necessary) of the CSV file 
                             containing the existing Pokémon card data.

    Returns:
        pd.DataFrame or None: The updated DataFrame if a card is added or updated; 
                              None if the operation is aborted due to invalid input or no matching card found.
    """
    #must already have using the same name as you did in new_pokemon_df
    cards_df = pd.read_csv(poke_csv_name)
    #Strip is used to clean out empty spaces in the beginning or end of the 
    url_or_name = input("Enter URL or Card Name - ").strip() #asks what the user input is to determine next function

    check_substr_1 = 'https://'
    if check_substr_1 in url_or_name:
        print('Entering add_card function: \n')
        df_poke_cards = add_card(cards_df, url_or_name, poke_csv_name)
    else:
        if url_or_name in cards_df['Card_Name'].values:
            print(f"{url_or_name} is present in the 'Card_Names' column.")
            count = cards_df['Card_Name'].value_counts()[url_or_name]
            if count > 1:
                print(f"Multiple instances of {url_or_name} are present in the 'Card_Names' column. \n")
                set_name_of_card = input("Please input set name -")
                if ((cards_df['Card_Name'] == url_or_name) & (cards_df['Set_Name'] == set_name_of_card)).any():
                    print('Entering update_price function: \n')
                    df_poke_cards = update_price(cards_df, url_or_name, set_name_of_card, poke_csv_name, call_flag = 1)
                else:
                    print(f"Card {url_or_name} in set {set_name_of_card} is not present in file. Double check csv file!")
                    return cards_df
            else:
                #Extract set name since card only appears once
                set_name_of_card = cards_df.loc[(cards_df['Card_Name'] == url_or_name), 'Set_Name'].values[0]
                print('Entering update_price function (only one instance of card found): \n')
                df_poke_cards = update_price(cards_df, url_or_name, set_name_of_card, poke_csv_name, call_flag = 1)
        else:
            print(f"Card {url_or_name} is not present in file. Double check csv file!")
            return cards_df
    return df_poke_cards

def multi_update_poke_df(poke_csv_name):
    #must already have using the same name as you did in new_pokemon_df
    cards_df = pd.read_csv(poke_csv_name)

    for i in range(0, len(cards_df)):
        df_poke_cards = update_price(cards_df, cards_df['Card_Name'][i], cards_df['Set_Name'][i], poke_csv_name, call_flag = 2)
        time.sleep(random.uniform(2.0, 4.0)) #add a time delay to prevent bot detection and to properly use this function

    return cards_df

def user_update_price(poke_csv_name):
    """
    Prompts the user for a row index in the Pokémon CSV file and updates the prices for that row, as well
    as determine if we should grade the card.

    Args:
        poke_csv_name (str): The filename (including .csv extension) of the Pokémon data file to update.

    Returns:
        pandas.DataFrame: The updated DataFrame after modifying the pricing.
    """
    df_poke_cards = pd.read_csv(poke_csv_name)
    user_input = input("Enter row index to update quantity: ").strip()
    
    # Validate that input is an integer
    while not (user_input.isdigit()):
        user_input = input("Not a valid choice! Input only an integer for the index: ").strip()
    
    #Check if that integer value is actually a row value in the df
    index_update = int(user_input) #turn into an integer to work for index
    if index_update in df_poke_cards.index:
        print(f"Updating card price: {df_poke_cards['Card_Name'][index_update]} from {df_poke_cards['Set_Name'][index_update]}.")
        #Extract url
        url = df_poke_cards['url'][index_update]
        
        # Extract prices and determine if we should grade it
        ungraded_price = extract_price(url, 'Ungraded')
        psa10_price = extract_price(url, 'PSA 10')
        grade_choice = determine_psa_worth(psa10_price)
            
        # Display results
        print(f"Card Name: {df_poke_cards['Card_Name'][index_update]}")
        print(f"Url: {url}")
        print(f"Updated Ungraded Price: ${ungraded_price}")
        print(f"Updated PSA 10 Price: ${psa10_price}")
        
        #Update df
        df_poke_cards.at[index_update, 'ungraded_price'] = ungraded_price
        df_poke_cards.at[index_update, 'PSA10_price'] = psa10_price
        df_poke_cards.at[index_update, 'grade_yn'] = grade_choice
        
        df_poke_cards.to_csv(poke_csv_name, index=False) #resave new dataframe
    else:
        print(f"Index {index_to_drop} not found in DataFrame")
        
    return df_poke_cards
    
def user_update_quantity(poke_csv_name):
    """
    Prompts the user for a row index in the Pokémon CSV file and updates the 'quantity' value for that row.

    Args:
        poke_csv_name (str): The filename (including .csv extension) of the Pokémon data file to update.

    Returns:
        pandas.DataFrame: The updated DataFrame after modifying the quantity.
    """
    df_poke_cards = pd.read_csv(poke_csv_name)
    user_input = input("Enter row index to update quantity: ").strip()
    
    # Validate that input is an integer
    while not (user_input.isdigit()):
        user_input = input("Not a valid choice! Input only an integer for the index: ").strip()
    
    #Check if that integer value is actually a row value in the df
    index_to_drop = int(user_input) #turn into an integer to work for index
    if index_to_drop in df_poke_cards.index:
        print(f"Updating card: {df_poke_cards['Card_Name'][index_to_drop]} from {df_poke_cards['Set_Name'][index_to_drop]}. You currently have {df_poke_cards['quantity'][index_to_drop]}.")

        #Ask the user for quantity
        quantity_input = input("How many do you own now? - ") #single number
        # Validate that input is an integer
        while not (user_input.isdigit()):
            user_input = input("Not a valid choice! Input only an integer for the index: ").strip()
        quantity_input_clean = quantity_input.strip()
        quantity_input_float = int(quantity_input_clean)
        
        df_poke_cards.at[index_to_drop, 'quantity'] = quantity_input_float
    else:
        print(f"Index {index_to_drop} not found in DataFrame")
        return df_poke_cards

    # Save updated DataFrame
    print('Saving csv file.')
    df_poke_cards.to_csv(poke_csv_name, index=False) #resave new dataframe
    return df_poke_cards