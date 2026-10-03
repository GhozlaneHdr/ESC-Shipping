import { cn } from "@/lib/utils";
import { useQuery } from "@tanstack/react-query";
import { getBranding } from "@/lib/api";
import fallbackLogo from "@/assets/logo.png";

export function Logo({ light = false, className }: { light?: boolean; className?: string }) {
  const { data: branding } = useQuery({
    queryKey: ["branding"],
    queryFn: getBranding,
    staleTime: 5 * 60 * 1000,
  });

  return (
    <span className={cn("inline-flex h-14 w-40 items-center overflow-hidden", className)}>
      <img
        src={branding?.logo || fallbackLogo}
        alt="ESC — Express Shipping Company"
        className="h-full w-full scale-[1.8] object-contain"
      />
    </span>
  );
}
