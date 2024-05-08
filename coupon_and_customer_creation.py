import pandas as pd
import stripe
import api_keys

def coupon_and_customer_creation():
    """
    This program will import data from a csv file and create a list of customers 
    in Stripe. There is a sample .csv file available to see the format of the
    input dataset. For this job, products and prices already exist in the account, so
    linking to existing subscription IDs is necessary.

    Here is the workflow:
    1. Create coupon list in Stripe
    2. Create customers list in Stripe and link to coupons
    3. Link customers and subscriptions
    """
    stripe.api_key = api_keys.stripe_api_key
    
    # All dates sent to Stripe must be epoch timestaps so this is a list of all columns to be parsed as dates
    date_cols = [7]
    date_format = "%d.%m.%Y"

    ######################
    ## COUPONS CREATION ##
    ######################

    # Creating a dictionary of coupon durations and display names in this form {1: "1 Month Free",...}
    coupon_durations = list(range(1,13)) 
    coupon_names = list()

    for duration in coupon_durations:
        if duration == 1:
            coupon_names.append(f"{duration} Month Free")
        else:
            coupon_names.append(f"{duration} Months Free")

    coupons = dict(zip(coupon_durations,coupon_names))
    
    # Creating coupons and pulling unique IDs created by Stripe
    for coupon in coupons:
        _ = stripe.Coupon.create(
            duration = "repeating",
            duration_in_months = coupon,
            percent_off = 100,
            currency = "eur",
            name = coupons[coupon]
            )
        
    # Retrieve Stripe coupon IDs generated via Stripe
    stripe_coupon_list = stripe.Coupon.list()

    stripe_coupon_ids = dict()

    for stripe_coupon in stripe_coupon_list["data"]:
        stripe_coupon_ids[stripe_coupon["duration_in_months"]] = stripe_coupon["id"]

    #######################
    ## CUSTOMER CREATION ##
    #######################

    # Importing customer list and converting dates
    df = pd.read_csv("customer_details.csv",parse_dates=date_cols,date_format=date_format)
    
    #### NEEDS FIXING UNIX TIME NEEDS TO BE IN SECONDS NOT NANOSECONDS
    df["start_date_epoch"] = df["Date subscription will start"].astype("int64")
    
    # Joining coupon IDs from Stripe
    df["Coupon_ID"] = df["Coupon Months"].map(stripe_coupon_ids)

    customer_ID_list = list()

    for _,customer in df.iterrows():
        stripe_customer = stripe.Customer.create(
            name=customer["Name"],
            email=customer["email"],
            address={"country":customer["Billing country"],
                    "city":customer["City"],
                    "line1":customer["Address Line 1"],
                    #"line2":customer["Address Line 2],
                    "postal_code":customer["Post code"]},
            preferred_locales=[customer["Language"]],
            coupon = customer["Coupon_ID"]
            )
                       
        customer_ID_list.append(stripe_customer["id"])
    
    df['Customer_ID'] = customer_ID_list
    df.to_csv('customer_details_updated.csv')
    print('Successful Customer Upload!')

if __name__ == "__main__":
    coupon_and_customer_creation()
