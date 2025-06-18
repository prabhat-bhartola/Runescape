import { RunescapeBaseSchema } from "./base_model";
import { PriceRead } from "./price";

export interface ItemRead extends RunescapeBaseSchema {
  id: string;
  name: string;
  examine: string;
  limit?: number;
  members: boolean;
  lowalch?: number;
  value: number;
  highalch?: number;
  icon: string;
  price?: PriceRead;
}
