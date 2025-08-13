import GoogleMapReact from "google-map-react";
import { Tent, MapPin } from "lucide-react";

interface MapMarkerProps {
  lat: number;
  lng: number;
  label?: string;
  type?: "recreation-area" | "campground";
}

const MapMarker = ({ label, type = "recreation-area" }: MapMarkerProps) => (
  <div
    className={`group`}
    style={{
      transform: "translate(-50%, -100%)",
      zIndex: type === "recreation-area" ? 20 : 10,
      position: "relative",
    }}
  >
    <div
      className={`flex items-center justify-center w-8 h-8 rounded-full border-2 border-white shadow-lg transition-transform group-hover:scale-110 ${
        type === "recreation-area" ? "bg-green-600" : "bg-blue-600"
      }`}
    >
      {type === "recreation-area" ? (
        <Tent className="w-4 h-4 text-white" />
      ) : (
        <MapPin className="w-4 h-4 text-white" />
      )}
    </div>
    {label && (
      <div
        className={`absolute top-10 left-1/2 transform -translate-x-1/2 px-2 py-1 rounded-md shadow-lg text-xs font-medium whitespace-nowrap border transition-opacity ${
          type === "recreation-area"
            ? "opacity-100 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 border-gray-200 dark:border-gray-600"
            : "opacity-0 group-hover:opacity-100 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 border-gray-200 dark:border-gray-600"
        }`}
        style={{ minWidth: "max-content" }}
      >
        {label}
      </div>
    )}
  </div>
);

interface MapLocation {
  lat: number;
  lng: number;
  label?: string;
  type?: "recreation-area" | "campground";
}

interface MapComponentProps {
  latitude: number;
  longitude: number;
  label?: string;
  additionalLocations?: MapLocation[];
  zoom?: number;
  className?: string;
}

export function MapComponent({
  latitude,
  longitude,
  label,
  additionalLocations = [],
  zoom = 12,
  className = "h-64 rounded-lg overflow-hidden border",
}: MapComponentProps) {
  // Calculate bounds to fit all markers
  // Separate recreation area and campgrounds to control render order
  const recreationAreaLocation = {
    lat: latitude,
    lng: longitude,
    label,
    type: "recreation-area" as const,
  };
  const campgroundLocations = additionalLocations;

  // Adjust zoom based on bounds if there are additional locations
  const calculatedZoom = additionalLocations.length > 0 ? 10 : zoom;

  return (
    <div className={className}>
      <GoogleMapReact
        bootstrapURLKeys={{
          key: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || "",
        }}
        defaultCenter={{
          lat: latitude,
          lng: longitude,
        }}
        defaultZoom={calculatedZoom}
        options={{
          disableDefaultUI: true,
          zoomControl: true,
        }}
      >
        {/* Render campgrounds first (lower z-index) */}
        {campgroundLocations.map((location, index) => (
          <MapMarker
            key={`campground-${index}`}
            lat={location.lat}
            lng={location.lng}
            label={location.label}
            type={location.type}
          />
        ))}
        {/* Render recreation area last (higher z-index) to ensure it's on top */}
        <MapMarker
          key="recreation-area"
          lat={recreationAreaLocation.lat}
          lng={recreationAreaLocation.lng}
          label={recreationAreaLocation.label}
          type={recreationAreaLocation.type}
        />
      </GoogleMapReact>
    </div>
  );
}
