import 'dotenv/config';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;

//console.log("SUPABASE_URL:", supabaseUrl); // Debugging: Ensure it's not undefined
//console.log("SUPABASE_KEY:", supabaseKey ? "Loaded" : "Missing"); // Avoid printing full key

export const supabase = createClient(supabaseUrl, supabaseKey);
