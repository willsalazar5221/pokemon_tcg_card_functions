# `1_pokemon_cards_funcs`


**Author: William B. Salazar**


## Description

This recipe guides you through the two different scripts prepared for sorting and pricing cards/products. The first two scripts work very similarly since we scrape through the same site (PriceCharting.com). A csv file is outputted for your record keeping for both scripts.

## Version History

* `poke_cards_funcs_v4.py` (v4) - November 2025 by W. B. Salazar

This version has been streamlined to work using a single function to add and update card pricing. Other functions added to remove cards and multi-update cards all at once.

* `poke_product_funcs_v1.py` (v1) - November 2025 by W. B. Salazar

Primarily built from the above function. Since products are not graded, I removed this column in the saved csv file.

Python blocks/lines will be preceded by >>> for clarity.



## INITIAL SETUP

For this procedure, we solely need to run Python scripts and functions. I primarily used Jupyter Notebooks from Anaconda to run this whole process. I currently don't have an easy website to run this from, but the example notebooks are simple enough. Two example notebooks in `example_notebooks` are made for your convenience of all the functions you can use.


## Background

For both scripts, the main function is to record the card/product and know the market price of your item. I scrape PriceCharting since it reliably tells you the price of a PSA 10 version of a card. For those that prefer TCGPlayer, while ungraded card prices are more accurate, it's not possible to scrape the website using the functions I made. In addition, PriceCharting can also find products, so it was easiest to just recreate the same functions for the products.

There are several functions used, but only three main ones you will use. I will detail them below, however in the scripts you with also find docstrings that detail the functions in great detail.

One small background detail I have embedded into the first functions is the flag of whether you should grade your card. This binary "Yes" or "No" flag is decided by the function `determine_psa_worth`. The price to grade a card through PSA (as of December 2025) is 21.99. I like to grade cards if I know the value is worth double the cost of grading said card. Hence, I use the formula (on line 243)

$$ min\\_price\\_grade = 22 \* 2.2$$

,where `min_price_grade` is checked against the price of the PSA 10 version of the card. This is assuming you get a PSA 10, which will depend wildly on the card's condition and the mood of the grader. I rounded up and added a .2 multiplier to account for tax or fees. This is easy to change for your purposes and how you value cards.



## Functions

I will briefly detail the functions you will use. As said, docstrings are in the scripts for more details. I will split this section in two different subsections for the differences between the card and product functions.


## ${\\color{red}Card \\space Functions}$


### ${\\color{purple} Making \\space New \\space CSV \\space File }$

**new\_pokemon\_df(name\_of\_csv)**

The purpose of this function is to initialize an empty csv file to record and keep track of all your cards and pricing. It will contain the following columns: 'Card\_Name', 'Set\_Name', 'url', 'ungraded\_price', 'PSA10\_price', 'grade\_yn'.

  **Parameters:  name\_of\_csv  :  *str***
<br>
           Name you choose to give the csv file (do not include .csv extension).



### ${\\color{purple} Adding/Updating \\space Single \\space Card }$

**update\_poke\_df(poke\_csv\_name)**

Main function to update your csv file. Once you run the line, it will prompt the user to enter a card name or url. If a card name is entered, it will search your csv file and ask to update it if it exists. If a URL is entered, the card is entered into the csv file if it does not exist already. If it does exist, it prompts to update.

  **Parameters:  poke\_csv\_name  :  *str***
<br>
           Name of the csv file with all the cards (include .csv extension)



### ${\\color{purple} Multi-updating \\space CSV \\space File }$

**multi\_update\_poke\_df(poke\_csv\_name)**

Supplemental function to update your whole csv file. It runs through each card and updates the price by visiting the url in the url column and scarping the website. Convenient for updating your collection in one go.

  **Parameters:  poke\_csv\_name  :  *str***
<br>
           Name of the csv file with all the cards (include .csv extension)



### ${\\color{purple} Removing \\space Card }$

**remove\_card(poke\_csv\_name)**

Remove a card from the csv file. It will prompt the user to either enter the index in the DataFrame or the card name.

  **Parameters:  poke\_csv\_name  :  *str***
<br>
           Name of the csv file with all the cards (include .csv extension)



## ${\\color{red}Product \\space Functions}$



### ${\\color{purple} Making \\space New \\space CSV \\space File }$

**new\_pokemon\_products\_df(name\_of\_csv)**

The purpose of this function is to initialize an empty csv file to record and keep track of all your cards and pricing. It will contain the following columns: 'Product\_Name', 'Set\_Name', 'url', 'MSRP', 'market\_price', 'quantity'.

  **Parameters:  name\_of\_csv  :  *str***
<br>
           Name you choose to give the csv file (do not include .csv extension).



### ${\\color{purple} Adding/Updating \\space Single \\space Product }$

**update\_poke\_prod\_df(poke\_csv\_name)**

Main function to update your csv file. Once you run the line, it will prompt the user to enter a url. It will then prompt the user for the MSRP price (or you can enter the price you paid) and the quantity you own of the product. If the product is already in the csv file, it will prompt you to update the price. You can type `yes` to do so instead. Otherwise, nothing happens.

  **Parameters:  poke\_csv\_name  :  *str***
<br>
           Name of the csv file with all the cards (include .csv extension)



### ${\\color{purple} Multi-updating \\space CSV \\space File }$

**multi\_update\_price\_poke\_product\_df(poke\_csv\_name)**

Supplemental function to update your whole csv file. It runs through each product and updates the price by visiting the url in the url column and scarping the website. Convenient for updating your collection in one go.

  **Parameters:  poke\_csv\_name  :  *str***
<br>
           Name of the csv file with all the cards (include .csv extension).



### ${\\color{purple} Updating \\space Quantity }$

**update\_quant\_prod(poke\_csv\_name)**

Update the quantity of a product from the csv file. It will prompt the user to enter the index of the item in the DataFrame and ask `"How many do you own now?"`.

  **Parameters:  poke\_csv\_name  :  *str***
<br>
           Name of the csv file with all the cards (include .csv extension).

