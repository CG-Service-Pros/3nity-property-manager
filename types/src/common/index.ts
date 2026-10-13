export * from './collections.js';
export * from './environmentvalues.js';
export * from './locales.js';
export * from './redisclient.js';
export * from './service.js';

export type ConnectionRole = 'administrator' | 'renter' | 'tenant' | 'read_only';
export type UserRole = Exclude<ConnectionRole, 'tenant' | 'read_only'>;
export type ConnectionType = 'service' | 'user' | 'application'; // 'service' is for internal services, 'user' is for users, 'application' is for external applications

export type PaymentMethod = 'transfer' | 'credit-card' | 'cash' | 'check';
export type PaymentStatus = 'paid' | 'partially-paid' | 'unpaid';
export type LeaseStatus = 'active' | 'ended' | 'terminated';
export type LeaseTimeRange = 'days' | 'weeks' | 'months' | 'years';
