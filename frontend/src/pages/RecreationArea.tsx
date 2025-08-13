import { useParams, useNavigate } from "react-router-dom";
import {
  Mountain,
  MapPin,
  Tent,
  ExternalLink,
  ChevronRight,
} from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { SearchBar } from "@/components/SearchBar";
import { MapComponent } from "@/components/MapComponent";
import { CollapsibleDescription } from "@/components/CollapsibleDescription";
import { getRecreationArea, getProvider, getCampgrounds } from "@/lib/api";
import { toTitleCase } from "@/lib/utils";

export function RecreationArea() {
  const { providerId, recreationAreaId } = useParams<{
    providerId: string;
    recreationAreaId: string;
  }>();
  const navigate = useNavigate();

  const {
    data: recreationArea,
    isLoading: isRecAreaLoading,
    error: recAreaError,
  } = useQuery({
    queryKey: ["recreationArea", providerId, recreationAreaId],
    queryFn: () => getRecreationArea(Number(providerId!), recreationAreaId!),
    enabled: !!(providerId && recreationAreaId),
  });

  const {
    data: provider,
    isLoading: isProviderLoading,
    error: providerError,
  } = useQuery({
    queryKey: ["provider", providerId],
    queryFn: () => getProvider(Number(providerId!)),
    enabled: !!providerId,
  });

  const {
    data: campgrounds,
    isLoading: isCampgroundsLoading,
    error: campgroundsError,
  } = useQuery({
    queryKey: ["campgrounds", providerId, recreationAreaId],
    queryFn: () => getCampgrounds(Number(providerId!), recreationAreaId!),
    enabled: !!(providerId && recreationAreaId),
  });

  if (isRecAreaLoading || isProviderLoading || isCampgroundsLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-2/3 mb-8"></div>
            <div className="h-64 bg-gray-200 rounded mb-6"></div>
            <div className="h-32 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (recAreaError || providerError || !recreationArea || !provider) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <Card>
            <CardContent className="p-8 text-center">
              <h2 className="text-xl font-semibold mb-2">
                Recreation Area Not Found
              </h2>
              <p className="text-muted-foreground">
                The Recreation Area You're Looking for Could Not Be Found.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

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
            <Mountain className="h-8 w-8 text-primary" />
            <div>
              <h1 className="text-3xl font-bold">
                {toTitleCase(recreationArea.name)}
              </h1>
              <p className="text-muted-foreground flex items-center space-x-2">
                <span>Provided by {toTitleCase(provider.name)}</span>
                {provider.url && (
                  <a
                    href={recreationArea.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center space-x-1 text-primary hover:underline"
                  >
                    <ExternalLink className="h-3 w-3" />
                  </a>
                )}
              </p>
            </div>
          </div>
        </div>

        <div className="grid gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MapPin className="h-5 w-5" />
                <span>Recreation Area</span>
              </CardTitle>
              <CardDescription>
                <CollapsibleDescription
                  description={recreationArea.description}
                  fallback="Information About This Recreation Area"
                />
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[recreationArea.state, recreationArea.country].filter(Boolean)
                  .length > 0 && (
                  <div>
                    <span className="font-medium text-sm">Location:</span>
                    <p className="text-muted-foreground">
                      {[recreationArea.state, recreationArea.country]
                        .filter(Boolean)
                        .map((item) => item!.toUpperCase())
                        .join(", ")}
                    </p>
                  </div>
                )}
                {recreationArea.latitude && recreationArea.longitude && (
                  <MapComponent
                    latitude={recreationArea.latitude}
                    longitude={recreationArea.longitude}
                    label={toTitleCase(recreationArea.name)}
                    additionalLocations={
                      campgrounds
                        ?.filter((c) => c.latitude && c.longitude)
                        .map((c) => ({
                          lat: c.latitude!,
                          lng: c.longitude!,
                          label: toTitleCase(c.name),
                          type: "campground" as const,
                        })) || []
                    }
                    className="h-96 rounded-lg overflow-hidden border"
                  />
                )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Tent className="h-5 w-5" />
                <span>Campgrounds</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {campgroundsError ? (
                <p className="text-sm text-muted-foreground">
                  Error Loading Campgrounds Information.
                </p>
              ) : !campgrounds || campgrounds.length === 0 ? (
                <p className="text-sm text-muted-foreground">
                  No Campgrounds Found for This Recreation Area.
                </p>
              ) : (
                <div className="space-y-4">
                  {campgrounds.map((campground) => (
                    <div
                      key={campground.id}
                      className="group p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors cursor-pointer"
                      onClick={() =>
                        navigate(`/campground/${providerId}/${campground.id}`)
                      }
                    >
                      <div className="flex justify-between items-center">
                        <h4 className="font-medium">
                          {toTitleCase(campground.name)}
                        </h4>
                        <div className="flex items-center space-x-2">
                          <div className="flex items-center space-x-2 text-xs">
                            {campground.enabled && (
                              <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full">
                                Active
                              </span>
                            )}
                            {campground.reservable && (
                              <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                                Reservable
                              </span>
                            )}
                          </div>
                          <ChevronRight className="w-4 h-4 text-gray-400 group-hover:text-gray-600 transition-colors" />
                        </div>
                      </div>
                      {[campground.state, campground.country].filter(Boolean)
                        .length > 0 && (
                        <div className="text-xs text-muted-foreground mt-1">
                          {[campground.state, campground.country]
                            .filter(Boolean)
                            .map((item) => item!.toUpperCase())
                            .join(", ")}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
