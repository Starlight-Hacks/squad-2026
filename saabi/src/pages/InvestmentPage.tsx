import { TrendingUp, Shield, Rocket, Globe, BarChart, ArrowUpRight, CheckCircle2, Lightbulb, Wallet } from "lucide-react";
import { motion } from "motion/react";
import { cn } from "@/src/lib/utils";

const stats = [
  { label: "Nigerians with Investment Access", value: "< 5%", detail: "Mostly High-Income Earners" },
  { label: "Informal Traders", value: "40M+", detail: "Driving the Economy" },
  { label: "SAABI Micro-Investors", value: "250k+", detail: "Growing Daily" },
  { label: "Minimum Investment", value: "₦500", detail: "Start Small, Grow Big" }
];

const plans = [
  {
    name: "Oja Daily Savings",
    amount: "₦500 - ₦2,000 / day",
    return: "8% p.a.",
    duration: "Flexible (Withdraw anytime)",
    features: ["Daily WhatsApp Reminders", "Auto-save from sales", "No withdrawal fees"],
    popular: false,
  },
  {
    name: "Trader's Trust Fund",
    amount: "₦5,000 / week",
    return: "12% p.a.",
    duration: "3 - 6 Months",
    features: ["Quarterly Dividends", "Compound Interest", "Business Emergency Loan access"],
    popular: true,
  },
  {
    name: "Next Level Capital",
    amount: "₦20,000 / month",
    return: "15% p.a.",
    duration: "1 Year fixed",
    features: ["Highest Returns", "GTB Partnership Backed", "Free Business Consulting"],
    popular: false,
  }
];

const tips = [
  "Start small: No amount is too small, consistency is the master key.",
  "Don't eat your seed: Try to reinvest your profit to grow your money faster.",
  "Separate business cash from savings: Use SAABI to keep your profit safe.",
  "Emergency fund first: Always keep some quick cash before fixing the rest."
];

