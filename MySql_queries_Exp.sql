select * from overallexpense_2024_2025;
use expense_tracker;

-- PROVIDED QUESTION
-- 1.What is the total amount spent in each category?
SELECT category, SUM(Amount) AS Total_Amount
FROM overallexpense_2024_2025
GROUP BY Category;

ALTER TABLE overallexpense_2024_2025
CHANGE COLUMN `Payment Mode` `Payment_Mode` VARCHAR(45) NULL DEFAULT NULL AFTER `Amount`;

-- 2.What is the total amount spent using each payment mode?
SELECT Payment_Mode, ROUND(SUM(Amount)) AS Total_Amount
FROM overallexpense_2024_2025
GROUP BY Payment_Mode;

-- 3.What is the total cashback received across all transactions?
SELECT ROUND(SUM(cashback)) AS Total_Cashback
FROM overallexpense_2024_2025;

-- 4.Which are the top 5 most expensive categories in terms of spending?
SELECT category AS Top5_most_expensive_categories, ROUND(SUM(Amount)) AS Total_Amount
FROM overallexpense_2024_2025
GROUP BY Category
ORDER BY Total_Amount DESC
LIMIT 5;

-- 5.How much was spent on transportation using different payment modes?
SELECT Payment_Mode, ROUND(SUM(Amount)) AS Total_Amount
FROM overallexpense_2024_2025
WHERE Category = 'Transportation'
GROUP BY Payment_Mode;

-- 6.Which transactions resulted in cashback?
select * from overallexpense_2024_2025
where cashback > 0;


-- 7.What is the total amount spent in each month?
SELECT 
    MONTHNAME(date) AS Month, 
    ROUND(SUM(Amount)) AS Total_Expense_Monthly
FROM overallexpense_2024_2025
GROUP BY MONTHNAME(date), MONTH(date);

-- 8.Which months have the highest spending in categories like "Travel," "Entertainment," or "Gifts"?
SELECT MONTHNAME(date) AS Month, ROUND(SUM(Amount)) AS Total_Spending
FROM overallexpense_2024_2025
WHERE category IN ('Travel', 'Entertainment', 'Gifts')
GROUP BY MONTHNAME(date), category
ORDER BY Total_Spending DESC
LIMIT 1;


-- 9.Are there any recurring expenses that occur during specific months of the year (e.g., insurance premiums, property taxes)?
SELECT category, MONTHNAME(date) AS Month, COUNT(*) AS Frequency
FROM overallexpense_2024_2025
WHERE category IN ('Insurance', 'Property Tax')  -- Adjust categories as needed
GROUP BY category, MONTHNAME(date)
HAVING COUNT(*) > 1;

-- 10.How much cashback or rewards were earned in each month?
SELECT MONTHNAME(date) AS Month, ROUND(SUM(cashback)) AS Total_Cashback
FROM overallexpense_2024_2025
GROUP BY MONTHNAME(date)
ORDER BY MONTHNAME(date);

SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- 11.How has your overall spending changed over time (e.g., increasing, decreasing, remaining stable)?
SELECT YEAR(date) AS Year, MONTHNAME(date) AS Month, ROUND(SUM(Amount)) AS Total_Expense_Monthly
FROM overallexpense_2024_2025
GROUP BY YEAR(date), MONTH(date), MONTHNAME(date)
ORDER BY YEAR(date) ASC, MONTH(date) ASC;

SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- 12.What are the typical costs associated with different types of travel (e.g., flights, accommodation, transportation)?
SELECT category, ROUND(SUM(Amount)) AS Total_Expense
FROM overallexpense_2024_2025
WHERE `Category` IN ('Flights','Accommodation','Transportation')
GROUP BY category;

-- 13.Are there any patterns in grocery spending (e.g., higher spending on weekends, increased spending during specific seasons)?
SELECT MONTHNAME(date) AS Month, ROUND(AVG(Amount)) AS Average_spending
FROM overallexpense_2024_2025
WHERE Category = 'Groceries'
GROUP BY MONTH(date),MONTHNAME(date), Category
ORDER BY YEAR(date),MONTH(date);

-- 14.Define High and Low Priority Categories
SELECT Category AS High_Priority_Category,ROUND(SUM(Amount)) AS Total_Amount
FROM overallexpense_2024_2025
GROUP BY category
ORDER BY Total_Amount DESC
LIMIT 1;

SELECT Category AS Low_Priority_Category,ROUND(SUM(Amount)) AS Total_Amount
FROM overallexpense_2024_2025
GROUP BY category
ORDER BY Total_Amount
LIMIT 1;

-- 15.Which category contributes the highest percentage of the total spending?
SELECT Category, ROUND(SUM(Amount)) AS Total_Spending,(ROUND(SUM(Amount)) / (SELECT ROUND(SUM(Amount)) FROM overallexpense_2024_2025)) * 100 AS Percentage_Contribution
FROM overallexpense_2024_2025
GROUP BY Category
ORDER BY Percentage_Contribution DESC;


