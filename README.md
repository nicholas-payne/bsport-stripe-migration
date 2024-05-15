# Migration to Stripe

The two python scripts upload customer information stored in a csv file from an excel spreadsheet using the the Stripe API as part of a migration of payment services to Stripe.

The api key should be stored in api_keys.py, with a sample file provided (sample-api_keys.py).

The script coupon_and_customer_creation.py first creates coupons labelled 1 Month Free, 2 Months Free etc. up to one year to facilitate prearranged cash payments. The customers are then created from the csv file (Sample Data.csv is the required format) and linked to the appropriate coupon (if any) indicated in the csv file.

The second script subscription_creation then links the products in Stripe to the appropriate customer by pulling the appropriate price_ID to create a Subscription Schedule so that the start date can be specified.
