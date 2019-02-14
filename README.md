# AryaBot-Web-App
Project created for the Pointman interview process!

First time using Flask to make a Web Application!
The web app is being hosted on AWS Elastic Beanstalk and you can go to it by typing in ```aryabot.me``` in your browser

## Overview
My original plan was to make a bot to purchase limited and highly sought after sneakers on jimmyjazz.com to maximize potential profit.
Due to a shortcoming described in the setbacks section I had to change my idea. I decided to keep the web app the same in every aspect 
other than the main bot functionality. I still kept everything else and that is why things might not fully make sense as to why they are 
there, I just figured I would keep them as they still showcase the knowledge I learned and applied while doing this project. Instead of the
bot I decided to make a simple random joke generator that makes an API call to a jokes API that has a mixture of some programming jokes and
some corny jokes. I also have a button that a user can click which will send out a tweet to my AryaBot twitter account stating that they are
satisfied as well as a random joke. This is the link to my twitter account ```https://twitter.com/BotArya```. Finally I also have the option
for a user to send a random joke in the form of a text message using the Twilio API. As of right now my phone number is the only number that
can have messages sent to it as I am only using a trial account, but at if any time I wanted to upgrade my account then the script would work
perfect.

## Setbacks
1) The bot script I was working can no longer checkout due to a suspected update to the site's anti bot measures.
The script can still get the available sizes of a certain product and add a product to cart but no longer checkout.
I included the ```botRun.py``` script anyways in the repository but it has nothing to do with the current state of the web app.

2) When a user tries creating a new profile the information doesn't get posted to the database. This was a problem that I was stuck on for quite
some time and didn't end up figuring out the issue. To combat that I manually added profiles into the database myself.

3) On the Account page all user profiles show up instead of the specific profiles to the current user that is logged in. For this 
problem I had a pretty solid understanding of how to go about and prevent this but I was having all kinds of problems trying to get the 
current_user id which prevented me from solving this.

4) Lastly the 'Remember Me?' text that should be next to the radio button on the login page is on top of it instead. Tried a few things
to fix it and nothing seemed to change so I decided to not worry about it too much as it is only a very minor problem.

## Summary
Overall, I really enjoyed working on this. Being a developer who will soon be fresh in the industry I know that there is so much ahead for me
to learn and I enjoy being put in situations where I am required to get out of my comfort zone, try new techologies/frameworks/etc, and ultimately
grow. There were definitely many frustrating points in this project where I would get stuck and feel like I couldn't figure it out but then find a way
to solve my issue which would only motivate me further to keep grinding out this project. This experience has been very rewarding for me and I have
learned a great deal of knowledge. By doing this, I will now have a better grasp on web app development and I will be able to put forth that
knowledge when I start my semester long project in my Software Engineering course which will be a web app created for reporting potholes and creating a
ticket system for them so that towns all over WNY can track them better and hopefully fix the awful potholes sooner.
