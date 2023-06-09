import { ListingImage } from "./interfaces.d";
export interface CityData {
  id: number;
  name: string;
  city_image: string;
  modified_at: Date;
  created_at: Date;
}

export interface RegionData {
  id: number;
  city: string;
  name: string;
  modified_at: Date;
  created_at: Date;
  fk_city: number;
  parent: number | undefined;
}

export interface PropertyUSP {
  id: number;
  name: string;
  modified_at: Date;
  created_at: Date;
}

export interface BuilderData {
  id: number;
  name: string;
  description: string;
  modified_at: Date;
  created_at: Date;
}

export interface ListingImage {
  id: number;
  name: string;
  fk_listing: number;
  modified_at: Date;
  created_at: Date;
}

export interface ListingVideo {
  id: number;
  name: string;
  fk_listing: number;
  modified_at: Date;
  created_at: Date;
}

export interface ListingData {
  display_image: string;
  id: number | undefined | null;
  name: string;
  dealer_approved: boolean;
  property_usp: PropertyUSP[] | [];
  listing_image: ListingImage[] | [];
  listing_video: ListingVideo[] | [];
  premium_amount: number | undefined | null;
  fk_builder: BuilderData | undefined | null;
  fk_region: RegionData | undefined | null;
  modified_at: Date | undefined | null;
  created_at: Date | undefined | null;
}

interface ErrorNotFoundMessage {
  Message: string;
}

export interface UserData {
  name: string;
  alt_name: string;
  email: string;
  alt_email: string;
  phone_number: string;
  alt_phone_number: string;
}

export interface FilterListingData {
  item: ListingData;
  refIndex: number;
}

export interface TokenData {
  refresh: string;
  access: string;
}

export interface toVerifyTime {
  verify: Boolean;
  ttl: string;
}

export interface ListingData {
  id: number;
  name: string;
  city: string;
  region: string;
}

export interface CouponData {
  id: number;
  name: string;
  fk_user: number;
  fk_listing: number;
  listing_data: ListingData;
  fk_payment_request?: any;
  is_paid: boolean;
  is_premium: boolean;
  is_expired: boolean;
  expiration_date: string;
  modified_at: Date | null;
  created_at: Date | null;
}
export interface AuthFieldError {
  name?: string;
  email?: string;
  altEmail?: string;
  phoneNumber?: string;
  altPhoneNumber?: string;
  userExists?: string;
  userDoesntExists?: string;
}
