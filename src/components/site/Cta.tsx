import { Link } from "@tanstack/react-router";
import { cva, type VariantProps } from "class-variance-authority";
import type { ComponentProps } from "react";
import { cn } from "@/lib/utils";

export const ctaVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-full font-semibold transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-60",
  {
    variants: {
      variant: {
        primary:
          "bg-primary text-primary-foreground shadow-card hover:bg-primary-dark hover:shadow-lift hover:-translate-y-0.5",
        outline:
          "border border-border bg-background text-foreground hover:border-primary hover:text-primary hover:-translate-y-0.5",
        ghostLight:
          "border border-navy-foreground/30 text-navy-foreground hover:bg-navy-foreground/10 hover:-translate-y-0.5",
        soft: "bg-accent text-accent-foreground hover:bg-primary hover:text-primary-foreground",
      },
      size: {
        md: "h-12 px-6 text-sm",
        lg: "h-14 px-8 text-base",
      },
      block: { true: "w-full", false: "" },
    },
    defaultVariants: { variant: "primary", size: "md", block: false },
  },
);

type CtaProps = VariantProps<typeof ctaVariants> & { className?: string };

export function CtaLink({
  variant,
  size,
  block,
  className,
  ...props
}: CtaProps & ComponentProps<typeof Link>) {
  return <Link className={cn(ctaVariants({ variant, size, block }), className)} {...props} />;
}

export function CtaButton({
  variant,
  size,
  block,
  className,
  ...props
}: CtaProps & ComponentProps<"button">) {
  return <button className={cn(ctaVariants({ variant, size, block }), className)} {...props} />;
}

export function CtaAnchor({
  variant,
  size,
  block,
  className,
  ...props
}: CtaProps & ComponentProps<"a">) {
  return <a className={cn(ctaVariants({ variant, size, block }), className)} {...props} />;
}
