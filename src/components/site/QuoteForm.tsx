import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import { Send } from "lucide-react";
import { CtaButton } from "./Cta";
import { services } from "@/data/site";
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
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ resolver: zodResolver(schema), mode: "onBlur" });

  const onSubmit = async (values: FormValues) => {
    await new Promise((r) => setTimeout(r, 600));
    toast.success("Demande enregistrée", {
      description: `Merci ${values.nom}. Notre équipe vous recontacte rapidement.`,
    });
    reset();
  };

  const Error = ({ name }: { name: keyof FormValues }) =>
    errors[name] ? (
      <p className="mt-1.5 text-xs font-medium text-destructive">{errors[name]?.message}</p>
    ) : null;

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      noValidate
      className="rounded-3xl border border-border bg-card p-6 shadow-card sm:p-8"
    >
      <h3 className="font-display text-2xl font-bold text-navy sm:text-3xl">Demandez votre devis</h3>
      <p className="mt-2 text-sm text-muted-foreground">
        Décrivez votre besoin, nous revenons vers vous avec une proposition adaptée.
      </p>

      <div className="mt-8 grid gap-5 sm:grid-cols-2">
        <div>
          <label className={labelClass} htmlFor="nom">
            Nom complet *
          </label>
          <input
            id="nom"
            className={cn(fieldClass, errors.nom && "border-destructive")}
            placeholder="Votre nom"
            {...register("nom")}
          />
          <Error name="nom" />
        </div>
        <div>
          <label className={labelClass} htmlFor="entreprise">
            Entreprise
          </label>
          <input
            id="entreprise"
            className={fieldClass}
            placeholder="Nom de votre société"
            {...register("entreprise")}
          />
        </div>
        <div>
          <label className={labelClass} htmlFor="email">
            Email *
          </label>
          <input
            id="email"
            type="email"
            className={cn(fieldClass, errors.email && "border-destructive")}
            placeholder="vous@entreprise.com"
            {...register("email")}
          />
          <Error name="email" />
        </div>
        <div>
          <label className={labelClass} htmlFor="telephone">
            Téléphone *
          </label>
          <input
            id="telephone"
            type="tel"
            className={cn(fieldClass, errors.telephone && "border-destructive")}
            placeholder="+213 ..."
            {...register("telephone")}
          />
          <Error name="telephone" />
        </div>
        <div className="sm:col-span-2">
          <label className={labelClass} htmlFor="service">
            Type de service *
          </label>
          <select
            id="service"
            defaultValue=""
            className={cn(fieldClass, errors.service && "border-destructive")}
            {...register("service")}
          >
            <option value="" disabled>
              Sélectionnez un service
            </option>
            {services.map((s) => (
              <option key={s.slug} value={s.name}>
                {s.name}
              </option>
            ))}
            <option value="Autre">Autre / plusieurs services</option>
          </select>
          <Error name="service" />
        </div>
        <div>
          <label className={labelClass} htmlFor="depart">
            Ville / Pays de départ *
          </label>
          <input
            id="depart"
            className={cn(fieldClass, errors.depart && "border-destructive")}
            placeholder="Ex. Alger, Algérie"
            {...register("depart")}
          />
          <Error name="depart" />
        </div>
        <div>
          <label className={labelClass} htmlFor="destination">
            Ville / Pays de destination *
          </label>
          <input
            id="destination"
            className={cn(fieldClass, errors.destination && "border-destructive")}
            placeholder="Ex. Marseille, France"
            {...register("destination")}
          />
          <Error name="destination" />
        </div>
        <div className="sm:col-span-2">
          <label className={labelClass} htmlFor="message">
            Message
          </label>
          <textarea
            id="message"
            rows={5}
            className={cn(fieldClass, "h-auto resize-y py-3")}
            placeholder="Nature de la marchandise, volume, délais souhaités..."
            {...register("message")}
          />
        </div>
      </div>

      <CtaButton type="submit" size="lg" block className="mt-8" disabled={isSubmitting}>
        {isSubmitting ? "Envoi en cours..." : "Envoyer ma demande"}
        <Send className="h-4 w-4" />
      </CtaButton>
      <p className="mt-3 text-center text-xs text-muted-foreground">
        Vous pouvez aussi nous écrire à contact@ex-shipping.com
      </p>
    </form>
  );
}
