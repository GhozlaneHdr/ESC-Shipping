/**
 * API client for ESC Shipping backend.
 * Base URL defaults to localhost:8000 for development.
 */

const API_BASE_URL = (import.meta.env as any)["VITE_API_URL"] || "http://127.0.0.1:8000/api/v1";

export async function fetchFromAPI<T>(endpoint: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

// =============================================================================
// CMS Endpoints
// =============================================================================

export interface Stat {
  id: number;
  value: number;
  suffix: string;
  label: string;
  order: number;
}

export interface ServiceStep {
  id: number;
  title: string;
  text: string;
  order: number;
}

export interface Service {
  id: string;
  slug: string;
  name: string;
  short_description: string;
  long_intro: string;
  image: string;
  benefits: string;
  benefits_list: string[];
  why_us: string;
  why_us_list: string[];
  steps: ServiceStep[];
  is_active: boolean;
  order: number;
}

export interface MaritimeCampaign {
  id: string;
  title: string;
  subtitle: string;
  route_from: string;
  route_to: string;
  discount: string;
  description: string;
  highlights: string;
  highlights_list: string[];
  valid_until: string;
  status: string;
  is_published: boolean;
  created_at: string;
}

export interface AssociatedCampaign {
  id: string;
  category: string;
  title: string;
  description: string;
  badge: string;
  status: string;
  valid_until: string;
  is_published: boolean;
  created_at: string;
}

export interface TrustedPartner {
  id: string;
  name: string;
  logo: string;
  website: string;
  is_active: boolean;
  order: number;
}

// =============================================================================
// API Functions
// =============================================================================

export async function getStats(): Promise<Stat[]> {
  const data = await fetchFromAPI<{ results: Stat[] }>("/cms/stats/");
  return data.results;
}

export async function getServices(): Promise<Service[]> {
  const data = await fetchFromAPI<{ results: Service[] }>("/cms/services/");
  return data.results;
}

export async function getServiceBySlug(slug: string): Promise<Service> {
  return fetchFromAPI<Service>(`/cms/services/${slug}/`);
}

export async function getMaritimeCampaigns(): Promise<MaritimeCampaign[]> {
  const data = await fetchFromAPI<{ results: MaritimeCampaign[] }>("/cms/maritime-campaigns/");
  return data.results;
}

export async function getAssociatedCampaigns(): Promise<AssociatedCampaign[]> {
  const data = await fetchFromAPI<{ results: AssociatedCampaign[] }>("/cms/associated-campaigns/");
  return data.results;
}

export async function getTrustedPartners(): Promise<TrustedPartner[]> {
  const data = await fetchFromAPI<{ results: TrustedPartner[] }>("/cms/partners/");
  return data.results;
}