export default function InvestmentPage() {
  return (
    <div className="pt-32 px-6 max-w-7xl mx-auto pb-40 relative">
      {/* Aesthetic strokes */}
      <div className="absolute top-0 left-0 w-[1px] h-full bg-gradient-to-b from-white/10 via-transparent to-transparent -z-10" />
      <div className="absolute top-[30%] left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-white/5 to-transparent -z-10" />

      {/* Header section with Pidgin Slogans */}
      <div className="relative mb-24 text-center md:text-left">
        <div className="absolute top-0 left-1/2 md:left-0 -translate-x-1/2 md:translate-x-0 -top-20 w-64 h-64 bg-gt-orange/20 blur-[100px] -z-10" />
        <h1 className="text-5xl md:text-8xl font-black tracking-tighter mb-6 leading-[0.9] uppercase text-white">
          Make that <span className="text-gt-orange text-glow">2k</span> <br /> work for you.
        </h1>
        <p className="text-white/60 text-xl font-medium max-w-3xl mb-4 leading-relaxed">
          Sabi your money, make your money Sabi for you! No amount is too small to build your future. 
        </p>
        <div className="inline-block bg-gt-orange/10 border border-gt-orange/20 text-gt-orange px-4 py-2 rounded-full text-sm font-bold tracking-widest uppercase mt-4">
          Powered by SAABI Engine
        </div>
      </div>

      {/* Stats highlighting micro-transaction focus */}
      <div className="mb-24">
        <div className="flex flex-col md:flex-row items-baseline gap-4 mb-8">
           <h2 className="text-3xl font-bold">The Reality Check</h2>
           <p className="text-white/40 text-sm">Why we focus on Micro-Transactions</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="glass-card p-8 rounded-[32px] border-white/5 hover:border-gt-orange/30 transition-colors group"
            >
              <h3 className="text-4xl font-black mb-2 group-hover:text-gt-orange transition-colors">{s.value}</h3>
              <p className="text-white/80 text-sm font-bold mb-1">{s.label}</p>
              <p className="text-white/40 text-xs">{s.detail}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Main Content Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12 items-start mb-24">
        
        {/* Micro Investment Plans */}
        <div className="lg:col-span-2">
           <h2 className="text-3xl font-bold mb-2">Available Plans</h2>
           <p className="text-white/40 mb-8">Simple, secure, and tailored for your hustle.</p>
           
           <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {plans.map((plan, i) => (
                 <div key={i} className={cn(
                    "relative p-8 rounded-[32px] border transition-all",
                    plan.popular ? "bg-gt-orange/10 border-gt-orange/50 shadow-[0_0_30px_-10px_rgba(228,93,0,0.3)]" : "bg-white/5 border-white/10 hover:border-white/20"
                 )}>
                    {plan.popular && (
                       <div className="absolute -top-3 left-8 bg-gt-orange text-white text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-full shadow-lg">
                          Most Popular
                       </div>
                    )}
                    <h3 className="text-xl font-bold text-white mb-1 mt-2">{plan.name}</h3>
                    <div className="text-2xl font-black text-gt-orange mb-6">{plan.return}</div>
                    
                    <div className="space-y-4 mb-8">
                       <div className="flex justify-between border-b border-white/10 pb-2">
                          <span className="text-white/50 text-sm">Commitment</span>
                          <span className="text-white font-bold text-sm">{plan.amount}</span>
                       </div>
                       <div className="flex justify-between border-b border-white/10 pb-2">
                          <span className="text-white/50 text-sm">Lock Period</span>
                          <span className="text-white font-bold text-sm">{plan.duration}</span>
                       </div>
                    </div>
                    
                    <ul className="space-y-3 mb-8">
                       {plan.features.map((feat, j) => (
                          <li key={j} className="flex items-start gap-2 text-sm text-white/70">
                             <CheckCircle2 size={16} className="text-gt-orange mt-0.5 shrink-0" />
                             {feat}
                          </li>
                       ))}
                    </ul>
                    
                    <button className={cn(
                       "w-full py-4 rounded-2xl font-bold text-sm transition-colors",
                       plan.popular ? "bg-gt-orange text-white hover:bg-gt-orange-hover" : "bg-white/10 text-white hover:bg-white/20"
                    )}>
                       Start Investing
                    </button>
                 </div>
              ))}
           </div>
        </div>

        {/* Sidebar: GTB & Tips */}
        <div className="space-y-8">
           {/* GTB Integration Box */}
           <div className="glass-card p-8 rounded-[32px] border-white/10 bg-gradient-to-br from-white/5 to-[#dd4f05]/10 relative overflow-hidden group">
              <div className="absolute -right-10 -top-10 w-40 h-40 bg-[#dd4f05]/20 blur-[50px] pointer-events-none group-hover:bg-[#dd4f05]/40 transition-colors" />
              <div className="flex justify-between items-start mb-6">
                 <h3 className="text-xl font-bold">Guaranty Trust Bank Services</h3>
                 <div className="w-10 h-10 bg-white shadow-md rounded-lg flex items-center justify-center p-2 shrink-0">
                    <span className="font-black text-[#dd4f05] text-xs">GTB</span>
                 </div>
              </div>
              <p className="text-sm text-white/60 leading-relaxed mb-6">
                 Link your SAABI wallet directly to any GTB account. Move your profits securely to your formal bank account anytime, instantly.
              </p>
              <ul className="space-y-3 mb-8">
                 <li className="flex items-center gap-2 text-sm font-medium"><Shield size={16} className="text-[#dd4f05]" /> Zero Transfer Fees to GTB</li>
                 <li className="flex items-center gap-2 text-sm font-medium"><Rocket size={16} className="text-[#dd4f05]" /> Qualify for GTB SME Loans</li>
              </ul>
              <button className="w-full bg-white text-[#dd4f05] font-bold py-3.5 rounded-xl text-sm hover:bg-gray-100 transition-colors">
                 Link GTB Account
              </button>
           </div>
           
           {/* Investment Tips */}
           <div className="glass-card p-8 rounded-[32px]">
              <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                 <Lightbulb className="text-yellow-500" size={20} />
                 SAABI Market Tips
              </h3>
              <div className="space-y-6">
                 {tips.map((tip, i) => (
                    <div key={i} className="flex gap-4 items-start">
                       <span className="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center text-xs font-bold text-white/40 shrink-0">
                          {i + 1}
                       </span>
                       <p className="text-sm text-white/70 leading-relaxed">{tip}</p>
                    </div>
                 ))}
              </div>
           </div>
        </div>

      </div>
    </div>
  );
}
