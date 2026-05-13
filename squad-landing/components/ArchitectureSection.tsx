import { MessageCircle, BrainCircuit, CreditCard } from "lucide-react";
import { Reveal } from "./Reveal";

export const ArchitectureSection = () => {
  return (
    <section className="py-32 px-6 bg-[#020202] relative border-t border-white/5 overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-blue-900/10 via-transparent to-transparent"></div>
      
      <div className="max-w-6xl mx-auto relative z-10">
        <Reveal>
          <div className="text-center mb-20">
            <h2 className="text-4xl md:text-6xl font-bold text-white tracking-tight">The Missing Identity Layer</h2>
            <p className="text-gray-400 mt-6 text-xl max-w-2xl mx-auto">
              Capture it cheaply via WhatsApp (zero install, universal reach), enrich it with AI, and process it with Squad.
            </p>
          </div>
        </Reveal>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative">
          {/* Connector Line */}
          <div className="hidden md:block absolute top-1/2 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-blue-500/50 to-transparent -translate-y-1/2 z-0"></div>

          {/* Block 1 */}
          <Reveal delay={100} className="relative z-10">
            <div className="bg-[#0A0A0A] border border-white/10 rounded-3xl p-8 hover:border-blue-500/50 transition-colors h-full">
              <div className="w-14 h-14 rounded-2xl bg-green-500/10 border border-green-500/20 text-green-400 flex items-center justify-center mb-6">
                <MessageCircle size={28} />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">1. WhatsApp API</h3>
              <p className="text-sm text-gray-400 mb-4 uppercase tracking-wider font-semibold">Traders, Customers, Gigs</p>
              <p className="text-gray-500 text-sm leading-relaxed">
                Natural-language and voice payments. The primary channel for informal users. No app install required.
              </p>
            </div>
          </Reveal>

          {/* Block 2 */}
          <Reveal delay={300} className="relative z-10">
            <div className="bg-[#0A0A0A] border border-white/10 rounded-3xl p-8 hover:border-indigo-500/50 transition-colors h-full shadow-[0_0_40px_rgba(79,70,229,0.1)]">
              <div className="w-14 h-14 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center mb-6">
                <BrainCircuit size={28} />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">2. Application Server</h3>
              <p className="text-sm text-gray-400 mb-4 uppercase tracking-wider font-semibold">Anthropic Claude / Postgres</p>
              <p className="text-gray-500 text-sm leading-relaxed">
                Intent parsing translates messages into structured logic. ML models generate credit scores and job embeddings.
              </p>
            </div>
          </Reveal>

          {/* Block 3 */}
          <Reveal delay={500} className="relative z-10">
            <div className="bg-[#0A0A0A] border border-white/10 rounded-3xl p-8 hover:border-blue-500/50 transition-colors h-full">
              <div className="w-14 h-14 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center mb-6">
                <CreditCard size={28} />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">3. Squad Payments</h3>
              <p className="text-sm text-gray-400 mb-4 uppercase tracking-wider font-semibold">Transfers & NIBSS</p>
              <p className="text-gray-500 text-sm leading-relaxed">
                The execution layer. Instant bank transfers, virtual accounts, and webhooks to finalize the transaction.
              </p>
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  );
};