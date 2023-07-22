<div align="center">
<a href="https://github.com/juftin/camply">
  <img src="https://raw.githubusercontent.com/juftin/camply/main/docs/_static/camply.svg"
    width="400" height="400" alt="camply">
</a>
</div>

**`camply`**, the campsite finder ⛺️, is a tool to help you book a campsite online. Finding
reservations at sold out campgrounds can be tough. That's where camply comes in. It searches
thousands of campgrounds across the ~~USA~~ world via the APIs of booking services like
[recreation.gov](https://recreation.gov). It continuously checks for cancellations and
availabilities to pop up - once a campsite becomes available, camply sends you a notification
to book your spot!

---

---

[![PyPI](https://img.shields.io/pypi/v/camply?color=blue&label=⛺️camply)](https://github.com/juftin/camply)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/camply)](https://pypi.python.org/pypi/camply/)
[![Docker Image Version](https://img.shields.io/docker/v/juftin/camply?color=blue&label=docker&logo=docker)](https://hub.docker.com/r/juftin/camply)
[![Testing Status](https://github.com/juftin/camply/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/juftin/camply/actions/workflows/tests.yaml)
[![GitHub License](https://img.shields.io/github/license/juftin/camply?color=blue&label=License)](https://github.com/juftin/camply/blob/main/LICENSE)
[![Black Codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)]()
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-lightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![Gitmoji](https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg)](https://gitmoji.dev)
[![Discord Chat](https://img.shields.io/static/v1?label=chat&message=discord&color=blue&logo=discord)](https://discord.gg/qZDr78kKvB)

## [Check Out The Docs](https://juftin.com/camply/)

## Installing

Install camply via `pip` or [pipx](https://github.com/pypa/pipx):

```commandline
pipx install camply
```

## Usage

Search for a specific recreation area (recreation areas contain campgrounds):

```commandline
camply recreation-areas --search "Glacier National Park"
```

Search for campgrounds (campgrounds contain campsites):

```commandline
camply campgrounds --search "Fire Lookout Towers" --state CA
```

Search for available campsites, get a notification whenever one becomes
available, and continue searching after the first one is found. The below command
is using `silent` notifications as an example but camply also supports `Email`,
`Slack`, `Twilio` (SMS), `Pushover`, `Pushbullet`, `Ntfy`, `Apprise`, and `Telegram`.

```commandline
camply campsites \
    --rec-area 2725 \
    --start-date 2023-07-10 \
    --end-date 2023-07-18 \
    --notifications silent \
    --search-forever
```

## Providers

camply works with a number of providers. A "provider" is an online booking
service that lists camping and recreation inventory.

-   **`RecreationDotGov`**: Searches on [Recreation.gov](https://recreation.gov) for Campsites (default provider)
-   **`Yellowstone`**: Searches on [YellowstoneNationalParkLodges.com](https://yellowstonenationalparklodges.com) for
    Campsites
-   **`ReserveCalifornia`**: Searches on [ReserveCalifornia.com](https://reservecalifornia.com) for Campsites (California
    State Parks)
-   **`GoingToCamp`**: Searches on [GoingToCamp](https://goingtocamp.com) for Campsites
    -   Parks Canada - Canada National Parks - [reservation.pc.gc.ca](https://reservation.pc.gc.ca/)
    -   Washington State Parks - Washington, USA - [washington.goingtocamp.com](https://washington.goingtocamp.com)
    -   Wisconsin State Parks - Wisconsin, USA - [wisconsin.goingtocamp.com](https://wisconsin.goingtocamp.com)
    -   Michigan State Parks - Michigan, USA - [midnrreservations.com](https://midnrreservations.com/)
    -   BC Parks - British Columbia, CA - [camping.bcparks.ca](https://camping.bcparks.ca)
    -   Maryland State Parks - Maryland, USA - [parkreservations.maryland.gov](https://parkreservations.maryland.gov)
    -   Nova Scotia Parks - Nova Scotia, CA - [novascotia.goingtocamp.com](https://novascotia.goingtocamp.com)
    -   Manitoba Parks - Manitoba, CA - [manitoba.goingtocamp.com](https://manitoba.goingtocamp.com)
    -   New Brunswick Provincial Parks - New Brunswick, CA - [parcsnbparks.info](https://www.parcsnbparks.info/)
    -   Newfoundland & Labrador Provincial Parks - Newfoundland and Labrador, CA - [nlcamping.ca](https://nlcamping.ca)
    -   Long Point Region - Ontario, CA - [longpoint.goingtocamp.com](https://longpoint.goingtocamp.com)
    -   Algonquin Highlands - Ontario, CA - [ahtrails.ca](https://ahtrails.ca)
    -   Maitland Valley, Ontario, CA - [maitlandvalley.goingtocamp.com](https://maitlandvalley.goingtocamp.com)
    -   Saugeen Valley - Ontario, CA - [saugeen.goingtocamp.com](https://saugeen.goingtocamp.com)
    -   St. Clair Region - Ontario, CA - [stclair.goingtocamp.com](https://stclair.goingtocamp.com)
    -   Tacoma Power Parks, Washington, USA - [tacomapower.goingtocamp.com](https://tacomapower.goingtocamp.com)
    -   Gatineau Park - Ontario-Quebec, CA - [reservations.ncc-ccn.gc.ca](https://reservations.ncc-ccn.gc.ca)
-   **`AlabamaStateParks`**: Searches on [ReserveAlaPark.com](https://reservealapark.com) for Campsites
-   **`ArizonaStateParks`**: Searches on [AZStateParks.com](https://azstateparks.com) for Campsites
-   **`FloridaStateParks`**: Searches on [FloridaStateParks.org](https://www.reserve.floridastateparks.org) for Campsites
-   **`MinnesotaStateParks`**: Searches on [ReserveMN.usedirect.com](https://reservemn.usedirect.com) for Campsites
-   **`MissouriStateParks`**: Searches on [icampmo1.usedirect.com](https://icampmo1.usedirect.com) for Campsites
-   **`OhioStateParks`**: Searches on [ReserveOhio.com](https://reserveohio.com) for Campsites
-   **`VirginiaStateParks`**: Searches on [ReserveVAParks.com](https://reservevaparks.com) for Campsites
-   **`NorthernTerritory`**: Searches the [Australian Northern Territory](https://parkbookings.nt.gov.au) for Campsites
-   **`FairfaxCountyParks`**: Searches on [fairfax.usedirect.com](https://fairfax.usedirect.com) for Campsites (Virginia)
-   **`MaricopaCountyParks`**: Searches on [MaricopaCountyParks.org](https://maricopacountyparks.org) for Campsites (Arizona)
-   **`OregonMetro`**: Searches on [OregonMetro.gov](https://oregonmetro.gov) for Campsites (Portland Metro)
-   **`RecreationDotGovTicket`**: Searches on [Recreation.gov](https://recreation.gov) for Tickets and Tours
-   **`RecreationDotGovTimedEntry`**: Searches on [Recreation.gov](https://recreation.gov) for Timed Entries

Run **`camply providers`** to list current providers and visit the [Providers](https://juftin.com/camply/providers/)
section in the docs to learn more.

## Documentation

Head over to the [camply documentation](https://juftin.com/camply/) to see what you can do!

```console
❯ camply --help

 Usage: camply [OPTIONS] COMMAND [ARGS]...

 Welcome to camply, the campsite finder.
 Finding reservations at sold out campgrounds can be tough. That's where camply comes in. It searches the
 APIs of booking services like https://recreation.gov (which indexes thousands of campgrounds across the
 USA) to continuously check for cancellations and availabilities to pop up. Once a campsite becomes
 available, camply sends you a notification to book your spot!


 visit the camply documentation at https://juftin.com/camply

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                        │
│  --debug/--no-debug             Enable extra debugging output                                          │
│  --provider              TEXT   Camping Search Provider. Defaults to 'RecreationDotGov'                │
│  --version                      Show the version and exit.                                             │
│  --help                         Show this message and exit.                                            │
│                                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                        │
│  campgrounds              Search for Campgrounds (inside of Recreation Areas) and list them            │
│  campsites                Find Available Campsites with Custom Search Criteria                         │
│  configure                Set up camply configuration file with an interactive console                 │
│  equipment-types          Get a list of supported equipment                                            │
│  list-campsites           List campsite IDs for a given campground or recreation area                  │
│  providers                List the different camply providers                                          │
│  recreation-areas         Search for Recreation Areas and list them                                    │
│  test-notifications       Test your notification provider setup                                        │
│  tui                      Open Textual TUI.                                                            │
│                                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Contributing

Camply doesn't support your favorite campsite booking provider yet? Consider
[contributing](https://juftin.com/camply/contributing/) 😉.

<br/>

Recreation data provided by [**Recreation.gov**](https://ridb.recreation.gov/)

---

---

<br/>

[<p align="center" ><img src="https://raw.githubusercontent.com/juftin/juftin/main/static/juftin.png" width="120" height="120"  alt="juftin logo"> </p>](https://github.com/juftin)
