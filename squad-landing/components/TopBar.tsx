import { Search, Bell } from "lucide-react";

interface TopbarProps {
  activeView: string;
  setActiveView: (view: string) => void;
}

export const Topbar = ({ activeView, setActiveView }: TopbarProps) => (
  <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 z-10">
    <div className="text-sm font-medium text-gray-500 hidden md:block">
      {activeView === 'macro' && 'Overview / Operations'}
      {activeView === 'trader' && 'Underwriting / Assessment'}
      {activeView === 'notifications' && 'System / Alerts'}
      {activeView === 'logs' && 'System / Audit Logs'}
    </div>
    
    <div className="flex items-center space-x-3 ml-auto">
      <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-lg transition-colors">
        <Search size={18} />
      </button>
      <button 
        onClick={() => setActiveView('notifications')}
        className={`p-2 rounded-lg transition-colors relative ${activeView === 'notifications' ? 'bg-blue-50 text-blue-600' : 'text-gray-400 hover:text-gray-600 hover:bg-gray-50'}`}
      >
        <Bell size={18} />
        <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 border-2 border-white rounded-full"></span>
      </button>
    </div>
  </header>
);