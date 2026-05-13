"use-client"
import { Sidebar } from "@/components/SideBar";
import { Topbar } from "@/components/TopBar";
import { MacroDashboard } from "@/Dashboard/dashPages/MacroDashboard";
import { NotificationCenter } from "@/Dashboard/dashPages/NotificationCenter";
import { TraderProfile } from "@/Dashboard/dashPages/TraderProfile";
import { WhatsAppLogs } from "@/Dashboard/dashPages/WhatsappLogs";
import {useState} from "react"

export default function App() {
  const [activeView, setActiveView] = useState('macro');

  return (
    <div className="min-h-screen bg-gray-50/50 font-sans text-gray-900 flex">
      <Sidebar activeView={activeView} setActiveView={setActiveView} />

      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        <Topbar activeView={activeView} setActiveView={setActiveView} />

        <div className="flex-1 overflow-y-auto p-4 md:p-8">
          <div className="max-w-5xl mx-auto">
            {activeView === 'macro' && <MacroDashboard />}
            {activeView === 'trader' && <TraderProfile />}
            {activeView === 'notifications' && <NotificationCenter />}
            {activeView === 'logs' && <WhatsAppLogs />}
            {activeView === 'settings' && <div className="p-8 text-center text-gray-500">Settings Configuration</div>}
          </div>
        </div>
      </main>
    </div>
  );
}