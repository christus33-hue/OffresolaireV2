import { createClient } from '@supabase/supabase-js';

// Initialize a Supabase client on the client side.  Values come from
// environment variables prefixed with NEXT_PUBLIC_ so they are exposed to the
// browser when using Next.js.

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL as string;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY as string;

export const supabase = createClient(supabaseUrl, supabaseKey);