import { useParams } from "react-router-dom";
import { Mountain, MapPin, Tent } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { SearchBar } from "@/components/SearchBar";

export function RecreationArea() {
  const { providerId, recreationAreaId } = useParams<{
    providerId: string;
    recreationAreaId: string;
  }>();

  // TODO: Fetch recreation area data using the provider ID and recreation area ID
  // For now, we'll show a placeholder

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Search Bar at top */}
      <div className="mb-8">
        <SearchBar
          placeholder="Search campgrounds..."
          className="max-w-4xl mx-auto"
        />
      </div>

      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-6">
            <Mountain className="h-8 w-8 text-primary" />
            <div>
              <h1 className="text-3xl font-bold">Recreation Area Details</h1>
              <p className="text-muted-foreground">
                Recreation Area Information
              </p>
            </div>
          </div>
        </div>

        <div className="grid gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MapPin className="h-5 w-5" />
                <span>Recreation Area Information</span>
              </CardTitle>
              <CardDescription>
                Details about this recreation area will be displayed here.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <p className="text-muted-foreground">
                  <span className="font-medium">Provider ID:</span> {providerId}
                </p>
                <p className="text-muted-foreground">
                  <span className="font-medium">Recreation Area ID:</span>{" "}
                  {recreationAreaId}
                </p>
              </div>
              <p className="text-sm text-muted-foreground mt-4">
                This is a placeholder page. Recreation area data fetching and
                display will be implemented here.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Tent className="h-5 w-5" />
                <span>Available Campgrounds</span>
              </CardTitle>
              <CardDescription>
                Campgrounds within this recreation area.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                List of campgrounds within this recreation area will be
                displayed here.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
