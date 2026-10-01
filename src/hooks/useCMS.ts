/**
 * React Query hooks for CMS data.
 * Replace static imports with live API calls.
 */

import { useQuery } from "@tanstack/react-query";
import {
  getAssociatedCampaigns,
  getMaritimeCampaigns,
  getServices,
  getStats,
  getTrustedPartners,
} from "@/lib/api";

export function useStats() {
  return useQuery({
    queryKey: ["stats"],
    queryFn: getStats,
  });
}

export function useServices() {
  return useQuery({
    queryKey: ["services"],
    queryFn: getServices,
  });
}

export function useMaritimeCampaigns() {
  return useQuery({
    queryKey: ["maritime-campaigns"],
    queryFn: getMaritimeCampaigns,
  });
}

export function useAssociatedCampaigns() {
  return useQuery({
    queryKey: ["associated-campaigns"],
    queryFn: getAssociatedCampaigns,
  });
}

export function useTrustedPartners() {
  return useQuery({
    queryKey: ["partners"],
    queryFn: getTrustedPartners,
  });
}
