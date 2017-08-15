# TweetStream

Twitter streaming with [RxPy](https://github.com/ReactiveX/RxPY) and [Flask](http://flask.pocoo.org/).

### Setup

## Prerequisites

A couple of things you will need

1. [Virtualenv](https://virtualenv.pypa.io/en/stable/)
    
   This will be used to create a virtual environment for your application, unless you want these `dangerous` dependencies on your local machine, I suggest you have this installed
  
  ```bash
  $ [sudo] pip install virtualenv
  ```
  > This installs virtualenv on your local machine(dev environ), this you will need on your development environ


2. [Twitter Credentials](https://apps.twitter.com/app)

   You will need to create a Twitter application and obtain credentials and secret tokens in order to use this application. Ensure that you do not check them into VCS.
   
   Add these credentials to a `.env` file and DO NOT check this file into VCS as well.
   
   ```plain
   TWITTER_CONSUMER_KEY=<CONSUMER_KEY
   TWITTER_CONSUMER_SECRET=<CONSUMER_SECRET>
   ...
   <OTHER CREDENTIALS>
   ```

3. A love for Python
  
  This has to be obvious for this project. :D :smile:


Clone repository (or fork it, whatever tickles your fancy)

```bash
$ git clone https://github.com/Wyvarn/tweetstream.git
$ cd tweetstream
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py runserver
```
> This is from downloading the code to starting up the application

Enjoy!