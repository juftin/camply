# Providers

camply works with a number of providers. A "provider" is an Online Booking
Service that lists camping and recreation inventory.

## Recreation.gov

![](_static/recreation_dot_gov_logo.png){: .center}

[Recreation.gov](https://recreation.gov) is (so far) the largest and most widely supported
provider. This provider spans over thousands of campgrounds across the USA including most of our National
parks.

You can find the best documentation for searching for campsites over at the main documentation
page: [Command Line Usage](command_line_usage.md#Command-Line-Usage)

```commandline
camply campgrounds --provider RecreationDotGov --state CA --search "Fire Towers"
```

## Yellowstone

![](_static/yellowstone_logo.png){: .center}

Yellowstone is one of the few National Parks that uses a Campsite Booking provider other
than [Recreation.gov](#recreationgov). A number of the campgrounds in Yellowstone can be
booked through [YellowstoneNationalParkLodges.com](https://www.yellowstonenationalparklodges.com/stay/camping/).
Read more about using camply to search this provider on
the [documentation](command_line_usage.md#look-for-a-campsite-inside-of-yellowstone).

```commandline
camply --provider Yellowstone campgrounds
```

The Yellowstone Provider currently supports the following Campgrounds:

- Bridge Bay Campground (YLYB:RV)
- Canyon Campground (YLYC:RV)
- Fishing Bridge RV Park (YLYF:RV)
- Grant Campground (YLYG:RV)
- Madison Campground (YLYM:RV)

## GoingToCamp

![](_static/goingtocamp_logo.png){: .center}

[GoingToCamp](https://goingtocamp.com/) provides campground listing and booking services for several US state and
Canadian provincial parks.

To get a listing of GoingToCamp recreation areas

```
camply --provider goingtocamp recreation-areas
```

Unlike other camply providers, when using GoingToCamp you must restrict campground and campsites searches to a single
recreation area. Since recreation areas may list every campground in a state or provincial park system, it feels natural
to filter searches by recreation area when using GoingToCamp.

The GoingToCamp Provider currently contains the following Recreation Areas:

- Hamilton, Ontario, CA (#6)
- Long Point Region, Ontario, CA (#1)
- Maitland Valley, Ontario, CA (#7)
- Oroville Park, Washington, USA (#8)
- Saugreen Valley, Ontario, CA (#9)
- St. Clair Region, Ontario, CA (#2)
- Tacoma Power Parks, Washington, USA (#10)
- Washington State Parks, Washington, USA (#4)
- Wisconsin State Parks, Wisconsin, USA (#11)
- Yukon (Backcountry), Yukon, CA (#5)

Check out the following documentation examples for more details on searching GoingToCamp recreation
areas:

- [Look for a Campsite from GoingToCamp](command_line_usage.md#look-for-a-campsite-from-goingtocamp)
- [Searching GoingToCamp Using Equipment](command_line_usage.md#searching-goingtocamp-using-equipment)

## Recreation.gov Tickets, Tours, & Timed-Entry

![](_static/recreation_dot_gov_logo.png){: .center}

Apart from reservations for campsites, Recreation.gov also supports reserving tickets & tours
- there are thousands of tickets and tours options available around the USA.

[Search for Tickets, Tours, & Timed-Entry Online](https://www.recreation.gov/search?inventory_type=tours)

### Tours & Tickets

```commandline
camply campgrounds --provider RecreationDotGovTicket --state HI
```

### Timed Entry

```commandline
camply campgrounds --provider RecreationDotGovTimedEntry --state OR
```

- [Searching for Tickets and Timed Entries](command_line_usage.md#searching-for-tickets-and-timed-entries)
    - [Tickets + Tours](command_line_usage.md#tickets-tours)
    - [Timed Entry](command_line_usage.md#timed-entry)
    - [Using the Daily Providers](command_line_usage.md#using-the-daily-providers)
