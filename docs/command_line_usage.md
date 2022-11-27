# Command Line Usage

When installed, `camply`'s command line utility can be invoked with the command, `camply`. The CLI
tool accepts one of four sub-arguments: `campsites`, `recreation-areas`, `campgrounds`,
and `configure`.

```text
❯ camply --help

Usage: camply [OPTIONS] COMMAND [ARGS]...

  Welcome to camply, the campsite finder.

  Finding reservations at sold out campgrounds can be tough. That's where
  camply comes in. It searches the APIs of booking services like
  https://recreation.gov (which indexes thousands of campgrounds across the
  USA) to continuously check for cancellations and availabilities to pop up.
  Once a campsite becomes available, camply sends you a notification to book
  your spot!

  visit the camply documentation at https://github.com/juftin/camply

Options:
  --version             Show the version and exit.
  --provider TEXT       Camping Search Provider. Options available are
                        'Yellowstone' and 'RecreationDotGov'. Defaults to
                        'RecreationDotGov', not case-sensitive.
  --debug / --no-debug  Enable extra debugging output
  --help                Show this message and exit.

Commands:
  campgrounds       Search for Campgrounds (inside of Recreation Areas)...
  campsites         Find available Campsites using search criteria
  configure         Set up camply configuration file with an interactive...
  recreation-areas  Search for Recreation Areas and list them
```

## campsites

Search for a campsite within camply. Campsites are returned based on the search criteria provided.
Campsites contain properties like booking date, site type (tent, RV, cabin, etc), capacity, price,
and a link to make the booking. Required parameters include `--start-date`, `--end-date`,
`--rec-area` / `--campground` / `--campsite`. Constant searching functionality can be enabled with
`--continuous` and notifications via Email, Pushover, Pushbullet, and Telegram can be enabled using
`--notifications`.

### Arguments

