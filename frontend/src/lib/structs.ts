export interface SearchResult {
  id: string;
  entity_type: string;
  provider_id: number;
  provider_name: string;
  recreation_area_id: string | null;
  recreation_area_name: string | null;
  campground_id: string | null;
  campground_name: string | null;
}

export interface RecreationArea {
  id: string;
  provider_id: number;
  name: string;
  description: string | null;
  country: string | null;
  state: string | null;
  longitude: number | null;
  latitude: number | null;
  reservable: boolean;
  enabled: boolean;
  url: string;
}

export interface Provider {
  id: number;
  name: string;
  description: string | null;
  url: string;
  enabled: boolean;
}

export interface Campground {
  id: string;
  provider_id: number;
  recreation_area_id: string | null;
  name: string;
  description: string | null;
  country: string | null;
  state: string | null;
  longitude: number | null;
  latitude: number | null;
  reservable: boolean;
  enabled: boolean;
  url: string;
}
