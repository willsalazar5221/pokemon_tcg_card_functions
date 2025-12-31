# `2_pokemon_dex_sorting`


**Author: William B. Salazar**


## Description

This recipe guides you through the Pokedex binder script. I use a csv file with the Pokémon national dex numbers to help decide where it belongs in your binder. A csv file is outputted for your record keeping.

## Version History

- `page_sorting_v2.py` (v2) - December 2025 by W. B. Salazar

It takes in a Pokémon name and decides on what oage and on what slot in a 3x3 binder page it should go on. Note that I do not account for regional variants, forme variants, or shiny variants. For example, Mega Charizard X/Y and Charizard all have the same dex number, so simply put in Charizard as the Pokémon name. In this version you can also just input the name lowercase and it will recognize it.

Python blocks/lines will be preceded by >>> for clarity.


## INITIAL SETUP

For this procedure, we solely need to run Python scripts and functions. I primarily used Jupyter Notebooks from Anaconda to run this whole process. I currently don't have an easy website to run this from, but the example notebooks are simple enough. For these functions, under `example_notebooks` you can find the notebook titled `example_2_national_dex.ipynb`, made for your convenience showcasing all the functions you can use.

*Note*: You will also need the National Pokedex csv file I use, titled `pokemon_dex_num.csv`. It is added under `scripts_and_files` for your convenience.


## Background

The code is fairly straightforward here with some plotting routines for visualization and Panda DataFrame manipulations. To find the accurate page number and the slot on the 3x3 grid, I devised the following. An example would be everyone's favorite Pokémon, Caterpie. Caterpie's national dex number is 10. If a page fits 9 cards, Caterpie is on page 2, the first card on the page (this would be top left, since we read the page from left to right, top to bottom). Thus, we use simple division. The formula for the page and the slot number is as follows

$$page\\_number = poke\\_national\\_dex\\_num / / 9$$

and 

$$page\\_index = poke\\_national\\_dex\\_num \% 9$$ 


In non-computer coding, this is simply the quotient and the remainder. We need to make our numbers in base 9 essentially. Notice if you punch in 10/9 into a calculator, we get 1.1 (rounded). So, our page number is wrong, thus we add one to it. Our index on the page is correct though, so we leave it as is. However there is a case where a number is divisible by 9. Think of 18. This Pokemon (Pidgeot), should land on page 2, bottom right. We note that 18/9 is two. There is no remainder though. The page is now right, but the remainder is wrong. Hence for this case we keep the page and set the remainder to be 9. The function `plot_page_pos` does this arithmetic. The rest of the code helps to keep a record of all this.


## Functions

I will briefly detail the functions you will use. Docstrings are in the scripts for more details and additional helper functions are embedded.


### ${\color{purple} Creating \space New \space CSV \space File }$

**create_record_csv_poke(name_of_csv)**

The purpose of this function is to initialize an empty csv file to record and keep track the cards in your binder. Only run this once. It contains the following columns: 'pokemon_name', 'nat_dex_num', 'set', 'foil_flag', 'full_art_flag', 'url'.

&emsp; **Parameters:&ensp; name_of_csv &nbsp;: &nbsp;*str***
<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp; Name you choose to give the csv file (do not include .csv extension).  


### ${\color{purple} Finding \space Name/Dex \space of \space Pokemon }$

**find_dex_num_or_pokemon_name()**

We use this function to simply find the name or the national dex number of the pokemon. This searches the national dex csv file. It prompts for a user input when ran.

&emsp; **Parameters:&ensp; None, User Input &nbsp;: &nbsp;*int or str***
<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp; Take in either a number or a name of a pokemon. Names of pokemon must be capitalized.


### ${\color{purple} Plot \space and \space Record \space Cards}$

**card_recording(record_csv_name)**

This is the main function to determine where you would place your card in the binder. There are four user inputs that help record keep your collection. They ask about the set it came from, if the art is a foil (and if it is, it asks if it is a full art card), and to provide a link to an image of the card. The last one is for your convenience so you do not have to look in the binder physically.

&emsp; **Parameters:&ensp; record_csv_name &nbsp;: &nbsp;*str***
<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp; Name of the csv file with all the cards (include .csv extension)


### ${\color{purple} Check \space Existence \space of \space Card }$

**check_existence_in_record(record_csv_name)**

This function is to help check if a card exists in your records and where it is if it does exist.

&emsp; **Parameters:&ensp; None, User Input &nbsp;: &nbsp;*str***
<br>

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp; User is prompted to enter name of Pokémon.

