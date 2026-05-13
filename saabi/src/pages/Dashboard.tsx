import { useState } from "react";
import { 
  BarChart3, 
  Search, 
  Map as MapIcon, 
  Users, 
  ArrowUpRight, 
  ArrowDownRight, 
  Activity,
  MessageCircle,
  Wallet,
  ShieldCheck,
  Star,
  Send,
  MapPin,
  Briefcase
} from "lucide-react";
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  BarElement, 
  Title, 
  Tooltip, 
  Legend, 
  Filler,
  ArcElement
} from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';
import { motion } from "motion/react";
import { cn } from "@/src/lib/utils";
import { supabase } from "@/src/lib/supabase";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

// --- SEEDED DATA ---
const userStats = [
  { label: "Total Transactions", value: "₦142,500", change: "+12.5%", positive: true, icon: Wallet },
  { label: "WhatsApp Chats", value: "24", change: "+5.2%", positive: true, icon: MessageCircle },
  { label: "Service Searches", value: "12", change: "-2.1%", positive: false, icon: Search },
  { label: "Active Requests", value: "3", change: "+1", positive: true, icon: Activity },
];

const monthlyActivityData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Volume (₦)',
      data: [45000, 52000, 38000, 65000, 59000, 92000],
      backgroundColor: '#E45D00',
      borderRadius: 6,
    },
  ],
};

const credibilityData = {
  labels: ['Credibility Score', 'Remaining'],
  datasets: [
    {
      data: [85, 15],
      backgroundColor: ['#E45D00', 'rgba(255, 255, 255, 0.05)'],
      borderWidth: 0,
      circumference: 270,
      rotation: 225,
      cutout: '80%',
    },
  ],
};

const sectorActivityData = {
  labels: ['Artisan', 'Logistics', 'Retail', 'Tech Repair', 'Food'],
  datasets: [
    {
      label: 'Search Volume',
      data: [400, 300, 200, 150, 500],
      backgroundColor: 'rgba(255, 255, 255, 0.8)',
      borderRadius: 4,
    },
    {
      label: 'Provider Count',
      data: [150, 80, 120, 50, 200],
      backgroundColor: 'rgba(255, 255, 255, 0.3)',
      borderRadius: 4,
    },
    {
      label: 'Transaction Value (₦000s)',
      data: [850, 420, 310, 290, 750],
      backgroundColor: '#E45D00',
      borderRadius: 4,
    }
  ],
};

const whatsappHistory = [
  { id: 1, type: "payment", text: "Sent ₦5,000 to Baba Tolu", date: "Today, 10:45 AM", amount: "-₦5,000", status: "Completed" },
  { id: 2, type: "search", text: "Found 3 Electricians in Ikeja", date: "Yesterday, 2:15 PM", amount: null, status: "Resolved" },
  { id: 3, type: "payment", text: "Received ₦15,000 from Client Opay", date: "Yesterday, 9:00 AM", amount: "+₦15,000", status: "Completed" },
  { id: 4, type: "error", text: "Failed transfer to Quick Fix", date: "May 10, 4:20 PM", amount: "-₦2,000", status: "Failed" },
];

const discoveredProviders = [
  { name: "Baba Tolu", service: "Plumbing", location: "Ikeja", rating: 5.0, rate: "₦5k/hr" },
  { name: "Quick Fix", service: "Electrician", location: "Yaba", rating: 4.8, rate: "₦4k/hr" },
  { name: "Mama Nkechi", service: "Food Delivery", location: "Lekki", rating: 4.9, rate: "₦2k/meal" },
  { name: "Tech Bro Repairs", service: "Phone Repair", location: "Computer Village", rating: 4.7, rate: "Varies" },
];

const lgaHeatmap = [
  { name: "Ikeja", intensity: 90 },
  { name: "Yaba", intensity: 75 },
  { name: "Lekki", intensity: 85 },
  { name: "Surulere", intensity: 60 },
  { name: "Oshodi", intensity: 45 },
  { name: "Ajah", intensity: 40 },
  { name: "Victoria Island", intensity: 95 },
  { name: "Ikorodu", intensity: 30 },
  { name: "Agege", intensity: 50 },
  { name: "Badagry", intensity: 15 },
  { name: "Epe", intensity: 10 },
  { name: "Apapa", intensity: 55 },
];

import { User } from "@supabase/supabase-js";

