import { Link } from "react-router-dom";
import { Mountain, Heart, Compass, ArrowRight, User } from "lucide-react";
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
          nature. Our mission is to tear down the barriers that keep people from
          accessing the outdoor spaces they love.
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
            <div>
              <h3 className="text-xl font-semibold mb-4 text-center text-primary">
                The Booking Struggle
              </h3>
              <p className="text-muted-foreground mb-4">
                Popular campgrounds book up within minutes of reservations
                opening. Families plan months ahead, only to find their dream
                campsite unavailable. The current system favors those with
                flexible schedules and constant internet access. The result is
                that working families, first-time campers, and those without
                technical know-how are left out in the cold.
              </p>
              <p className="text-muted-foreground">
                This isn't just inconvenient; it's creating an equity problem
                where outdoor recreation becomes a privilege for the few rather
                than a right for everyone.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-4 text-center text-primary">
                The Bright Side
              </h3>
              <p className="text-muted-foreground mb-4">
                Online camping reservation providers have generous cancellation
                policies. Even though campgrounds fill up quickly, new
                availabilities pop up all the time. That's where camply comes
                in. We monitor these campgrounds 24/7, so you don't have to. Our
                goal is to level the playing field and give everyone equal
                access to outdoor opportunities.
              </p>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* The Impact Section */}
      <section className="mb-16">
        <Card className="border-green-200 bg-green-50 dark:bg-green-950/20 dark:border-green-800">
          <CardHeader className="text-center">
            <CardTitle className="text-3xl mb-4">
              The Impact We're Making
            </CardTitle>
            <CardDescription className="text-lg">
              Every successful reservation represents more than just a booking;
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
                    Unfortunately, it didn't support every campground we were
                    hoping to stay in along the way. So I decided to buiild
                    something to to do it myself. We ended up being able to
                    secure a campsite everywhere we traveled throughout the
                    trip.
                  </p>
                  <p className="text-lg leading-relaxed mt-0">
                    My wife and I ended up getting engaged at Iceberg Lake in
                    Glacier National Park on that trip. We stayed in Many
                    Glacier Campground that night with a beautiful view of the
                    mountains under the stars. Since then, I've been proud to
                    share camply with others to help them find those same
                    camping opportunities for free — and I hope to help you find
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
