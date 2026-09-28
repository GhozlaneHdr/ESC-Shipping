import { createFileRoute } from "@tanstack/react-router";
import { ServiceDetail, serviceHead } from "@/components/site/ServiceDetail";

export const Route = createFileRoute("/services/transport-routier")({
  head: () => serviceHead("transport-routier"),
  component: TransportRoutierPage,
});

function TransportRoutierPage() {
  return <ServiceDetail slug="transport-routier" />;
}
