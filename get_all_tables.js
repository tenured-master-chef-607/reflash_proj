//returns list of names of all tables under the database

import { supabase } from './supabaseClient.js';

const getAllTables = async () => {
  try {
    const { data, error } = await supabase.rpc('get_table_names');

    if (error) {
      console.error(JSON.stringify({ error: error.message })); 
      process.exit(1); 
    }

    const tableNames = data.map(row => row.tablename);

    console.log(JSON.stringify(tableNames));

  } catch (error) {
    console.error(JSON.stringify({ error: error.message })); 
    process.exit(1); 
  }
};

getAllTables();
