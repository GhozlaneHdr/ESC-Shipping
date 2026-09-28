import { createFileRoute } from "@tanstack/react-router";
import { ServiceDetail, serviceHead } from "@/components/site/ServiceDetail";

export const Route = createFileRoute("/services/agent-de-fret")({
  head: () => serviceHead("agent-de-fret"),
  component: AgentDeFretPage,
});

function AgentDeFretPage() {
  return <ServiceDetail slug="agent-de-fret" />;
}
