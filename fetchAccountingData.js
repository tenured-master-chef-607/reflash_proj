import { supabase } from './supabaseClient.js';

const fetchData = async () => {
    try {
        const { data: accountsData, error: accountsError } = await supabase
            .from('accounting_accounts')
            .select('*');
        if (accountsError) throw accountsError;

        const { data: balanceSheetsData, error: balanceSheetsError } = await supabase
            .from('accounting_balance_sheets')
            .select('*');
        if (balanceSheetsError) throw balanceSheetsError;

        const result = { accounting_accounts: accountsData, accounting_balance_sheets: balanceSheetsData };

        // ✅ Ensure the data is logged to stdout so Python can capture it
        //console.log(JSON.stringify(result));

        return result;
    } catch (error) {
        console.error('Error fetching data:', error.message);
        console.log(JSON.stringify({})); // Ensures Python does not receive an empty string
        return null;
    }
};

// Call fetchData and ensure the result is logged
fetchData().then((data) => console.log(JSON.stringify(data)));