SELECT Category, ROUND(SUM(Amount)) AS Total_Spending,(ROUND(SUM(Amount)) / (SELECT ROUND(SUM(Amount)) FROM overallexpense_2024_2025)) * 100 AS Percentage_Contribution
FROM overallexpense_2024_2025
GROUP BY Category
ORDER BY Percentage_Contribution DESC
LIMIT 1;

-- OWN QUESTIONS
-- 1.Which month has a highest spendings?
SELECT MONTH(DATE) AS Higest_spended_Month,ROUND(SUM(Amount)) AS Total_Amount
FROM overallexpense_2024_2025
GROUP BY  MONTH(DATE)
ORDER BY Total_Amount DESC;

SELECT MONTH(DATE) AS Higest_spended_Month,ROUND(SUM(Amount)) AS Total_Amount
FROM overallexpense_2024_2025
GROUP BY  MONTH(DATE)
ORDER BY Total_Amount DESC
LIMIT 1;

-- 2.Total amount spent on Investment
SELECT category,ROUND(SUM(Amount)) AS Total_Amount
FROM overallexpense_2024_2025
WHERE category = 'Investments'
GROUP BY category;

-- 3.Which payment mode is used the most for large transactions?
SELECT payment_mode AS Payment_Mode_Large_Transaction, ROUND(SUM(Amount)) AS Total_Amount
FROM overallexpense_2024_2025
GROUP BY payment_mode
ORDER BY Total_Amount DESC
LIMIT 1;

-- 4.How much was spent on 'Subscriptions' in the last 6 months?
SELECT Category, ROUND(SUM(Amount)) AS last_6_month_Expense
FROM overallexpense_2024_2025
WHERE Category = 'Subscriptions' 
AND date >= CURDATE() - INTERVAL 6 MONTH
GROUP BY Category;

-- 5.How much was spent using digital wallets compared to credit/debit cards?
SELECT 
    CASE 
        WHEN payment_mode IN ('Credit Card', 'Debit Card') THEN 'Credit/Debit Cards'
        WHEN payment_mode IN ('UPI', 'wallet') THEN 'Digital Wallets'
        ELSE 'Other' 
    END AS payment_group,
    ROUND(SUM(Amount)) AS Total_Amount
FROM overallexpense_2024_2025
WHERE payment_mode IN ('UPI', 'wallet', 'Credit Card', 'Debit Card')
GROUP BY payment_group;

-- 6.Which payment method is most frequently used for transactions?
SELECT payment_mode AS frequently_used, COUNT(*) AS transaction_count
FROM overallexpense_2024_2025
GROUP BY payment_mode
ORDER BY transaction_count DESC
LIMIT 1;

-- 7.Which recurring transactions could be optimized for better savings?
SELECT category AS Recurring_Transaction, ROUND(AVG(Amount)) AS Average_Spent_Monthly
FROM overallexpense_2024_2025
WHERE category IS NOT NULL
GROUP BY category
HAVING COUNT(*) > 1
ORDER BY Average_Spent_Monthly DESC;

-- 8.What is the most frequent category where you overspend each month?

WITH MonthlyAverage AS (
    SELECT 
        MONTHNAME(date) AS Month,
        ROUND(AVG(Amount), 2) AS Avg_Monthly_Spending
    FROM overallexpense_2024_2025
    GROUP BY MONTH(date), MONTHNAME(date)
),
OverspendingCategories AS (
    SELECT 
        e.category,
        MONTHNAME(e.date) AS Month,
        ROUND(SUM(e.Amount), 2) AS Total_Spent,
        m.Avg_Monthly_Spending,
        ROUND(SUM(e.Amount) - m.Avg_Monthly_Spending, 2) AS Overspent_Amount
    FROM overallexpense_2024_2025 e
    JOIN MonthlyAverage m ON MONTHNAME(e.date) = m.Month
    GROUP BY e.category, MONTHNAME(e.date), m.Avg_Monthly_Spending
    HAVING Overspent_Amount > 0
)
SELECT 
    category, 
    Month, 
    Total_Spent, 
    Overspent_Amount
FROM OverspendingCategories
ORDER BY Overspent_Amount DESC;


-- 9.Total amount Investmented yearly
SELECT YEAR(date),ROUND(SUM(Amount)) AS Invested_Amount
FROM overallexpense_2024_2025
WHERE `Category` = 'Investments'
GROUP BY YEAR(date);

-- 10.How much personal loan amount have been paid till now?
SELECT ROUND(SUM(Amount)) AS Total_Personal_loan_Paid
FROM overallexpense_2024_2025
WHERE Description LIKE '%personal loan%';