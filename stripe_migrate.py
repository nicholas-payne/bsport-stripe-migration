import pandas as pd
import stripe

def stripe_migrate():
    """
    This program will import data from a csv file and create a list of customers 
    in Stripe. This is for a specific job and the columns headers are that I am
    using are, as follows:

    Name,email,Billing country,Language,Subscription ID,Subscription Price ID,
    Customer Coupon ID,Date subscription will start,Address Line 1,Post code,City,IBAN

    Here is the workflow:
    1. Create customers list in Stripe with name, email, address, language
    2. Create coupon list in Stripe
    3. Modify customer to add coupon code #THIS ORDERING IS VERY IMPORTANT TO AVOID CREATING INCORRECT INVOICES
    4. Modify customer to add subscription

    
    """
    df = pd.read_csv('customer_details.csv')




if __name__ == "__main__":
    stripe_migrate()
