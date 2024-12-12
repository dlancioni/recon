-- DELL LATAM 15/FEB
select 
external_billing_doc_nr,
settlement_date,
maturity_date,
currency_id,
gross_amount
from billing_document
where external_billing_doc_nr = '6146880'