import { createFileRoute, Link } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Airplay, ArrowRight, BarChart3, Box, ChevronRight, CircleHelp, Container, PackageCheck, Plane } from "lucide-react";
import { Layout } from "@/components/site/Layout";
import { getResources, type ResourceItem } from "@/lib/api";
import fallbackImage from "@/assets/hero-port.jpg";

export const Route = createFileRoute("/resources")({
  head: () => ({ meta: [{ title: "Resources — ESC Shipping" }, { name: "description", content: "Shipping equipment, air freight and Incoterms reference by ESC." }] }),
  component: ResourcesPage,
});

const typeMeta = {
  container: { label: "Sea containers", icon: Container, description: "Select the right equipment for your cargo." },
  air_freight: { label: "Air freight units", icon: PackageCheck, description: "ULD dimensions and capacity at a glance." },
  aircraft: { label: "Aircraft profile", icon: Plane, description: "Access points and compatible loading units." },
  incoterm: { label: "Incoterms guide", icon: CircleHelp, description: "Map costs, risk and handover points." },
  load_chart: { label: "Load charts", icon: BarChart3, description: "Visual pallet plans for common container loads." },
};

function imageUrl(image: string | null) {
  if (!image) return fallbackImage;
  return image.startsWith("http") ? image : `http://127.0.0.1:8000${image}`;
}

function EquipmentArtwork({ item }: { item: ResourceItem }) {
  const Icon = item.resource_type === "aircraft" ? Plane : item.resource_type === "air_freight" ? Airplay : Box;
  return (
    <div className="relative grid aspect-[16/9] place-items-center overflow-hidden rounded-2xl bg-gradient-to-br from-accent via-surface to-white p-8">
      <div className="absolute inset-0 opacity-[0.05] [background-image:radial-gradient(var(--color-primary)_1px,transparent_1px)] [background-size:16px_16px]" />
      {item.image ? <img src={imageUrl(item.image)} alt="" className="relative h-full w-full object-contain" /> : <Icon className="relative h-28 w-28 text-primary/20" strokeWidth={1} />}
    </div>
  );
}

function SpecificationCard({ item }: { item: ResourceItem }) {
  return (
    <article className="group overflow-hidden rounded-3xl border border-border bg-card shadow-card transition duration-300 hover:-translate-y-1 hover:shadow-lift">
      <EquipmentArtwork item={item} />
      <div className="p-6">
        <p className="text-xs font-bold uppercase tracking-[0.16em] text-primary">{item.resource_type.replace("_", " ")}</p>
        <h3 className="mt-2 font-display text-2xl font-extrabold text-navy">{item.title}</h3>
        <p className="mt-3 min-h-12 text-sm leading-relaxed text-muted-foreground">{item.summary}</p>
        <dl className="mt-5 grid grid-cols-2 gap-x-4 gap-y-3 border-t border-border pt-5">
          {Object.entries(item.specifications).slice(0, 4).map(([label, value]) => (
            <div key={label}><dt className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">{label}</dt><dd className="mt-1 text-sm font-semibold text-navy">{Array.isArray(value) ? value.join(", ") : value}</dd></div>
          ))}
        </dl>
      </div>
    </article>
  );
}

