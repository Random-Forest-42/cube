SELECT *
FROM competitions
where
id = 'wc2025'
limit 100

el id parece el mismo que el de la url

SELECT *
FROM competition_events
where
competition_id = 'wc2025'

limit 100

and event_id = '333'
125048 es el id de 333 de wca 2025


#	id	name	city_name	country_id	information	venue	venue_address	venue_details	external_website	cell_name	show_at_all	latitude	longitude	contact	remarks	registration_open	registration_close	use_wca_registration	guests_enabled	results_posted_at	results_nag_sent_at	generate_website	announced_at	base_entry_fee_lowest_denomination	currency_code	connected_stripe_account_id	start_date	end_date	enable_donations	competitor_limit_enabled	competitor_limit	competitor_limit_reason	extra_registration_requirements	on_the_spot_registration	on_the_spot_entry_fee_lowest_denomination	refund_policy_percent	refund_policy_limit_date	guests_entry_fee_lowest_denomination	created_at	updated_at	results_submitted_at	early_puzzle_submission	early_puzzle_submission_reason	qualification_results	qualification_results_reason	name_reason	external_registration_page	confirmed_at	event_restrictions	event_restrictions_reason	registration_reminder_sent_at	announced_by	results_posted_by	main_event_id	cancelled_at	cancelled_by	waiting_list_deadline_date	event_change_deadline_date	guest_entry_status	allow_registration_edits	competition_series_id	use_wca_live_for_scoretaking	allow_registration_without_qualification	guests_per_registration_limit	events_per_registration_limit	force_comment_in_registration	posting_by	forbid_newcomers	forbid_newcomers_reason	competitor_can_cancel	newcomer_month_reserved_spots	auto_close_threshold	auto_accept_registrations	auto_accept_disable_threshold
-- 1	WC2025	Rubik's WCA World Championship 2025	Seattle, Washington	USA	We are excited to announce Rubik's WCA World Championship 2025! This will be the twelfth Rubik's Cube World Championship. **Please refer to the competition website, [cubingusa.org/worlds](https://www.cubingusa.org/worlds), for full competition details.** ![](https://www.worldcubeassociation.org/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsiZGF0YSI6MzgxMzIsInB1ciI6ImJsb2JfaWQifX0=--22c9f6aafe20797d5b78471910301fe3dcf7573a/rubiks.png) ![](https://www.worldcubeassociation.org/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsiZGF0YSI6MzgxMzcsInB1ciI6ImJsb2JfaWQifX0=--35c99a56aef69985e79641864d3437b966da72a4/wca.png)![](https://www.worldcubeassociation.org/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsiZGF0YSI6MzgxMzgsInB1ciI6ImJsb2JfaWQifX0=--a6ee67197318dd487984b236337c56f7980ce0d8/cubingusa.png)	Seattle Convention Center	705 Pike St	Arch Building	https://cubingusa.org/worlds	WCA World Championship 2025	1	47611387	-122332554	[Contact form](https://www.cubingusa.org/worlds/contact)	remarks to the board here	2025-01-03 14:00:00	2025-01-10 14:00:00	1	0			0	2024-10-08 22:00:00	12000	USD		2025-07-03	2025-07-06	0	1	2000	Our sanity.		0		50	2025-05-15 06:59:00	1500	2023-09-10 13:49:25	2025-06-03 11:48:19		1	Multi Blind cube submission.	1	Qualification times previously approved by WCAT.	Name specified in contract between CubingUSA and WCA.		2024-10-05 00:51:14	0		2025-01-02 14:00:14	19818		333			2025-05-29 06:59:00	2025-05-29 06:59:00	0	1		1	0			0		0		2			0


SELECT *
FROM registrations
where
competition_id = 'wc2025'
limit 100

user_id ? 5569, 185473, etc... no es el wca id

--- hubo gente que se registro mas pronto, mas tarde... a dedo??

SELECT
date(created_at) as date_create
, count(1)
FROM registrations
where
competition_id = 'wc2025'
group by date_create
order by 1
limit 100


registration_competition_events: los que se han registrado a un evento en especifico dentro de una competicion.

        select
            *
        from
            registration_competition_events
where
competition_event_id = '125048'
limit 100

hay 2496 filas... no cuadra

#	id	registration_id	competition_event_id
1	5682582	1005695	125048
2	5682588	1005696	125048
3	5682607	1005700	125048