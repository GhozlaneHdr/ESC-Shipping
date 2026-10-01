import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import { CheckCircle2, Send } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { useLocation } from "@tanstack/react-router";
import { CtaButton } from "./Cta";
import { getServices } from "@/lib/api";
import { useI18n } from "@/lib/i18n";
import { cn } from "@/lib/utils";

const schema = z.object({
  nom: z.string().min(2, "Veuillez indiquer votre nom complet."),
  entreprise: z.string().optional(),
  email: z.string().email("Adresse email invalide."),
  telephone: z.string().min(6, "Veuillez indiquer un numéro valide."),
  service: z.string().min(1, "Veuillez choisir un type de service."),
  depart: z.string().min(2, "Veuillez indiquer la ville ou le pays de départ."),
  destination: z.string().min(2, "Veuillez indiquer la ville ou le pays de destination."),
  message: z.string().max(1500).optional(),
});

type FormValues = z.infer<typeof schema>;

const fieldClass =
  "h-12 w-full rounded-xl border border-input bg-background px-4 text-sm text-foreground outline-none transition-colors placeholder:text-muted-foreground focus:border-primary focus:ring-2 focus:ring-ring/25";

const labelClass = "mb-2 block text-sm font-medium text-navy";

export function QuoteForm() {
  const { t } = useI18n();
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const prefilledService = searchParams.get("service");

  const {
    register,
    handleSubmit,
    reset,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ resolver: zodResolver(schema), mode: "onBlur" });

  useEffect(() => {
    if (prefilledService) {
      setValue("service", prefilledService);
    }
  }, [prefilledService, setValue]);

  const { data: services } = useQuery({
    queryKey: ["services"],
    queryFn: getServices,
  });

  const onSubmit = async (values: FormValues) => {
    setSuccessMessage(null);
    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/devis/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          full_name: values.nom,
          company: values.entreprise || "",
          email: values.email,
          phone: values.telephone,
          service_type: values.service,
          departure: values.depart,
          destination: values.destination,
          message: values.message || "",
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const message = (errorData as any).message || "Une erreur est survenue.";
        throw new (Error as any)(message);
      }

      const msg = t("quote.success.message").replace("{name}", values.nom);
      setSuccessMessage(msg);
      toast.success(t("quote.success"), {
        description: msg,
      });
      reset();
    } catch (error: any) {
      toast.error(t("quote.error"), {
        description: error.message || t("quote.error.message"),
      });
    }
  };

  const Error = ({ name }: { name: keyof FormValues }) =>
    errors[name] ? (
      <p className="mt-1.5 text-xs font-medium text-destructive">{errors[name]?.message}</p>
    ) : null;

  return (
    <form
      id="devis"
      onSubmit={handleSubmit(onSubmit)}
      noValidate
      className="rounded-3xl border border-border bg-card p-6 shadow-card sm:p-8"
    >
      <h3 className="font-display text-2xl font-bold text-navy sm:text-3xl">{t("quote.title")}</h3>
      <p className="mt-2 text-sm text-muted-foreground">
        {t("quote.subtitle")}
      </p>

      {successMessage && (
        <div className="mt-6 flex items-start gap-3 rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-emerald-800 dark:border-emerald-800 dark:bg-emerald-950/50 dark:text-emerald-300">
          <CheckCircle2 className="h-5 w-5 shrink-0 text-emerald-600 dark:text-emerald-400 mt-0.5" />
          <div>
            <h4 className="font-bold text-sm">{t("quote.success")}</h4>
            <p className="mt-0.5 text-sm leading-relaxed">{successMessage}</p>
          </div>
        </div>
      )}

      <div className="mt-8 grid gap-5 sm:grid-cols-2">
        <div>
          <label className={labelClass} htmlFor="nom">
            {t("quote.name")}
          </label>
          <input
            id="nom"
            className={cn(fieldClass, errors.nom && "border-destructive")}
            placeholder={t("quote.name.placeholder")}
            {...register("nom")}
          />
          <Error name="nom" />
        </div>
        <div>
          <label className={labelClass} htmlFor="entreprise">
            {t("quote.company")}
          </label>
          <input
            id="entreprise"
            className={fieldClass}
            placeholder={t("quote.company.placeholder")}
            {...register("entreprise")}
          />
        </div>
        <div>
          <label className={labelClass} htmlFor="email">
            {t("quote.email")}
          </label>
          <input
            id="email"
            type="email"
            className={cn(fieldClass, errors.email && "border-destructive")}
            placeholder={t("quote.email.placeholder")}
            {...register("email")}
          />
          <Error name="email" />
        </div>
        <div>
          <label className={labelClass} htmlFor="telephone">
            {t("quote.phone")}
          </label>
          <input
            id="telephone"
            type="tel"
            className={cn(fieldClass, errors.telephone && "border-destructive")}
            placeholder={t("quote.phone.placeholder")}
            {...register("telephone")}
          />
          <Error name="telephone" />
        </div>
        <div className="sm:col-span-2">
          <label className={labelClass} htmlFor="service">
            {t("quote.service")}
          </label>
          <select
            id="service"
            defaultValue=""
            className={cn(fieldClass, errors.service && "border-destructive")}
            {...register("service")}
          >
            <option value="" disabled>
              {t("quote.service.placeholder")}
            </option>
            {(services || []).map((s) => (
              <option key={s.slug} value={s.name}>
                {s.name}
              </option>
            ))}
            <option value="Autre">{t("quote.service.other")}</option>
          </select>
          <Error name="service" />
        </div>
        <div>
          <label className={labelClass} htmlFor="depart">
            {t("quote.departure")}
          </label>
          <input
            id="depart"
            className={cn(fieldClass, errors.depart && "border-destructive")}
            placeholder={t("quote.departure.placeholder")}
            {...register("depart")}
          />
          <Error name="depart" />
        </div>
        <div>
          <label className={labelClass} htmlFor="destination">
            {t("quote.destination")}
          </label>
          <input
            id="destination"
            className={cn(fieldClass, errors.destination && "border-destructive")}
            placeholder={t("quote.destination.placeholder")}
            {...register("destination")}
          />
          <Error name="destination" />
        </div>
        <div className="sm:col-span-2">
          <label className={labelClass} htmlFor="message">
            {t("quote.message")}
          </label>
          <textarea
            id="message"
            rows={5}
            className={cn(fieldClass, "h-auto resize-y py-3")}
            placeholder={t("quote.message.placeholder")}
            {...register("message")}
          />
        </div>
      </div>

      <CtaButton type="submit" size="lg" block className="mt-8" disabled={isSubmitting}>
        {isSubmitting ? t("quote.submitting") : t("quote.submit")}
        <Send className="h-4 w-4" />
      </CtaButton>
      <p className="mt-3 text-center text-xs text-muted-foreground">
        {t("quote.contact")}
      </p>
    </form>
  );
}
