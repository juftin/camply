import { useState } from "react";
import { Search, MapPin, Clock, Shield, Star, Heart, Tent } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Link } from "react-router-dom";
import { DismissibleBanner } from "@/components/DismissibleBanner";

export function Home() {
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <>
      {/* Development Banner */}
      <DismissibleBanner
        id="home-development"
        icon={Tent}
        className="bg-orange-100 border-b border-orange-200 py-3 px-4 text-orange-800"
        closeButtonClassName="hover:bg-orange-200 text-orange-800"
        storageType="session"
      >
        <p className="text-sm font-medium text-center">
          camply is currently in development and not ready for use yet. Follow
          our progress on{" "}
          <a
            href="https://github.com/juftin/camply-web"
            target="_blank"
            rel="noopener noreferrer"
            className="underline hover:no-underline font-semibold"
          >
            GitHub
          </a>
          .
        </p>
      </DismissibleBanner>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <h1 className="text-5xl font-bold mb-6">
            Find Campsites at
            <span className="text-primary"> Sold-Out</span> Campgrounds
          </h1>
          <p className="text-xl text-muted-foreground mb-4 max-w-2xl mx-auto">
            Never miss out on your dream camping spot again. camply monitors
            availability and alerts you when cancellations open up at popular
            campgrounds.
          </p>
          <p className="text-lg font-medium text-primary mb-8">
            🏕️ Free and Open Source 🏕
          </p>

          {/* Search Bar */}
          <div className="max-w-md mx-auto mb-8">
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                <Input
                  placeholder="Search campgrounds..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Button>Search</Button>
            </div>
          </div>

          <div className="flex flex-wrap justify-center gap-4 text-sm text-muted-foreground">
            <Link
              to="/providers"
              className="flex items-center gap-1 hover:text-foreground transition-colors"
            >
              <MapPin className="h-4 w-4" />
              National Parks
            </Link>
            <Link
              to="/providers"
              className="flex items-center gap-1 hover:text-foreground transition-colors"
            >
              <MapPin className="h-4 w-4" />
              State Parks
            </Link>
            <Link
              to="/providers"
              className="flex items-center gap-1 hover:text-foreground transition-colors"
            >
              <MapPin className="h-4 w-4" />
              Recreation Areas
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 bg-muted/50">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">
            Why Choose camply?
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <Card>
              <CardHeader>
                <Clock className="h-10 w-10 text-primary mb-2" />
                <CardTitle>Real-Time Monitoring</CardTitle>
                <CardDescription>
                  We check availability every few minutes, so you'll know the
                  instant a spot opens up.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <Shield className="h-10 w-10 text-primary mb-2" />
                <CardTitle>Instant Alerts</CardTitle>
                <CardDescription>
                  Get notified immediately via email, SMS, or push notification
                  when your desired campsite becomes available.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <Star className="h-10 w-10 text-primary mb-2" />
                <CardTitle>Easy Setup</CardTitle>
                <CardDescription>
                  Set up alerts in seconds. Just select your campground, dates,
                  and notification preferences.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <Heart className="h-10 w-10 text-primary mb-2" />
                <CardTitle>Always Free</CardTitle>
                <CardDescription>
                  100% free and open source. No hidden fees, no subscriptions.
                  Built by campers, for campers.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 px-4">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
          <div className="max-w-4xl mx-auto">
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="bg-primary text-primary-foreground rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  1
                </div>
                <h3 className="text-xl font-semibold mb-2">Search & Select</h3>
                <p className="text-muted-foreground">
                  Find your desired campground and select your preferred dates
                  and campsite types.
                </p>
              </div>

              <div className="text-center">
                <div className="bg-primary text-primary-foreground rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  2
                </div>
                <h3 className="text-xl font-semibold mb-2">Set Up Alerts</h3>
                <p className="text-muted-foreground">
                  Choose how you want to be notified and we'll start monitoring
                  availability for you.
                </p>
              </div>

              <div className="text-center">
                <div className="bg-primary text-primary-foreground rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  3
                </div>
                <h3 className="text-xl font-semibold mb-2">Get Notified</h3>
                <p className="text-muted-foreground">
                  Receive instant alerts when campsites become available and
                  book quickly through official sites.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-primary text-primary-foreground">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">
            Ready to Find Your Perfect Campsite?
          </h2>
          <p className="text-xl opacity-90 mb-8">
            Join thousands of campers who never miss out on their favorite
            spots. Check our{" "}
            <Link to="/providers" className="underline hover:no-underline">
              supported campgrounds
            </Link>{" "}
            and{" "}
            <Link to="/faq" className="underline hover:no-underline">
              FAQ
            </Link>
            .
          </p>
          <Button size="lg" variant="secondary" asChild>
            <Link to="/auth?mode=signup">Get Started</Link>
          </Button>
        </div>
      </section>
    </>
  );
}
