import { useParams } from "react-router-dom";
import { Tent, MapPin } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { SearchBar } from "@/components/SearchBar";

export function Campground() {
  const { providerId, campgroundId } = useParams<{
    providerId: string;
    campgroundId: string;
  }>();

  // TODO: Fetch campground data using the provider ID and campground ID
  // For now, we'll show a placeholder

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Search Bar at top */}
      <div className="mb-8">
        <SearchBar
          placeholder="Search other campgrounds..."
          className="max-w-4xl mx-auto"
        />
      </div>

      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-6">
            <Tent className="h-8 w-8 text-primary" />
            <div>
              <h1 className="text-3xl font-bold">Campground Details</h1>
              <p className="text-muted-foreground">Campground Information</p>
            </div>
          </div>
        </div>

        <div className="grid gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MapPin className="h-5 w-5" />
                <span>Campground Information</span>
              </CardTitle>
              <CardDescription>
                Details about this campground will be displayed here.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <p className="text-muted-foreground">
                  <span className="font-medium">Provider ID:</span> {providerId}
                </p>
                <p className="text-muted-foreground">
                  <span className="font-medium">Campground ID:</span>{" "}
                  {campgroundId}
                </p>
              </div>
              <p className="text-sm text-muted-foreground mt-4">
                This is a placeholder page. Campground data fetching and display
                will be implemented here.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
