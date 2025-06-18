import { RunescapeBaseSchema } from "./base_model";
import { Price } from "./price";

export interface Item extends RunescapeBaseSchema {
  id: string;
  name: string;
  examine: string;
  limit?: number;
  members: boolean;
  lowalch?: number;
  value: number;
  highalch?: number;
  icon: string;
  price?: Price;
}
