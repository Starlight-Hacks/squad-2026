import { DashCard } from "../dashComponents/DashCard";
import { MACRO_DATA } from "@/data/constants";
import { 
  Users, 
  Wallet, 
  Banknote, 
  TrendingUp, 
  ArrowRightLeft,
} from 'lucide-react';
import { AnimatedNumber } from "../dashComponents/AnimatedNumber";


export const MacroDashboard = () => (
  <div className="space-y-6 animate-in fade-in duration-500">
    <div className="flex items-center justify-between mb-8 pb-4 border-b border-gray-200">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Macro Intelligence</h1>
        <p className="text-sm text-gray-500 mt-1">Aggregated economic flows from the informal economy.</p>
      </div>
      <div className="flex items-center space-x-2 bg-blue-50 text-blue-700 px-3 py-1.5 rounded-md border border-blue-200 shadow-sm">
        <div className="w-2 h-2 rounded-full bg-blue-600 animate-pulse"></div>
        <span className="text-[11px] font-bold uppercase tracking-wider">Live WhatsApp/Squad Webhooks</span>
      </div>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <DashCard >
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm font-medium text-gray-500">Total Transacted Volume</p>
            <h3 className="text-3xl font-bold text-gray-900 mt-2 tracking-tight">
              <AnimatedNumber value= {JSON.stringify(MACRO_DATA.totalVolume)} prefix="₦" />
            </h3>
            <p className="text-xs text-green-600 mt-2 flex items-center font-medium">
              <TrendingUp size={14} className="mr-1" /> +24% this week
            </p>
          </div>
          <div className="p-2.5 bg-gray-50 border border-gray-100 rounded-lg text-gray-400">
            <Banknote size={20} />
          </div>
        </div>
      </DashCard>
      <DashCard>
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm font-medium text-gray-500">Active Informal Profiles</p>
            <h3 className="text-3xl font-bold text-gray-900 mt-2 tracking-tight">
              <AnimatedNumber value={JSON.stringify(MACRO_DATA.activeTraders)} prefix={""} suffix={""} />
            </h3>
            <p className="text-xs text-gray-500 mt-2 flex items-center">
              1,204 onboarded today
            </p>
          </div>
          <div className="p-2.5 bg-gray-50 border border-gray-100 rounded-lg text-gray-400">
            <Users size={20} />
          </div>
        </div>
      </DashCard>
      <DashCard>
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm font-medium text-gray-500">Credit Disbursed</p>
            <h3 className="text-3xl font-bold text-gray-900 mt-2 tracking-tight">
              <AnimatedNumber value={JSON.stringify(MACRO_DATA.creditDisbursed)} prefix="₦" suffix={""} />
            </h3>
            <p className="text-xs text-gray-500 mt-2 flex items-center">
              Squad API • 452 accounts
            </p>
          </div>
          <div className="p-2.5 bg-gray-50 border border-gray-100 rounded-lg text-gray-400">
            <Wallet size={20} />
          </div>
        </div>
      </DashCard>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
      <DashCard className="lg:col-span-2">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-base font-semibold text-gray-900">Cash Velocity by Sector</h3>
          <button className="text-sm text-blue-600 font-medium hover:underline">View Report</button>
        </div>
        <div className="space-y-5">
          {MACRO_DATA.sectorData.map((sector, idx) => (
            <div key={idx}>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-600 font-medium">{sector.name}</span>
                <span className="text-gray-900 font-semibold">{sector.value}%</span>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                <div 
                  className={`h-2 rounded-full ${sector.color} transition-all duration-1000 ease-out`}
                  style={{ width: '0%', animation: `fillBar 1s forwards ${idx * 0.1}s` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </DashCard>
      <DashCard noPadding>
        <div className="p-5 border-b border-gray-100 flex items-center justify-between">
          <h3 className="text-base font-semibold text-gray-900">Live Ledger</h3>
          <ArrowRightLeft size={16} className="text-gray-400" />
        </div>
        <div className="divide-y divide-gray-100">
          {MACRO_DATA.recentTransactions.map((trx, idx) => (
            <div key={idx} className="flex items-center justify-between p-4 hover:bg-gray-50 transition-colors">
              <div>
                <p className="text-sm font-semibold text-gray-900">{trx.type}</p>
                <p className="text-xs text-gray-500 mt-0.5">{trx.sector} • {trx.time}</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-bold text-gray-900">₦{trx.amount.toLocaleString()}</p>
                <p className={`text-[10px] font-semibold mt-1 uppercase tracking-wider ${trx.status === 'Cleared' ? 'text-green-600' : 'text-amber-500'}`}>
                  {trx.status}
                </p>
              </div>
            </div>
          ))}
        </div>
      </DashCard>
    </div>
    
    <style dangerouslySetInnerHTML={{__html: `
      @keyframes fillBar { to { width: var(--target-width); } }
      ${MACRO_DATA.sectorData.map((s, i) => `div:nth-child(${i+1}) > div > div { --target-width: ${s.value}%; }`).join('\n')}
    `}} />
  </div>
);

