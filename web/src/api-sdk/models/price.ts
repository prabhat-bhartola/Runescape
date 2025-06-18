import { RunescapeBaseSchema } from "./base_model";

export interface Price extends RunescapeBaseSchema {
  high: number;
  high_time: number;
  low: number;
  low_time: number;
}

export interface PriceWS {
  id: string;
  item_id: string;
  high: number;
  high_time: number;
  low: number;
  low_time: number;
  created_at?: Date;
  updated_at?: Date;
}
