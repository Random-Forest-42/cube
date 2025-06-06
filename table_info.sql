SELECT *
FROM information_schema.tables
where
table_type = 'BASE TABLE'
order by TABLE_ROWS desc

events: los diferentes puzzles, 333, 444...
competitions:
competition_events

SELECT distinct table_catalog, table_schema, engine, table_type
FROM information_schema.tables

#	TABLE_CATALOG	TABLE_SCHEMA	ENGINE	TABLE_TYPE
1	def	information_schema		SYSTEM VIEW
2	def	performance_schema	PERFORMANCE_SCHEMA	BASE TABLE
3	def	wca_development	InnoDB	BASE TABLE
4	def	wca_development	MyISAM	BASE TABLE