function IncotermsGuide({ item }: { item: ResourceItem }) {
  const terms = (item.specifications.terms || []) as string[];
  const stages = item.responsibilities.stages || [];
  const seller = item.responsibilities.seller || {};
  const notes = item.responsibilities.notes || {};
  return <section id="incoterms" className="scroll-mt-24 rounded-[2rem] bg-navy p-6 text-navy-foreground sm:p-10">
    <div className="flex flex-col justify-between gap-6 md:flex-row md:items-end"><div><p className="eyebrow text-cyan-300">Trade clarity</p><h2 className="mt-3 font-display text-3xl font-extrabold sm:text-4xl">Incoterms® 2020, made practical.</h2><p className="mt-3 max-w-2xl text-navy-foreground/70">See where the seller’s responsibility ends along the shipment journey. This is a quick orientation tool—ESC can help confirm the right term for your contract.</p></div><CircleHelp className="h-11 w-11 shrink-0 text-primary" /></div>
    <div className="mt-8 overflow-x-auto rounded-2xl border border-white/10 bg-white/5 p-4">
      <div className="min-w-[700px]"><div className="grid grid-cols-[72px_repeat(6,minmax(82px,1fr))] gap-1 text-center text-[10px] font-semibold text-navy-foreground/60"><span />{stages.map((stage) => <span key={stage} className="px-1">{stage}</span>)}</div>
      <div className="mt-3 space-y-2">{terms.map((term) => { const covered = seller[term] || 0; return <button type="button" key={term} title={notes[term]} className="grid w-full grid-cols-[72px_repeat(6,minmax(82px,1fr))] gap-1 text-left"><span className="grid place-items-center rounded-lg bg-primary px-2 py-2 text-xs font-extrabold text-white">{term}</span>{stages.map((stage, index) => <span key={stage} className={index < covered ? "h-9 rounded-md bg-cyan-400" : "h-9 rounded-md bg-white/10"} />)}</button>; })}</div></div>
    </div>
    <div className="mt-5 flex flex-wrap gap-5 text-sm text-navy-foreground/75"><span className="flex items-center gap-2"><i className="h-3 w-3 rounded-sm bg-cyan-400" /> Seller arranges / pays</span><span className="flex items-center gap-2"><i className="h-3 w-3 rounded-sm bg-white/15" /> Buyer arranges / pays</span></div>
    <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{terms.map((term) => <div key={term} className="rounded-xl border border-white/10 bg-white/5 p-4"><span className="text-sm font-extrabold text-cyan-300">{term}</span><p className="mt-1 text-sm leading-relaxed text-navy-foreground/70">{notes[term]}</p></div>)}</div>
  </section>;
}

