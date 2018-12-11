# herokuServer
> A basic Python Server for a web service, deployed on Heroku. 

## Steps to deployment

* Check your server code into a new local Git repository.
* Sign up for a free Heroku account.
* Download the Heroku command-line interface (CLI).
* Authenticate the Heroku CLI with your account: heroku login
* Create configuration files ```Procfile```, ```requirements.txt```, and ```runtime.txt``` and check them into your Git repository.
* Modify your server to listen on a configurable port.
* Create your Heroku app: heroku create your-app-name
* Push your code to Heroku with Git: ```git push heroku master```

# Usage Explanation - Detail Explanation of the Stepd to Deployment:
Check in your code

Heroku (and many other web hosting services) works closely with Git: you can deploy a particular version of your code to Heroku by pushing it with the ```git push command```. So in order to deploy your code, it first needs to be checked into a local Git repository.

This Git repository should be separate from the one created when you downloaded the exercise code (the ```course-ud303``` directory). Create a new directory outside of that directory and copy the bookmark server code (the file BookmarkServer.py from last lesson) into it. Then set this new directory up as a Git repository:

    
    git init
    git add BookmarkServer.py
    git commit -m "Checking in my bookmark server!"
    


# Sign up for a free Heroku account

First, visit this link and follow the instructions to sign up for a free Heroku account:

[Signup here](https://signup.heroku.com/dc)

Make sure to write down your username and password!

# Install the Heroku CLI and authenticate

You'll need the Heroku [command-line interface](https://devcenter.heroku.com/articles/heroku-cli) (CLI) tool to set up and configure your app. Download and install it now. Once you have it installed, the ```heroku``` command will be available in your shell.

From the command line, use ```heroku login``` to authenticate to Heroku. It will prompt you for your username and password; use the ones that you just set up when you created your account. This command will save your authentication information in a hidden file (```.netrc```) so you will not need to ender your password again on the same computer.

# Create configuration files

There are a few configuration files that Heroku requires for deployment, to tell its servers how to run your application. For the case of the bookmark server, I'll just give you the required content for these files. These are just plain text files and can be created in your favorite text editor.

```runtime.txt``` tells Heroku what version of Python you want to run. [Check the currently supported runtimes in the Heroku documentation; this will change over time!](https://devcenter.heroku.com/articles/python-runtimes) As of early 2017, the currently supported version of Python 3 is ```python-3.6.0```; so this file just needs to contain the text ```python-3.6.0```.

```requirements.txt``` is used by Heroku (through ```pip```) to install dependencies of your application that aren't in the Python standard library. The bookmark server has one of these: the ```requests``` module. We'd like a recent version of that, so this file can contain the text ```requests>=2.12```. This will install version 2.12 or a later version, if one has been released.

```Procfile``` is used by Heroku to specify the command line for running your application. It can support running multiple servers, but in this case we're only going to run a web server. [Check the Heroku documentation about process types for more details](https://devcenter.heroku.com/articles/procfile). If your bookmark server is in ```BookmarkServer.py```, then the contents of Procfile should be ```web: python BookmarkServer.py```.

Create each of these files in the same directory as your code, and commit them all to your Git repository.
Displaying the contents of runtime.txt, requirements.txt, and Procfile.

# Listen on a configurable port

There's one small change that you have to make to your server code to make it run on Heroku. The bookmark server from Lesson 2 listens on ```port 8000```. But Heroku runs many users' processes on the same computer, and multiple processes can't (normally) listen on the same port. So Heroku needs to be able to tell your server what port to listen on.

The way it does this is through an environment variable — a configuration variable that is passed to your server from the program that starts it, usually the shell. Python code can access environment variables in the ```os.environ``` dictionary. The names of environment variables are usually capitalized; and the environment variable we need here is called, unsurprisingly, ```PORT```.

The port your server listens on is configured when it creates the ```HTTPServer``` instance, near the bottom of the server code. We can make it work with or without the ```PORT``` environment variable, like so:

```
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))   # Use PORT if it's there.
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, Shortener)
    httpd.serve_forever()
```

To access ```os.environ```, you will also need to ```import os``` at the top of the file.

Make these changes to your server code, run the server locally to test that it still works, then commit it to your Git repository:

```
git add BookmarkServer.py
git commit -m "Use PORT from environment."
```

# Create and push your app

Before you can put your service on the web, you have to give it a name. You can call it whatever you want, as long as the name is not already taken by another user! Your app's name will appear in the URI of your deployed service. For instance, if you name your app ```silly-pony```, it will appear on the web at ```https://silly-pony.herokuapp.com/```.

Use ```heroku create your-app-name``` to tell Heroku about your app and give it a name. Again, you can choose any name you like, but it will have to be unique — the service will tell you if you're choosing a name that someone else has already claimed.

Finally, use ```git push heroku master``` to deploy your app!
Pushing my bookmark server to Heroku using Git.

If all goes well, your app will now be accessible on the web! The URI appears in the output from the ```git``` command.

# Accessing server logs

If your app doesn't work quite right as deployed, one resource that can be very helpful is the server log. Since your service isn't running on your own local machine any more, those logs aren't going to show up in your terminal! Instead, they're available from the Heroku dashboard.

Take a look at ```https://dashboard.heroku.com/apps/little-bookmarks/logs```, but replace ```"little-bookmarks"``` with your own app's name.

# Server URL
[SERVER](https://pflash-bookmark-server.herokuapp.com/)
