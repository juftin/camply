import { useParams, useNavigate } from "react-router-dom";
import {
  Tent,
  MapPin,
  Mountain,
  ExternalLink,
  ChevronLeft,
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
import {
  getCampground,
  getProvider,
  getRecreationArea,
  getCampgrounds,
} from "@/lib/api";
import { toTitleCase } from "@/lib/utils";

export function Campground() {
  const { providerId, campgroundId } = useParams<{
    providerId: string;
    campgroundId: string;
  }>();
  const navigate = useNavigate();

  const {
    data: campground,
    isLoading: isCampgroundLoading,
    error: campgroundError,
  } = useQuery({
    queryKey: ["campground", providerId, campgroundId],
    queryFn: () => getCampground(Number(providerId!), campgroundId!),
    enabled: !!(providerId && campgroundId),
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

  const { data: recreationArea, isLoading: isRecAreaLoading } = useQuery({
    queryKey: ["recreationArea", providerId, campground?.recreation_area_id],
    queryFn: () =>
      getRecreationArea(Number(providerId!), campground!.recreation_area_id!),
    enabled: !!(providerId && campground?.recreation_area_id),
  });

  const { data: otherCampgrounds } = useQuery({
    queryKey: ["campgrounds", providerId, campground?.recreation_area_id],
    queryFn: () =>
      getCampgrounds(Number(providerId!), campground!.recreation_area_id!),
    enabled: !!(providerId && campground?.recreation_area_id),
  });

  if (isCampgroundLoading || isProviderLoading || isRecAreaLoading) {
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

  if (campgroundError || providerError || !campground || !provider) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <Card>
            <CardContent className="p-8 text-center">
              <h2 className="text-xl font-semibold mb-2">
                Campground Not Found
              </h2>
              <p className="text-muted-foreground">
                The Campground You're Looking for Could Not Be Found.
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
            <Tent className="h-8 w-8 text-primary" />
            <div>
              <h1 className="text-3xl font-bold">
                {toTitleCase(campground.name)}
              </h1>
              <p className="text-muted-foreground flex items-center space-x-2">
                <span>Provided by {toTitleCase(provider.name)}</span>
                {provider.url && (
                  <a
                    href={provider.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center space-x-1 text-primary hover:underline"
                  >
                    <ExternalLink className="h-3 w-3" />
                  </a>
                )}
              </p>
              {recreationArea && (
                <div className="mt-2">
                  <button
                    onClick={() =>
                      navigate(`/rec-area/${providerId}/${recreationArea.id}`)
                    }
                    className="inline-flex items-center space-x-1 text-sm text-muted-foreground hover:text-primary transition-colors"
                  >
                    <ChevronLeft className="h-3 w-3" />
                    <Mountain className="h-3 w-3" />
                    <span>{toTitleCase(recreationArea.name)}</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="grid gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MapPin className="h-5 w-5" />
                <span>Campground</span>
              </CardTitle>
              <CardDescription>
                <CollapsibleDescription
                  description={campground.description}
                  fallback="Information About This Campground"
                />
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[campground.state, campground.country].filter(Boolean).length >
                  0 && (
                  <div>
                    <span className="font-medium text-sm">Location:</span>
                    <p className="text-muted-foreground">
                      {[campground.state, campground.country]
                        .filter(Boolean)
                        .map((item) => toTitleCase(item!))
                        .join(", ")}
                    </p>
                  </div>
                )}
                <div>
                  <span className="font-medium text-sm">Status:</span>
                  <div className="flex items-center space-x-2 mt-1">
                    {campground.enabled && (
                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">
                        Active
                      </span>
                    )}
                    {campground.reservable && (
                      <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
                        Reservable
                      </span>
                    )}
                  </div>
                </div>
                {campground.latitude && campground.longitude && (
                  <MapComponent
                    latitude={campground.latitude}
                    longitude={campground.longitude}
                    label={toTitleCase(campground.name)}
                    additionalLocations={
                      otherCampgrounds
                        ?.filter(
                          (c) =>
                            c.id !== campgroundId && c.latitude && c.longitude,
                        )
                        .map((c) => ({
                          lat: c.latitude!,
                          lng: c.longitude!,
                          label: toTitleCase(c.name),
                          type: "campground" as const,
                          onClick: () =>
                            navigate(`/campground/${providerId}/${c.id}`),
                        })) || []
                    }
                    className="h-96 rounded-lg overflow-hidden border"
                  />
                )}
              </div>
            </CardContent>
          </Card>

          {/* Other Campgrounds Section */}
          {recreationArea &&
            otherCampgrounds &&
            otherCampgrounds.length > 1 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Mountain className="h-5 w-5" />
                    <span>
                      Other Campgrounds in {toTitleCase(recreationArea.name)}
                    </span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {otherCampgrounds
                      .filter((c) => c.id !== campgroundId) // Exclude current campground
                      .map((otherCampground) => (
                        <div
                          key={otherCampground.id}
                          className="group p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors cursor-pointer"
                          onClick={() =>
                            navigate(
                              `/campground/${providerId}/${otherCampground.id}`,
                            )
                          }
                        >
                          <div className="flex justify-between items-center">
                            <h4 className="font-medium">
                              {toTitleCase(otherCampground.name)}
                            </h4>
                            <div className="flex items-center space-x-2">
                              <div className="flex items-center space-x-2 text-xs">
                                {otherCampground.enabled && (
                                  <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full">
                                    Active
                                  </span>
                                )}
                                {otherCampground.reservable && (
                                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                                    Reservable
                                  </span>
                                )}
                              </div>
                              <ChevronRight className="w-4 h-4 text-gray-400 group-hover:text-gray-600 transition-colors" />
                            </div>
                          </div>
                          {[
                            otherCampground.state,
                            otherCampground.country,
                          ].filter(Boolean).length > 0 && (
                            <div className="text-xs text-muted-foreground mt-1">
                              {[otherCampground.state, otherCampground.country]
                                .filter(Boolean)
                                .map((item) => toTitleCase(item!))
                                .join(", ")}
                            </div>
                          )}
                        </div>
                      ))}
                  </div>
                </CardContent>
              </Card>
            )}
        </div>
      </div>
    </div>
  );
}
