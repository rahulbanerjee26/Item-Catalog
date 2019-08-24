
  

<h1>Restful Web App  </h1>
<h2> Item Catalog </h2> 

  

<h2> Nanodegree : Full Stack Web Developer, Udacity </h2>

  

  

<p><b>Skills:

 - Flask 
 - Jinja 
 - sqlalchemy 
 - sqlite 
 - Bootstrap 
 - Google OAuth  
 - Facebook OAuth 
 - CRUD Operations
 - Foreign Key Relations

</b></p>

  

  

<h3>  <u> Description </u></h3>

  

<p>An application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.  This project uses persistent data storage to create a RESTful web application. <br>

<b>Features:</b>

 - log in using google/facebook account
 -   local permission system
 -   user has to login to create categories/items
 -   user can only edit/delete their own categories/items
 -   user can view other's categories/items but not edit/delete them
 -   users can safely log out
 -   return information about categories,items,users in JSON format
 -   Flash messages to improve user experience

</p>

  

  


<h3>  <u> Software Required </u>  </h3>

  
  

<a  href="https://www.virtualbox.org/wiki/Download_Old_Builds_5_1">Virtual Box</a>

  

<a  href="https://www.vagrantup.com/">Vagrant </a>

<a  href="https://www.python.org/downloads/"> Python </a>

<a  href="https://git-scm.com/"> Git Bash </a>

<a  href="https://www.sqlalchemy.org/"> Sqlalchemy </a>

  
  
  

  

<h3>  <u> Steps to Run </u>  </h3>

  

<ul>

  

<li> Install Vagrant and Virtual Box </li>

  

<li> Log in using vagrant ssh </li>

  

<li> Clone Repo </li>

  

<li> Using git bash cd to the folder </li>

  

<li> Create the database by typing

    python databaseSetup.py
    
    
 </li>
 
 <li> go to <a href="https://console.developers.google.com"> google's console developer </a> and get a client id for OAuth. </li>
 <li> Edit project and Add http://localhost:5000 to js origins </li>
 <li> Add http://localhost:5000/login and http://localhost:5000/gconnect to redirect_uris </li>
 <li> download the json file and rename to client_secrets.json and paste it in same folder as index.py </li>
 <li> update your client id in login.html </li>
 <li> Follow above steps for FaceBook Authentication </li>
 <li> Run on server 5000 by typing 
		

    python app.py

</li>

</ul>


  

  <h3><u>JSON End Points </u>  </h3>
  

 - /categories/JSON 
 - /items/JSON
 - /users/JSON
 - /item/<int:id>/JSON
 - /user/<int:id>/JSON
 - /category/<int:id>/JSON

<h3><u>CRUD End Points </u>  </h3>

 - /createCategory
 - /viewCategories
 - /<int:id>/updateCategory
 - /<int:id>/deleteCategory
 - /createItem
 - /<int:id>/viewItems
 - /<int:id>/viewItem
 - /<int:id>/updateItem
 - /<int:id>/deleteItem
 - /login

<h3><u>Improvement</u>  </h3>

 - Styling
 - User Experience

  

<h3><u> Author</u>  </h3>

<b>Rahul Banerjee</b>