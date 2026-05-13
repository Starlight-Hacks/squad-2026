import { Reveal } from "./Reveal"
import { 
  ArrowRight, 
  ShieldCheck, 
  TrendingUp, 
  Briefcase,
  Database,
  Network
} from 'lucide-react';


export const PillarsSection = () => {
  return (
    <section className="py-32 px-6 bg-[#050505] relative border-t border-white/5">
      <div className="max-w-6xl mx-auto">
        <Reveal>
          <h2 className="text-4xl md:text-6xl font-bold text-white tracking-tight mb-4 text-center">
            Three pillars fall out.
          </h2>
          <p className="text-gray-400 text-center mb-16 text-lg">Each pillar makes the others stronger.</p>
        </Reveal>

        <div className="grid grid-cols-1 md:grid-cols-6 gap-6 auto-rows-[minmax(280px,auto)]">
          
          {/* Pillar 1: Credit */}
          <Reveal delay={100} className="md:col-span-4">
            <div className="bg-gradient-to-br from-[#0A0A0A] to-[#111] border border-white/10 rounded-3xl p-10 h-full flex flex-col relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-[400px] h-[400px] bg-blue-600/5 blur-[80px] rounded-full group-hover:bg-blue-600/10 transition-all duration-700"></div>
              
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center mb-8">
                <TrendingUp size={24} />
              </div>
              
              <div className="relative z-10 max-w-md">
                <h3 className="text-2xl md:text-3xl font-bold text-white mb-4">Credit Scoring</h3>
                <p className="text-gray-400 text-lg leading-relaxed">
                  Generated from transaction patterns. Unlocks loans, BNPL, savings, and micro-insurance for users with no formal history.
                </p>
              </div>

              {/* Decorative Data UI */}
              <div className="absolute bottom-6 right-6 flex items-end space-x-2 opacity-30 group-hover:opacity-80 transition-opacity duration-500">
                <div className="w-8 bg-blue-500/40 h-12 rounded-t-sm"></div>
                <div className="w-8 bg-blue-500/60 h-20 rounded-t-sm"></div>
                <div className="w-8 bg-blue-500/80 h-16 rounded-t-sm"></div>
                <div className="w-8 bg-blue-500 h-28 rounded-t-sm"></div>
              </div>
            </div>
          </Reveal>

          {/* Pillar 2: Trust */}
          <Reveal delay={200} className="md:col-span-2">
            <div className="bg-[#0A0A0A] border border-white/10 rounded-3xl p-8 h-full flex flex-col relative overflow-hidden group hover:border-gray-600 transition-colors">
              <div className="w-12 h-12 rounded-xl bg-white/5 border border-white/10 text-gray-300 flex items-center justify-center mb-auto">
                <ShieldCheck size={24} />
              </div>
              <div className="relative z-10 mt-8">
                <h3 className="text-2xl font-bold text-white mb-3">Trust Scoring</h3>
                <p className="text-gray-400 leading-relaxed">
                  A verified marketplace unlocking B2B commerce among informal traders.
                </p>
              </div>
            </div>
          </Reveal>

          {/* Pillar 3: Jobs */}
          <Reveal delay={300} className="md:col-span-6">
            <div className="bg-gradient-to-r from-indigo-900/20 to-[#0A0A0A] border border-indigo-500/20 rounded-3xl p-10 flex flex-col md:flex-row items-start md:items-center justify-between relative overflow-hidden group">
              <div className="max-w-2xl relative z-10">
                <div className="w-12 h-12 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center mb-6">
                  <Briefcase size={24} />
                </div>
                <h3 className="text-2xl md:text-3xl font-bold text-white mb-4">Skill Graphs</h3>
                <p className="text-gray-400 text-lg leading-relaxed">
                  Derived from gig history. Unlocks job matching for under-25s with no formal work history using vector embeddings.
                </p>
              </div>
              
              <div className="mt-8 md:mt-0 relative z-10 hidden md:block">
                 <div className="bg-black/50 border border-white/10 p-4 rounded-2xl flex items-center space-x-4 backdrop-blur-sm">
                    <Database size={20} className="text-indigo-400" />
                    <ArrowRight size={16} className="text-gray-600" />
                    <Network size={20} className="text-blue-400" />
                    <span className="text-xs text-gray-300 font-mono">pgvector</span>
                 </div>
              </div>
            </div>
          </Reveal>

        </div>
      </div>
    </section>
  );
};

