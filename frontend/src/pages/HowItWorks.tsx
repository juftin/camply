import { Link } from "react-router-dom";
import {
  Search,
  Bell,
  Calendar,
  MapPin,
  Clock,
  Smartphone,
  Mail,
  Zap,
  Shield,
  Settings,
  CheckCircle,
  ArrowRight,
  RefreshCw,
  AlertCircle,
  TentTree,
  Tent,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export function HowItWorks() {
  return (
    <div className="container mx-auto py-12 px-4 max-w-6xl">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <div className="mb-6">
          <Tent className="h-16 w-16 text-primary mx-auto mb-4" />
        </div>
        <h1 className="text-5xl font-bold mb-6">
          How camply
          <span className="text-primary"> Works</span>
        </h1>
        <p className="text-xl text-muted-foreground max-w-4xl mx-auto leading-relaxed">
          From search to reservation, here's exactly how camply monitors
          campsite availability and gets you notified the moment your perfect
          spot becomes available.
        </p>
      </div>

      {/* Quick Overview */}
      <section className="mb-16">
        <Card className="border-blue-200 bg-blue-50 dark:bg-blue-950/20 dark:border-blue-800">
          <CardHeader className="text-center">
            <CardTitle className="text-3xl mb-4">The Simple Process</CardTitle>
            <CardDescription className="text-lg">
              Four easy steps to never miss a campsite again
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="bg-primary text-primary-foreground rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  1
                </div>
                <Search className="h-8 w-8 text-primary mx-auto mb-2" />
                <h3 className="font-semibold mb-2">Search</h3>
                <p className="text-sm text-muted-foreground">
                  Find your desired campground and dates
                </p>
              </div>
              <div className="text-center">
                <div className="bg-primary text-primary-foreground rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  2
                </div>
                <Settings className="h-8 w-8 text-primary mx-auto mb-2" />
                <h3 className="font-semibold mb-2">Configure</h3>
                <p className="text-sm text-muted-foreground">
                  Set your preferences and notification methods
                </p>
              </div>
              <div className="text-center">
                <div className="bg-primary text-primary-foreground rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  3
                </div>
                <RefreshCw className="h-8 w-8 text-primary mx-auto mb-2" />
                <h3 className="font-semibold mb-2">Monitor</h3>
                <p className="text-sm text-muted-foreground">
                  We check availability every few minutes
                </p>
              </div>
              <div className="text-center">
                <div className="bg-primary text-primary-foreground rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  4
                </div>
                <Bell className="h-8 w-8 text-primary mx-auto mb-2" />
                <h3 className="font-semibold mb-2">Get Notified</h3>
                <p className="text-sm text-muted-foreground">
                  Instant alerts when spots open up
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Detailed Steps */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-12">
          Step-by-Step Guide
        </h2>

        {/* Step 1 */}
        <div className="mb-12">
          <Card>
            <CardContent className="p-8">
              <div className="grid md:grid-cols-2 gap-8 items-center">
                <div>
                  <div className="flex items-center gap-4 mb-4">
                    <div className="bg-primary text-primary-foreground rounded-full w-10 h-10 flex items-center justify-center text-lg font-bold">
                      1
                    </div>
                    <h3 className="text-2xl font-semibold">
                      Find Your Campground
                    </h3>
                  </div>
                  <p className="text-muted-foreground mb-4">
                    Start by searching for your desired campground using our
                    search tool. You can search by name, location, or browse our
                    supported providers including National Parks, State Parks,
                    and Recreation Areas.
                  </p>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <MapPin className="h-4 w-4 text-primary" />
                      <span className="text-sm">
                        Search by campground name or location
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Calendar className="h-4 w-4 text-primary" />
                      <span className="text-sm">Select your desired dates</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <TentTree className="h-4 w-4 text-primary" />
                      <span className="text-sm">
                        Choose campsite types and preferences
                      </span>
                    </div>
                  </div>
                </div>
                <div className="bg-muted/30 rounded-lg p-6 text-center">
                  <Search className="h-16 w-16 text-primary mx-auto mb-4" />
                  <p className="text-sm text-muted-foreground">
                    Search interface with filters for dates, campsite types, and
                    amenities
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Step 2 */}
        <div className="mb-12">
          <Card>
            <CardContent className="p-8">
              <div className="grid md:grid-cols-2 gap-8 items-center">
                <div className="bg-muted/30 rounded-lg p-6 text-center order-2 md:order-1">
                  <Settings className="h-16 w-16 text-primary mx-auto mb-4" />
                  <p className="text-sm text-muted-foreground">
                    Notification preferences and monitoring settings
                  </p>
                </div>
                <div className="order-1 md:order-2">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="bg-primary text-primary-foreground rounded-full w-10 h-10 flex items-center justify-center text-lg font-bold">
                      2
                    </div>
                    <h3 className="text-2xl font-semibold">
                      Set Your Preferences
                    </h3>
                  </div>
                  <p className="text-muted-foreground mb-4">
                    Configure how and when you want to be notified. Choose your
                    notification methods, set specific campsite preferences, and
                    customize monitoring frequency to match your needs.
                  </p>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <Mail className="h-4 w-4 text-primary" />
                      <span className="text-sm">Email notifications</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Smartphone className="h-4 w-4 text-primary" />
                      <span className="text-sm">SMS alerts (coming soon)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Bell className="h-4 w-4 text-primary" />
                      <span className="text-sm">
                        Push notifications (coming soon)
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Step 3 */}
        <div className="mb-12">
          <Card>
            <CardContent className="p-8">
              <div className="grid md:grid-cols-2 gap-8 items-center">
                <div>
                  <div className="flex items-center gap-4 mb-4">
                    <div className="bg-primary text-primary-foreground rounded-full w-10 h-10 flex items-center justify-center text-lg font-bold">
                      3
                    </div>
                    <h3 className="text-2xl font-semibold">We Monitor 24/7</h3>
                  </div>
                  <p className="text-muted-foreground mb-4">
                    Once you've set up your alerts, camply takes over. Our
                    system automatically checks campsite availability every few
                    minutes, around the clock, so you don't have to constantly
                    refresh booking websites.
                  </p>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <Clock className="h-4 w-4 text-primary" />
                      <span className="text-sm">Checks every 2-5 minutes</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Shield className="h-4 w-4 text-primary" />
                      <span className="text-sm">
                        Reliable, automated monitoring
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Zap className="h-4 w-4 text-primary" />
                      <span className="text-sm">
                        Instant detection of new availability
                      </span>
                    </div>
                  </div>
                </div>
                <div className="bg-muted/30 rounded-lg p-6 text-center">
                  <RefreshCw className="h-16 w-16 text-primary mx-auto mb-4" />
                  <p className="text-sm text-muted-foreground">
                    Continuous monitoring dashboard showing real-time status
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Step 4 */}
        <div className="mb-12">
          <Card>
            <CardContent className="p-8">
              <div className="grid md:grid-cols-2 gap-8 items-center">
                <div className="bg-muted/30 rounded-lg p-6 text-center order-2 md:order-1">
                  <Bell className="h-16 w-16 text-primary mx-auto mb-4" />
                  <p className="text-sm text-muted-foreground">
                    Instant notification with booking link and campsite details
                  </p>
                </div>
                <div className="order-1 md:order-2">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="bg-primary text-primary-foreground rounded-full w-10 h-10 flex items-center justify-center text-lg font-bold">
                      4
                    </div>
                    <h3 className="text-2xl font-semibold">
                      Get Instant Alerts
                    </h3>
                  </div>
                  <p className="text-muted-foreground mb-4">
                    The moment a campsite becomes available, you'll receive an
                    instant notification with all the details you need to book
                    quickly. Each alert includes a direct link to the official
                    booking site.
                  </p>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <Zap className="h-4 w-4 text-primary" />
                      <span className="text-sm">Instant notifications</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-primary" />
                      <span className="text-sm">Direct booking links</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <MapPin className="h-4 w-4 text-primary" />
                      <span className="text-sm">
                        Campsite details and pricing
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Behind the Scenes */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-12">
          Behind the Scenes
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          <Card>
            <CardHeader className="text-center">
              <RefreshCw className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle>Smart Monitoring</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-muted-foreground">
                Our system intelligently schedules checks based on campground
                patterns, peak times, and cancellation trends to catch
                availability the moment it appears.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <Shield className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle>Reliable Infrastructure</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-muted-foreground">
                Built on robust infrastructure with redundancy and failover
                systems to ensure we never miss an availability opening, even
                during high-traffic periods.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <Zap className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle>Lightning Fast</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-muted-foreground">
                Notifications are sent within seconds of detecting availability.
                Our optimized delivery system ensures you get notified before
                anyone manually checking websites.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-12">
          Common Questions
        </h2>
        <div className="space-y-6 max-w-4xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertCircle className="h-5 w-5 text-primary" />
                How often do you check for availability?
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                We check campsite availability every 2-5 minutes, 24/7. The
                exact frequency depends on the campground and how close your
                dates are, with more frequent checks closer to arrival dates.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertCircle className="h-5 w-5 text-primary" />
                Do I book through camply?
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                No, camply only monitors and notifies. When we find
                availability, we send you a direct link to the official booking
                site (like Recreation.gov or ReserveAmerica) where you complete
                your reservation.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertCircle className="h-5 w-5 text-primary" />
                How fast do I need to book after getting notified?
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Popular campsites can book up within minutes, so we recommend
                booking immediately after receiving a notification. Our
                notifications give you a significant head start over manual
                checking.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertCircle className="h-5 w-5 text-primary" />
                Which campgrounds do you support?
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                We support campgrounds on Recreation.gov (National Parks,
                National Forests, Army Corps of Engineers) and many state park
                systems. Check our{" "}
                <Link to="/providers" className="text-primary hover:underline">
                  providers page
                </Link>{" "}
                for the complete list.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Call to Action */}
      <section className="text-center">
        <Card className="bg-primary/5 border-primary/20">
          <CardContent className="py-12">
            <TentTree className="h-16 w-16 text-primary mx-auto mb-6" />
            <h2 className="text-3xl font-bold mb-6">Ready to Get Started?</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-8">
              Set up your first campsite alert in minutes and never miss your
              perfect camping spot again.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild>
                <Link to="/auth?mode=signup">
                  Start Monitoring
                  <ArrowRight className="h-4 w-4 ml-2" />
                </Link>
              </Button>
              <Button variant="outline" size="lg" asChild>
                <Link to="/providers">View Supported Campgrounds</Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
