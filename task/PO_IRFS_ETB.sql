select
substring(po.buyer_purchase_order_nr,1,22) as [PO Number],
isnull(po.currency_id,'') as [Currency],
po.total_po_amount as [PO Amount],
cast(po.document_date as date) as [Document Date],
cast(po.entry_date as date) as [Download Date],
isnull(po.sales_order_number,'') as [SO Number],
po.external_buyer_id as [Buyer External ID],
po.external_vendor_id as [Vendor External ID],
p.program_code as [Program],
isnull(ls.description, '') as [Limit Status],
isnull(po.response_code, 0) as [Limit Approval Number],
t.description as [Status],
srt.description as [Status Reason Type],
CASE WHEN po.source_edi_message_id IS NOT NULL THEN 'EDI'
ELSE 'Manual' END as [Upload] 
from purchaseorder po with (nolock)
left join buyer b with (nolock) on po.buyer_id = b.buyer_id 
left join vendor_ext_ident v with (nolock) on po.vendor_ext_ident_id = v.vendor_ext_ident_id
left join program p with (nolock) on b.program_id = p.program_id and v.program_id = p.program_id
left join type t with (nolock) on po.status_id = t.type_id
left join status_reason_type srt with (nolock) on po.status_reason_type_id = srt.status_reason_type_id
left join limit_status ls with (nolock) on po.limit_status_id = ls.limit_status_id
where
po.entry_date between DATEADD(DAY, -10, getdate()) and DATEADD(DAY, 2, getdate())