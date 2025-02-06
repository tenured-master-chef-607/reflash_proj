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
  
      console.log(JSON.stringify(result));
      return result;
    } catch (error) {
      console.error('Error fetching data:', error.message);
  
      console.log(JSON.stringify({}));
      return null;
    }
  };
  

const listKeys = async () => {
  try {
    const { accountsData, balanceSheetsData } = await fetchData();

    if (!accountsData || !balanceSheetsData) {
      console.error('Failed to retrieve data for listing keys.');
      return;
    }

    const accountsKeys = accountsData.length > 0 ? Object.keys(accountsData[0]) : [];
    const balanceSheetsKeys = balanceSheetsData.length > 0 ? Object.keys(balanceSheetsData[0]) : [];

    console.log('Keys in accounting_accounts:', accountsKeys);
    console.log('Keys in accounting_balance_sheets:', balanceSheetsKeys);
  } catch (error) {
    console.error('Error listing keys:', error.message);
  }
};

fetchData();