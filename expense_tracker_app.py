import mysql.connector
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Rithikka@27",
    database = "expense_tracker"
)

if mydb.is_connected():
    print("connected to SQL")

mycursor = mydb.cursor()

page = st.sidebar.selectbox("Description",["Expense Analysis","Asked Questions","Own Questions"],index = 0)

if page == "Expense Analysis":
    st.header("ANALYSING PERSONAL EXPENSES")
    st.subheader("PROJECT OBJECTIVE:")
    st.markdown("This project focuses on creating an expense tracker for an individual using the Faker library. "
    "It generates realistic monthly expense data, processes and stores it in an SQL database, and formulates SQL queries to gain insights into spending patterns. "
    "A Streamlit app is developed to visualize these insights and display the results of the SQL queries. The tracker will categorize expenses, such as bills, "
    "groceries, subscriptions, and personal spending, offering a comprehensive overview of financial habits throughout the year.")

    st.subheader("Business Use Cases:")
    st.markdown("""
        - Automating the tracking of personal or business expenses from e-commerce platforms.
        - Analyzing and categorizing spending habits to create actionable savings plans.
        - Building financial dashboards for tracking income and expenditure trends.Providing businesses insights into procurement and inventory purchasing patterns.
    """)

    st.subheader("PROJECT OBJECTIVES:")
    st.markdown("""
        - **Data Simulation:** Use the Faker library to generate a realistic dataset that depicts a person’s expense throughout the month.create 12 different tables for each month.
        - **Database Creation:** Create a SQL database schema and load the generated dataset for querying.
        - **EDA:** Analyze the dataset using Python libraries to extract insights about spending patterns and trends.
        - **Streamlit App:** Develop a user-friendly web application showcasing visualizations and SQL query outputs.
        - **Insights & Recommendations:** Provide actionable takeaways based on simulated data analysis.
    """)

    


