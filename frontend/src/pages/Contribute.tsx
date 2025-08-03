import { Link } from "react-router-dom";
import {
  Heart,
  Server,
  Bell,
  Shield,
  DollarSign,
  ExternalLink,
  HeartHandshake,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export function Contribute() {
  return (
    <div className="container mx-auto py-12 px-4 max-w-6xl">
      <div className="text-center mb-12">
        <div className="mb-6">
          <HeartHandshake className="h-16 w-16 text-primary mx-auto mb-4" />
        </div>
        {/*<h1 className="text-4xl font-bold mb-4">Contribute to camply</h1>*/}
        <h1 className="text-5xl font-bold mb-6">
          <span className="text-primary"> Contribute </span>
          to camply
        </h1>
        <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
          Help keep camply running and accessible to everyone. Your
          contributions ensure we can continue providing free campsite
          monitoring to the outdoor community.
        </p>
      </div>

      {/* Commitment Section */}
      <section className="mb-16">
        <Card className="border-primary/20 bg-primary/5">
          <CardHeader className="text-center">
            <CardTitle className="flex items-center justify-center gap-2 text-2xl">
              <Shield className="h-6 w-6 text-primary" />
              Our Commitment
            </CardTitle>
          </CardHeader>
          <CardContent className="text-center space-y-4">
            <p className="text-lg font-medium">
              We personally commit to <strong>never taking any profit</strong>{" "}
              from camply.
            </p>
            <p className="text-muted-foreground">
              100% of all contributions go directly towards maintaining the
              service, covering hosting costs, notification delivery, and
              keeping the lights on. This is a labor of love for the outdoor
              community, not a business venture.
            </p>
            <div className="text-sm text-muted-foreground mt-4">
              <span className="text-center">
                All expenses are tracked transparently on our{" "}
                <a
                  href="https://github.com/juftin/camply-web"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary hover:text-primary/80 font-medium"
                >
                  GitHub repository
                </a>
              </span>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* What Your Contribution Supports */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-8">
          What Your Contribution Supports
        </h2>
        <div className="grid md:grid-cols-3 gap-6">
          <Card>
            <CardHeader className="text-center">
              <Server className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle>Hosting & Infrastructure</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-muted-foreground">
                <li>• Cloud server hosting costs</li>
                <li>• Database maintenance</li>
                <li>• Content delivery networks</li>
                <li>• Backup and security systems</li>
                <li>• Monitoring and uptime services</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <Bell className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle>Notification Services</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-muted-foreground">
                <li>• Email delivery services</li>
                <li>• SMS notification costs</li>
                <li>• Push notification infrastructure</li>
                <li>• API rate limits and usage</li>
                <li>• Real-time monitoring systems</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <Heart className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle>Service Improvements</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-muted-foreground">
                <li>• Adding new campground providers</li>
                <li>• Faster notification delivery</li>
                <li>• Enhanced filtering options</li>
                <li>• Mobile app development</li>
                <li>• Community feature requests</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Contribution Options */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-8">
          Ways to Contribute
        </h2>
        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <Card>
            <CardHeader className="text-center">
              <CardTitle className="flex items-center justify-center gap-2">
                <DollarSign className="h-5 w-5" />
                One-Time Contribution
              </CardTitle>
              <CardDescription>
                Make a one-time contribution to support camply
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <Button variant="outline" className="h-12">
                  $5
                </Button>
                <Button variant="outline" className="h-12">
                  $10
                </Button>
                <Button variant="outline" className="h-12">
                  $15
                </Button>
                <Button variant="outline" className="h-12">
                  $20
                </Button>
              </div>
              <Button className="w-full" size="lg" asChild>
                <a
                  href="https://buymeacoffee.com/juftin"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Heart className="h-4 w-4 mr-2" />
                  Buy Us a Coffee
                </a>
              </Button>
              <Button className="w-full" size="lg">
                <Heart className="h-4 w-4 mr-2" />
                Contribute via PayPal
              </Button>
              <Button className="w-full" size="lg">
                <Heart className="h-4 w-4 mr-2" />
                Contribute via GitHub Sponsors
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <CardTitle className="flex items-center justify-center gap-2">
                <Heart className="h-5 w-5" />
                Monthly Support
              </CardTitle>
              <CardDescription>
                Become a monthly contributor for ongoing costs
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex justify-between items-center p-3 border rounded">
                  <div>
                    <div className="font-medium">Coffee Contributor</div>
                    <div className="text-sm text-muted-foreground">
                      Covers basic hosting
                    </div>
                  </div>
                  <div className="text-lg font-bold">$3/mo</div>
                </div>
                <div className="flex justify-between items-center p-3 border rounded">
                  <div>
                    <div className="font-medium">Trail Contributor</div>
                    <div className="text-sm text-muted-foreground">
                      Hosting + notifications
                    </div>
                  </div>
                  <div className="text-lg font-bold">$5/mo</div>
                </div>
                <div className="flex justify-between items-center p-3 border rounded">
                  <div>
                    <div className="font-medium">Summit Contributor</div>
                    <div className="text-sm text-muted-foreground">
                      Full operations support
                    </div>
                  </div>
                  <div className="text-lg font-bold">$10/mo</div>
                </div>
              </div>
              <Button className="w-full" size="lg">
                <Heart className="h-4 w-4 mr-2" />
                Start Monthly Contributions
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Alternative Support */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-8">
          Other Ways to Help
        </h2>
        <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <Card>
            <CardHeader className="text-center">
              <CardTitle className="text-lg">Spread the Word</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-muted-foreground mb-4">
                Share camply with fellow outdoor enthusiasts and camping
                communities
              </p>
              <Button variant="outline" className="w-full">
                Share on Social Media
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <CardTitle className="text-lg">Contribute Code</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-muted-foreground mb-4">
                Help improve camply by contributing to our open-source codebase.
                Check our{" "}
                <Link
                  to="/faq"
                  className="text-primary hover:text-primary/80 underline"
                >
                  FAQ
                </Link>{" "}
                for common questions.
              </p>
              <Button variant="outline" className="w-full" asChild>
                <a
                  href="https://github.com/juftin/camply-web"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  View on GitHub
                </a>
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <CardTitle className="text-lg">Report Issues</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-muted-foreground mb-4">
                Help us improve by reporting bugs and suggesting new features
              </p>
              <Button variant="outline" className="w-full" asChild>
                <a
                  href="https://github.com/juftin/camply-web/issues"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Report an Issue
                </a>
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Transparency */}
      <section className="mb-16">
        <Card>
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">
              Transparency & Accountability
            </CardTitle>
            <CardDescription>
              We believe in complete transparency about how contributions are
              used
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="text-center">
              <p className="text-muted-foreground mb-4">
                As camply grows, we are committed to maintaining complete
                transparency about operational costs and how contributions are
                used. All financial information will be shared openly with the
                community.
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h4 className="font-semibold mb-3">
                  Our Commitment to Transparency
                </h4>
                <ul className="space-y-2 text-muted-foreground">
                  <li>• All expenses tracked and documented</li>
                  <li>• Regular financial updates to the community</li>
                  <li>• Open-source approach to financial management</li>
                  <li>• Zero profit guarantee - all funds go to operations</li>
                  <li>• Community input on major expenditures</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-3">What We'll Track</h4>
                <ul className="space-y-2 text-muted-foreground">
                  <li>• Server and hosting costs</li>
                  <li>• Email and notification service fees</li>
                  <li>• Database and storage expenses</li>
                  <li>• Third-party service integrations</li>
                  <li>• Any infrastructure improvements</li>
                </ul>
              </div>
            </div>

            <div className="text-center pt-4">
              <Button variant="outline" asChild>
                <a
                  href="https://github.com/juftin/camply-web"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <ExternalLink className="h-4 w-4 mr-2" />
                  Follow Our Progress on GitHub
                </a>
              </Button>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Thank You */}
      <section className="text-center">
        <Card className="bg-primary/5 border-primary/20">
          <CardContent className="py-8">
            <Heart className="h-12 w-12 text-primary mx-auto mb-4" />
            <h2 className="text-2xl font-bold mb-4">Thank You</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Every contribution, no matter the size, helps keep camply free and
              accessible to outdoor enthusiasts everywhere. Your support enables
              us to continue this mission without compromise.
            </p>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
