import { createFileRoute } from "@tanstack/react-router";
import { ServiceDetail, serviceHead } from "@/components/site/ServiceDetail";

export const Route = createFileRoute("/services/agent-maritime")({
  head: () => serviceHead("agent-maritime"),
  component: AgentMaritimePage,
});

function AgentMaritimePage() {
  return <ServiceDetail slug="agent-maritime" />;
}