if page == "Asked Questions":
    st.title("ASKED QUESTIONS")

    Question = st.selectbox("Select a Question",[
        "1. What is the total amount spent in each category?",
        "2. What is the total amount spent using each payment mode?",
        "3. What is the total cashback received across all transactions?",
        "4. Which are the top 5 most expensive categories in terms of spending?",
        "5. How much was spent on transportation using different payment modes?",
        "6. Which transactions resulted in cashback?",
        "7. What is the total amount spent in each month?",
        "8. Which months have the highest spending in categories like Travel,Entertainment, or Gifts?",
        "9. Are there any recurring expenses that occur during specific months of the year (e.g., insurance premiums, property taxes)?",
        "10.How much cashback or rewards were earned in each month?",
        "11.How has your overall spending changed over time (e.g., increasing, decreasing, remaining stable)",
        "12.What are the typical costs associated with different types of travel (e.g., flights, accommodation, transportation)?",
        "13.Are there any patterns in grocery spending (e.g., higher spending on weekends, increased spending during specific seasons)?",
        "14.Define High and Low Priority Categories",
        "15.Which category contributes the highest percentage of the total spending?"
    ])

    if Question == "1. What is the total amount spent in each category?":
        st.subheader("Total amount spent in each category:")
        # Query to get total amount spent per category
        mycursor.execute("""
            SELECT category, ROUND(SUM(Amount)) AS Total_Amount
            FROM overallexpense_2024_2025
            GROUP BY category;
        """)
        myresult = mycursor.fetchall()
        # Display the results in a nice format
        df = pd.DataFrame(myresult, columns=["Category", "Total Amount"])
        st.dataframe(df) 
        # Displays the result in a chart
        chart = px.bar(df,x = 'Category',color = 'Category', y = 'Total Amount',text = 'Total Amount')
        st.write(chart)

    if Question == "2. What is the total amount spent using each payment mode?":
        # Query to get Total amount spent using each payment mode
        st.subheader("Total amount spent using each payment mode:")
        mycursor.execute("""
            SELECT Payment_Mode, ROUND(SUM(Amount)) AS Total_Amount
            FROM overallexpense_2024_2025
            GROUP BY Payment_Mode;"
        """)
        myresult = mycursor.fetchall()
        # Display result in a data frame
        df = pd.DataFrame(myresult, columns = ["Payment Modes","Total Amount"])
        st.dataframe(df)
        # Display result in a chart
        chart = px.bar(df, x = "Payment Modes", color = "Payment Modes", y = "Total Amount",text = "Total Amount")
        st.write(chart)

    if Question == "3. What is the total cashback received across all transactions?":
        st.subheader("Total cashback received across all transactions:")
        # Query to get Total cashback received across all transactions
        mycursor.execute("""
            SELECT ROUND(SUM(cashback)) AS Total_Cashback
            FROM overallexpense_2024_2025;
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns = ["Total Cashback:"])
        df = df.reset_index(drop =True)
        st.write(df.to_string(index=False))

    if Question == "4. Which are the top 5 most expensive categories in terms of spending?":
        st.subheader("Top 5 most expensive categories in terms of spending:")
        mycursor.execute("""
            SELECT category AS Top5_most_expensive_categories, ROUND(SUM(Amount)) AS Total_Amount
            FROM overallexpense_2024_2025
            GROUP BY Category
            ORDER BY Total_Amount DESC
            LIMIT 5; 
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns = ["Top 5 Most Expensive Categories","Total Amount"])

        st.dataframe(df)

        chart = px.bar(df,x = "Top 5 Most Expensive Categories",color = "Top 5 Most Expensive Categories",y = "Total Amount",text = "Total Amount")
        st.write(chart)

    if Question == "5. How much was spent on transportation using different payment modes?":
        st.subheader(" Amount spent on transportation using different payment modes:")
        mycursor.execute("""
            SELECT Payment_Mode, ROUND(SUM(Amount)) AS Total_Amount
            FROM overallexpense_2024_2025
            WHERE Category = 'Transportation'
            GROUP BY Payment_Mode;
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns = ["Payment Modes used for Transportation","Total Amount"])

        st.dataframe(df)

        fig = px.pie(df,values = "Total Amount",names = "Payment Modes used for Transportation")
        st.plotly_chart(fig,use_container_width=True)

    if Question == "6. Which transactions resulted in cashback?":
        st.subheader("Transactions resulted in cashback:")

        mycursor.execute("""
            select * from overallexpense_2024_2025
            where cashback > 0;
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns = ["Date","Category","Description","Amount","Payment_Mode","Cashback"])

        st.write(df)

    if Question == "7. What is the total amount spent in each month?":
        st.subheader("Total amount spent in each month:")
        # SQL query to get total expenses per month, ensuring all months are represented
        mycursor.execute("""
            SELECT 
                MONTHNAME(date) AS Month, 
                ROUND(SUM(Amount)) AS Total_Expense_Monthly
            FROM overallexpense_2024_2025
            GROUP BY MONTHNAME(date), MONTH(date);
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns = ["Month","Total Expense Monthly"])
        st.dataframe(df)
        chart = px.pie(
            df, 
            values="Total Expense Monthly", 
            names="Month", 
            title="Total Expense Per Month"
        )
        st.plotly_chart(chart,use_container_width=True)
    
    if Question == "8. Which months have the highest spending in categories like Travel,Entertainment, or Gifts?":
        st.subheader("Months having the highest spending in categories like Travel,Entertainment, or Gifts")

        mycursor.execute("""
            SELECT MONTHNAME(date) AS Month, ROUND(SUM(Amount)) AS Total_Spending
            FROM overallexpense_2024_2025
            WHERE category IN ('Travel', 'Entertainment', 'Gifts')
            GROUP BY MONTHNAME(date), category
            ORDER BY Total_Spending DESC
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult, columns = ["Month","Amount Spent in Travel, Entertainment or Gifts"])
        st.dataframe(df)

        amount_spent_fig = px.bar(
            df,
            x="Amount Spent in Travel, Entertainment or Gifts", 
            y="Month",
            orientation='h',  # Changed to horizontal for better readability
            title="Chart: Months with Highest Spending in Travel, Entertainment, or Gifts",
            color_discrete_sequence=["#0083b8"],  # Using a single color
            template="plotly_white"
        )

        # Display chart in Streamlit
        st.plotly_chart(amount_spent_fig, use_container_width=True)

    if Question == "9. Are there any recurring expenses that occur during specific months of the year (e.g., insurance premiums, property taxes)?":
        st.subheader("Recurring expenses that occur during specific months of the year (e.g., insurance premiums, property taxes):")

        mycursor.execute("""
            SELECT category, MONTHNAME(date) AS Month, COUNT(*) AS Frequency
            FROM overallexpense_2024_2025
            WHERE category IN ('Insurance', 'Property Tax')  -- Adjust categories as needed
            GROUP BY category, MONTHNAME(date)
            HAVING COUNT(*) > 1;
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns = ["category","Month","Frequency"])

        st.write(df)

    if Question == "10.How much cashback or rewards were earned in each month?":
        st.subheader("cashback or rewards were earned in each month:")

        mycursor.execute("""
            SELECT MONTHNAME(date) AS Month, ROUND(SUM(cashback)) AS Total_Cashback
            FROM overallexpense_2024_2025
            GROUP BY MONTHNAME(date)
            ORDER BY MONTHNAME(date);
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns = ["Month","Total cashbacks"])

        st.dataframe(df)

        cashback_fig = px.bar(
            df,
            x="Month",
            y="Total cashbacks",
            orientation='v',  # Changed to horizontal for better readability
            title="Chart: Months with Highest Spending in Travel, Entertainment, or Gifts",
            color_discrete_sequence=["#0083b8"],  # Using a single color
            template="plotly_white")
        
        st.plotly_chart(cashback_fig,use_container_width=True)

    if Question == "11.How has your overall spending changed over time (e.g., increasing, decreasing, remaining stable)":
        st.subheader("Overall spending changed over time:")

        mycursor.execute("""
            SELECT YEAR(date) AS Year, MONTHNAME(date) AS Month, ROUND(SUM(Amount)) AS Total_Expense_Yearly
            FROM overallexpense_2024_2025
            GROUP BY YEAR(date), MONTH(date),MONTHNAME(date)
            ORDER BY YEAR(date) ASC, MONTH(date) ASC;
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns=["Year","Month","Amount Spent Monthly"])

        st.dataframe(df)

        fig = px.line(df,x = "Month",y = "Amount Spent Monthly",title = "Pettern of Monthly Spending",template = "gridon")

        st.plotly_chart(fig, use_container_width=True)


    if Question == "12.What are the typical costs associated with different types of travel (e.g., flights, accommodation, transportation)?":
        st.subheader("Typical costs associated with different types of travel (e.g., flights, accommodation, transportation):")

        mycursor.execute("""
            SELECT category, ROUND(SUM(Amount)) AS Total_Expense
            FROM overallexpense_2024_2025
            WHERE `Category` IN ('Flights','Accommodation','Transportation')
            GROUP BY category;
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns=["Categoty","Total Expense"])

        st.write(df)

    if Question == "13.Are there any patterns in grocery spending (e.g., higher spending on weekends, increased spending during specific seasons)?":
        st.subheader("Spendin patterns in grocery:")
        st.write("As we can see in the chart below, April has the lowest spending average, with an average spending value of Rs. 3,462. "
        "Spending rises in May, June, July, and August to Rs. 5,421. There is a sudden drop in September to Rs. 4,006, followed by a gradual increase to Rs. 6,955 by March.")

        mycursor.execute("""
            SELECT MONTHNAME(date) AS Month, ROUND(AVG(Amount)) AS Average_spending
            FROM overallexpense_2024_2025
            WHERE Category = 'Groceries'
            GROUP BY MONTH(date),MONTHNAME(date), Category
            ORDER BY YEAR(date),MONTH(date);
        """)
        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns=["Month","Average Spending"])

        st.dataframe(df)

        fig = px.line(df,x = "Month",y = "Average Spending",title = "Average spending in Groceries Monthly")

        st.plotly_chart(fig,use_container_width=True)

    if Question == "14.Define High and Low Priority Categories":
        st.subheader("High and Low Priority Categories:")

        mycursor.execute("""SELECT Category AS High_Priority_Category,ROUND(SUM(Amount)) AS Total_Amount
            FROM overallexpense_2024_2025
            GROUP BY category
            ORDER BY Total_Amount DESC
            LIMIT 1;
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns=["High Priority Category","Total Amount"])

        st.dataframe(df)

        mycursor.execute("""
            SELECT Category AS Low_Priority_Category,ROUND(SUM(Amount)) AS Total_Amount
            FROM overallexpense_2024_2025
            GROUP BY category
            ORDER BY Total_Amount
            LIMIT 1;
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns = ["Low Priority Category","Total Amount"])

        st.dataframe(df)

    if Question == "15.Which category contributes the highest percentage of the total spending?":
        st.subheader("category that contributes the highest percentage of the total spending:")

        mycursor.execute("""
            SELECT Category, ROUND(SUM(Amount)) AS Total_Spending,(ROUND(SUM(Amount)) / (SELECT ROUND(SUM(Amount)) FROM overallexpense_2024_2025)) * 100 AS Percentage_Contribution
            FROM overallexpense_2024_2025
            GROUP BY Category
            ORDER BY Percentage_Contribution DESC;
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns=["Categories","Total Spending","Contribution Percentage"])

        st.dataframe(df)

        fig = px.pie(df,values="Contribution Percentage",names="Categories")

        st.plotly_chart(fig,use_container_width=True)


if page == "Own Questions":
    st.title("OWN QUESTIONS")

    Question = st.selectbox("Select a Question",[
        "1.Which month has a highest spendings?",
        "2.Total amount spent on Investment",
        "3.Which payment mode is used the most for large transactions?",
        "4.How much was spent on 'Subscriptions' in the last 6 months?",
        "5.How much was spent using digital wallets compared to credit/debit cards?",
        "6.Which payment method is most frequently used for transactions?",
        "7.Which recurring transactions could be optimized for better savings?",
        "8.What is the most frequent category where you overspend each month?",
        "9.Total amount Investmented yearly",
        "10.How much personal loan amount have been paid till now?"
    ])

    if Question == "1.Which month has a highest spendings?":
        st.subheader("Highest spendings Month:")

        mycursor.execute("""
            SELECT MONTHNAME(DATE) AS Higest_spended_Month,ROUND(SUM(Amount)) AS Total_Amount
            FROM overallexpense_2024_2025
            GROUP BY  MONTH(DATE)
            ORDER BY Total_Amount DESC
            LIMIT 1;
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns = ["Highest Spending Month","Total Amount"])

        st.dataframe(df)

        mycursor.execute("""
            SELECT MONTHNAME(DATE) AS Higest_spended_Month,ROUND(SUM(Amount)) AS Total_Amount
            FROM overallexpense_2024_2025
            GROUP BY  MONTH(DATE)
            ORDER BY Total_Amount DESC;
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns=["Months","Spendings Monthly"])

        fig = px.bar(df,x = "Months",y = "Spendings Monthly",title = "Monthly Spending:",text = "Spendings Monthly")

        st.plotly_chart(fig)

    if Question == "2.Total amount spent on Investment":
        st.subheader("Total amount spent on Investment:")

        mycursor.execute("""
            SELECT category,ROUND(SUM(Amount)) AS Total_Amount
            FROM overallexpense_2024_2025
            WHERE category = 'Investments'
            GROUP BY category;
        """)

        myresult = mycursor.fetchall()

        df = pd.DataFrame(myresult,columns=["Category","Total Amount Spent on Investment"])

        st.dataframe(df)

    if Question == "3.Which payment mode is used the most for large transactions?":
       
        mycursor.execute("""
            SELECT Payment_Mode, COUNT(*) AS Transaction_Count, ROUND(AVG(Amount)) AS Average_Amount
            FROM overallexpense_2024_2025
            WHERE Amount > (SELECT AVG(Amount) FROM overallexpense_2024_2025)
            GROUP BY Payment_Mode
            ORDER BY Transaction_Count DESC
            LIMIT 1;
        """)

        myresult = mycursor.fetchone()

        if myresult:
            payment_mode, transaction_count, avg_amount = myresult
            st.subheader("Most Used Payment Mode for Large Transactions:")
            st.write(f" **Payment Mode:** {payment_mode}")
            st.write(f" **Number of Transactions:** {transaction_count}")
            st.write(f" **Average Transaction Amount:** Rs. {avg_amount}")
    

    if Question == "4.How much was spent on 'Subscriptions' in the last 6 months?":
        st.subheader("Amount spent on 'Subscriptions' in the last 6 months:")

        mycursor.execute("""
            SELECT Category, ROUND(SUM(Amount)) AS last_6_month_Expense
            FROM overallexpense_2024_2025
            WHERE Category = 'Subscriptions' 
            AND date >= CURDATE() - INTERVAL 6 MONTH
            GROUP BY Category;
        """)

        myresult = mycursor.fetchall()

        if myresult:
            Category,last_6_month_Expense = myresult[0]
            st.write(f" **Category:** {Category}")
            st.write(f" **Last 6 Month Expense:** Rs.{last_6_month_Expense}")


    if Question == "5.How much was spent using digital wallets compared to credit/debit cards?":
        st.subheader("Amount spent using digital wallets compared to credit/debit cards:")

        mycursor.execute("""
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
        """)

        myresult = mycursor.fetchall()

        if myresult:
           
            df = pd.DataFrame(myresult, columns=["Payment Group", "Total Amount"])
            
           
            st.dataframe(df)

           
            import plotly.express as px
            fig = px.bar(df, x="Payment Group", y="Total Amount", 
                        title="Comparison of Digital Wallets vs Credit/Debit Cards", 
                        text="Total Amount", color="Payment Group")
            st.plotly_chart(fig, use_container_width=True)


    if Question == "6.Which payment method is most frequently used for transactions?":
        st.subheader("payment method that is used most frequently for transactions:")

        mycursor.execute("""
            SELECT payment_mode AS frequently_used, COUNT(*) AS transaction_count
            FROM overallexpense_2024_2025
            GROUP BY payment_mode
            ORDER BY transaction_count DESC
            LIMIT 1;
        """)

        myresult = mycursor.fetchall()

        if myresult:

            frequently_used,transaction_count = myresult[0]
            st.write(f" **Frequently Used Transaction:** {frequently_used}")
            st.write(f" **Transaction Count:** {transaction_count}")

    
    if Question == "7.Which recurring transactions could be optimized for better savings?":
        st.subheader("Recurring transactions that could be optimized for better savings:")
        st.markdown("""
            **Utility Bills (₹5443) and Rent (₹5441) are essential** and difficult to reduce.  
            **Entertainment (₹5214) and Miscellaneous (₹5108) are high-cost but non-essential**, making them ideal for cost-cutting.\n
            **Entertainment:**  
            - Reduce **streaming subscriptions** (e.g., Netflix, Prime, etc.).  
            - Cut down on **unnecessary outings**.  
            - Look for **free or lower-cost alternatives.**\n
            **Miscellaneous:** 
            - Identify **impulse purchases** and reduce unnecessary expenses.  
            - Set a fixed **monthly budget** for miscellaneous spending.  
            - Track **where the money is going** and eliminate unnecessary items. 
        """)

        mycursor.execute("""
            SELECT category AS Recurring_Transaction, ROUND(AVG(Amount)) AS Average_Spent_Monthly
            FROM overallexpense_2024_2025
            WHERE category IS NOT NULL
            GROUP BY category
            HAVING COUNT(*) > 1
            ORDER BY Average_Spent_Monthly DESC;
        """)

        myresult = mycursor.fetchall()

        if myresult:

            df = pd.DataFrame(myresult,columns=["Recurring Transaction","Average Spent Monthly"])

            st.dataframe(df)

            fig = px.bar(df,x = "Average Spent Monthly",y ="Recurring Transaction",title = "Comparing Recurring Transactions",text ="Average Spent Monthly")

            st.plotly_chart(fig)

    if Question == "8.What is the most frequent category where you overspend each month?":
        st.subheader("Most Frequent Category Where You Overspend Each Month")

        # Query to calculate overspending categories
        mycursor.execute("""        
            WITH MonthlyAverage AS (
                SELECT 
                    YEAR(date) AS Year,
                    MONTH(date) AS Month_Num,
                    MONTHNAME(date) AS Month,
                    ROUND(AVG(Amount), 2) AS Avg_Monthly_Spending
                FROM overallexpense_2024_2025
                GROUP BY YEAR(date), MONTH(date), MONTHNAME(date)
            ),
            OverspendingCategories AS (
                SELECT 
                    e.category,
                    YEAR(e.date) AS Year,
                    MONTHNAME(e.date) AS Month,
                    MONTH(e.date) AS Month_Num,
                    ROUND(SUM(e.Amount), 2) AS Total_Spent,
                    m.Avg_Monthly_Spending,
                    ROUND(SUM(e.Amount) - m.Avg_Monthly_Spending, 2) AS Overspent_Amount
                FROM overallexpense_2024_2025 e
                JOIN MonthlyAverage m 
                    ON YEAR(e.date) = m.Year AND MONTH(e.date) = m.Month_Num
                GROUP BY e.category, YEAR(e.date), MONTHNAME(e.date), MONTH(e.date), m.Avg_Monthly_Spending
                HAVING Overspent_Amount > 0
            )
            SELECT 
                category, 
                Month, 
                Total_Spent, 
                Overspent_Amount
            FROM OverspendingCategories
            ORDER BY Year, Month_Num, Overspent_Amount DESC;
        """)

        # Fetch and display results
        myresult = mycursor.fetchall()

        if myresult:
            # Convert to DataFrame
            df = pd.DataFrame(myresult, columns=["Category", "Month", "Total Spent", "Overspent Amount"])
            st.dataframe(df)

            # Plot the overspending trend
            fig = px.bar(df, x="Category", y="Overspent Amount", color="Month",
                        title="Most Frequent Categories Where You Overspend", text="Overspent Amount")
            st.plotly_chart(fig, use_container_width=True)

    if Question == "9.Total amount Investmented yearly":
        st.subheader("Total Amount Invested Yearly:")

        mycursor.execute("""
            SELECT YEAR(date) AS Year, ROUND(SUM(Amount)) AS Invested_Amount
            FROM overallexpense_2024_2025
            WHERE Category = 'Investments'
            GROUP BY YEAR(date);
        """)

        myresult = mycursor.fetchall()

        if myresult:
            df = pd.DataFrame(myresult, columns=["Year", "Invested Amount"])
            st.dataframe(df)

            # Pie Chart with Updated Text Label
            fig = px.pie(df, values="Invested Amount", names="Year")

            st.plotly_chart(fig, use_container_width=True)

    if Question == "10.How much personal loan amount have been paid till now?":
        st.subheader("Personal loan amount have been paid till now:")

        mycursor.execute("""
            SELECT ROUND(SUM(Amount)) AS Total_Personal_loan_Paid
            FROM overallexpense_2024_2025
            WHERE Description LIKE '%personal loan%';
        """)

        myresult = mycursor.fetchall()

        if myresult and myresult[0][0]:
            Total_Personal_loan_Paid = myresult[0][0]
            st.write(f" **Total Personal Loan Amount Paid:** Rs. {Total_Personal_loan_Paid}")

