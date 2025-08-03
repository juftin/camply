import {
  ExternalLink,
  MapPin,
  Users,
  Calendar,
  Star,
  Caravan,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

interface Provider {
  name: string;
  description: string;
  website: string;
  logo?: string;
  features: string[];
  campgroundCount?: number;
  coverage: string[];
  popular?: boolean;
}

const providers: Provider[] = [
  {
    name: "Recreation.gov",
    description:
      "The official federal recreation portal for reserving campsites at National Parks, National Forests, and other federal recreation areas.",
    website: "https://recreation.gov",
    features: [
      "National Parks",
      "National Forests",
      "National Wildlife Refuges",
      "Campsites & Tickets",
      "Timed Entries",
    ],
    campgroundCount: 3000,
    coverage: ["Federal Lands", "National Parks"],
    popular: true,
  },
  {
    name: "Reserve California",
    description:
      "Official reservation system for California State Parks offering diverse camping from beaches to deserts to mountains.",
    website: "https://reservecalifornia.com",
    features: [
      "Beach Camping",
      "Desert Camping",
      "Mountain Camping",
      "Historic Sites",
    ],
    campgroundCount: 280,
    coverage: ["California State Parks"],
    popular: true,
  },
  {
    name: "Yellowstone Lodges",
    description:
      "Official booking system for Yellowstone National Park's campgrounds and lodging facilities.",
    website: "https://yellowstonenationalparklodges.com",
    features: [
      "Yellowstone Campsites",
      "Lodge Reservations",
      "RV Sites",
      "Backcountry Permits",
    ],
    campgroundCount: 12,
    coverage: ["Yellowstone National Park"],
    popular: true,
  },
  {
    name: "Alabama State Parks",
    description:
      "Reservation system for Alabama's state parks and outdoor recreation areas.",
    website: "https://reservealpark.com",
    features: [
      "State Park Camping",
      "Cabins",
      "Group Facilities",
      "Beach Access",
    ],
    coverage: ["Alabama State Parks"],
  },
  {
    name: "Arizona State Parks",
    description:
      "Official booking platform for Arizona's desert state parks and recreation areas.",
    website: "https://azstateparks.com",
    features: [
      "Desert Camping",
      "Hiking Trails",
      "Lake Recreation",
      "Historic Sites",
    ],
    coverage: ["Arizona State Parks"],
  },
  {
    name: "Florida State Parks",
    description:
      "Reservation system for Florida's diverse state parks from beaches to springs to wetlands.",
    website: "https://floridastateparks.org",
    features: [
      "Beach Camping",
      "Spring Sites",
      "Wetland Parks",
      "Cabins & Lodges",
    ],
    coverage: ["Florida State Parks"],
  },
  {
    name: "Minnesota State Parks",
    description:
      "Booking platform for Minnesota's state parks and recreation areas with lakes and forests.",
    website: "https://reservemn.usedirect.com",
    features: ["Lake Camping", "Forest Sites", "Cabins", "Group Camps"],
    coverage: ["Minnesota State Parks"],
  },
  {
    name: "Missouri State Parks",
    description:
      "Reservation system for Missouri's state parks and historic sites.",
    website: "https://icampmo1.usedirect.com",
    features: ["Ozark Camping", "Lake Sites", "Historic Parks", "Cabins"],
    coverage: ["Missouri State Parks"],
  },
  {
    name: "Ohio State Parks",
    description:
      "Official booking system for Ohio's state parks and recreation facilities.",
    website: "https://reserveohio.com",
    features: [
      "Lake Camping",
      "Forest Sites",
      "Cabins & Lodges",
      "Group Facilities",
    ],
    coverage: ["Ohio State Parks"],
  },
  {
    name: "Virginia State Parks",
    description:
      "Reservation platform for Virginia's state parks from mountains to coast.",
    website: "https://reservevaparks.com",
    features: ["Mountain Camping", "Coastal Sites", "Historic Parks", "Cabins"],
    coverage: ["Virginia State Parks"],
  },
  {
    name: "Fairfax County Parks",
    description:
      "Local parks and recreation booking system for Fairfax County, Virginia.",
    website: "https://fairfaxcounty.gov/parks",
    features: [
      "Local Parks",
      "Recreation Centers",
      "Group Sites",
      "Special Events",
    ],
    coverage: ["Fairfax County, VA"],
  },
  {
    name: "Maricopa County Parks",
    description:
      "Arizona county parks system offering desert recreation and camping opportunities.",
    website: "https://maricopa.gov/parks",
    features: [
      "Desert Camping",
      "Regional Parks",
      "Hiking Trails",
      "Group Areas",
    ],
    coverage: ["Maricopa County, AZ"],
  },
  {
    name: "Oregon Metro Parks",
    description:
      "Regional parks and natural areas in the Portland metropolitan region.",
    website: "https://oregonmetro.gov/parks",
    features: [
      "Regional Parks",
      "Natural Areas",
      "Trail Access",
      "Environmental Programs",
    ],
    coverage: ["Portland Metro Area"],
  },
  {
    name: "Northern Territory Parks",
    description:
      "Australian park booking system for Northern Territory's unique landscapes and wildlife areas.",
    website: "https://nt.gov.au/leisure/parks-reserves",
    features: [
      "Outback Camping",
      "Wildlife Parks",
      "Cultural Sites",
      "Adventure Tourism",
    ],
    coverage: ["Northern Territory, Australia"],
  },
];

export function Providers() {
  return (
    <div className="container mx-auto py-12 px-4 max-w-6xl">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <div className="mb-6">
          <Caravan className="h-16 w-16 text-primary mx-auto mb-4" />
        </div>
        <h1 className="text-5xl font-bold mb-6">
          Supported <span className="text-primary">Providers</span>
        </h1>
        <p className="text-xl text-muted-foreground mb-8 max-w-4xl mx-auto leading-relaxed">
          camply monitors availability across major booking platforms and
          recreation systems. Find campsites from thousands of campgrounds
          nationwide.
        </p>

        <div className="flex flex-wrap justify-center gap-6 text-sm text-muted-foreground">
          <span className="flex items-center gap-2">
            <MapPin className="h-4 w-4" />
            15+ Booking Platforms
          </span>
          <span className="flex items-center gap-2">
            <Users className="h-4 w-4" />
            Federal & State Parks
          </span>
          <span className="flex items-center gap-2">
            <Calendar className="h-4 w-4" />
            Real-time Availability
          </span>
        </div>
      </div>

      {/* Popular Providers */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-4">
          Most Popular Providers
        </h2>
        <p className="text-muted-foreground text-center mb-12 max-w-2xl mx-auto">
          These platforms offer the largest selection of campgrounds and are
          monitored most frequently by camply.
        </p>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {providers
            .filter((p) => p.popular)
            .map((provider) => (
              <Card key={provider.name} className="relative">
                {provider.popular && (
                  <div className="absolute -top-3 left-4">
                    <span className="bg-primary text-primary-foreground px-3 py-1 rounded-full text-xs font-medium flex items-center gap-1">
                      <Star className="h-3 w-3" />
                      Popular
                    </span>
                  </div>
                )}
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    {provider.name}
                    <a
                      href={provider.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-muted-foreground hover:text-foreground transition-colors"
                    >
                      <ExternalLink className="h-4 w-4" />
                    </a>
                  </CardTitle>
                  <CardDescription>{provider.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-semibold text-sm mb-2">Coverage:</h4>
                      <div className="flex flex-wrap gap-1">
                        {provider.coverage.map((area) => (
                          <span
                            key={area}
                            className="bg-secondary text-secondary-foreground px-2 py-1 rounded-md text-xs"
                          >
                            {area}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div>
                      <h4 className="font-semibold text-sm mb-2">Features:</h4>
                      <ul className="text-sm text-muted-foreground space-y-1">
                        {provider.features.slice(0, 3).map((feature) => (
                          <li key={feature} className="flex items-center gap-2">
                            <div className="w-1 h-1 bg-primary rounded-full"></div>
                            {feature}
                          </li>
                        ))}
                      </ul>
                    </div>

                    {provider.campgroundCount && (
                      <div className="text-sm">
                        <span className="font-semibold">
                          {provider.campgroundCount.toLocaleString()}+
                        </span>
                        <span className="text-muted-foreground">
                          {" "}
                          campgrounds
                        </span>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
        </div>
      </section>

      {/* All Providers */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-4">
          All Supported Providers
        </h2>
        <p className="text-muted-foreground text-center mb-12 max-w-2xl mx-auto">
          Complete list of booking platforms and reservation systems that camply
          monitors for availability.
        </p>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {providers.map((provider) => (
            <Card key={provider.name}>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  {provider.name}
                  <a
                    href={provider.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-muted-foreground hover:text-foreground transition-colors"
                  >
                    <ExternalLink className="h-4 w-4" />
                  </a>
                </CardTitle>
                <CardDescription>{provider.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div>
                    <div className="flex flex-wrap gap-1">
                      {provider.coverage.map((area) => (
                        <span
                          key={area}
                          className="bg-secondary text-secondary-foreground px-2 py-1 rounded-md text-xs"
                        >
                          {area}
                        </span>
                      ))}
                    </div>
                  </div>

                  {provider.campgroundCount && (
                    <div className="text-sm">
                      <span className="font-semibold">
                        {provider.campgroundCount.toLocaleString()}+
                      </span>
                      <span className="text-muted-foreground">
                        {" "}
                        campgrounds
                      </span>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Coming Soon */}
      <section className="text-center">
        <h2 className="text-3xl font-bold mb-4">More Providers Coming Soon</h2>
        <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
          We're constantly adding support for new booking platforms and
          recreation systems. Have a specific provider you'd like us to support?
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button size="lg" asChild>
            <a
              href="https://github.com/juftin/camply-web/issues/new?template=feature_request.md"
              target="_blank"
              rel="noopener noreferrer"
            >
              Request a Provider
            </a>
          </Button>
          <Button size="lg" variant="outline" asChild>
            <Link to="/faq">View FAQ</Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
