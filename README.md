<p align="center">
  <img src="https://i.pinimg.com/originals/28/0f/f3/280ff34e4be0123c7eb383ad2d48958f.png" width="230" height="150"  alt="yellowstone-camping logo">
  <img src="https://raw.githubusercontent.com/juftin/resume/master/resume/web/favicon.png" width="150" height="150"  alt="juftin logo">
</p>

# yellowstone-camping

`yellowstone-camping` is a Campsite Reservation Cancellation Finder for Yellowstone National Park.
This simple Python application will continuously
check [Yellowstone's Campground Availability](https://secure.yellowstonenationalparklodges.com/booking/lodging)
API and let you know as soon as a reservation is available with a Push Notification on your Android
or iOS device. Don't stress about finding a campsite in that booked out campground,
let `yellowstone-camping` do the work for you.

## How to set up your campsite search

Make a file called `yellowstone-camping.env` and place it at the root of this repository, you can
use the [example.yellowstone-camping.env](example.yellowstone-camping.env) file as a template. Once
the `yellowstone-camping.env` file is ready, fill out your lodging details and Pushover credentials:

```shell
export BOOKING_DATE_START="2021-07-31" # YELLOWSTONE ARRIVAL DATE (YYYY-MM-DD)
export NUMBER_OF_GUESTS=2 # NUMBER OF PEOPLE IN THE CAMPING RESERVATION
export NUMBER_OF_NIGHTS=1 # NUMBER OF NIGHTS IN THE CAMPING RESERVATION
export POLLING_INTERVAL=600 # HOW OFTER TO CHECK FOR NEW RESERVATIONS (IN SECONDS)

export PUSHOVER_PUSH_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxx" # PUSHOVER API TOKEN
export PUSHOVER_PUSH_USER="xxxxxxxxxxxxxxxxxxxxxxxx" # PUSHOVER USER KEY
```

### Running with Docker

```shell
./scripts/check-yellowstone.sh
```

To run the reservation search in a Docker container you'll run
the [check-yellowstone.sh](scripts/check-yellowstone.sh) file, this creates a docker container
called `yellowstone-camping` that runs in the background. Once the scraper has found its first
booking it will exit (you can always run `docker logs -f yellowstone-camping` to check up on the
active logs, or `docker stop yellowstone-camping` to kill the container and stop searching).

### Running Locally with Python

Don't work with Docker? No problem. The docker image is based on Python `3.8.X`, but any version of
Python 3 you have locally should suffice. Source the `yellowstone-camping.env` file and run the
python script (this requires the `requests` package to be installed):

```shell
source yellowstone-camping.env && python scripts/find_availability.py
```

## How do I set up Pushover for Push Notifications to my phone?

Pushover is an neat service/app that allows you to easily send push notifications to your mobile
device. More details on how to set up Pushover can be found on
their [website](https://pushover.net/). **FYI**: Pushover is a paid service (a lifetime subscription
costs $5.00). However, if Pushover is not right for you then
the [source code](yellowstone_availability/check_yellowstone.py)
can be manually changed to use your preferred method of sending notifications. To bypass logging to
Pushover, just remove the variables, set them to empty, or leave them untouched; the script will
simply log `CRITICAL` events to the console when a campsite is available.

* * *

* * *

<br/>
<br/>

### *About this Project*

My partner and I are taking a trip this summer (July, 2021) from home in Colorado through
Wyoming to Glacier National Park. Like all national parks right now, the campsites in Glacier are a
hot commodity and tough to come by.

To help us get an advantage in finding a site we signed up for
[*Campnab*](https://campnab.com/), a service that lets you sign up for text notifications when
booked out campgrounds receive cancellations. Long story short, it's totally worth it and get's a
big recommendation from me. We found a 5 day cancellation and booked our first choice campground
within a couple weeks of signing up.

Later in our trip, we'll be going through Yellowstone and Grand Tetons National Park. Unfortunately,
Campnab doesn't (currently) work for most sites in Yellowstone, since they use a different booking
provider than the rest of the National Park System. Instead, I decided to play around with the
booking website and build my own integration with their API. It's built in Python, runs in a docker
container, and sends push notifications through via [Pushover](https://pushover.net/).

Feature Requests and Technical Feedback / Questions are best done though
the [Issues Page](https://github.com/juftin/yellowstone-camping/issues). Some basic command line
skills and an always-on computer are required to run this.

We're still waiting for our Yellowstone spot as of writing this and can't wait to get back there
this summer. I hope `yellowstone-camping` is useful for someone out there, good luck hunting for
your next spot!

<br/>
<br/>
<br/>

###### Cool stuff happens in Denver, CO [<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Flag_of_Denver%2C_Colorado.svg/800px-Flag_of_Denver%2C_Colorado.svg.png" width="25" alt="Denver">](https://denver-devs.slack.com/)