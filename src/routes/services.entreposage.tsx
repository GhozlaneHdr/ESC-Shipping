import { createFileRoute } from "@tanstack/react-router";
import { ServiceDetail, serviceHead } from "@/components/site/ServiceDetail";

export const Route = createFileRoute("/services/entreposage")({
  head: () => serviceHead("entreposage"),
  component: EntreposagePage,
});

function EntreposagePage() {
  return <ServiceDetail slug="entreposage" />;
}
