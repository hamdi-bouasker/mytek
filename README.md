# MyTech® - Your Technology

### Django e-commerce website with Advanced Features and SEO Friendly

![mytech.gif](https://github.com/hamdi-bouasker/mytek/blob/main/mytechAPI.gif)

### Images and Prices are only used for Demo purpose and does not reflect real products! 

### Admin credentials

Email address: `admin@mytek.com` 
Password: `mytek2021`

### Run the project

- Install `requirements.txt` in your `venv` or `pipenv`
- You will need paypal business account and 2 paypal sandboxed accounts: Customer and Store Owner. Then, copy paste your public key in base.html (open base.html and you will find out exactly where to paste it)

### Frontend

- `HTML`, `CSS`, `Bootstrap`, `JavaScript`, `jQuery`

- Templates downloaded for free from https://www.templateshub.net/template/Electro-eCommerce-Website-Templates 

  I modified few parts to meet the required specifications. Else, backend is coded and integrated from the scratch.
  
- Templates I coded: cart.html, checkout.html, accounts templates, order templates

### Backend 

- `Python`, `Django`

### Local DB
- sqlite3

### Live Demo DB
- PostgreSQL DB


## Project current functionalities

### User Management

- `User signup` and `password reset` with email verification - Please check your spam folder as well. 
- `User password change` while logged in
- Change basic information

### Category Functionalities

- Query of products related categrory

### Products Functionalities

- Auto-decrement `Stock` product
- `Auto-Discount` appliance
- `Product rating` and `average rating` calculation
- If stock is 0, `Out of stock` will take the place of `Add to cart button`

### Cart Functionalities

- `Add` and `remove` products in cart
- Cart items are saved before and after login using `sessionID`
- `Add` and `remove` cart items

### Search Bar

- Query using `keywords`

### Pagination

- Products pagination

### Orders

- Products `checkout`
- PayPal payment with `PayPal sandbox demonstration`
- `Order review` before confirmation
- `Order receipt`
- Use your customer paypal sanboxed email address to test payment

### Newsletter

- Customer is able to subscribe to newsletter regardless of being registered or not.
- Above the footer, input your email address in the subscribe form and click on `subscribe`.

### Modal Contact Form

- Customer is able to send message regardless of being registered or not.

- In the footer menu, click on `Contact`.


### Admin Functionalities

- Python-decouple
- Admin Honeypot

### Django Rest Framework API

- Django-filter Backend

![mytech.gif](https://github.com/IT-Support-L2/mytek/blob/main/mytechAPI.gif)

### CACHE

- Per-view cache: Deleted as it caused Cart Items are not synchronized on all pages. Working on different CACHE integration.
### Run the project from `Docker container`

- Navigate to the project root directory
- Copy paste this command `docker-compose build` and hit enter
- Copy paste this command `docker-compose up` and hit enter
- Open your browser and go to `127.0.0.1:8000` and not to `0.0.0.0:8000` 😁

### Project Live demo was served with Heroku and AWS Elastic Beanstalk but due charges I decided to stop it.

### You have to set few configurations and settings in order to successfully run the project.
