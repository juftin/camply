<p align="center">
  <img src="https://raw.githubusercontent.com/juftin/resume/master/resume/web/favicon.png" width="150" height="150"  alt="juftin logo">
  <img src="https://i.pinimg.com/originals/28/0f/f3/280ff34e4be0123c7eb383ad2d48958f.png" width="230" height="150"  alt="juftin logo">
</p>

# yellowstone-camping

Camping Reservation Scraper for Yellowstone National Park. This simple Python application will
continuously check Yellowstone's Campground Availability API and let you know as soon as a
reservation is available with a Push Notification on your Android or iOS device. Don't stress about
finding a campsite in that booked out campground, let `yellowstone-camping` do the work for you.

## How to set up your campsite search

Make a file called `.env`, you can use the [`example.env`](example.env) file for this. Once the .env
file is ready, fill out your lodging details and Pushover credentials.

That's it. Next, you'll run the [check_yellowstone.sh](check_yellowstone.sh) which creates a docker
image called `yellowstone-camping` that runs in the background. Once the script has found its first
booking it will exit in the background (you can always run `docker logs -f yellowstone-camping` to
check up on the logs, or `docker stop yellowstone-camping` to stop searching).

```shell
./check_yellowstone.sh
```

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