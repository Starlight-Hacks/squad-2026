import { DashCard } from "../dashComponents/DashCard";
export const NotificationCenter = () => (
  <div className="space-y-6 animate-in fade-in duration-300">
    <div className="pb-4 border-b border-gray-200">
      <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Notifications</h1>
      <p className="text-sm text-gray-500 mt-1">System alerts and pending actions.</p>
    </div>
    <DashCard noPadding>
      <div className="divide-y divide-gray-100">
        {[
          { title: "Squad API Webhook Failed", desc: "Timeout connecting to NIBSS. Retrying...", time: "2m ago", type: "error" },
          { title: "New Trader Onboarded", desc: "Basirat Adeyemi completed BVN verification.", time: "1hr ago", type: "info" },
          { title: "Loan Disbursed", desc: "₦50,000 sent to TRD-7729 successfully.", time: "3hrs ago", type: "success" },
        ].map((notif, i) => (
          <div key={i} className="p-4 hover:bg-gray-50 cursor-pointer flex items-start space-x-4">
            <div className={`mt-1 w-2 h-2 rounded-full ${notif.type === 'error' ? 'bg-red-500' : notif.type === 'success' ? 'bg-green-500' : 'bg-blue-500'}`} />
            <div className="flex-1">
              <p className="text-sm font-semibold text-gray-900">{notif.title}</p>
              <p className="text-sm text-gray-500 mt-0.5">{notif.desc}</p>
            </div>
            <span className="text-xs text-gray-400 font-medium">{notif.time}</span>
          </div>
        ))}
      </div>
    </DashCard>
  </div>
);