function LoadChartGallery({ charts }: { charts: ResourceItem[] }) {
  return <div className="grid gap-6 lg:grid-cols-2">{charts.map((chart) => <article key={chart.id} className="overflow-hidden rounded-3xl border border-border bg-card shadow-card"><div className="bg-white p-3"><img src={imageUrl(chart.image)} alt={chart.title} className="h-auto w-full rounded-2xl" /></div><div className="p-6"><p className="text-xs font-bold uppercase tracking-[0.16em] text-primary">Capacity plan</p><h3 className="mt-2 font-display text-xl font-extrabold text-navy">{chart.title}</h3><p className="mt-2 text-sm leading-relaxed text-muted-foreground">{chart.summary}</p><dl className="mt-5 grid grid-cols-2 gap-x-4 gap-y-3 border-t border-border pt-5">{Object.entries(chart.specifications).slice(0, 4).map(([label, value]) => <div key={label}><dt className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">{label}</dt><dd className="mt-1 text-sm font-semibold text-navy">{Array.isArray(value) ? value.join(", ") : value}</dd></div>)}</dl></div></article>)}</div>;
}

function ResourcesPage() {
  const [activeTab, setActiveTab] = useState<keyof typeof typeMeta>("container");
  const { data = [], isLoading } = useQuery({ queryKey: ["resources"], queryFn: getResources });
  const equipment = data.filter((item) => item.resource_type !== "incoterm" && item.resource_type !== "load_chart");
  const incoterm = data.find((item) => item.resource_type === "incoterm");
  const charts = data.filter((item) => item.resource_type === "load_chart");
  return <Layout><main>
    <section className="relative overflow-hidden bg-navy py-28 text-navy-foreground sm:py-36"><div className="grid-lines absolute inset-0 opacity-60" /><div className="container-esc relative"><p className="eyebrow text-cyan-300">ESC resource library</p><h1 className="mt-4 max-w-3xl font-display text-5xl font-extrabold leading-[1.03] sm:text-6xl">Plan every shipment with more confidence.</h1><p className="mt-6 max-w-2xl text-lg leading-relaxed text-navy-foreground/75">Equipment specifications, air-cargo references and trade terms in one clear, practical guide.</p><div className="mt-9 flex flex-wrap gap-3"><a href="#equipment" className="rounded-full bg-primary px-5 py-3 text-sm font-bold text-white">Browse equipment <ArrowRight className="ml-1 inline h-4 w-4" /></a><a href="#incoterms" className="rounded-full border border-white/20 px-5 py-3 text-sm font-bold">Explore Incoterms</a></div></div></section>
    <section id="equipment" className="section scroll-mt-20"><div className="container-esc"><div className="max-w-2xl"><p className="eyebrow">Equipment finder</p><h2 className="mt-3 font-display text-3xl font-extrabold text-navy sm:text-4xl">Know the space before you book it.</h2></div>
      <div className="mt-8 flex gap-2 overflow-x-auto border-b border-border pb-px" role="tablist" aria-label="Resource categories">{Object.entries(typeMeta).map(([type, meta]) => { const Icon = meta.icon; const active = activeTab === type; const count = type === "incoterm" ? (incoterm ? 1 : 0) : type === "load_chart" ? charts.length : equipment.filter((item) => item.resource_type === type).length; return <button key={type} type="button" role="tab" aria-selected={active} onClick={() => setActiveTab(type as keyof typeof typeMeta)} className={`flex shrink-0 items-center gap-2 border-b-2 px-4 py-3 text-sm font-bold transition ${active ? "border-primary text-primary" : "border-transparent text-muted-foreground hover:text-navy"}`}><Icon className="h-4 w-4" />{meta.label}<span className="rounded-full bg-accent px-2 py-0.5 text-xs text-primary">{count}</span></button>; })}</div>
      {isLoading ? <p className="mt-10 text-muted-foreground">Loading resources…</p> : activeTab === "incoterm" ? <div className="mt-10">{incoterm && <IncotermsGuide item={incoterm} />}</div> : activeTab === "load_chart" ? <div className="mt-10"><div className="mb-6 flex items-center gap-3"><span className="grid h-10 w-10 place-items-center rounded-xl bg-accent text-primary"><BarChart3 className="h-5 w-5" /></span><div><h3 className="font-display text-xl font-extrabold text-navy">Load charts</h3><p className="text-sm text-muted-foreground">Extracted pallet plans from the ESC cargo reference PDF.</p></div></div><LoadChartGallery charts={charts} /></div> : <div className="mt-10"><div className="mb-5 flex items-center gap-3"><span className="grid h-10 w-10 place-items-center rounded-xl bg-accent text-primary">{(() => { const Icon = typeMeta[activeTab].icon; return <Icon className="h-5 w-5" />; })()}</span><div><h3 className="font-display text-xl font-extrabold text-navy">{typeMeta[activeTab].label}</h3><p className="text-sm text-muted-foreground">{typeMeta[activeTab].description}</p></div></div><div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">{equipment.filter((item) => item.resource_type === activeTab).map((item) => <SpecificationCard item={item} key={item.id} />)}</div></div>}
    </div></section>
    <section className="pb-20"><div className="container-esc"><div className="flex flex-col items-start justify-between gap-5 rounded-3xl bg-surface p-7 sm:flex-row sm:items-center"><div><p className="font-display text-2xl font-extrabold text-navy">Need help choosing the right option?</p><p className="mt-1 text-muted-foreground">Tell ESC about the cargo, route and deadlines.</p></div><Link to="/contact" hash="devis" className="inline-flex items-center gap-2 rounded-full bg-primary px-5 py-3 text-sm font-bold text-white">Request a quote <ChevronRight className="h-4 w-4" /></Link></div></div></section>
  </main></Layout>;
}
