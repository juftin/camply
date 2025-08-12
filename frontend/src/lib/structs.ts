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
