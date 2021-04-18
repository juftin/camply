# yellowstone-camping

<p align="center">
  <img src="https://raw.githubusercontent.com/juftin/resume/master/resume/web/favicon.png" width="200" height="200"  alt="juftin logo">
</p>

Camping Reservation Scraper for Yellowstone National Park

## How to set up your campsite search

Make a file called `.env`, you can use the [`example.env`](example.env) file for this. Once the .env
file is ready, fill out your lodging details and Pushover credentials.

That's it. Next, you'll run the [check_yellowstone.sh](check_yellowstone.sh) which creates a docker
image called `yellowstone-camping` that runs in the background. Once the script has found its first
booking it will exit in the background.

## How do I set up Pushover for Push Notifications to my phone?

Pushover is an awesome service that allows you to easily send push notifications to your mobile
device. A lifetime subscription costs $5.00 and it's totally worth it. More details on how to set up
Pushover can be found on their [website](https://pushover.net/).

* * *

* * *

<br/>
<br/>
<br/>

###### Cool stuff happens in Denver, CO [<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Flag_of_Denver%2C_Colorado.svg/800px-Flag_of_Denver%2C_Colorado.svg.png" width="25" alt="Denver">](https://denver-devs.slack.com/)