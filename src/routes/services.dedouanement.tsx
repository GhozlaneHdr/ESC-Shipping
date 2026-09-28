import { createFileRoute } from "@tanstack/react-router";
import { ServiceDetail, serviceHead } from "@/components/site/ServiceDetail";

export const Route = createFileRoute("/services/dedouanement")({
  head: () => serviceHead("dedouanement"),
  component: DedouanementPage,
});

function DedouanementPage() {
  return <ServiceDetail slug="dedouanement" />;
}
