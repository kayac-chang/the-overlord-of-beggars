import { clsx, ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { z } from "zod";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

function searchParamsToValues(
  searchParams: URLSearchParams
): Record<string, any> {
  return Array.from(searchParams.keys()).reduce((record, key) => {
    const values = searchParams.getAll(key);
    return { ...record, [key]: values.length > 1 ? values : values[0] };
  }, {} as Record<string, any>);
}

export function makeSearchParamsObjSchema<
  Schema extends z.ZodObject<z.ZodRawShape>
>(schema: Schema) {
  return z
    .instanceof(URLSearchParams)
    .transform(searchParamsToValues)
    .pipe(schema);
}

export function coerceToArray<Schema extends z.ZodArray<z.ZodTypeAny>>(
  schema: Schema
) {
  return z.union([z.any().array(), z.any().transform((x) => [x])]).pipe(schema);
}