* `--rec-area`: `RECREATION_AREA_ID`
    + Add Recreation Areas (comprised of campgrounds) by ID.
      [**_example_](#searching-for-a-campsite)
* `--campground`: `CAMPGROUND_ID`
    + Add individual Campgrounds by ID.
      [**_example_](#searching-for-a-campsite-by-campground-id)
* `--campsite`: `CAMPSITE_ID`
    + Add individual Campsites by ID.
      [**_example_](#searching-for-a-specific-campsite-by-id)
* `--start-date`: `START_DATE`
    + `YYYY-MM-DD`: Start of Search window. You will be arriving this day.
      [**_example_](#searching-for-a-campsite)
* `--end-date`: `END_DATE`
    + `YYYY-MM-DD`: End of Search window. You will be checking out this day..
      [**_example_](#searching-for-a-campsite)
* `--weekends`
    + Only search for weekend bookings (Fri/Sat nights).
      [**_example_](#look-for-weekend-campsite-availabilities)
* `--nights`
    + Search for campsite stays with consecutive nights. Defaults to 1 which returns all campsites
      found.
      [**_example_](#look-for-consecutive-nights-at-the-same-campsite)
* `--provider`: `PROVIDER`
    + Camping Search Provider. Options available are 'Yellowstone' and 'RecreationDotGov'. Defaults
      to 'RecreationDotGov', not case-sensitive.
      [**_example_](#look-for-a-campsite-inside-of-yellowstone)
* `--continuous`
    + Continuously check for a campsite to become available, and quit once at least one campsite is
      found.
      [**_example_](#continuously-searching-for-a-campsite)
* `--search-forever`
    + If `--continuous` is activated, this method continues to search after the first availability
      has been found. The one caveat is that it will never notify about the same identical campsite
      for the same booking date.
      [**_example_](#continue-looking-after-the-first-match-is-found)
* `--notifications`: `NOTIFICATIONS`
    + If `--continuous` is activated, types of notifications to receive. Options available
      are`email`, `pushover`, `pushbullet`, `telegram`, or `silent`. Defaults to `silent` - which just logs
      messages to console.
      [**_example_](#send-a-push-notification)
* `--equipment`
    + Search for campsites compatible with your camping equipment. This argument accepts two
      options, the equipment name and its length If you don't want to filter based on length provide
      a length of 0. Accepted equipment names include `Tent`, `RV`. `Trailer`, `Vehicle` and are
      not case-sensitive.
      [**_example_](#searching-for-a-campsite-that-fits-your-equipment)
* `--notify-first-try`
    + If `--continuous` is activated, whether to send all non-silent notifications if more than 5
      matching campsites are found on the first try. Defaults to false which only sends the first5.
      [**_example_](#continuously-searching-for-a-campsite)
* `--polling-interval`: `POLLING_INTERVAL`
    + If `--continuous` is activated, how often to wait in between checks (in minutes). Defaults to
      10, cannot be less than 5.
      [**_example_](#look-for-weekend-campsite-availabilities)
* `--yaml-config`
    + Rather than provide arguments to the command line utility, instead pass a file path to a YAML
      configuration file. See the documentation for more information on how to structure your
      configuration file.
      [**_example_](#using-a-yaml-configuration-file-to-search-for-campsites)

```commandline
camply campsites \
    --rec-area 2725 \
    --start-date 2023-07-10 \
    --end-date 2023-07-18
```

## recreation-areas

Search for Recreation Areas and their IDs. Recreation Areas are places like National Parks and
National Forests that can contain one or many campgrounds.

### Arguments

* `--search` `SEARCH`
    + Search for Campgrounds or Recreation Areas by search string.
* `--state` `STATE`
    + Filter by US state code.

```commandline
camply recreation-areas --search "Yosemite National Park"
```

**_see the [examples](#search-for-recreation-areas-by-query-string) for more informatio

## campgrounds

Search for Campgrounds and their IDs. Campgrounds are facilities inside of Recreation Areas that
contain campsites. Most 'campgrounds' are areas made up of multiple campsites, others are facilities
like fire towers or cabins that might only contain a single 'campsite' to book.

### Arguments

* `--search` `SEARCH`
    + Search for Campgrounds or Recreation Areas by search string.
* `--state` `STATE`
    + Filter by US state code.
* `--rec-area`: `RECREATION_AREA_ID`
    + Add Recreation Areas (comprised of campgrounds) by ID.
* `--campground`: `CAMPGROUND_ID`
    + Add individual Campgrounds by ID.

```commandline
camply campgrounds --search "Fire Tower Lookout" --state CA
```

**_see the [examples](#look-for-specific-campgrounds-by-query-string) for more information_

## configure

Set up `camply` configuration file with an interactive console

In order to send notifications through `camply` you must set up some authorization values. Whether
you need to set up [Pushover notifications](https://pushover.net)
, [PushBullet](https://www.pushbullet.com/#settings/account), [Telegram](https://core.telegram.org/bots),
or Email messages, everything can be done through the `configure` command. The end result is a file called
[`.camply`](examples/example.camply) in your home folder. See
the [Running in Docker](docker.md#running-in-docker) section to see how you can use environment variables
instead of a config file.

```commandline
camply configure
```

## Examples

Read through the examples below to get a better understanding of `camply`, its features, and the
functionality of the different arguments provided to the CLI.

### Searching for a Campsite

The below search looks for campsites inside of Recreation Area ID #2725 (Glacier National Park)
between 2023-07-10 and 2023-07-17. The search will be performed once and any results will be logged
to the console. camply searches for campsites inside of search windows in increments of one night.
`--start-date` and `--end-date` define the bounds of the search window, you will be leaving the day
after `--end-date`.

```commandline
camply campsites \
    --rec-area 2725 \
    --start-date 2023-07-10 \
    --end-date 2023-07-18
```

### Searching for a Campsite by Campground ID

The below search looks for across three campgrounds (all inside Glacier National Park)
between 2023-07-10 and 2023-07-17. Multiple Campgrounds (and Recreation Areas too) can be found by
supplying the arguments more than once.

```commandline
camply campsites \
    --campground 232493 \
    --campground 251869 \
    --campground 232492 \
    --start-date 2023-07-10 \
    --end-date 2023-07-18
```

### Searching for a Specific Campsite by ID

Sometimes you have a favorite campsite inside your favorite campground. To search for just a
specific campsite (and not just all campsites within a campground) you can give its ID to `camply`
with the `--campsite` argument. For example, site `R035` in Many Glacier Campground, MT is close to
a trailhead. Its URL
is [https://www.recreation.gov/camping/campsites/98363](https://www.recreation.gov/camping/campsites/98363)
, here we can see that it's ID is `98363`. You can search for one or many campsites by ID by
supplying the `--campsite` argument. You can provide the `--campsite` argument once or multiple
times to search for different campsites. Note, `--campsite` arguments override any `--rec-area`
or `--campground` parameters provided.

```commandline
camply campsites \
    --campsite 98363 \
    --start-date 2023-07-10 \
    --end-date 2023-07-18
```

### Continuously Searching for A Campsite

Sometimes you want to look for campgrounds until an eventual match is found. The below snippet will
search for matching campsites until it finds a match. It also sends a notification via `pushover`
once matches are found. Alternate notification methods are `email`, `pushbullet`, `telegram`, and `silent` (
default).

__Important Note__: When `camply` is told to run `--continuous` with non-silent notifications set up
and it finds more than 5 matching campsites on the first try, it will only send notifications for
the first 5 campsites. This is to prevent thousands of campsites flooding your notifications. It's
always encouraged to perform an initial online search before setting up a `camply` search. To bypass
this behavior and send all notifications, pass the `--notify-first-try` argument.

```commandline
camply campsites \
    --rec-area 2725 \
    --start-date 2023-07-12 \
    --end-date 2023-07-13 \
    --continuous \
    --notifications pushover \
    --notify-first-try
```

### Continue Looking After The First Match Is Found

Sometimes you want to search for all possible matches up until your arrival date. No problem. Add
the `--search-forever` and `camply` won't stop sending notifications after the first match is found.
One important note, `camply` will save and store all previous notifications when `--search-forever`
is enabled, so it won't notify you about the exact same campsite availability twice. This can be
problematic when certain campsites become available more than once.

```commandline
camply campsites \
    --rec-area 2725 \
    --start-date 2023-07-01 \
    --end-date 2023-08-01 \
    --continuous \
    --notifications pushover \
    --search-forever
```

### Send a Push Notification

camply supports notifications via `Pushbullet`, `Pushover`, `Telegram`, and `Email`. Pushbullet is a great
option because it's
a [free and easy service to sign up for](https://www.pushbullet.com/#settings/account)
and it supports notifications across different devices and operating systems. Similar to `Pushover`,
`Pushbullet` requires that you create an account and an API token, and share that token with camply
through a [configuration file](examples/example.camply) (via the `camply configure`
command) or though environment variables (`PUSHBULLET_API_TOKEN`).

```commandline
camply campsites \
    --rec-area 2991 \
    --start-date 2023-09-10 \
    --end-date 2023-09-21 \
    --continuous \
    --notifications pushbullet
```

### Send a Text Message

If you want to sign up for a [Twilio](https://www.twilio.com/try-twilio) account, camply also supports
sending text messages via SMS. You can set up your Twilio configuration via `camply configure`. You will need
to set the following config values for Twilio: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`,
`TWILIO_SOURCE_NUMBER`, `TWILIO_DEST_NUMBERS`.

Sending text messages via Twilio also requires the `twilio` extras:

```
pip install camply[twilio]
```

```commandline
camply campsites \
    --rec-area 2991 \
    --start-date 2023-09-10 \
    --end-date 2023-09-21 \
    --continuous \
    --notifications twilio
```

### Send a Notification to Different Services

camply supports notifications from different providers. To send notifications to multiple providers
you can pass the --notifications parameter multiple times. YAML config entries also
accept an array as well.

```commandline
camply campsites \
    --rec-area 2991 \
    --start-date 2023-09-10 \
    --end-date 2023-09-21 \
    --continuous \
    --notifications email \
    --notifications pushover
```

### Look for Weekend Campsite Availabilities

This below search looks across larger periods of time, but only if a campground is available to book
on a Friday or Saturday night (`--weekends`). It also uses the `--polling-interval` argument which
checks every 5 minutes instead of the default 10 minutes.

```commandline
camply campsites \
    --rec-area 2991 \
    --start-date 2023-05-01 \
    --end-date 2023-08-01 \
    --weekends \
    --continuous \
    --notifications email \
    --polling-interval 5
```

### Look for Consecutive Nights at the Same Campsite

A lot of times you need to search for consecutive nights at the same campsite. By default, any and
all campsites with a single nights booking are returned by camply. To search for campsites with
consecutive night stays, pass the `--nights` argument.

Note, the `--nights` argument handles issues with improper search parameters. For example, if you
set the `--weekends` parameter the maximum number of consecutive nights possible is 2. If you supply
more than this your `--nights` parameter will be overwritten to 2.

```commandline
camply campsites \
    --rec-area 2991 \
    --start-date 2023-05-01 \
    --end-date 2023-08-01 \
    --nights 4
```

### Look for a Campsite Inside of Yellowstone

Yellowstone doesn't use https://recreation.gov to manage its campgrounds, instead it uses its own
proprietary system. In order to search the Yellowstone API for campsites, make sure to pass
the `--provider "yellowstone"` argument. This flag disables `--rec-area` argument.

To learn more about using `camply` to find campsites at Yellowstone, check out
this [discussion](https://github.com/juftin/camply/discussions/15#discussioncomment-783657).

```commandline
camply campsites \
    --provider yellowstone \
    --start-date 2023-07-09 \
    --end-date 2023-07-17 \
    --continuous
```

### Look for a Campsite Across Multiple Recreation areas

You don't have to confine your search to a single Recreation or Campground ID. Adding multiple
arguments to the command line will search across multiple IDs. Keep in mind that any `--campground`
arguments will overwrite all `--rec-area` arguments.

```commandline
camply campsites \
    --rec-area 2991 \
    --rec-area 1074 \
    --start-date 2023-07-09 \
    --end-date 2023-07-17 \
    --nights 5
```

### Using a YAML Configuration file to search for campsites

Sometimes, using a YAML configuration file is easier to manage all of your search options. See the
below [YAML example file](examples/example_search.yaml) and corresponding camply command:

```yaml
provider: RecreationDotGov  # RecreationDotGov IF NOT PROVIDED
recreation_area: # (LIST OR SINGLE ENTRY)
  - 2991  # Yosemite National Park, CA (All Campgrounds)
  - 1074  # Sierra National Forest, CA (All Campgrounds)
campgrounds: null  # ENTIRE FIELD CAN BE OMITTED IF NOT USED - (LIST OR SINGLE ENTRY)
campsites: null   # OVERRIDES CAMPGROUNDS / RECREATION AREA - (LIST OR SINGLE ENTRY)
start_date: 2023-09-12  # YYYY-MM-DD
end_date: 2023-09-13  # YYYY-MM-DD
weekends: false  # FALSE BY DEFAULT
nights: 1  # 1 BY DEFAULT
continuous: true  # DEFAULTS TO TRUE
polling_interval: 5  # DEFAULTS TO 10 , CAN'T BE LESS THAN 5
notifications: email  # (silent, email, pushover, pushbullet, and telegram), DEFAULTS TO `silent`
search_forever: true  # FALSE BY DEFAULT
notify_first_try: false  # FALSE BY DEFAULT
equipment: null # Array of Equipment Search Lists - DEFAULTS TO `null`
offline_search: false    # FALSE BY DEFAULT
offline_search_path: camply_campsites.json # Defaults to `camply_campsites.json`
```

```commandline
camply campsites --yaml-config example_search.yaml
```

### Searching for a Campsite That Fits Your Equipment

Camply can help you filter campsites to fit your specific equipment, like a Trailer or an RV.
Most likely, you care that the campsite fits the length of your RV so you can specify that as well.
To search for specific equipment and its length provide the `--equipment` option with two arguments,
the equipment name and the equipment length. If you don't want to filter based on length provide a
length of zero. If you provide multiple `--equipment` options, sites matching any of your search
equipment will be returned.

Current supported equipment names are `Vehicle`, `Tent`, `RV`, and `Trailer`. Be careful when
filtering on `Tents` and `Vehicle` length, sometimes Recreation.gov doesn't provide that information,
it is safer to set length to 0.

```commandline
camply campsites \
    --rec-area 2991 \
    --start-date 2023-07-09 \
    --end-date 2023-07-17 \
    --nights 5 \
    --equipment RV 25
```

Here's what the above search would look like on a YAML Config:

```yaml
recreation_area:
  - 2991
start_date: 2023-07-09
end_date: 2023-07-17
nights: 5
equipment:
  - [ RV, 25 ]
```

Finally, here's a search that accommodates trailers of all lengths:

```commandline
camply campsites \
    --rec-area 2991 \
    --start-date 2023-07-09 \
    --end-date 2023-07-17 \
    --nights 5 \
    --equipment Trailer 0
```

### Saving the Results of a Search

In some cases, you might want to save all the campsites found during one
search and load them into a new search, so you don't receive duplicate notifications.
This can be achieved by passing the `--offline-search` flag. By default, camply will save
the results in a file called `camply_campsites.json`.

Optionally, you can also path the `--offline-search-path` flag to specify a certain file
path to save the results as. When a file path with a `.json` extension is passed
camply will export the results as a JSON file. When the `.pkl` or `.pickle` extension is
used, camply will use a serialized Pickle file.

```commandline
camply \
  campsites \
  --campground 232064 \
  --start-date 2023-09-01 \
  --end-date 2023-10-01 \
  --continuous \
  --offline-search
```

```commandline
camply \
  campsites \
  --campground 232064 \
  --start-date 2023-09-01 \
  --end-date 2023-10-01 \
  --continuous \
  --offline-search \
  --offline-search-path campsites.pkl
```

### Search for Recreation Areas by Query String

Just need to find what your local Recreation Area ID number is? This simple command allows you to
search and list recreation areas. It accepts `--search` and `--state` arguments.

```commandline
camply recreation-areas --search "Yosemite National Park"
```

### Look for Specific Campgrounds Within a Recreation Area

Need to get even more specific and search for a particular campground? This search lists campgrounds
attached to a recreation area id `--rec-area`. It also accepts `--search` and `--state`
arguments.

```commandline
camply campgrounds --rec-area 2991
```

### Look for Specific Campgrounds by Query String

The below search looks for Fire Lookout Towers to stay in inside of California.

```commandline
camply campgrounds --search "Fire Tower Lookout" --state CA
```
