import { DashCard as Card } from "../dashComponents/DashCard";
export const WhatsAppLogs = () => (
  <div className="space-y-6 animate-in fade-in duration-300">
    <div className="pb-4 border-b border-gray-200 flex justify-between items-center">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 tracking-tight">System Logs</h1>
        <p className="text-sm text-gray-500 mt-1">Raw webhook data from WhatsApp & Intent Parser.</p>
      </div>
      <button className="text-sm bg-white border border-gray-300 px-3 py-1.5 rounded-md font-medium text-gray-700 hover:bg-gray-50 shadow-sm">
        Export CSV
      </button>
    </div>
    <Card noPadding className="overflow-hidden">
      <table className="w-full text-left text-sm">
        <thead className="bg-gray-50 border-b border-gray-200">
          <tr>
            <th className="px-4 py-3 font-semibold text-gray-600 text-xs uppercase tracking-wider">Timestamp</th>
            <th className="px-4 py-3 font-semibold text-gray-600 text-xs uppercase tracking-wider">Source</th>
            <th className="px-4 py-3 font-semibold text-gray-600 text-xs uppercase tracking-wider">Raw Payload / Intent</th>
            <th className="px-4 py-3 font-semibold text-gray-600 text-xs uppercase tracking-wider">Status</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100 bg-white">
          {[
            { time: "14:02:11", src: "WhatsApp Cloud", payload: "abeg pay am 5k for transport", status: "Parsed" },
            { time: "14:02:12", src: "Groq LLM", payload: "{intent: 'transfer', amount: 5000, category: 'transport'}", status: "Success" },
            { time: "14:03:00", src: "Squad API", payload: "Transfer successful to Acc: 0123***", status: "Cleared" },
          ].map((log, i) => (
            <tr key={i} className="hover:bg-gray-50">
              <td className="px-4 py-3 text-gray-500 font-mono text-xs">{log.time}</td>
              <td className="px-4 py-3 font-medium text-gray-900">{log.src}</td>
              <td className="px-4 py-3 text-gray-600 truncate max-w-xs font-mono text-xs">{log.payload}</td>
              <td className="px-4 py-3">
                <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-gray-100 text-gray-700">
                  {log.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </Card>
  </div>
);