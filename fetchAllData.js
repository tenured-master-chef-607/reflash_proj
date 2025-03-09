import { supabase } from './supabaseClient.js';

const fetchData = async (tableName) => {
    try {
        if (!tableName) {
            throw new Error("Table name is required");
        }

        const { data: tableData, error: tableError } = await supabase
            .from(tableName)  
            .select('*');

        if (tableError) throw tableError;

        console.log(JSON.stringify({ [tableName]: tableData }));

    } catch (error) {
        console.error('Error fetching data:', error.message);
        console.log(JSON.stringify({ [tableName]: [] }));
    }
};

const tableName = process.argv[2]?.replace(/^"|"$/g, '') || '';
fetchData(tableName);
