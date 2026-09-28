import type { ReactNode } from "react";

export function PageHero({
  eyebrow,
  title,
  description,
  image,
}: {
  eyebrow: string;
  title: ReactNode;
  description?: ReactNode;
  image: string;
}) {
  return (
    <section className="relative isolate overflow-hidden bg-navy">
      <img src={image} alt="" className="absolute inset-0 -z-10 h-full w-full object-cover opacity-30" />
      <div className="absolute inset-0 -z-10 bg-gradient-to-r from-navy via-navy/85 to-navy/40" />
      <div className="container-esc py-24 sm:py-32">
        <p className="eyebrow text-navy-foreground/70">{eyebrow}</p>
        <h1 className="mt-4 max-w-3xl font-display text-4xl font-extrabold leading-[1.05] text-navy-foreground sm:text-5xl lg:text-6xl">
          {title}
        </h1>
        {description ? (
          <p className="mt-6 max-w-2xl text-lg leading-relaxed text-navy-foreground/75">{description}</p>
        ) : null}
      </div>
    </section>
  );
}

export function CtaBand() {
  return null;
}
