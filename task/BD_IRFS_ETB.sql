select distinct
bd.external_billing_doc_nr as [Billing Document Number],
bdt.description as [Doc Type],
cast(bd.external_billing_doc_date as date) as [Issue Date],
cast(bd.entry_date as date) as [Download Date],
bd.external_buyer_id as [Buyer External ID],
bd.external_vendor_id as [Vendor External ID],
isnull(bd.currency_id,'') as [Currency],
bd.gross_amount as [Gross Amount],
bd.vat_amount as [Tax Amount],
isnull(po.buyer_purchase_order_nr,'') as [PO Number],
isnull(po.sales_order_number,'') as [SO Number],
isnull(p.program_code,'') as [Program],
s.description as [Status],
srt.description as [Status Reason Type],
isnull(ls.description, '') as [Limit Status],
CASE WHEN bd.edi_id IS NOT NULL THEN 'EDI'
 ELSE 'Manual' END as [Upload] 

from billing_document bd 
left join purchaseorder po on bd.external_purchaseorder_nr = po.buyer_purchase_order_nr
left join buyer b on bd.buyer_id = b.buyer_id 
left join vendor_ext_ident v on bd.vendor_ext_ident_id = v.vendor_ext_ident_id
left join program p on b.program_id = p.program_id and v.program_id = p.program_id
left join status s on bd.status_id = s.status_id
left join status_reason_type srt on bd.status_reason_type_id = srt.status_reason_type_id
left join limit_status ls on bd.limit_status_id = ls.limit_status_id
left join billing_document_type bdt on bd.bill_doc_type_id = bdt.bill_doc_type_id
where 
bd.entry_date between DATEADD(DAY, -9, getdate()) and DATEADD(DAY, -0, getdate())