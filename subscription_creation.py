import pandas as pd
import stripe
import api_keys

def subscription_creation():

    """
    This script links existing customers with existing subscriptions in a
    Stripe account. In this case, we have a spreadsheet with a list of 
    customers and the associated subscription they have.
    """

    stripe.api_key = api_keys.stripe_api_key

    #####################
    ## PRICE RETRIEVAL ##
    #####################

    stripe_product_list = stripe.Product.list()
    
    stripe_price_ids = dict()

    for stripe_product in stripe_product_list["data"]:
        stripe_price_ids[stripe_product["name"]] = stripe_product["default_price"]

    ###########################
    ## SUBSCRIPTION CREATION ##
    ###########################

    # Reading in customer_data (no need to parse dates because we are using start_date_epoch column)
    df = pd.read_csv("customer_details_updated.csv")

    # Joining price IDs from Stripe
    df['Price_ID'] = df['Product Name'].map(stripe_price_ids)   

    for _,customer in df.iterrows():

        _ = stripe.SubscriptionSchedule.create(
            customer=customer["Customer_ID"],
            start_date=customer["start_date_epoch"],
            end_behavior="release",
            phases=[{"items":[{"price":customer["Price_ID"],"quantity":1}],
                     "iterations":12}]
        )

if __name__ == "__main__":
    subscription_creation()
