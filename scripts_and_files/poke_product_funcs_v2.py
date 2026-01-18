import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random

def new_pokemon_products_df(name_of_csv):
    """
    Creates a new CSV file with the specified name containing an empty Pokémon card DataFrame 
    with the following columns: 'Product_Name', 'Set_Name', 'url', 'MSRP', 'market_price', 'quantity'
    Meant for tracking product prices using Price Charting website (https://www.pricecharting.com/)

    Args:
        name_of_csv (str): The base name (without .csv extension) to use for the new CSV file.

    Returns:
        None (saves a csv file to your computer)
    """
    poke_df = pd.DataFrame(columns = ['Product_Name', 'Set_Name', 'url', 'MSRP', 'market_price', 'quantity'])
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

def add_product(df_poke_cards, url, poke_csv_name):
    """
    Adds a new Pokemon product to the DataFrame and updates the CSV file if the product is not already present.
    If the product is already in the DataFrame, prompts the user to optionally update its price instead.

    Args:
        df_poke_cards (pd.DataFrame): The existing DataFrame containing Pokémon card data.
        url (str): The PriceCharting URL for the Pokémon card to add.
        poke_csv_name (str): The filename of the CSV file to update (including '.csv').

    Returns:
        pd.DataFrame: The updated DataFrame, either with a new card added or with prices optionally updated.
    """
    # Get the card name and set name
    check_card_name, set_name_only = extract_card_name_set(url)
    
    if ((df_poke_cards['Product_Name'] == check_card_name) & (df_poke_cards['Set_Name'] == set_name_only)).any():
        print(f"{check_card_name} from {set_name_only} is present in spreadsheet.")
        #Want to either update price or quantity
        choice_input = input("Would you like to:\n1. Update price? \n2. Update quantity?\n").strip()
        while not (choice_input.isdigit() and (int(choice_input) == 1 or int(choice_input) == 2)):
            choice_input = input("Not a valid choice! Choose 1 or 2!:\n").strip()
        #Call diff. function based on choice above
        if int(choice_input) == 1:
            df_poke_cards = update_price_prod(df_poke_cards, check_card_name, set_name_only, poke_csv_name)
        elif int(choice_input) == 2:
            df_poke_cards = update_quantity_prod(df_poke_cards, check_card_name, set_name_only, poke_csv_name)
        else:
            print('No new product added nor price updated.')
    else:
        print(f"{check_card_name} from {set_name_only} is not present in the 'Product_Name' column. Adding product:")
        
        # Extract prices and determine if we should grade it
        product_price = extract_price(url, 'Ungraded')
        msrp_input = input("What is the MSRP? - ") #its a price we paid for at the time, often a decimal
        quantity_input = input("How many do you own? - ") #single number

        #Clean and make float/int inputs
        msrp_input_clean = msrp_input.strip()
        msrp_input_float = float(msrp_input_clean)
        
        quantity_input_clean = quantity_input.strip()
        quantity_input_float = int(quantity_input_clean)
            
        # Display results
        print(f"Url: {url}")
        print(f"Market Price: {product_price}")
        print(f"Quantity: {quantity_input}")
        
        #Row to append as a dictionary
        new_row = {'Product_Name': check_card_name, 'Set_Name': set_name_only, 'url': url, \
                   'MSRP': msrp_input_float, 'market_price': product_price, 'quantity': quantity_input_float}
        
        # Append the row (returns a new DataFrame)
        df_poke_cards.loc[len(df_poke_cards)] = new_row
        df_poke_cards.to_csv(poke_csv_name, index=False) #resave new dataframe
        
    return df_poke_cards

def update_price_prod(df_poke_cards, card_name, set_name, poke_csv_name):
    """
    Updates the price for a specific Pokémon product in the DataFrame,
    and saves the updated DataFrame to CSV.
    NOTE: Names of variables reused from other function but I dont wanna rename

    Args:
        df_poke_cards (pd.DataFrame): The existing DataFrame containing Pokémon card data.
        card_name (str): The name of the product to update.
        set_name (str): The set name the card belongs to.
        poke_csv_name (str): The filename of the CSV file to save the updated DataFrame to.

    Returns:
        pd.DataFrame: The updated DataFrame with revised price and grading information for the specified product.
    """
    #Extract url
    url = df_poke_cards.loc[(df_poke_cards['Product_Name'] == card_name) & (df_poke_cards['Set_Name'] == set_name), 'url'].values[0]
    
    # Extract prices
    product_price = extract_price(url, 'Ungraded')
        
    # Display results
    print(f"Url: {url}")
    print(f"Market Price: {product_price} \n")
    
    #Update df
    df_poke_cards.loc[(df_poke_cards['Product_Name'] == card_name) & (df_poke_cards['Set_Name'] == set_name), 'market_price'] = product_price
    
    df_poke_cards.to_csv(poke_csv_name, index=False) #resave new dataframe
        
    return df_poke_cards

