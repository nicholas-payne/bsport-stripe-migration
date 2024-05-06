import pandas as pd
import stripe
import api_keys

def stripe_migrate():
    """
    This program will import data from a csv file and create a list of customers 
    in Stripe. This is for a specific job and the columns headers are that I am
    using are, as follows:

    Name,email,Billing country,Language,Subscription ID,Subscription Price ID,
    Customer Coupon ID,Date subscription will start,Address Line 1,Post code,City,IBAN

    Here is the workflow:
    1. Create coupon list in Stripe
    2. Create customers list in Stripe with name, email, address, language
    3. Modify customer to add coupon code #THIS ORDERING IS VERY IMPORTANT TO AVOID CREATING INCORRECT INVOICES
    4. Modify customer to add subscription    
    """
    stripe.api_key = api_keys.stripe_api_key
    
    ######################
    ## COUPONS CREATION ##
    ######################

    # Creating a dictionary of coupon durations and display names in this form {1: "1 Month Free",...}
    coupon_durations = list(range(1,13)) 
    coupon_names = list()

    for duration in coupon_durations:
        if duration == 1:
            coupon_names.append(f'{duration} Month Free')
        else:
            coupon_names.append(f'{duration} Months Free')

    coupons = dict(zip(coupon_durations,coupon_names))
    
    # Creating coupons and pulling unique ID's created by Stripe
    for coupon in coupons:
        stripe.Coupon.create(
            duration = "repeating",
            duration_in_months = coupon,
            percent_off = 100,
            coupon_currency = 'EUR',
            name = coupons[coupon]
            )
        
    # Retrieve Stripe coupon IDs generated via Stripe
    coupon_list = stripe.Coupon.list()

    stripe_coupon_ids = {}
    for coupon in coupon_list['data']:
        stripe_coupon_ids[coupon['duration_in_months']] = coupon['id']

    #######################
    ## CUSTOMER CREATION ##
    #######################

    # Read and upload customer details including coupon IDs created in Stripe
    df = pd.read_csv('customer_details.csv')
    df['Coupon_ID'] = df['Coupon_months'].map(stripe_coupon_ids)

    for _,customer in df.iterrows():
        stripe.Customer.create(
            name=customer['Name'],
            email=customer['email'],
            address={'country':customer['Billing contry'],
                    'city':customer['City'],
                    'line1':customer['Address Line 1'],
                    #'line2':customer['Address Line 2],
                    'postal_code':customer['Post code']},
            preferred_locales=[customer['Language']],
            coupon = customer['Coupon_ID']
            )

    # Retrieve customer IDs generated via Stripe    
    customer_list = stripe.Customer.list(limit=2)

    stripe_customer_ids = {}
    for customer in customer_list['data']:
        stripe_customer_ids[customer['name']] = customer['id']

    






if __name__ == "__main__":
    stripe_migrate()
