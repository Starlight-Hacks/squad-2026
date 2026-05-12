import { BarChart3, Users, MessageSquare, Settings } from "lucide-react";
import { Reveal } from "./Reveal";

interface SidebarProps {
  activeView: string;
  setActiveView: (view: string) => void;
}

interface IconProps{
    size?: number;
    className?: string;

}

export const Sidebar = ({ activeView, setActiveView }: SidebarProps) => {
  const NavItem = ({ id, icon: Icon, label }: { id: string; icon: React.ComponentType<IconProps>; label: string }) => (
    <button 
      onClick={() => setActiveView(id)}
      className={`w-full flex items-center px-3 py-2.5 rounded-lg transition-all text-sm font-medium ${
        activeView === id 
        ? 'bg-blue-50 text-blue-700' 
        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
      }`}
    >
      <Icon size={18} className={activeView === id ? 'text-blue-600' : 'text-gray-400'} />
      <span className="hidden lg:block ml-3">{label}</span>
    </button>
  );

  return (
    <aside className="w-16 lg:w-64 bg-white border-r border-gray-200 flex flex-col transition-all duration-300 z-20">
      <div className="h-16 flex items-center justify-center lg:justify-start lg:px-6 border-b border-gray-200">
        <div className="w-8 h-8 rounded bg-blue-600 flex items-center justify-center shadow-sm shadow-blue-600/20">
          <span className="text-white font-bold text-lg leading-none">S</span>
        </div>
        <span className="hidden lg:block ml-3 font-bold text-lg text-gray-900 tracking-tight">Identity<span className="text-blue-600">Layer</span></span>
      </div>
      
      <div className="flex-1 py-6 px-3 space-y-1">
        <div className="hidden lg:block px-3 mb-2 text-xs font-bold text-gray-400 uppercase tracking-wider">Dashboards</div>
        <NavItem id="macro" icon={BarChart3} label="Macro Intelligence" />
        <NavItem id="trader" icon={Users} label="Investment / Trader" />
        
        <div className="hidden lg:block px-3 mt-6 mb-2 text-xs font-bold text-gray-400 uppercase tracking-wider">System</div>
        <NavItem id="logs" icon={MessageSquare} label="System Logs" />
        <NavItem id="settings" icon={Settings} label="Configuration" />
      </div>
      
      <div className="p-3 border-t border-gray-200">
         <div className="flex items-center px-2 py-2 rounded-lg hover:bg-gray-50 cursor-pointer">
           <div className="w-8 h-8 rounded-full bg-gray-100 border border-gray-200 flex items-center justify-center text-gray-600 text-xs font-bold">
             OP
           </div>
           <div className="hidden lg:block ml-3">
             <p className="text-sm font-semibold text-gray-900">Ops Admin</p>
             <p className="text-xs text-gray-500">Government View</p>
           </div>
         </div>
      </div>
    </aside>
  );
};