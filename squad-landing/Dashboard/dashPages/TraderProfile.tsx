import {
  Wallet, 
  Search, 
  ShieldCheck, 
  BrainCircuit,
  Briefcase,
  CheckCircle2,
} from 'lucide-react';
import { DashCard } from '../dashComponents/DashCard';
import { MOCK_TRADER } from '@/data/constants';
import { TrustScoreGauge } from '../dashComponents/TrustScoreGuage';


 export const TraderProfile = () => (
  <div className="space-y-6 animate-in fade-in duration-500">
    <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 pb-4 border-b border-gray-200">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Investment Assessment</h1>
        <p className="text-sm text-gray-500 mt-1">AI-inferred profile from transaction history.</p>
      </div>
      <div className="mt-4 md:mt-0 relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
        <input 
          type="text" 
          placeholder="Search BVN or ID..." 
          className="bg-white border border-gray-300 text-gray-900 text-sm pl-9 pr-4 py-2 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 w-full md:w-64 transition-shadow"
        />
      </div>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <DashCard className="lg:col-span-1">
        <div className="flex flex-col items-center text-center">
          <div className="w-16 h-16 bg-gray-100 text-gray-600 rounded-full flex items-center justify-center mb-4 border border-gray-200">
            <Briefcase size={24} />
          </div>
          <h2 className="text-lg font-bold text-gray-900">{MOCK_TRADER.name}</h2>
          <p className="text-sm text-gray-500 mt-1">{MOCK_TRADER.businessType} • {MOCK_TRADER.location}</p>
          
          <div className="w-full mt-6 pt-6 border-t border-gray-100 text-left space-y-4">
            <div>
              <span className="block text-xs font-medium text-gray-500 uppercase tracking-wider mb-1">Owner</span>
              <span className="text-gray-900 text-sm font-semibold">{MOCK_TRADER.owner}</span>
            </div>
            <div>
              <span className="block text-xs font-medium text-gray-500 uppercase tracking-wider mb-1">WhatsApp ID</span>
              <span className="text-gray-900 text-sm font-mono">{MOCK_TRADER.phone}</span>
            </div>
            <div>
              <span className="block text-xs font-medium text-gray-500 uppercase tracking-wider mb-1">KYC Status</span>
              <span className="inline-flex items-center text-green-700 text-xs font-bold bg-green-50 px-2 py-1 rounded border border-green-200">
                <ShieldCheck size={14} className="mr-1" /> BVN VERIFIED
              </span>
            </div>
          </div>
        </div>
      </DashCard>

      <div className="lg:col-span-2 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <DashCard className="flex flex-col items-center justify-center">
            <h3 className="text-gray-500 text-xs font-bold mb-4 uppercase tracking-widest">AI Trust Score</h3>
            <TrustScoreGauge score={MOCK_TRADER.trustScore} />
            <div className="mt-4 flex items-center text-green-700 bg-green-50 px-3 py-1 rounded-full text-xs font-semibold border border-green-100">
              <CheckCircle2 size={14} className="mr-1.5" /> Low Risk Profile
            </div>
          </DashCard>

          <DashCard className="relative overflow-hidden bg-blue-50/50 border-blue-100">
             <div className="absolute top-0 left-0 w-1 h-full bg-blue-600"></div>
             <h3 className="text-blue-900 font-bold flex items-center mb-3 text-sm">
               <BrainCircuit size={16} className="mr-2 text-blue-600" />
               LLM Profile Inference
             </h3>
             <p className="text-sm text-blue-900/80 leading-relaxed font-medium">
               {MOCK_TRADER.aiAnalysis}
             </p>
             <div className="mt-5 pt-4 border-t border-blue-200/50 flex justify-between items-center">
               <span className="text-xs text-blue-600 font-medium">Engine: Groq Llama-3</span>
               <span className="text-[10px] font-bold tracking-wider text-blue-700 bg-blue-100 px-2 py-1 rounded uppercase">Conf: 94%</span>
             </div>
          </DashCard>
        </div>

        <DashCard>
          <div className="flex justify-between items-end mb-8">
            <div>
              <h3 className="text-base font-semibold text-gray-900">Revenue Trajectory</h3>
              <p className="text-xs text-gray-500 mt-1">Captured via WhatsApp & Squad API</p>
            </div>
            <div className="text-right">
              <h2 className="text-2xl font-bold text-gray-900">₦{MOCK_TRADER.monthlyRevenue.toLocaleString()}</h2>
              <span className="text-xs font-medium text-gray-500 uppercase tracking-widest">Monthly Avg</span>
            </div>
          </div>
          
          <div className="h-40 w-full relative flex items-end justify-between pt-4 border-b border-gray-100 pb-2">
            {MOCK_TRADER.revenueHistory.map((val, idx) => (
              <div key={idx} className="flex flex-col items-center w-1/6 group">
                <div 
                  className="w-full max-w-[32px] bg-blue-100 rounded-t transition-all duration-500 ease-out group-hover:bg-blue-600 relative"
                  style={{ height: '0%', animation: `growUp 0.8s forwards ${idx * 0.1}s` }}
                >
                  <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 opacity-0 group-hover:opacity-100 bg-gray-900 text-white text-[10px] font-bold py-1 px-2 rounded shadow-md transition-opacity z-10">
                    {val}k
                  </div>
                </div>
                <span className="text-xs text-gray-400 mt-3 font-medium">M{idx+1}</span>
              </div>
            ))}
          </div>
        </DashCard>

        <div className="flex space-x-3">
          <button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 px-4 rounded-lg transition-colors flex items-center justify-center text-sm shadow-sm">
            <Wallet size={16} className="mr-2" /> Disburse ₦150k via Squad
          </button>
          <button className="bg-white hover:bg-gray-50 text-gray-700 font-semibold py-2.5 px-6 rounded-lg transition-colors border border-gray-300 flex items-center text-sm shadow-sm">
            Decline
          </button>
        </div>
      </div>
    </div>
    <style dangerouslySetInnerHTML={{__html: `
      @keyframes growUp { to { height: calc((var(--val) / 1000) * 100%); } }
      ${MOCK_TRADER.revenueHistory.map((val, i) => `div.group:nth-child(${i+1}) > div:first-child { --val: ${val}; }`).join('\n')}
    `}} />
  </div>
);
