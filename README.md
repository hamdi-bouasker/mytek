# MyTech® - Your Technology

### Django e-commerce website with Advanced Features and SEO Friendly

![mytech.gif](https://github.com/IT-Support-L2/mytek/blob/main/mytech.gif)

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


### Admin Functionalities

- Python-decouple
- Admin Honeypot

### Project live demo is served with:

- `Heroku web server` with Heroku CLI
- `Microsoft Azure Storage`
- `Postgres DB`

### Project Live Demo URL

- https://mytek.herokuapp.com


### Project Next Functionalities

- MFA
- CACHE
- Sub-Categories
- Live Chat Support
- Change Email address
- Newsletter
- Wishlist
- Automated email alert once the stock reached 10 pieces as exemple
- The most feature I am very interested to implement, is: Automated live analytics with automated daily report sent to admin or store owner email address. 









