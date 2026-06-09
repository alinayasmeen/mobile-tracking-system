'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/lib/auth-context';
import { useRouter } from 'next/navigation';
import { adminAPI } from '@/lib/api';
import { User, Phone, Report, TransferRequest, RetailerPurchase, AdminStats, Match } from '@/types';
import { Users, Smartphone, AlertTriangle, TrendingUp, LogOut, CheckCircle, XCircle } from 'lucide-react';
import Button from '@/components/Button';
import Card from '@/components/Card';
import Badge from '@/components/Badge';
import Loading from '@/components/Loading';
import toast from 'react-hot-toast';

export default function AdminDashboard() {
  const { user, loading: authLoading, logout } = useAuth();
  const router = useRouter();
  
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [phones, setPhones] = useState<Phone[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [purchases, setPurchases] = useState<RetailerPurchase[]>([]);
  const [transfers, setTransfers] = useState<TransferRequest[]>([]);
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'stats' | 'users' | 'phones' | 'reports' | 'transfers' | 'matches'>('stats');

  useEffect(() => {
    if (!authLoading && (!user || user.role !== 'admin')) {
      router.push('/login');
    } else if (user) {
      loadData();
    }
  }, [user, authLoading, router]);

  const loadData = async () => {
    try {
      const [statsRes, usersRes, phonesRes, reportsRes, purchasesRes, transfersRes, matchesRes] = await Promise.all([
        adminAPI.getStats(),
        adminAPI.getUsers(),
        adminAPI.getPhones(),
        adminAPI.getReports(),
        adminAPI.getPurchases(),
        adminAPI.getTransferRequests(),
        adminAPI.getMatches(),
      ]);
      
      setStats(statsRes.data);
      setUsers(usersRes.data);
      setPhones(phonesRes.data);
      setReports(reportsRes.data);
      setPurchases(purchasesRes.data);
      setTransfers(transfersRes.data);
      setMatches(matchesRes.data);
    } catch (error) {
      toast.error('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateReportStatus = async (reportId: number, status: string) => {
    try {
      await adminAPI.updateReportStatus(reportId, status);
      toast.success('Report status updated!');
      loadData();
    } catch (error) {
      toast.error('Failed to update report status');
    }
  };

  const handleUpdateTransfer = async (transferId: number, status: string, notes?: string) => {
    try {
      await adminAPI.updateTransferStatus(transferId, { status, admin_notes: notes });
      toast.success('Transfer status updated!');
      loadData();
    } catch (error) {
      toast.error('Failed to update transfer status');
    }
  };

  const getStatusBadge = (status: string) => {
    const variants: any = {
      pending: 'warning', verified: 'info', matched: 'danger', cleared: 'success',
      approved: 'success', rejected: 'danger', active: 'success', lost: 'warning', snatched: 'danger',
    };
    return <Badge variant={variants[status] || 'default'}>{status.toUpperCase()}</Badge>;
  };

  if (authLoading || loading) return <Loading />;
  if (!user || !stats) return null;

  return (
    <div className="min-h-screen pb-12">
      <div className="bg-gradient-to-r from-purple-600 to-purple-800 text-white p-6 shadow-lg">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">Admin Dashboard</h1>
            <p className="text-purple-100 mt-1">System Management & Monitoring</p>
          </div>
          <Button variant="secondary" onClick={logout}>
            <LogOut className="w-4 h-4" />
            Logout
          </Button>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 mt-8">
        {/* Stats Overview */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          {[
            { icon: <Users className="w-6 h-6" />, label: 'Total Users', value: stats.total_users, color: 'primary' },
            { icon: <Smartphone className="w-6 h-6" />, label: 'Registered Phones', value: stats.total_phones, color: 'success' },
            { icon: <AlertTriangle className="w-6 h-6" />, label: 'Active Reports', value: stats.pending_reports, color: 'danger' },
            { icon: <TrendingUp className="w-6 h-6" />, label: 'Matched Cases', value: stats.matched_reports, color: 'warning' },
          ].map((stat, i) => (
            <Card key={i} className="p-6">
              <div className="flex items-center gap-4">
                <div className={`w-12 h-12 bg-${stat.color}-100 rounded-xl flex items-center justify-center text-${stat.color}-600`}>
                  {stat.icon}
                </div>
                <div>
                  <p className="text-gray-600 text-sm">{stat.label}</p>
                  <p className="text-2xl font-bold">{stat.value}</p>
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* Alert Cards */}
        {(stats.matched_reports > 0 || stats.pending_transfers > 0) && (
          <div className="grid md:grid-cols-2 gap-6 mb-8">
            {stats.matched_reports > 0 && (
              <Card className="p-6 border-2 border-danger-200 bg-danger-50">
                <div className="flex items-start gap-4">
                  <AlertTriangle className="w-6 h-6 text-danger-600 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-bold text-danger-900 mb-1">IMEI Matches Found!</h3>
                    <p className="text-sm text-danger-700">{stats.matched_reports} stolen devices found in retailer records</p>
                    <Button size="sm" variant="danger" className="mt-3" onClick={() => setActiveTab('matches')}>
                      View Matches
                    </Button>
                  </div>
                </div>
              </Card>
            )}
            {stats.pending_transfers > 0 && (
              <Card className="p-6 border-2 border-warning-200 bg-warning-50">
                <div className="flex items-start gap-4">
                  <AlertTriangle className="w-6 h-6 text-warning-600 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-bold text-warning-900 mb-1">Pending Transfer Requests</h3>
                    <p className="text-sm text-warning-700">{stats.pending_transfers} ownership transfers awaiting approval</p>
                    <Button size="sm" className="mt-3 bg-warning-600 hover:bg-warning-700" onClick={() => setActiveTab('transfers')}>
                      Review Transfers
                    </Button>
                  </div>
                </div>
              </Card>
            )}
          </div>
        )}

        {/* Tabs */}
        <div className="flex flex-wrap gap-2 mb-6">
          {['stats', 'users', 'phones', 'reports', 'transfers', 'matches'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab as any)}
              className={`px-6 py-3 rounded-xl font-semibold transition-all ${
                activeTab === tab ? 'bg-purple-600 text-white shadow-lg' : 'bg-white text-gray-600 hover:bg-gray-100'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {/* Stats Tab */}
        {activeTab === 'stats' && (
          <div className="space-y-6">
            <Card className="p-6">
              <h3 className="text-xl font-bold mb-4">System Statistics</h3>
              <div className="grid md:grid-cols-3 gap-4">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Citizens</p>
                  <p className="text-2xl font-bold text-primary-600">{stats.total_citizens}</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Retailers</p>
                  <p className="text-2xl font-bold text-success-600">{stats.total_retailers}</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Total Purchases</p>
                  <p className="text-2xl font-bold text-warning-600">{stats.total_purchases}</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Snatched Reports</p>
                  <p className="text-2xl font-bold text-danger-600">{stats.snatched_reports}</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Matched Cases</p>
                  <p className="text-2xl font-bold text-danger-600">{stats.matched_reports}</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Pending Reports</p>
                  <p className="text-2xl font-bold text-warning-600">{stats.pending_reports}</p>
                </div>
              </div>
            </Card>
          </div>
        )}

        {/* Users Tab */}
        {activeTab === 'users' && (
          <div>
            <h2 className="text-2xl font-bold mb-6">All Users</h2>
            <div className="space-y-4">
              {users.filter(u => u.role !== 'admin').map((u) => (
                <Card key={u.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-bold">{u.email}</h3>
                      <p className="text-sm text-gray-600">CNIC: {u.cnic}</p>
                      {u.ntn && <p className="text-sm text-gray-600">NTN: {u.ntn}</p>}
                    </div>
                    <Badge variant={u.role === 'retailer' ? 'success' : 'info'}>{u.role.toUpperCase()}</Badge>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Phones Tab */}
        {activeTab === 'phones' && (
          <div>
            <h2 className="text-2xl font-bold mb-6">All Registered Phones</h2>
            <div className="grid md:grid-cols-2 gap-4">
              {phones.map((phone) => (
                <Card key={phone.id} className="p-6">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="font-bold">{phone.brand} {phone.model}</h3>
                      <p className="text-sm text-gray-600">IMEI: {phone.imei}</p>
                      <p className="text-sm text-gray-600">Owner ID: {phone.owner_id}</p>
                    </div>
                    {getStatusBadge(phone.status)}
                  </div>
                  <p className="text-sm text-gray-600">SIMs: {phone.sim_numbers.join(', ') || 'None'}</p>
                  <p className="text-sm text-gray-600">Emails: {phone.emails.join(', ') || 'None'}</p>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Reports Tab */}
        {activeTab === 'reports' && (
          <div>
            <h2 className="text-2xl font-bold mb-6">All Reports</h2>
            <div className="space-y-4">
              {reports.map((report) => (
                <Card key={report.id} className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="font-bold">{report.phone?.brand} {report.phone?.model}</h3>
                        <Badge variant={report.report_type === 'snatched' ? 'danger' : 'warning'}>
                          {report.report_type.toUpperCase()}
                        </Badge>
                        {getStatusBadge(report.status)}
                      </div>
                      <p className="text-sm text-gray-600">IMEI: {report.phone?.imei}</p>
                      <p className="text-sm text-gray-600">Citizen ID: {report.citizen_id}</p>
                      {report.description && <p className="text-sm mt-2">{report.description}</p>}
                      {report.culprit_description && (
                        <div className="bg-danger-50 p-3 rounded-lg mt-2">
                          <p className="text-sm font-semibold text-danger-700">Culprit: {report.culprit_description}</p>
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    {report.status === 'pending' && (
                      <>
                        <Button size="sm" onClick={() => handleUpdateReportStatus(report.id, 'verified')}>Verify</Button>
                        <Button size="sm" variant="danger" onClick={() => handleUpdateReportStatus(report.id, 'cleared')}>Clear</Button>
                      </>
                    )}
                    {report.status === 'matched' && (
                      <Button size="sm" variant="success" onClick={() => handleUpdateReportStatus(report.id, 'cleared')}>Mark Cleared</Button>
                    )}
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Transfers Tab */}
        {activeTab === 'transfers' && (
          <div>
            <h2 className="text-2xl font-bold mb-6">Transfer Requests</h2>
            <div className="space-y-4">
              {transfers.map((transfer) => (
                <Card key={transfer.id} className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <h3 className="font-bold mb-2">{transfer.phone?.brand} {transfer.phone?.model}</h3>
                      <p className="text-sm text-gray-600">From Citizen ID: {transfer.from_citizen_id}</p>
                      <p className="text-sm text-gray-600">To CNIC: {transfer.to_citizen_cnic}</p>
                      <p className="text-sm text-gray-600">To Email: {transfer.to_citizen_email}</p>
                      {transfer.admin_notes && <p className="text-sm mt-2 text-gray-700">Notes: {transfer.admin_notes}</p>}
                    </div>
                    {getStatusBadge(transfer.status)}
                  </div>
                  {transfer.status === 'pending' && (
                    <div className="flex gap-2">
                      <Button size="sm" variant="success" onClick={() => handleUpdateTransfer(transfer.id, 'approved', 'Transfer approved by admin')}>
                        <CheckCircle className="w-4 h-4" />
                        Approve
                      </Button>
                      <Button size="sm" variant="danger" onClick={() => handleUpdateTransfer(transfer.id, 'rejected', 'Transfer rejected by admin')}>
                        <XCircle className="w-4 h-4" />
                        Reject
                      </Button>
                    </div>
                  )}
                </Card>
              ))}
            </div>
            {transfers.length === 0 && (
              <Card className="p-12 text-center">
                <p className="text-gray-600">No transfer requests</p>
              </Card>
            )}
          </div>
        )}

        {/* Matches Tab */}
        {activeTab === 'matches' && (
          <div>
            <h2 className="text-2xl font-bold mb-6">IMEI Matches (Stolen Devices Found)</h2>
            <div className="space-y-6">
              {matches.map((match) => (
                <Card key={match.report.id} className="p-6 border-2 border-danger-300 bg-danger-50">
                  <div className="bg-white rounded-lg p-4 mb-4">
                    <h3 className="text-lg font-bold text-danger-700 mb-3">⚠️ MATCH FOUND</h3>
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold mb-2">Snatched Report</h4>
                        <p className="text-sm"><span className="font-semibold">Phone:</span> {match.phone.brand} {match.phone.model}</p>
                        <p className="text-sm"><span className="font-semibold">IMEI:</span> {match.phone.imei}</p>
                        <p className="text-sm"><span className="font-semibold">Citizen:</span> {match.citizen?.email}</p>
                        <p className="text-sm"><span className="font-semibold">Report Type:</span> {match.report.report_type}</p>
                        {match.report.culprit_description && (
                          <p className="text-sm mt-2 p-2 bg-danger-100 rounded"><span className="font-semibold">Culprit:</span> {match.report.culprit_description}</p>
                        )}
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Retailer Purchase</h4>
                        <p className="text-sm"><span className="font-semibold">Retailer:</span> {match.retailer?.email}</p>
                        <p className="text-sm"><span className="font-semibold">Retailer CNIC:</span> {match.retailer?.cnic}</p>
                        <p className="text-sm"><span className="font-semibold">Retailer NTN:</span> {match.retailer?.ntn}</p>
                        {match.purchase.seller_cnic ? (
                          <p className="text-sm"><span className="font-semibold">Seller CNIC:</span> {match.purchase.seller_cnic}</p>
                        ) : (
                          <>
                            <p className="text-sm"><span className="font-semibold">Customer:</span> {match.purchase.customer_email}</p>
                            <p className="text-sm"><span className="font-semibold">Customer CNIC:</span> {match.purchase.customer_cnic}</p>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button size="sm" variant="success" onClick={() => handleUpdateReportStatus(match.report.id, 'cleared')}>
                      Mark as Resolved
                    </Button>
                  </div>
                </Card>
              ))}
            </div>
            {matches.length === 0 && (
              <Card className="p-12 text-center">
                <CheckCircle className="w-16 h-16 text-success-500 mx-auto mb-4" />
                <p className="text-gray-600">No IMEI matches found</p>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
