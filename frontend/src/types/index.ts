export interface User {
  id: number;
  email: string;
  role: 'citizen' | 'retailer' | 'admin';
  cnic: string;
  ntn?: string;
  shop_address?: string;
  created_at: string;
}

export interface Phone {
  id: number;
  owner_id: number;
  brand: string;
  model: string;
  imei: string;
  sim_numbers: string[];
  emails: string[];
  status: 'active' | 'lost' | 'snatched' | 'sold';
  created_at: string;
}

export interface Report {
  id: number;
  citizen_id: number;
  phone_id: number;
  phone?: Phone;
  report_type: 'lost' | 'snatched';
  description?: string;
  culprit_description?: string;
  status: 'pending' | 'verified' | 'matched' | 'cleared';
  matched_purchase_id?: number;
  created_at: string;
  updated_at: string;
}

export interface TransferRequest {
  id: number;
  from_citizen_id: number;
  to_citizen_cnic: string;
  to_citizen_email: string;
  phone_id: number;
  phone?: Phone;
  status: 'pending' | 'approved' | 'rejected';
  admin_notes?: string;
  created_at: string;
  updated_at: string;
}

export interface RetailerPurchase {
  id: number;
  retailer_id: number;
  customer_cnic: string;
  customer_email: string;
  phone_imei: string;
  phone_brand: string;
  phone_model: string;
  phone_emails: string[];
  seller_cnic?: string;
  created_at: string;
}

export interface AdminStats {
  total_users: number;
  total_citizens: number;
  total_retailers: number;
  total_phones: number;
  total_reports: number;
  snatched_reports: number;
  matched_reports: number;
  pending_reports: number;
  pending_transfers: number;
  total_purchases: number;
}

export interface Match {
  report: Report;
  purchase: RetailerPurchase;
  retailer?: User;
  citizen?: User;
  phone: Phone;
}
