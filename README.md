# FYP - Ghumi Phiri - Rayan Dongol
## Overview
GhumiPhiri is a web applicaiton built using the Django framework and HTML/CSS with JS. The project aims to simplify the process of booking packages provided by hotels and travel agencies. The packages created by the hotels and packages are listed and can be easily accessed. The user can then pick their desired package and check the availability of their booking date. Once the booking date is confirmed, the user can then proceed to checkout whrere they can enter their payment credentials.

## Setup
Cloning the repo
```sh
git clone https://github.com/chirayanmabu/FYP.git
$ cd Development/"Ghumi Phiri"
```


Setting up a virtual environment
```sh
python -m venv venv
venv\Scripts\activate
```


Install the requirement.txt file
```sh
(env)$ pip install -r requirements.txt
```
Note: The (env) indicates that the terminal is operating in a previously created virtual environment.


Setting up the Stripe webhook
To properly run the stripe endpoint, download the stripe cli form [here](https://docs.stripe.com/stripe-cli).
```sh
stripe listen --forward-to localhost:8000/webhook/
```

Finally, make sure to have your database credentials in the settings.py file.
`Development/Ghumi Phiri/GhumiPhiri/GhumiPhiri/settings.py`
```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your database name',
        'USER': 'your username',
        'PASSWORD': 'your password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Run the following commands to run the program.
Make sure to cd into the directory where manage.py is present
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
The application should run in your localhost.

  

## Walkthrough
### For unregistered users
The website can be accessed without registering as user. However, some functionalities such as favoriting packages and booking packages will not be available. The user can freely access the site and view the available packages.

#### Registering as seller
The user can register as a seller by clicking the "Seller account" link in the nav bar.

The register page appears for sellers and the user can be registered as a seller by providing valid credentials.

After registering, the user is redirected to the log in page where the user can login with the registered credentials.


#### Registering as buyer
The user can registering as a buyer buy clicking the log in link in the navigation bar. 

The login page appears and cliking the sign up button allows the user to register as a buyer.

After registering, the user is redirected to the log in page where the user can login with the registered credentials.

#  

### For seller users
The sellers will have access to the dashboard page. The dashboard page has a sidebar from where they can access the "My Package" page. The "My Package" page lists all the packages created by the user and allows the user to create/update/delete packages.

The main "Dashboard" page in the sidebar displays data regarding the number of sales, bookings done and total packages. Along with a table for viewing weekly bookings and a chart that displays the number of bookings done in each monht.

The "Payment" page in the sidebar allows the user to view every single booking that has been made for the user's packages.

THe "Account" page in the sidebar allows the user to view/edit their profile along with their favorite packages.

#  

### For buyer users
The buyer user can freely navigate the site. 

The user can choose their desired packages from the home page which opens the detail of the package.

In the package detail page, the user can add the package to their favorites by clicking the heart button.

The user can also check the availability of the booking date of the package by choosing the date from the Book button.

If the date is available, a checkout button appears next to the book button. The chekout button redirects the user to the checkout page hosted by Stripe.

The user can view their profile information and their favorite packages by navigating to their profile by clicking the circlular image in the top right of the navigation bar and pressing the "Profile" button.


