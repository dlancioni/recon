-- Configurations / Buyers
select distinct
      p.program_code
	, c.short_name
	, bt.buyer_type_name
	, b.currency_id
	, b.active_from_date
	, b.active_to_date
	, c.company_name
from buyer b
	inner join company c on c.company_id = b.company_id
	inner join buyer_type bt on bt.buyer_type_id = b.buyer_type_id
	inner join program p on p.program_id = b.program_id
where p.program_code in ( 'DELAP', 'DELBR', 'DELEM', 'DELKB', 'DELKR', 'DELLA', 'DELNA' )
order by p.program_code, c.short_name;








