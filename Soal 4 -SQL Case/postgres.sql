/*Test Case 1: Channel Analysis*/
with top_country as ( 
	/*Create CTE that select top 5 countries and total revenue 
	 * that has highest total revenue */
	select 
		country,
		sum("productPrice" * "productQuantity") as totalRevenue
	from 
		dwh.public.ecommerce e 
	where "productQuantity"  notnull
	group by
		country
	order by 
		totalRevenue desc
	limit 5
	)
/* Select highest totalrevenue based on channelgroup 
 * that has country in top 5 country with highest total revenue*/
select 
	e."channelGrouping",
	sum("productPrice" * "productQuantity") as totalrevenue
from 
	dwh.public.ecommerce e 
where 
	country in (
		select 
			country 
		from 
			top_country
	)
	and "productQuantity" notnull 
group by 
	e."channelGrouping" 
order by 
	totalRevenue desc
;


-- Test Case 2: User Behavior Analysis
with usermetrics as (
	/*Create CTE that  average timeOnSite,
	 *  average pageviews, and 
	 * average sessionQualityDim for each fullVisitorId*/
	select 
		e."fullVisitorId",
		avg(e."timeOnSite") as avgtimeonsite,
		avg(e.pageviews) as avgpageviews,
		avg(e."sessionQualityDim") as avgsessionqualitydim
	from 
		dwh.public.ecommerce e
	where 
		e."timeOnSite"  notnull 
		and e."pageviews" notnull 
		and e."sessionQualityDim" notnull
	group by
	"fullVisitorId"
	)
/* Select users who spend above-average time on the site 
 * but view fewer pages than the average user from CTE usermetrics*/
SELECT
    "fullVisitorId",
    avgTimeOnSite,
    avgPageviews,
    avgSessionQualityDim
FROM
    usermetrics
WHERE
    avgTimeOnSite > (
        SELECT
            AVG(avgTimeOnSite)
        FROM
            UserMetrics
    )
    AND avgPageviews < (
        SELECT
            AVG(avgPageviews)
        FROM
            usermetrics
    );
   
   
   
-- Test Case 3: Product Performance
select 
	"v2ProductName",
	sum("productQuantity") as total_product_quantity_sold, 
	sum("productPrice" * "productQuantity") as totalRevenue
from
	dwh.public.ecommerce e 
where 
	"productQuantity" notnull 
group by
	"v2ProductName" 
order by 
	totalRevenue desc
; 



	
