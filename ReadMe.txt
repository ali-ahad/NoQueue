For Back End: (The back end is still changing and not yet finished)
1) Navigate to the folder and run the following command on the terminal: "python manage.py runserver"
2) Use the local host written at the end and navigate to the launch page.
3) Here you can choose if you want to login or register
4) If you choose to register, you can either register as an owner or a customer.
5) Once registered you can now log in.
6) If logged in as customer:
		a) The home page shows the photo of the customer with a list of all restaurants.
		b) The customer can select one of the restaurant to view its menu.
7) If logged in as a restaurant owner:
		a) The home page shows the photo of the restaurant owner with a list of all the restaurants he/she owns.
		b) There's an option to add/update a restaurant.

Further things to do:
1) For the customer:
		a) Add the functionality of selecting a restaurant and choose dishes from its menu.
		b) Provide add to cart, update cart, view total bill and payment functionalities.
		c) Provide recommendations based on order history
		d) Add functionality to change his/her own information.

2) For the restaurant:
		a) Add functionalities to delete the restaurant
		b) Add functionality to add menu to each restaurant
		C) Add functionality to provide estimate time before each order is finished
		d) Add functionality to accept or reject a customer's order
		e) Add functionality to change his/her own information.

Note: The backend is not fully integrated with the backend and therefore wont be able to provide the best user experience.


For Front End: (The front end is still changing and not yet finished)
1) Navigate to Front End folder
2) Run index.html
3) Pages we have built:	
	1) Landing Page for Customers and Restaurant Owners
	2) Login and Sign-Up pages for the both types of users
	3) Upon login(Click on login), redirected to specific pages for respective user
	4) Navigation Bar on every page for easier control flow
	For Customer:
		a) Recommended Restaurants with detailed info of each(3 recommended) 
		b) Upon choosing restaurant(Click Proceed to Restaurant), a food menu page (Only built a menu page for the first recommended restaurant)
		c) Can select date and time of pickup
		d) Customer specific profile page. (Click on Profile)
		e) Logout page (Click on logout)
	For Restaurant Owner:
		a) View all the restaurants owned by the user					
		b) Each restaurant has modify and delete options
		c) Option to add new restaurant at very end
		d) Restaurant specific profile page
		e) Logout page

Note: We have used a basic template from Colorlib (https://colorlib.com/wp/cat/restaurant/) to save some unnecessary design effort. However, a strong amount of front end design has been implemented by us too. (Adding of layers, designing website logo, designing specific buttons, functionality of sign up and log in forms, modificatoin across different pages to suit stylistic needs)