export default function Dashboard({ user }: { user?: User | null }) {
  const [showProviderModal, setShowProviderModal] = useState(false);

  const openWhatsApp = () => {
    window.open("https://wa.me/234800000SAABI", "_blank");
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="pt-28 px-6 max-w-[1600px] mx-auto pb-12 relative min-h-screen"
    >
      {/* Background Grid Pattern */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:64px_64px] pointer-events-none -z-10 [mask-image:radial-gradient(ellipse_60%_60%_at_50%_10%,#000_10%,transparent_100%)]" />

      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col md:flex-row items-start md:items-center justify-between mb-12 gap-6 relative z-10"
      >
        <div>
          <h1 className="text-3xl md:text-5xl font-black mb-2">Welcome back, <span className="text-gt-orange">{user?.user_metadata?.full_name?.split(' ')[0] || "Trader"}</span></h1>
          <p className="text-white/50">Your Personal Dashboard & Activity Summary</p>
        </div>
        <div className="flex items-center gap-3">
          <button 
             onClick={() => supabase.auth.signOut()}
             className="text-white/40 hover:text-white text-xs font-bold px-4 py-2 border border-white/10 rounded-xl bg-white/5 transition-colors"
          >
             Sign Out
          </button>
          <button 
            onClick={() => setShowProviderModal(true)}
            className="bg-white/10 border border-white/20 text-white px-5 py-2.5 rounded-xl text-sm font-bold flex items-center gap-2 hover:bg-white/20 transition-colors"
          >
            <Briefcase size={16} />
            Register as Provider
          </button>
          <button 
            onClick={openWhatsApp}
            className="bg-gt-orange text-white px-5 py-2.5 rounded-xl text-sm font-bold flex items-center gap-2 hover:bg-gt-orange-hover transition-colors"
          >
            <Send size={16} />
            Send Money
          </button>
        </div>
      </motion.div>

      {/* Grid of Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12 relative z-10">
        {userStats.map((stat, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="glass-card p-6 rounded-3xl relative overflow-hidden group hover:border-gt-orange/30 hover:bg-white/[0.02] transition-colors"
          >
            <div className="absolute top-0 right-0 w-32 h-32 bg-gt-orange/5 blur-[50px] group-hover:bg-gt-orange/10 transition-all rounded-full pointer-events-none" />
            <div className="flex items-center justify-between mb-4 relative z-10">
              <div className="w-10 h-10 bg-gt-orange/10 rounded-xl flex items-center justify-center text-gt-orange">
                <stat.icon size={20} />
              </div>
              <div className={cn(
                "flex items-center gap-1 text-xs font-bold px-2 py-1 rounded-lg",
                stat.positive ? "text-green-500 bg-green-500/10" : "text-red-500 bg-red-500/10"
              )}>
                {stat.positive ? <ArrowUpRight size={12} /> : <ArrowDownRight size={12} />}
                {stat.change}
              </div>
            </div>
            <p className="text-white/50 text-sm font-medium mb-1">{stat.label}</p>
            <h3 className="text-2xl font-black">{stat.value}</h3>
          </motion.div>
        ))}
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-12 relative z-10"
      >
        {/* Monthly Activity */}
        <div className="glass-card p-8 rounded-[36px] lg:col-span-2 relative overflow-hidden group hover:border-gt-orange/20 transition-colors">
          <div className="absolute -bottom-32 -right-32 w-64 h-64 bg-gt-orange/5 blur-[80px] group-hover:bg-gt-orange/10 transition-all rounded-full pointer-events-none" />
          <div className="flex items-center justify-between mb-8 relative z-10">
            <h3 className="text-xl font-bold flex items-center gap-2">
              <Activity className="text-gt-orange" size={20} />
              Monthly Activity
            </h3>
            <select className="bg-white/5 border border-white/10 rounded-lg text-xs px-2 py-1 focus:outline-none">
               <option>2026</option>
               <option>2025</option>
            </select>
          </div>
          <div className="h-[250px]">
            <Bar 
              data={monthlyActivityData}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                  y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: 'rgba(255,255,255,0.5)' } },
                  x: { grid: { display: false }, ticks: { color: 'rgba(255,255,255,0.5)' } }
                },
                plugins: { legend: { display: false } }
              }}
            />
          </div>
        </div>

        {/* Credibility Rating */}
        <div className="glass-card p-8 rounded-[36px] flex flex-col items-center justify-center relative overflow-hidden group hover:border-gt-orange/20 transition-colors">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 bg-gt-orange/5 blur-[60px] group-hover:bg-gt-orange/10 transition-all rounded-full pointer-events-none" />
          <h3 className="text-xl font-bold mb-4 w-full text-left flex items-center gap-2 relative z-10">
            <ShieldCheck className="text-gt-orange" size={20} />
            Credibility Rating
          </h3>
          <div className="relative w-[200px] h-[200px] flex items-center justify-center">
            <Doughnut 
              data={credibilityData}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: { enabled: false } },
                cutout: '80%'
              }}
            />
            <div className="absolute inset-0 flex flex-col items-center justify-center pt-8">
              <span className="text-4xl font-black text-gt-orange">85%</span>
              <span className="text-xs text-white/50 uppercase tracking-widest font-bold mt-1">Excellent</span>
            </div>
          </div>
        </div>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12 relative z-10"
      >
        {/* WhatsApp Transactions History */}
        <div className="glass-card p-8 rounded-[36px] relative overflow-hidden group hover:border-gt-orange/20 transition-colors">
          <div className="flex items-center justify-between mb-6 relative z-10">
             <h3 className="text-xl font-bold flex items-center gap-2">
                 <MessageCircle className="text-gt-orange" size={20} />
                 WhatsApp History
             </h3>
             <button className="text-xs text-gt-orange hover:underline font-bold">View All</button>
          </div>
          <div className="space-y-4">
             {whatsappHistory.map((tx) => (
                <div key={tx.id} className="flex items-center justify-between p-4 bg-white/5 border border-white/5 rounded-2xl">
                    <div className="flex items-center gap-4">
                       <div className={cn(
                          "w-10 h-10 rounded-full flex items-center justify-center",
                          tx.type === 'payment' ? 'bg-gt-orange/20 text-gt-orange' : 
                          tx.type === 'search' ? 'bg-blue-500/20 text-blue-500' : 'bg-red-500/20 text-red-500'
                       )}>
                          {tx.type === 'payment' ? <Wallet size={18} /> : 
                           tx.type === 'search' ? <Search size={18} /> : 
                           <Activity size={18} />}
                       </div>
                       <div>
                          <p className="text-sm font-bold">{tx.text}</p>
                          <p className="text-xs text-white/40">{tx.date}</p>
                       </div>
                    </div>
                    <div className="text-right">
                       {tx.amount && (
                           <p className={cn("text-sm font-bold", tx.amount.startsWith('+') ? 'text-green-500' : '')}>
                               {tx.amount}
                           </p>
                       )}
                       <p className={cn("text-[10px] uppercase tracking-wider font-bold mt-1", 
                          tx.status === 'Failed' ? 'text-red-500' : 'text-white/30'
                       )}>{tx.status}</p>
                    </div>
                </div>
             ))}
          </div>
        </div>

        {/* Cashflow Heatmap - Geographic Proxy */}
        <div className="glass-card p-8 rounded-[36px] relative overflow-hidden group hover:border-gt-orange/20 transition-colors">
          <div className="absolute top-0 right-0 w-64 h-64 bg-gt-orange/5 blur-[80px] pointer-events-none" />
          <div className="flex items-center justify-between mb-8 relative z-10">
            <h3 className="text-xl font-bold flex items-center gap-2">
               <MapIcon className="text-gt-orange" size={20} />
               Cashflow (LGA Map)
            </h3>
            <span className="text-xs text-white/50 bg-white/5 px-2 py-1 rounded-md">Last 30 Days</span>
          </div>
          <p className="text-xs text-white/40 mb-6">Geographic shading by transaction volume per Local Government Area.</p>
          <div className="grid grid-cols-3 md:grid-cols-4 gap-3">
             {lgaHeatmap.map((lga, i) => (
                <div 
                   key={i} 
                   className="relative h-20 rounded-xl overflow-hidden flex items-end p-2 border border-white/10"
                >
                   {/* Background color based on intensity */}
                   <div 
                      className="absolute inset-0 bg-gt-orange"
                      style={{ opacity: lga.intensity / 100 }}
                   />
                   <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent" />
                   <div className="relative z-10 w-full flex flex-col">
                      <span className="text-[10px] font-bold text-white leading-tight">{lga.name}</span>
                      <span className="text-[9px] text-white/70">{lga.intensity}% vol</span>
                   </div>
                </div>
             ))}
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12 relative z-10">
        {/* Sector Activity */}
        <div className="glass-card p-8 rounded-[36px]">
           <h3 className="text-xl font-bold flex items-center gap-2 mb-2">
              <BarChart3 className="text-gt-orange" size={20} />
              Sector Activity
           </h3>
           <p className="text-xs text-white/40 mb-8">Breakdown of searches, registered providers, and tx value.</p>
           <div className="h-[300px]">
             <Bar 
               data={sectorActivityData}
               options={{
                 responsive: true,
                 maintainAspectRatio: false,
                 scales: {
                   y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: 'rgba(255,255,255,0.5)' } },
                   x: { grid: { display: false }, ticks: { color: 'rgba(255,255,255,0.5)' } }
                 },
                 plugins: { 
                   legend: { position: 'bottom', labels: { color: 'white', usePointStyle: true, padding: 20 } } 
                 }
               }}
             />
           </div>
        </div>

        {/* Find Traders & Discovery */}
        <div className="glass-card p-8 rounded-[36px] flex flex-col relative overflow-hidden group hover:border-gt-orange/20 transition-colors">
           <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-gt-orange/5 blur-[80px] pointer-events-none" />
           <div className="flex items-center justify-between mb-8 relative z-10">
              <h3 className="text-xl font-bold flex items-center gap-2">
                 <Users className="text-gt-orange" size={20} />
                 Discover Service Providers
              </h3>
              <div className="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center hover:bg-white/10 cursor-pointer">
                 <Search size={14} />
              </div>
           </div>
           
           <div className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-1">
              {discoveredProviders.map((provider, i) => (
                 <div key={i} className="bg-white/5 border border-white/10 rounded-2xl p-4 flex flex-col justify-between hover:bg-white/10 transition-colors cursor-pointer relative overflow-hidden group">
                    <div className="absolute top-0 right-0 w-16 h-16 bg-gt-orange/20 blur-[30px] rounded-full group-hover:bg-gt-orange/40 transition-colors" />
                    <div>
                        <div className="flex justify-between items-start mb-2 relative z-10">
                            <h4 className="font-bold text-sm text-white">{provider.name}</h4>
                            <div className="flex items-center gap-1 text-xs text-yellow-500 bg-yellow-500/10 px-1.5 py-0.5 rounded-md font-bold">
                               <Star size={10} className="fill-yellow-500" />
                               {provider.rating}
                            </div>
                        </div>
                        <p className="text-xs text-gt-orange font-medium mb-1 relative z-10">{provider.service}</p>
                        <p className="text-xs text-white/40 flex items-center gap-1 relative z-10">
                           <MapPin size={10} /> {provider.location}
                        </p>
                    </div>
                    <div className="mt-4 flex items-center justify-between border-t border-white/10 pt-3 relative z-10">
                        <span className="text-xs font-bold text-white/80">{provider.rate}</span>
                        <button className="text-[10px] font-bold uppercase tracking-wider text-gt-orange hover:text-white transition-colors">Contact</button>
                    </div>
                 </div>
              ))}
           </div>
        </div>
      </div>

      {/* Provider Registration Modal */}
      {showProviderModal && (
         <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
            <motion.div 
               initial={{ opacity: 0, scale: 0.95 }}
               animate={{ opacity: 1, scale: 1 }}
               className="bg-[#0A0A0A] border border-white/10 rounded-[32px] p-8 max-w-md w-full shadow-2xl relative"
            >
               <button 
                  onClick={() => setShowProviderModal(false)}
                  className="absolute top-6 right-6 text-white/50 hover:text-white"
               >
                  ✕
               </button>
               <h2 className="text-2xl font-black mb-2">Register as a Provider</h2>
               <p className="text-sm text-white/50 mb-6">Join thousands of verified traders & service workers on SAABI.</p>
               
               <div className="space-y-4">
                  <div>
                     <label className="text-xs font-bold text-white/70 block mb-1.5">Full Name</label>
                     <input type="text" placeholder="John Doe" className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gt-orange text-white" />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                      <div>
                         <label className="text-xs font-bold text-white/70 block mb-1.5">Email Address</label>
                         <input type="email" placeholder="john@example.com" className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gt-orange text-white" />
                      </div>
                      <div>
                         <label className="text-xs font-bold text-white/70 block mb-1.5">Phone Number</label>
                         <input type="tel" placeholder="+234..." className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gt-orange text-white" />
                      </div>
                  </div>
                  <div>
                     <label className="text-xs font-bold text-white/70 block mb-1.5">Geo-Location (LGA/Area)</label>
                     <input type="text" placeholder="e.g. Ikeja, Lagos" className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gt-orange text-white" />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                      <div>
                         <label className="text-xs font-bold text-white/70 block mb-1.5">Service Category</label>
                         <select className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gt-orange text-white appearance-none">
                            <option>Plumbing</option>
                            <option>Food delivery</option>
                            <option>Electrician</option>
                            <option>Logistics</option>
                         </select>
                      </div>
                      <div>
                         <label className="text-xs font-bold text-white/70 block mb-1.5">Base Rate</label>
                         <input type="text" placeholder="e.g. ₦5,000/hr" className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gt-orange text-white" />
                      </div>
                  </div>
               </div>

               <div className="mt-6 bg-gt-orange/10 border border-gt-orange/20 rounded-xl p-4 flex items-start gap-3">
                  <ShieldCheck size={20} className="text-gt-orange shrink-0 mt-0.5" />
                  <div>
                     <h4 className="text-sm font-bold text-gt-orange mb-1">Verification Required</h4>
                     <p className="text-xs text-white/60 leading-relaxed">
                        Please note that a verification period for users will take effect soon. Make sure your details match your government ID.
                     </p>
                  </div>
               </div>

               <button className="w-full bg-gt-orange text-white font-bold py-3.5 rounded-xl mt-6 hover:bg-gt-orange-hover transition-colors">
                  Submit Application
               </button>
            </motion.div>
         </div>
      )}
    </motion.div>
  );
}

