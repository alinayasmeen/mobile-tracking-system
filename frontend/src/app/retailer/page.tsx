'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/lib/auth-context';
import { useRouter } from 'next/navigation';
import { retailerAPI } from '@/lib/api';
import { RetailerPurchase } from '@/types';
import { ShoppingCart, LogOut, Plus, X, Package } from 'lucide-react';
import Button from '@/components/Button';
import Input from '@/components/Input';
import Card from '@/components/Card';
import Loading from '@/components/Loading';
import toast from 'react-hot-toast';

export default function RetailerDashboard() {
  const { user, loading: authLoading, logout } = useAuth();
  const router = useRouter();
  
  const [purchases, setPurchases] = useState<RetailerPurchase[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'purchase' | 'received'>('purchase');
  const [showModal, setShowModal] = useState(false);
  
  const [purchaseForm, setPurchaseForm] = useState({
    customer_cnic: '', customer_email: '', phone_imei: '', phone_brand: '', phone_model: '', phone_emails: ['']
  });

  const [receivedForm, setReceivedForm] = useState({
    seller_cnic: '', phone_imei: '', phone_brand: '', phone_model: '', phone_emails: ['']
  });

  useEffect(() => {
    if (!authLoading && (!user || user.role !== 'retailer')) {
      router.push('/login');
    } else if (user) {
      loadPurchases();
    }
  }, [user, authLoading, router]);

  const loadPurchases = async () => {
    try {
      const response = await retailerAPI.getPurchases();
      setPurchases(response.data);
    } catch (error) {
      toast.error('Failed to load purchases');
    } finally {
      setLoading(false);
    }
  };

  const handlePurchaseSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await retailerAPI.registerPurchase({
        ...purchaseForm,
        phone_emails: purchaseForm.phone_emails.filter(e => e),
      });
      toast.success('Purchase registered successfully!');
      setShowModal(false);
      setPurchaseForm({ customer_cnic: '', customer_email: '', phone_imei: '', phone_brand: '', phone_model: '', phone_emails: [''] });
      loadPurchases();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to register purchase');
    }
  };

  const handleReceivedSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await retailerAPI.submitReceivedPhone({
        ...receivedForm,
        phone_emails: receivedForm.phone_emails.filter(e => e),
      });
      toast.success('Received phone submitted successfully!');
      setShowModal(false);
      setReceivedForm({ seller_cnic: '', phone_imei: '', phone_brand: '', phone_model: '', phone_emails: [''] });
      loadPurchases();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to submit received phone');
    }
  };

  if (authLoading || loading) return <Loading />;
  if (!user) return null;

  return (
    <div className="min-h-screen pb-12">
      <div className="bg-gradient-to-r from-success-600 to-success-800 text-white p-6 shadow-lg">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">Retailer Dashboard</h1>
            <p className="text-success-100 mt-1">Welcome back, {user.email}</p>
          </div>
          <Button variant="secondary" onClick={logout}>
            <LogOut className="w-4 h-4" />
            Logout
          </Button>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 mt-8">
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <Card className="p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-success-100 rounded-xl flex items-center justify-center">
                <ShoppingCart className="w-6 h-6 text-success-600" />
              </div>
              <div>
                <p className="text-gray-600 text-sm">Total Purchases</p>
                <p className="text-2xl font-bold">{purchases.length}</p>
              </div>
            </div>
          </Card>
          <Card className="p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-warning-100 rounded-xl flex items-center justify-center">
                <Package className="w-6 h-6 text-warning-600" />
              </div>
              <div>
                <p className="text-gray-600 text-sm">Received Phones</p>
                <p className="text-2xl font-bold">{purchases.filter(p => p.seller_cnic).length}</p>
              </div>
            </div>
          </Card>
        </div>

        <div className="flex gap-2 mb-6">
          <button onClick={() => setActiveTab('purchase')} className={`px-6 py-3 rounded-xl font-semibold transition-all ${activeTab === 'purchase' ? 'bg-success-600 text-white shadow-lg' : 'bg-white text-gray-600 hover:bg-gray-100'}`}>
            Register Purchase
          </button>
          <button onClick={() => setActiveTab('received')} className={`px-6 py-3 rounded-xl font-semibold transition-all ${activeTab === 'received' ? 'bg-success-600 text-white shadow-lg' : 'bg-white text-gray-600 hover:bg-gray-100'}`}>
            Received Phone
          </button>
        </div>

        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Purchase History</h2>
          <Button onClick={() => setShowModal(true)}>
            <Plus className="w-5 h-5" />
            {activeTab === 'purchase' ? 'New Purchase' : 'Submit Received'}
          </Button>
        </div>

        <div className="space-y-4">
          {purchases.map((purchase) => (
            <Card key={purchase.id} className="p-6">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <h3 className="text-lg font-bold mb-2">{purchase.phone_brand} {purchase.phone_model}</h3>
                  <p className="text-sm text-gray-600">IMEI: {purchase.phone_imei}</p>
                  <p className="text-sm text-gray-600">Emails: {purchase.phone_emails.join(', ') || 'None'}</p>
                </div>
                <div>
                  {purchase.seller_cnic ? (
                    <>
                      <p className="text-sm text-gray-600"><span className="font-semibold">Seller CNIC:</span> {purchase.seller_cnic}</p>
                      <p className="text-sm bg-warning-100 text-warning-700 px-3 py-1 rounded-lg inline-block mt-2">Received Phone</p>
                    </>
                  ) : (
                    <>
                      <p className="text-sm text-gray-600"><span className="font-semibold">Customer:</span> {purchase.customer_email}</p>
                      <p className="text-sm text-gray-600"><span className="font-semibold">CNIC:</span> {purchase.customer_cnic}</p>
                    </>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>

        {purchases.length === 0 && (
          <Card className="p-12 text-center">
            <ShoppingCart className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No purchases recorded yet</p>
          </Card>
        )}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-md p-6 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">{activeTab === 'purchase' ? 'Register Purchase' : 'Submit Received Phone'}</h2>
              <Button onClick={() => setShowModal(false)}><X className="w-6 h-6" /></Button>
            </div>
            {activeTab === 'purchase' ? (
              <form onSubmit={handlePurchaseSubmit} className="space-y-4">
                <Input label="Customer CNIC (13 digits)" value={purchaseForm.customer_cnic} onChange={(e) => setPurchaseForm({...purchaseForm, customer_cnic: e.target.value.replace(/\D/g, '').slice(0, 13)})} maxLength={13} required />
                <Input label="Customer Email" type="email" value={purchaseForm.customer_email} onChange={(e) => setPurchaseForm({...purchaseForm, customer_email: e.target.value})} required />
                <Input label="Phone IMEI (15 digits)" value={purchaseForm.phone_imei} onChange={(e) => setPurchaseForm({...purchaseForm, phone_imei: e.target.value.replace(/\D/g, '').slice(0, 15)})} maxLength={15} required />
                <Input label="Phone Brand" value={purchaseForm.phone_brand} onChange={(e) => setPurchaseForm({...purchaseForm, phone_brand: e.target.value})} required />
                <Input label="Phone Model" value={purchaseForm.phone_model} onChange={(e) => setPurchaseForm({...purchaseForm, phone_model: e.target.value})} required />
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Phone Emails</label>
                  {purchaseForm.phone_emails.map((email, i) => (
                    <Input key={i} type="email" value={email} onChange={(e) => {
                      const emails = [...purchaseForm.phone_emails];
                      emails[i] = e.target.value;
                      setPurchaseForm({...purchaseForm, phone_emails: emails});
                    }} className="mb-2" />
                  ))}
                  <Button type="button" size="sm" variant="outline" onClick={() => setPurchaseForm({...purchaseForm, phone_emails: [...purchaseForm.phone_emails, '']})}>+ Add Email</Button>
                </div>
                <Button type="submit" className="w-full">Register Purchase</Button>
              </form>
            ) : (
              <form onSubmit={handleReceivedSubmit} className="space-y-4">
                <Input label="Seller CNIC (13 digits)" value={receivedForm.seller_cnic} onChange={(e) => setReceivedForm({...receivedForm, seller_cnic: e.target.value.replace(/\D/g, '').slice(0, 13)})} maxLength={13} required />
                <Input label="Phone IMEI (15 digits)" value={receivedForm.phone_imei} onChange={(e) => setReceivedForm({...receivedForm, phone_imei: e.target.value.replace(/\D/g, '').slice(0, 15)})} maxLength={15} required />
                <Input label="Phone Brand" value={receivedForm.phone_brand} onChange={(e) => setReceivedForm({...receivedForm, phone_brand: e.target.value})} required />
                <Input label="Phone Model" value={receivedForm.phone_model} onChange={(e) => setReceivedForm({...receivedForm, phone_model: e.target.value})} required />
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Phone Emails</label>
                  {receivedForm.phone_emails.map((email, i) => (
                    <Input key={i} type="email" value={email} onChange={(e) => {
                      const emails = [...receivedForm.phone_emails];
                      emails[i] = e.target.value;
                      setReceivedForm({...receivedForm, phone_emails: emails});
                    }} className="mb-2" />
                  ))}
                  <Button type="button" size="sm" variant="outline" onClick={() => setReceivedForm({...receivedForm, phone_emails: [...receivedForm.phone_emails, '']})}>+ Add Email</Button>
                </div>
                <Button type="submit" className="w-full">Submit Received Phone</Button>
              </form>
            )}
          </Card>
        </div>
      )}
    </div>
  );
}
