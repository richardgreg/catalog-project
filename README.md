# Item (Classical Book) Catalog

## About

This is a **RESTful** web application, using the Python framework **Flask,**
which provides a list of items (books) within a variety of _categories_ (genres)
as well as provides user registration and authentication system. Registered 
users will have the ability to **post,** **edit** and **delete** their own items.

`'/' or '/categories'` - Homepage displaying categories and successful login.
![Homepage](https://github.com/richardgreg/catalog-project/blob/master/assets/successfull-loggin.png)

### Why this project and specifically a book catalog?
Modern web applications perform a variety of functions and provide amazing 
features and utilities to their users; but deep down, it’s really all just 
creating, reading, updating and deleting data.
I am a avid reader. I enjoyed reading classical books as a child. My favorite
genre was _Mythology._

`'/category/<int:category_id>/item/'` - Route displaying items relative to a category.
![Display Category Items](https://github.com/richardgreg/catalog-project/blob/master/assets/item-display2.png)

`'/category/<int:category_id>/item/<int:category_item_id>/'` - A single book
item description.
![Category Item Description](https://github.com/richardgreg/catalog-project/blob/master/assets/item-description.png)

`'/category/<int:category_id>/item/new/'` - Form to add a new book. User must
be logged in.
![Add Form](https://github.com/richardgreg/catalog-project/blob/master/assets/add-form.png)

`'/category/<int:category_id>/item/<int:category_item_id>/edit'` - Edit book
item. Edit is restricted to owner of item.
![Edit Form](https://github.com/richardgreg/catalog-project/blob/master/assets/edit-item.png)

`'/category/<int:category_id>/item/<int:category_item_id>/delete'` - Delete item.
![Delete Item](https://github.com/richardgreg/catalog-project/blob/master/assets/delete-item.png)

### What is needed:
You'll run these program using a Unix-style terminal on your computer; the
point of it is to be able to offer the same software (Linux) regardless of what
kind of computer you're running on. If you are using a Mac or Linux system,
your regular terminal program will do just fine. On Windows, we recommend using
the Git Bash terminal that comes with the Git software.

In order to make use of third party authentication and authorization
(google OAuth) feature, one will require a google account.

### Geting Started
##### Virtual machine
- Download and install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).
Install the platform package for your operating system. You do not need the
extension pack or the SDK. You do not need to launch VirtualBox after
installing it; Vagrant will do that. **Ubuntu users:** If you are running
Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due
to a reported bug, installing VirtualBox from the site may uninstall other
software you need.
- Download and Install [vagrant](https://www.vagrantup.com/downloads.html). 
You can check if vagrant is installed by running `vagrant --version`
- Download the [VM configuration](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip).
Unzip the file. Using the terminal, navigate into the vagrant subdirectory.
- Clone the **_catalog-project_** and move it into the
_/FSND-Virtual-Machine/vagrant/_ subdirectory. This particular step can
actually be done at any point in time, but to avoid any confusion, do this.
- From your terminal, inside the vagrant subdirectory, run the command
`vagrant up`. This will cause Vagrant to download the Linux operating system
and install it. This may take quite a while (many minutes) depending on how
fast your Internet connection is. When vagrant up is finished running, you will
get your shell prompt back. At this point, you can run `vagrant ssh` to log in
to your newly installed Linux VM! Inside the VM, change directory to
**_/vagrant_** and look around with `ls`.

The files you see here are the same as the ones in the
_/FSND-Virtual-Machine/vagrant/_ subdirectory on your computer
(where you started Vagrant from). Any file you create in one will be
automatically shared to the other. This means that you can edit code in your
favorite text editor, and run it inside the VM.

##### OAuth
- Go to [console.developers.google](https://console.developers.google.com/apis)
- Create a new project and name it _Book-ish_, just for the sake of
consistency, but you can name it whatever you like
- Go to the _Credentials_ section. Go to the _OAuth consent screen tab_
first of all. You only have to enter the _application name_. Then back to the
_credentials_ tab, create a new _OAuth client ID_. Make sure you select
**_Web Application_**. The name can be whatever. _Authorized JavaScript
origin:_ should be: _http://localhost:8000_.
_Authorized redirect URIs:_ _http://localhost:8000/login_ and
_http://localhost:8000/gconnect_. Save and create. You'll be presented with a
_client ID_ and _client secrets_.
- Now, download the _JSON_ attached to the _OAuth client ID_ you just created.
**Make sure you do this after the above steps have been completed. If you do
it before, the origins and authorized uris may not appear in the JSON file.**
- Rename the JSON file as **_client_secrets.json_**. You can delete the dummy
_public_client_secrets.json_ file that comes with the _catalog-project._

Open the _login.html_ template in _/template_ directory with your favorite
text editor.
``` html
<!-- GOOGLE PLUS SIGN IN BUTTON-->

          
          <div id="signinButton">
          <span class="g-signin"
            data-scope="openid email"
            data-clientid="CLIENT-ID"
            data-redirecturi="postmessage"
            data-accesstype="offline"
            data-cookiepolicy="single_host_origin"
            data-callback="signInCallback"
            data-approvalprompt="force">
          </span>
        </div>
```
Copy your google OAuth _cliend ID._ and replace `CLIENT-ID`.
And you're good to go for the authentication and authorization.

Files in the VM's _/vagrant_ directory are shared with the vagrant folder on
your computer. But other data inside the VM is not. For instance the project
dependencies **are not**. You can `cd` into the _/catalog-project_ directory
(or whatever you named it when cloning).

### How to run app
While in the the _project_ directory, via your terminal:

- First, enter the command `python3 database_setup.py`
- Secondly, enter `python3 install_categories.py`
- Finally, enter `python3 application.py`

:expressionless:


## Possible Improvements
- Structure the Flask app in a way that allows scalability.
- Run software packages with Docker instead of Vagrant since the former is more
light-weight.
- Use the `flask-restful` library to build scalable API endpoints.
- Give users an option to add/upload images for book items.
- More OAuth providers to expand userbase.
