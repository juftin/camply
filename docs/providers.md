# Providers

camply works with a number of providers. A "provider" is an Online Booking
Service that lists campsite and recreation inventory.

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

## GoingToCamp

![](_static/goingtocamp_logo.png){: .center}

[GoingToCamp](https://goingtocamp.com/) provides campground listing and booking services for several US state and Canadian provincial parks.

To get a listing of GoingToCamp recreation areas

```
camply --provider goingtocamp recreation-areas
```

Unlike other camply providers, when using GoingToCamp you must restrict campground and campsites searches to a single recreation area. Since recreation areas may list every campground in a state or provincial park system, it feels natural to filter searches by recreation area when using GoingToCamp.