def update_quantity_prod(df_poke_cards, card_name, set_name, poke_csv_name):
    """
    Updates price for a specific Pokémon product in the DataFrame,
    and saves the updated DataFrame to CSV. This function is specifically called for `add_product`
    NOTE: Names of variables reused from other functions

    Args:
        df_poke_cards (pd.DataFrame): The existing DataFrame containing Pokémon card data.
        card_name (str): The name of the product to update.
        set_name (str): The set name the card belongs to.
        poke_csv_name (str): The filename of the CSV file to save the updated DataFrame to.

    Returns:
        pd.DataFrame: The updated DataFrame with quantity.
    """
    #First it prints how many you own right now. You can either update it by adding one or manually tell how many you have now.
    quant_owned = df_poke_cards.loc[(df_poke_cards['Product_Name'] == card_name) & (df_poke_cards['Set_Name'] == set_name), 'quantity'].values[0]
    print(f"You currently have {quant_owned} of these cards.")

    #Next we have an input choice for quantity
    quant_input = input("Would you like to:\n1.Add one? \n2.Update manually?\n").strip()
    while not (quant_input.isdigit() and (int(quant_input) == 1 or int(quant_input) == 2)):
        quant_input = input("Not a valid choice! Choose 1 or 2!:\n").strip()
    
    if quant_input == '1':
        df_poke_cards.loc[(df_poke_cards['Product_Name'] == card_name) & (df_poke_cards['Set_Name'] == set_name), 'quantity'] = quant_owned + 1
    elif quant_input == '2':
        quant_choice = input("How many of the card do you own?: ").strip()
        while not (quant_choice.isdigit()):
            quant_choice = input("Not a valid choice! Input only an integer: ").strip()
        df_poke_cards.loc[(df_poke_cards['Product_Name'] == card_name) & (df_poke_cards['Set_Name'] == set_name), 'quantity'] = int(quant_choice)
    
    df_poke_cards.to_csv(poke_csv_name, index=False) #resave new dataframe

    return df_poke_cards

def user_update_quantity_prod(poke_csv_name):
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
    if not user_input.isdigit():
        print("Please enter a valid numeric index.")
        return df_poke_cards
    
    #Check if that integer value is actually a row value in the df
    index_to_drop = int(user_input) #turn into an integer to work for index
    if index_to_drop in df_poke_cards.index:
        print(f"Updating product: {df_poke_cards['Product_Name'][index_to_drop]} from {df_poke_cards['Set_Name'][index_to_drop]}. You currently have {df_poke_cards['quantity'][index_to_drop]}.")
        quantity_input = input("How many do you own now? - ") #single number
        
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

def update_poke_prod_df(poke_csv_name):
    """
    Prompts the user to either input a URL to add a new Pokemon product or if it exists, to update price.
    Based on the input, the function updates the Pokemon product DataFrame and the associated CSV file.

    Args:
        poke_csv_name (str): The file name (including path if necessary) of the CSV file 
                             containing the existing Pokémon card data.

    Returns:
        pd.DataFrame or None: The updated DataFrame if a product is added or updated; 
                              None if the operation is aborted due to invalid input or no matching card found.
    """
    #must already have using the same name as you did in new_pokemon_df
    cards_df = pd.read_csv(poke_csv_name)
    #Strip is used to clean out empty spaces in the beginning or end of the 
    url_or_name = input("Enter URL - ").strip() #asks what the user input is to determine next function

    check_substr_1 = 'https://'
    if check_substr_1 in url_or_name:
        print('Entering add_product function: \n')
        cards_df = add_product(cards_df, url_or_name, poke_csv_name)
    else:
        print(f"Product url is not valid! Must have https://")
        return cards_df

    return cards_df

def multi_update_price_poke_product_df(poke_csv_name):
    #must already have using the same name as you did in new_pokemon_df
    cards_df = pd.read_csv(poke_csv_name)

    for i in range(0, len(cards_df)):
        cards_df = update_price_prod(cards_df, cards_df['Product_Name'][i], cards_df['Set_Name'][i], poke_csv_name)
        time.sleep(random.uniform(2.0, 4.0)) #add a time delay to prevent bot detection and to properly use this function

    return cards_df