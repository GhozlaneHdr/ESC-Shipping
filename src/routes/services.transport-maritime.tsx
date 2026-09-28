import { createFileRoute } from "@tanstack/react-router";
import { ServiceDetail, serviceHead } from "@/components/site/ServiceDetail";

export const Route = createFileRoute("/services/transport-maritime")({
  head: () => serviceHead("transport-maritime"),
  component: TransportMaritimePage,
});

function TransportMaritimePage() {
  return <ServiceDetail slug="transport-maritime" />;
}
