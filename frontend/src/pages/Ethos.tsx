import { Link } from "react-router-dom";
import {
  Mountain,
  Heart,
  Users,
  TreePine,
  Sunrise,
  Compass,
  Star,
  ArrowRight,
  User,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export function Ethos() {
  return (
    <div className="container mx-auto py-12 px-4 max-w-6xl">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <div className="mb-6">
          <Mountain className="h-16 w-16 text-primary mx-auto mb-4" />
        </div>
        <h1 className="text-5xl font-bold mb-6">
          Making the Great Outdoors
          <span className="text-primary"> Accessible to All</span>
        </h1>
        <p className="text-xl text-muted-foreground max-w-4xl mx-auto leading-relaxed">
          At camply, we believe that everyone deserves the chance to experience
          the healing power of naturNow e. Our mission is to tear down the
          barriers that keep people from accessing the outdoors they love.
        </p>
      </div>

      {/* The Problem Section */}
      <section className="mb-16">
        <Card className="border-orange-200 bg-orange-50 dark:bg-orange-950/20 dark:border-orange-800">
          <CardHeader className="text-center">
            <CardTitle className="text-3xl mb-4">
              The Problem We're Solving
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-semibold mb-4">
                  The Booking Struggle
                </h3>
                <p className="text-muted-foreground mb-4">
                  Popular campgrounds book up within minutes of reservations
                  opening. Families plan months ahead, only to find their dream
                  campsite unavailable. The current system favors those with
                  flexible schedules and constant internet access.
                </p>
                <p className="text-muted-foreground">
                  This isn't just inconvenient, it's creating an equity problem
                  where outdoor recreation becomes a privilege for the few
                  rather than a right for everyone.
                </p>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-4">The Real Impact</h3>
                <ul className="space-y-3 text-muted-foreground">
                  <li className="flex items-start gap-2">
                    <Star className="h-5 w-5 text-orange-500 mt-0.5 flex-shrink-0" />
                    Working families miss out on affordable outdoor vacations
                  </li>
                  <li className="flex items-start gap-2">
                    <Star className="h-5 w-5 text-orange-500 mt-0.5 flex-shrink-0" />
                    First-time campers can't find beginner-friendly spots
                  </li>
                  <li className="flex items-start gap-2">
                    <Star className="h-5 w-5 text-orange-500 mt-0.5 flex-shrink-0" />
                    People give up on camping altogether
                  </li>
                  <li className="flex items-start gap-2">
                    <Star className="h-5 w-5 text-orange-500 mt-0.5 flex-shrink-0" />
                    The outdoors become less diverse and inclusive
                  </li>
                  <li className="flex items-start gap-2">
                    <Star className="h-5 w-5 text-orange-500 mt-0.5 flex-shrink-0" />
                    Mental health benefits of nature remain out of reach
                  </li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      <div className="mb-16">
        <p className="text-xl text-muted-foreground max-w-4xl mx-auto leading-relaxed text-center">
          There's a bright side to this problem, though: online camping
          reservations have generous cancellation policies and availabilities
          pop up all the time - that's where camply comes in.
        </p>
      </div>

      {/* Our Story Section */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-12">Our Story</h2>
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <Card>
              <CardContent className="p-8">
                <TreePine className="h-12 w-12 text-primary mb-6" />
                <h3 className="text-2xl font-semibold mb-4">
                  Born from Frustration
                </h3>
                <p className="text-muted-foreground mb-4">
                  camply was born from our own frustration with the camping
                  reservation system. Too many weekends were spent refreshing
                  booking websites, hoping for last-minute cancellations. Too
                  many camping trips were canceled because we couldn't secure a
                  spot.
                </p>
                <p className="text-muted-foreground">
                  We realized this wasn't just our problem, it was keeping
                  countless people from experiencing the restorative power of
                  nature.
                </p>
              </CardContent>
            </Card>
          </div>
          <div>
            <Card>
              <CardContent className="p-8">
                <Sunrise className="h-12 w-12 text-primary mb-6" />
                <h3 className="text-2xl font-semibold mb-4">
                  A Simple Solution
                </h3>
                <p className="text-muted-foreground mb-4">
                  What started as a personal tool quickly grew into something
                  bigger. We realized that by automating the monitoring process,
                  we could level the playing field and give everyone equal
                  access to outdoor opportunities.
                </p>
                <p className="text-muted-foreground">
                  Every notification we send represents another family getting
                  outside, another person finding solace in nature.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Our Values Section */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-12">
          What We Stand For
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          <Card>
            <CardHeader className="text-center">
              <Users className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle>Equity & Access</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-muted-foreground">
                Everyone deserves equal access to nature, regardless of their
                schedule, location, or technical expertise. We're committed to
                keeping camply free and accessible to all.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <Heart className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle>Community First</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-muted-foreground">
                We're built by campers, for campers. Every decision we make is
                guided by what's best for the outdoor community, not profit
                margins or corporate interests.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <TreePine className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle>Nature's Healing Power</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-muted-foreground">
                We believe deeply in the mental, physical, and spiritual
                benefits of spending time outdoors. Every campsite we help
                secure is an opportunity for connection.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* The Impact Section */}
      <section className="mb-16">
        <Card className="border-green-200 bg-green-50 dark:bg-green-950/20 dark:border-green-800">
          <CardHeader className="text-center">
            <CardTitle className="text-3xl mb-4">
              The Impact We're Making
            </CardTitle>
            <CardDescription className="text-lg">
              Every successful reservation represents more than just a booking,
              it's a night outside under the stars.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 text-center">
              <div>
                <div className="text-3xl font-bold text-primary mb-2">100%</div>
                <div className="text-sm text-muted-foreground">
                  Free & Open Source
                </div>
              </div>
              <div>
                <div className="text-3xl font-bold text-primary mb-2">24/7</div>
                <div className="text-sm text-muted-foreground">
                  Monitoring Coverage
                </div>
              </div>
              <div>
                <div className="text-3xl font-bold text-primary mb-2">∞</div>
                <div className="text-sm text-muted-foreground">
                  Opportunities Created
                </div>
              </div>
              <div>
                <div className="text-3xl font-bold text-primary mb-2">🏕️</div>
                <div className="text-sm text-muted-foreground">
                  Dreams Fulfilled
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Our Commitment Section */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-12">
          Our Promises to You
        </h2>
        <div className="grid md:grid-cols-2 gap-8">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Compass className="h-6 w-6 text-primary" />
                Always Free, Always Open
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground mb-4">
                camply will never be sold, never have ads, and never charge for
                basic functionality. We're committed to keeping outdoor access
                free for everyone.
              </p>
              <p className="text-muted-foreground">
                Our code is open source, our finances are transparent, and our
                decisions are made with the community in mind.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Heart className="h-6 w-6 text-primary" />
                Continuous Improvement
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground mb-4">
                We're constantly working to add new campgrounds, improve
                notification speed, and make the service more reliable. Your
                feedback directly shapes our development priorities.
              </p>
              <p className="text-muted-foreground">
                Every feature we build is designed to get more people outside
                and connected with nature.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Who We Are Section */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-12">Who We Are</h2>
        <div className="max-w-4xl mx-auto">
          <Card className="border-blue-200 bg-blue-50 dark:bg-blue-950/20 dark:border-blue-800">
            <CardContent className="p-8">
              <div className="text-center mb-8">
                <User className="h-16 w-16 text-primary mx-auto mb-4" />
                <h3 className="text-2xl font-semibold mb-2">Meet Justin</h3>
              </div>

              <div className="space-y-6 text-muted-foreground">
                <p className="text-lg leading-relaxed">
                  Hi there! 👋 I'm Justin, and I'm the person behind camply.
                  Right now, it's just me: writing code, monitoring servers, and
                  dreaming of a world where everyone can easily access the great
                  outdoors.
                </p>

                <div className="bg-background/50 rounded-lg mt-8">
                  <h3 className="text-2xl font-semibold mb-2 text-center text-foreground">
                    Why I Built This
                  </h3>
                  <p className="text-lg leading-relaxed mb-2">
                    In 2020, my partner and I took a road trip from our home in
                    Denver, Colorado through Grand Teton and Yellowstone
                    National Parks and up to Glacier National Park in Montana.
                    This trip was at the height of the COVID-19 pandemic, and
                    campsites were hard to come by. We planned the trip without
                    having any reservations locked down.
                  </p>
                  <p className="text-lg leading-relaxed mb-2">
                    I ended up paying for a service that would monitor campsite
                    availability and notify me when something opened up.
                    Unfortunately it didn't support every campground we were
                    hoping to stay in along the way, so I decided to write my
                    own code to do it myself and we were able to secure a
                    campsite everywhere we needed throughout the trip.
                  </p>
                  <p className="text-lg leading-relaxed mt-0">
                    My wife and I ended up getting engaged at Iceberg Lake in
                    Glacier National Park on that trip, we stayed in Many
                    Glacier Campground that night with a beautiful view of the
                    mountains under the stars. Since then, I've been proud to
                    share camply with others to help them find those same
                    camping opportunities for free - and I hope to help you find
                    yours too!
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Call to Action */}
      <section className="text-center">
        <Card className="bg-primary/5 border-primary/20">
          <CardContent className="py-12">
            <Mountain className="h-16 w-16 text-primary mx-auto mb-6" />
            <h2 className="text-3xl font-bold mb-6">Join Our Mission</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-8">
              Help us make the outdoors accessible to everyone. Whether you're
              looking for your next camping adventure or want to support our
              cause, you're part of building something bigger than just a
              booking tool.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild>
                <Link to="/auth?mode=signup">
                  Start Camping
                  <ArrowRight className="h-4 w-4 ml-2" />
                </Link>
              </Button>
              <Button variant="outline" size="lg" asChild>
                <Link to="/contribute">Support Our Mission</Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
