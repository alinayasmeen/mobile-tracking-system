'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/lib/auth-context';
import { useRouter } from 'next/navigation';
import { citizenAPI } from '@/lib/api';
import { Phone, Report, TransferRequest } from '@/types';
import { Smartphone, AlertTriangle, Send, LogOut, Plus, X } from 'lucide-react';
import Button from '@/components/Button';
import Input from '@/components/Input';
import Card from '@/components/Card';
import Badge from '@/components/Badge';
import Loading from '@/components/Loading';
import toast from 'react-hot-toast';

export default function CitizenDashboard() {
  const { user, loading: authLoading, logout } = useAuth();
  const router = useRouter();
  
  const [phones, setPhones] = useState<Phone[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [transfers, setTransfers] = useState<TransferRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'phones' | 'reports' | 'transfer'>('phones');
  
  // Modal states
  const [showRegisterPhone, setShowRegisterPhone] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);
  const [showTransferModal, setShowTransferModal] = useState(false);
  
  // Form states
  const [phoneForm, setPhoneForm] = useState({
    brand: '', model: '', imei: '', sim_numbers: [''], emails: ['']
  });
  const [reportForm, setReportForm] = useState({
    phone_id: 0, report_type: 'lost', description: '', culprit_description: ''
  });
  const [transferForm, setTransferForm] = useState({
    phone_id: 0, to_citizen_cnic: '', to_citizen_email: ''
  });

  useEffect(() => {
    if (!authLoading && (!user || user.role !== 'citizen')) {
      router.push('/login');
    } else if (user) {
      loadData();
    }
  }, [user, authLoading, router]);

  const loadData = async () => {
    try {
      const [phonesRes, reportsRes, transfersRes] = await Promise.all([
        citizenAPI.getPhones(),
        citizenAPI.getReports(),
        citizenAPI.getTransferRequests(),
      ]);
      setPhones(phonesRes.data);
      setReports(reportsRes.data);
      setTransfers(transfersRes.data);
    } catch (error: any) {
      toast.error('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterPhone = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await citizenAPI.registerPhone({
        ...phoneForm,
        sim_numbers: phoneForm.sim_numbers.filter(s => s),
        emails: phoneForm.emails.filter(e => e),
      });
      toast.success('Phone registered successfully!');
      setShowRegisterPhone(false);
      setPhoneForm({ brand: '', model: '', imei: '', sim_numbers: [''], emails: [''] });
      loadData();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to register phone');
    }
  };

  const handleCreateReport = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await citizenAPI.createReport(reportForm);
      toast.success('Report created successfully!');
      setShowReportModal(false);
      setReportForm({ phone_id: 0, report_type: 'lost', description: '', culprit_description: '' });
      loadData();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create report');
    }
  };

  const handleCreateTransfer = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await citizenAPI.createTransferRequest(transferForm);
      toast.success('Transfer request submitted!');
      setShowTransferModal(false);
      setTransferForm({ phone_id: 0, to_citizen_cnic: '', to_citizen_email: '' });
      loadData();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create transfer request');
    }
  };

  const getStatusBadge = (status: string) => {
    const variants: any = {
      pending: 'warning',
      verified: 'info',
      matched: 'danger',
      cleared: 'success',
      approved: 'success',
      rejected: 'danger',
      active: 'success',
      lost: 'warning',
      snatched: 'danger',
    };
    return <Badge variant={variants[status] || 'default'}>{status.toUpperCase()}</Badge>;
  };

  if (authLoading || loading) return <Loading />;
  if (!user) return null;

  return (
    <div className="min-h-screen pb-12">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 text-white p-6 shadow-lg">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">Citizen Dashboard</h1>
            <p className="text-primary-100 mt-1">Welcome back, {user.email}</p>
          </div>
          <Button variant="secondary" onClick={logout} className="flex items-center gap-2">
            <LogOut className="w-4 h-4" />
            Logout
          </Button>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 mt-8">
        {/* Stats Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card className="p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
                <Smartphone className="w-6 h-6 text-primary-600" />
              </div>
              <div>
                <p className="text-gray-600 text-sm">Registered Phones</p>
                <p className="text-2xl font-bold">{phones.length}</p>
              </div>
            </div>
          </Card>
          <Card className="p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-danger-100 rounded-xl flex items-center justify-center">
                <AlertTriangle className="w-6 h-6 text-danger-600" />
              </div>
              <div>
                <p className="text-gray-600 text-sm">Active Reports</p>
                <p className="text-2xl font-bold">{reports.filter(r => r.status !== 'cleared').length}</p>
              </div>
            </div>
          </Card>
          <Card className="p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-warning-100 rounded-xl flex items-center justify-center">
                <Send className="w-6 h-6 text-warning-600" />
              </div>
              <div>
                <p className="text-gray-600 text-sm">Pending Transfers</p>
                <p className="text-2xl font-bold">{transfers.filter(t => t.status === 'pending').length}</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          {['phones', 'reports', 'transfer'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab as any)}
              className={`px-6 py-3 rounded-xl font-semibold transition-all ${
                activeTab === tab
                  ? 'bg-primary-600 text-white shadow-lg'
                  : 'bg-white text-gray-600 hover:bg-gray-100'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {/* Phones Tab */}
        {activeTab === 'phones' && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">My Phones</h2>
              <Button onClick={() => setShowRegisterPhone(true)}>
                <Plus className="w-5 h-5" />
                Register Phone
              </Button>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {phones.map((phone) => (
                <Card key={phone.id} className="p-6" hover>
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-xl font-bold">{phone.brand} {phone.model}</h3>
                      <p className="text-gray-600 text-sm mt-1">IMEI: {phone.imei}</p>
                    </div>
                    {getStatusBadge(phone.status)}
                  </div>
                  <div className="space-y-2 text-sm">
                    <p><span className="font-semibold">SIM Numbers:</span> {phone.sim_numbers.join(', ') || 'None'}</p>
                    <p><span className="font-semibold">Emails:</span> {phone.emails.join(', ') || 'None'}</p>
                  </div>
                  <div className="mt-4 flex gap-2">
                    <Button size="sm" variant="danger" onClick={() => {
                      setReportForm({ ...reportForm, phone_id: phone.id });
                      setShowReportModal(true);
                    }}>
                      Report Lost/Snatched
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => {
                      setTransferForm({ ...transferForm, phone_id: phone.id });
                      setShowTransferModal(true);
                    }}>
                      Transfer
                    </Button>
                  </div>
                </Card>
              ))}
            </div>

            {phones.length === 0 && (
              <Card className="p-12 text-center">
                <Smartphone className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No phones registered yet</p>
                <Button className="mt-4" onClick={() => setShowRegisterPhone(true)}>
                  Register Your First Phone
                </Button>
              </Card>
            )}
          </div>
        )}

        {/* Reports Tab */}
        {activeTab === 'reports' && (
          <div>
            <h2 className="text-2xl font-bold mb-6">My Reports</h2>
            <div className="space-y-4">
              {reports.map((report) => (
                <Card key={report.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        <h3 className="text-lg font-bold">
                          {report.phone?.brand} {report.phone?.model}
                        </h3>
                        <Badge variant={report.report_type === 'snatched' ? 'danger' : 'warning'}>
                          {report.report_type.toUpperCase()}
                        </Badge>
                        {getStatusBadge(report.status)}
                      </div>
                      <p className="text-gray-600 text-sm mb-2">IMEI: {report.phone?.imei}</p>
                      {report.description && <p className="text-gray-700 mb-2">{report.description}</p>}
                      {report.culprit_description && (
                        <div className="bg-danger-50 border border-danger-200 rounded-lg p-3 mt-2">
                          <p className="text-sm font-semibold text-danger-700">Culprit Description:</p>
                          <p className="text-sm text-danger-600">{report.culprit_description}</p>
                        </div>
                      )}
                      {report.status === 'matched' && (
                        <div className="bg-danger-100 border border-danger-300 rounded-lg p-3 mt-2">
                          <p className="font-semibold text-danger-700">⚠️ Match Found!</p>
                          <p className="text-sm text-danger-600">This device has been flagged in retailer records.</p>
                        </div>
                      )}
                    </div>
                  </div>
                </Card>
              ))}
            </div>
            {reports.length === 0 && (
              <Card className="p-12 text-center">
                <AlertTriangle className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No reports filed</p>
              </Card>
            )}
          </div>
        )}

        {/* Transfer Tab */}
        {activeTab === 'transfer' && (
          <div>
            <h2 className="text-2xl font-bold mb-6">Transfer Requests</h2>
            <div className="space-y-4">
              {transfers.map((transfer) => (
                <Card key={transfer.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="text-lg font-bold mb-2">
                        {transfer.phone?.brand} {transfer.phone?.model}
                      </h3>
                      <p className="text-sm text-gray-600">To: {transfer.to_citizen_email}</p>
                      <p className="text-sm text-gray-600">CNIC: {transfer.to_citizen_cnic}</p>
                      {transfer.admin_notes && (
                        <p className="text-sm text-gray-700 mt-2"><span className="font-semibold">Admin Notes:</span> {transfer.admin_notes}</p>
                      )}
                    </div>
                    {getStatusBadge(transfer.status)}
                  </div>
                </Card>
              ))}
            </div>
            {transfers.length === 0 && (
              <Card className="p-12 text-center">
                <Send className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No transfer requests</p>
              </Card>
            )}
          </div>
        )}
      </div>

      {/* Register Phone Modal */}
      {showRegisterPhone && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-md p-6 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Register Phone</h2>
              <button onClick={() => setShowRegisterPhone(false)}>
                <X className="w-6 h-6" />
              </button>
            </div>
            <form onSubmit={handleRegisterPhone} className="space-y-4">
              <Input label="Brand" value={phoneForm.brand} onChange={(e) => setPhoneForm({...phoneForm, brand: e.target.value})} required />
              <Input label="Model" value={phoneForm.model} onChange={(e) => setPhoneForm({...phoneForm, model: e.target.value})} required />
              <Input label="IMEI (15 digits)" value={phoneForm.imei} onChange={(e) => setPhoneForm({...phoneForm, imei: e.target.value.replace(/\D/g, '').slice(0, 15)})} maxLength={15} required />
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">SIM Numbers</label>
                {phoneForm.sim_numbers.map((sim, i) => (
                  <Input key={i} value={sim} onChange={(e) => {
                    const sims = [...phoneForm.sim_numbers];
                    sims[i] = e.target.value;
                    setPhoneForm({...phoneForm, sim_numbers: sims});
                  }} className="mb-2" />
                ))}
                <Button type="button" size="sm" variant="outline" onClick={() => setPhoneForm({...phoneForm, sim_numbers: [...phoneForm.sim_numbers, '']})}>+ Add SIM</Button>
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Emails</label>
                {phoneForm.emails.map((email, i) => (
                  <Input key={i} type="email" value={email} onChange={(e) => {
                    const emails = [...phoneForm.emails];
                    emails[i] = e.target.value;
                    setPhoneForm({...phoneForm, emails});
                  }} className="mb-2" />
                ))}
                <Button type="button" size="sm" variant="outline" onClick={() => setPhoneForm({...phoneForm, emails: [...phoneForm.emails, '']})}>+ Add Email</Button>
              </div>
              <Button type="submit" className="w-full">Register Phone</Button>
            </form>
          </Card>
        </div>
      )}

      {/* Report Modal */}
      {showReportModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-md p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Report Phone</h2>
              <button onClick={() => setShowReportModal(false)}><X className="w-6 h-6" /></button>
            </div>
            <form onSubmit={handleCreateReport} className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Report Type</label>
                <select value={reportForm.report_type} onChange={(e) => setReportForm({...reportForm, report_type: e.target.value})} className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-primary-500 outline-none">
                  <option value="lost">Lost</option>
                  <option value="snatched">Snatched</option>
                </select>
              </div>
              <Input label="Description" value={reportForm.description} onChange={(e) => setReportForm({...reportForm, description: e.target.value})} />
              {reportForm.report_type === 'snatched' && (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Culprit Description</label>
                  <textarea value={reportForm.culprit_description} onChange={(e) => setReportForm({...reportForm, culprit_description: e.target.value})} className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-primary-500 outline-none" rows={3} />
                </div>
              )}
              <Button type="submit" variant="danger" className="w-full">Submit Report</Button>
            </form>
          </Card>
        </div>
      )}

      {/* Transfer Modal */}
      {showTransferModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-md p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Transfer Phone</h2>
              <button onClick={() => setShowTransferModal(false)}><X className="w-6 h-6" /></button>
            </div>
            <form onSubmit={handleCreateTransfer} className="space-y-4">
              <Input label="Recipient CNIC (13 digits)" value={transferForm.to_citizen_cnic} onChange={(e) => setTransferForm({...transferForm, to_citizen_cnic: e.target.value.replace(/\D/g, '').slice(0, 13)})} maxLength={13} required />
              <Input label="Recipient Email" type="email" value={transferForm.to_citizen_email} onChange={(e) => setTransferForm({...transferForm, to_citizen_email: e.target.value})} required />
              <div className="bg-warning-50 border border-warning-200 rounded-lg p-3">
                <p className="text-sm text-warning-700">This transfer requires admin approval</p>
              </div>
              <Button type="submit" className="w-full">Submit Transfer Request</Button>
            </form>
          </Card>
        </div>
      )}
    </div>
  );
}
