# Predicting Ages Through Facial Photos

## Introduction

Traditionally, the alcohol age verification process often acquires slow and sometimes inaccurate manual checks for identification. As cameras are located by the checkout area, the need for an employee to check a customer's identity may be replaced given the right model. Check out the [full notebook](python/good-seed.ipynb) and the [demo](https://www.loom.com/share/0479696709ec4e639a444299bf855180?sid=61dad59e-d590-471e-9b85-a563637bd5e9).

## Goal
Develop a model that identifies the age of a customer based on their portrait photo. Attain ages with the lowest mean absolute average on the test set, atleast below 8.0. 

## Key Findings
The model:

- Eliminates the need to manually identify the age of over a half of all customers that purchase alcohol (if results are replicated).

![predicted-ages](pics/predicted_ages1.png)

- Predicts ages within 6.1 years off person's actual age on average

![difference](pics/difference.png)

- Produces an F1 score that is better than constant models at 0.89 with precision at 0.82


## Data

7.5k photos with accompanying ages are saved in the `datasets/faces/` folder.

## Process

1. Prepare Data
    - Initialize packages
    - Load data
    
2. Exploratory Data Analysis
    - Assess distribution

3. Run Model
    - Load train (ImageDataGenerator)
    - Load test (ImageDataGenerator)
    - Create model (ResNet)
    - Train model

4. Draw Conclusions
    - How effective is the model?
    - How can it be used to save resources?

## Assumptions
- The distribution of the age of customers who purchase alcohol is similar to the distribition of the age of customers generally.
- The median age of customers is 44 years, according to this [article](https://adplanetads.com/spotlight/grocery-shopper-demographics-retail-dooh/#:~:text=Age%3A%20The%20average%20age%20of,their%20own%20ways%20of%20shopping.).

## Alternative Uses

This model could also help Good Seed financially by determining product demographics.

### Product Placement

Firstly, a grocery store could identify what products are being bought by each age group. For instance, they could identify certain products that are bought more by elderly people. As elderly people may require more help accessing products, the store could place these items closer to the front, making it easier for them to purchase items and incentivising shopping at their grocery store over others. 

### Supplier Marketing
Secondly, this information could also be useful for suppliers who might want to identify their target audiences. A grocery could sell this information and charge for specific shelf spacing based on customer preferences.


## Run Application

If you want to give the model a go, follow these steps:

1. Ensure [requirements](requirements.txt) are met
2. Save model as `python/models/age_prediction_model.h5`
3. Run in CLI `streamlit run python/app.py`
