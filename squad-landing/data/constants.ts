export const MACRO_DATA = {
  totalVolume: 125430000, 
  activeTraders: 14205,
  creditDisbursed: 45000000,
  recentTransactions: [
    { id: 'TRX-01', type: 'WhatsApp Payment', amount: 5000, sector: 'Transport', time: 'Just now', status: 'Cleared' },
    { id: 'TRX-02', type: 'Squad Transfer', amount: 12500, sector: 'Food', time: '2m ago', status: 'Cleared' },
    { id: 'TRX-03', type: 'Loan Repayment', amount: 2500, sector: 'Retail', time: '5m ago', status: 'Processing' },
    { id: 'TRX-04', type: 'Gig Payment', amount: 18000, sector: 'Services', time: '12m ago', status: 'Cleared' },
  ],
  sectorData: [
    { name: 'Food & Provision', value: 45, color: 'bg-blue-600' },
    { name: 'Transport (Danfo/Okada)', value: 30, color: 'bg-indigo-600' },
    { name: 'Artisans & Repairs', value: 15, color: 'bg-sky-500' },
    { name: 'Retail', value: 10, color: 'bg-slate-400' },
  ]
};

export const MOCK_TRADER = {
  id: 'TRD-8821',
  name: 'Iya Basira Canteen',
  owner: 'Basirat Adeyemi',
  phone: '+234 803 *** **21',
  location: 'Yaba, Lagos',
  businessType: 'Food Vendor',
  trustScore: 84,
  monthlyRevenue: 850000,
  bvnVerified: true,
  aiAnalysis: "Consistent daily inflows between 12PM-3PM (lunch rush). Customer retention is high (40% repeat payers via WhatsApp/Squad). Revenue growth slope is positive (+12% MoM). Recommended for a ₦150,000 working capital loan with low risk.",
  revenueHistory: [450, 520, 480, 610, 750, 850] 
};


