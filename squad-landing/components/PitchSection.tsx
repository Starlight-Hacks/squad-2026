import { ArrowRight} from 'lucide-react';
import { Reveal } from './Reveal';


export const PitchSection = () => (
  <section className="py-40 px-6 bg-black relative border-t border-white/5 overflow-hidden">
    <div className="absolute inset-0 bg-blue-600/5 bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] from-blue-900/20 via-black to-black"></div>
    <div className="max-w-5xl mx-auto text-center relative z-10">
      <Reveal>
        <h2 className="text-4xl md:text-7xl font-bold text-white tracking-tighter leading-tight mb-8">
          We're not building a fintech, <br className="hidden md:block" />
          a job board, or a marketplace.
        </h2>
      </Reveal>
      <Reveal delay={200}>
        <p className="text-blue-400 text-2xl md:text-4xl font-semibold mb-16 max-w-4xl mx-auto leading-snug">
          We're building the identity and intelligence layer the informal economy is missing.
        </p>
        <button className="bg-white text-black hover:bg-gray-200 px-10 py-5 rounded-full font-bold text-lg transition-all flex items-center mx-auto space-x-3 shadow-[0_0_40px_rgba(255,255,255,0.15)] group">
          <span>View The Dashboard</span>
          <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
        </button>
      </Reveal>
    </div>
  </section>
);