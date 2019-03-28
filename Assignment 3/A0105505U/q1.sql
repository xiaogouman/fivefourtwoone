copy (select xmlroot(
	xmlelement(name warehouses,
		(select xmlagg(x) from 
			(select xmlelement (name warehouse,
					  xmlelement(name id, w.w_id),
					  xmlelement(name name, w.w_name),
					  xmlelement(name address,
							 xmlelement(name street, w.w_street),
							 xmlelement(name city, w.w_city),
							 xmlelement(name country, w.w_country)),
					  xmlelement(name items,
							xmlagg(xmlelement(name item,
								xmlelement(name id, i.i_id),
								xmlelement(name im_id, i.i_im_id),
								xmlelement(name name, i.i_name),
								xmlelement(name price, i.i_price),
								xmlelement(name qty, s.s_qty))))) x
		from warehouse w, stock s, item i
		where w.w_id = s.w_id and i.i_id = s.i_id
		group by w.w_id) as tab))
,version '1.0'))
to '/home/cs4221/Shared/q1.xml';