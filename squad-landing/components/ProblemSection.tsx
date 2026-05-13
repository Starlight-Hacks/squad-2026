import { Reveal } from "./Reveal";

export const ProblemSection = () => (
  <section className="py-32 px-6 bg-[#050505] relative border-t border-white/5">
    <div className="max-w-5xl mx-auto">
      <Reveal>
        <h2 className="text-3xl md:text-5xl font-bold text-gray-500 tracking-tight leading-tight max-w-4xl">
          A mid-sized African nation. High youth unemployment. A fragmented informal economy. 
        </h2>
      </Reveal>
      <Reveal delay={200}>
        <p className="mt-8 text-2xl md:text-4xl font-medium text-gray-300 leading-snug max-w-4xl">
          Informal traders and gig workers are invisible to formal financial services — no payslips, no credit files, no work history...
          <span className="block mt-6 text-white font-bold">
            even though they generate real cashflow every day.
          </span>
        </p>
      </Reveal>
    </div>
  </section>
);