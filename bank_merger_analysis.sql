-- ===================================================================
-- SBI 2017 Mega-Merger: Pre vs. Post Operational & Financial Analysis
-- Database Schema Verification and Analytical Aggregations
-- ===================================================================

USE sbi_merger_analytics_db;

-- 1. Verify Ingested Records
SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT branch_code) AS unique_branches,
    MIN(fiscal_year) AS min_year,
    MAX(fiscal_year) AS max_year
FROM sbi_branch_metrics;

-- 2. Core Comparison: Pre-Merger (FY14-FY17) vs. Post-Merger (FY18-FY21)
SELECT 
    CASE 
        WHEN fiscal_year <= 2017 THEN 'Pre-Merger'
        ELSE 'Post-Merger'
    END AS merger_phase,
    COUNT(*) AS branch_observations,
    ROUND(AVG(gross_npa_pct), 2) AS avg_gross_npa_pct,
    ROUND(AVG(net_npa_pct), 2) AS avg_net_npa_pct,
    ROUND(AVG(roa_pct), 2) AS avg_roa_pct,
    ROUND(AVG(cost_to_income_pct), 2) AS avg_cost_to_income_pct,
    ROUND(AVG(car_crar_pct), 2) AS avg_capital_adequacy_pct,
    ROUND(AVG(casa_ratio_pct), 2) AS avg_casa_ratio_pct,
    ROUND(SUM(advances_inr_cr) / 100000, 2) AS total_advances_lakh_cr,
    ROUND(SUM(deposits_inr_cr) / 100000, 2) AS total_deposits_lakh_cr
FROM sbi_branch_metrics
GROUP BY merger_phase
ORDER BY merger_phase DESC;

-- 3. Regional Circle Performance Breakdown
SELECT 
    circle_zone,
    ROUND(AVG(CASE WHEN fiscal_year <= 2017 THEN gross_npa_pct END), 2) AS pre_merger_avg_gnpa,
    ROUND(AVG(CASE WHEN fiscal_year > 2017 THEN gross_npa_pct END), 2) AS post_merger_avg_gnpa,
    ROUND(
        AVG(CASE WHEN fiscal_year <= 2017 THEN gross_npa_pct END) - 
        AVG(CASE WHEN fiscal_year > 2017 THEN gross_npa_pct END), 
        2
    ) AS gnpa_reduction_pp,
    ROUND(AVG(CASE WHEN fiscal_year > 2017 THEN roa_pct END) - 
          AVG(CASE WHEN fiscal_year <= 2017 THEN roa_pct END), 
          2
    ) AS roa_expansion_pp
FROM sbi_branch_metrics
GROUP BY circle_zone
ORDER BY gnpa_reduction_pp DESC;

-- 4. Operating Efficiency by Branch Tier (Economies of Scale Assessment)
SELECT 
    branch_tier,
    ROUND(AVG(CASE WHEN fiscal_year <= 2017 THEN cost_to_income_pct END), 2) AS pre_merger_cost_income,
    ROUND(AVG(CASE WHEN fiscal_year > 2017 THEN cost_to_income_pct END), 2) AS post_merger_cost_income,
    ROUND(
        AVG(CASE WHEN fiscal_year <= 2017 THEN cost_to_income_pct END) - 
        AVG(CASE WHEN fiscal_year > 2017 THEN cost_to_income_pct END), 
        2
    ) AS efficiency_gain_pp
FROM sbi_branch_metrics
GROUP BY branch_tier
ORDER BY efficiency_gain_pp DESC;
