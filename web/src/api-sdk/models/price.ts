import { RunescapeBaseSchema } from "./base_model";

export interface PriceRead extends RunescapeBaseSchema {
  high: number;
  high_time: number;
  low: number;
  low_time: number;
}
