select
po.buyer_purchase_order_nr as [PO Number],
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
from etb_24_01_03.dbo.purchaseorder po 
left join etb_24_01_03.dbo.buyer b on po.buyer_id = b.buyer_id 
left join etb_24_01_03.dbo.vendor_ext_ident v on po.vendor_ext_ident_id = v.vendor_ext_ident_id
left join etb_24_01_03.dbo.program p on b.program_id = p.program_id and v.program_id = p.program_id
left join etb_24_01_03.dbo.type t on po.status_id = t.type_id
left join etb_24_01_03.dbo.status_reason_type srt on po.status_reason_type_id = srt.status_reason_type_id
left join etb_24_01_03.dbo.limit_status ls on po.limit_status_id = ls.limit_status_id
where
(DATENAME(WEEKDAY, GETDATE()) = 'Monday' AND 
(cast(po.entry_date as date) = DATEADD(DAY, -3, CAST(GETDATE() as DATE)) OR 
cast(po.entry_date as date) = DATEADD(DAY, -2, CAST(GETDATE() as DATE)) OR
cast(po.entry_date as date) = DATEADD(DAY, -1, CAST(GETDATE() as DATE))))
OR (DATENAME(WEEKDAY, GETDATE()) NOT IN ('Monday') AND cast(po.entry_date as date) = DATEADD(DAY, -1, CAST(GETDATE() as DATE)))