import { createFileRoute } from "@tanstack/react-router";
import { ServiceDetail, serviceHead } from "@/components/site/ServiceDetail";

export const Route = createFileRoute("/services/transport-aerien")({
  head: () => serviceHead("transport-aerien"),
  component: TransportAerienPage,
});

function TransportAerienPage() {
  return <ServiceDetail slug="transport-aerien" />;
}
