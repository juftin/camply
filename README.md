<p align="center">
  <img src="https://i.pinimg.com/originals/28/0f/f3/280ff34e4be0123c7eb383ad2d48958f.png" width="230" height="150"  alt="yellowstone-camping logo">
  <img src="https://raw.githubusercontent.com/juftin/resume/master/resume/web/favicon.png" width="150" height="150"  alt="juftin logo">
</p>

# yellowstone-camping

Camping Reservation Scraper for Yellowstone National Park. This simple Python application will
continuously
check [Yellowstone's Campground Availability](https://secure.yellowstonenationalparklodges.com/booking/lodging)
API and let you know as soon as a reservation is available with a Push Notification on your Android
or iOS device. Don't stress about finding a campsite in that booked out campground,
let `yellowstone-camping` do the work for you.

## How to set up your campsite search

Make a file called `yellowstone-camping.env` and place it at the root of this repository, you can
use the [example.yellowstone-camping.env](example.yellowstone-camping.env) file as a template. Once
the `yellowstone-camping.env` file is ready, fill out your lodging details and Pushover credentials:

```shell
export BOOKING_DATE_START="2021-07-16" # YELLOWSTONE ARRIVAL DATE
export NUMBER_OF_GUESTS=2 # NUMBER OF PEOPLE IN THE CAMPING RESERVATION
export NUMBER_OF_NIGHTS=1 # NUMBER OF NIGHTS IN THE CAMPING RESERVATION
export POLLING_INTERVAL=600 # HOW OFTER TO CHECK FOR NEW RESERVATIONS (IN SECONDS)

export PUSHOVER_PUSH_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxx" # PUSHOVER API TOKEN
export PUSHOVER_PUSH_USER="xxxxxxxxxxxxxxxxxxxxxxxx" # PUSHOVER USER KEY
```

### Running with Docker

```shell
./check-yellowstone.sh
```

To run the reservation search in a Docker container you'll run
the [check-yellowstone.sh](check-yellowstone.sh) file, this creates a docker container
called `yellowstone-camping` that runs in the background. Once the scraper has found its first
booking it will exit (you can always run `docker logs -f yellowstone-camping` to check up on the
active logs, or `docker stop yellowstone-camping` to kill the container and stop searching).

### Running Locally

Don't work with Docker? No problem. Souce the `yellowstone-camping.env` file and run the python
script (this requires the `requests` package to be installed):

```shell
source yellowstone-camping.env && python check_yellowstone.py
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