<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href=">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Small and Sustainable</h3>



<!-- ABOUT THE PROJECT -->
## About The Project

### Inspiration
We were inspired by Amazon, which is popular because of its convenience in finding products and its large catalogue, but is notoriously unethical in its business practices. We wanted to create an application that was convenient but ethical.

### What it does
Search Sustainable is a web application that helps users find everyday products from sustainable and ethical sources. The goal of this app is a helpful tool that directs consumers to better purchasing options.
A list of commonly used resources that I find helpful are listed in the acknowledgements.

### Process
To view one of our first prototypes click here: https://search-sustainable.herokuapp.com/ . Our app has evolved since then, and we will are excited to show off these new features at the demo!

<!-- AUTHORS-->
## Authors

* Hanieka Balint
* Eoin Daly
* Mia Kotalik
* Ethan Rush


### Built With

Our app is a Python Flask app that uses the Bootstrap framework and Jinja templating. The database is Google Firebase, which is a cloud NoSQL database. The Python packages Selenium, and LXML were used for webcrawling.
* [Bootstrap](https://getbootstrap.com)
* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Firebase](https://firebase.google.com/)
* [Selenium](https://pypi.org/project/selenium/)
* [LXML](https://lxml.de/)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* bash
  ```sh
  pip install -r requirements.txt
  ```
Python 3.8.2

### Installation

1. Clone the repo
   ```bash
   $ git clone https://github.com/mia-ktlk/hbp2021
   $ cd hbp2021
   ```
3. Export Flask environment variable
    ```bash
    $ export FLASK_APP=sustainable/sustainable.py
    ```
    or install python-dotenv
    ```bash
    $ pip install python dot-env
    $ echo "FLASK_APP=sustainable/sustainable.py" > .flaskenv
    ```
4. Run the app
    ```bash
    $ flask run
    ```

#### Firebase

This project makes use of firebase for its storage needs, and with a name like that we think you should as well. At our level of use it's free and once you get the hang of it fairly easy to use. If you decide to follow in our footsteps, you can find their website here: (https://firebase.google.com/). Make your account, create a realtime database, and copy the config information they give you and you're on your way to glory.
<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.


### Search

  Right in the middle of the websites homepage, you'll see a magnificent search bar. It comes loaded with all the features: text entry, a drop down menu for sorting (with 3 fantastic options), and even a button - Google wishes they had our stuff. To use this search, simply type the name of an item you'd want to buy, select what order you want the results displayed, and smash that ~~Like~~ search button. With the excellent work of your button pushing skills, you should be reaping the combined rewards of keyword selection and our advanced web crawlers. 

  #### Report

   Not impressed with one of the results? Smack that report button and get ready to let the admins have it (constructively of course). Once pressed, the button will bring you to a report form where you can fill out the multitude of reasons this particular item wasn't to your taste. Previous user examples include: 'its too expensive', 'this item isnt real', 'i searched for meat and got a statue of a rooster.' It's an open box, the page is yours (of course, stay on topic if you have any interest in getting it resolved).

  #### Suggestion

   For those of you with a less spiteful spirit, there's another way to help the admins of your local site: the suggestion button. Found at the bottom of the results page, this button will allow you to send the admins the name, description, and url of an item you'd wish to see on the store. But remember kids, this website is about sustainable goods, don't go spamming the admins to add the newest edition of Nintendos Yugi Monsters, its simply not what the site is for.


### Admin powers

So you want to ~~steal our idea~~ run your own version of the site? Lucky for you, we've prepared all the admin cases. I hope you read our prior sections about the report and suggestion features, because nothing beats spam like a dismiss button.

#### Logging In

  Here comes the hardest part, finding the *secret* log in page. It's a difficult task but I believe in each and every one of you. To get to the log in page, take the url (or localhost if you're offline) and add the following characters IN ORDER: */* *l*  *o*   *g*   *i*   *n*. The clever folks out there may notice that this looks a lot like "/login", but that's probably just a coincidence. 

  You difficult journey is nearly at an end, all you must do from here is remember you firebase username and password, and enter them in the correct places (always the hardest part for me). If successful, you'll be welcomed to a place of all power and glory: the admin dashboard.

##### Forgot your password?

  It happens to everyone, *but some more than others.* If you've been the victim of self induced amnesia, fear not we thought of that too. On the log in page you'll see the solution to all your problems: *Forgot Password?* Click this, input the email to your firebase account, and the angels of forgiveness will grant you with a password resets link. Forgot your email password? Sorry to hear that, moving on!


#### Dealing With Reports

  Remeber all those *hilarious* reports you've written to admins in your time? Well, it's time to be on the receiving end, get ready for spam. But don't worry, we've got your back. On your beautiful new admin dashboard you'll see list of messages for you and your team. These messages are made up of 2 types of responses: reports and suggestions. Reports (what we're talking about right now, stay focused) will have a delete entry and a dismiss option. 99% of the time you'll be using the dismiss button. This takes that report, smashes it into a ball, and throws it in the garbage can for you. **Delete Entry** on the other hand does exactly as it sounds. If, for once, a user has given a helpful report, this button will allow you to take the offending database entry and burn it in the fire of your rage. 

#### Dealing with Suggestions

  On the other side, we have suggestions. Just like the reports, you will be ignoring almost all of them. Luckily, this also contains a dismiss button that does exactly as it does with reports. The new button on the block is the Add to Database button. This will bring you straight to the source (firebase) for you to add with loveb (aka you gotta do it manually).



<!-- CONTACT -->
## Contact

Mia - [@miakotalik](https://twitter.com/miakotalik?lang=en)

Project Link: [https://github.com/mia-ktlk/hbp2021.git](https://github.com/mia-ktlk/hbp2021.git)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [ReadME Template](https://github.com/othneildrew/Best-README-Template)
* [Font Awesome](https://fontawesome.com)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/miakotalik/
[product-screenshot]: images/screenshot.png
