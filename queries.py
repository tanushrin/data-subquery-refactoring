# pylint:disable=C0111,C0103

def get_average_purchase(db):
    # return the average amount spent per order for each customer ordered by customer ID
    query = "WITH Order_Amounts AS (\
        SELECT SUM(od.UnitPrice * od.Quantity) AS amount, od.OrderID\
        FROM OrderDetails od\
        GROUP BY od.OrderID)\
        SELECT c.CustomerID,\
        ROUND(AVG(oa.amount), 2) AS average\
        FROM Customers c\
        JOIN Orders o ON c.CustomerID = o.CustomerID\
        JOIN Order_Amounts oa ON oa.OrderID = o.OrderID\
        GROUP BY c.CustomerID\
        ORDER BY c.CustomerID"

    db.execute(query)
    results = db.fetchall()
    return results

def get_general_avg_order(db):
    # return the average amount spent per order
    query = "WITH PerOrder_Sum AS (\
          SELECT od.OrderID , SUM(od.Quantity * od.UnitPrice) AS value\
          FROM OrderDetails od\
          GROUP BY od.OrderID\
        )\
        SELECT ROUND(AVG(ps.value), 2)\
        FROM PerOrder_Sum ps"

    db.execute(query)
    results = db.fetchone()[0]
    return results

def best_customers(db):
    # return the customers who have an average purchase greater than the general average purchase
    query = "WITH PerOrder_Sum AS (\
          SELECT SUM(od.UnitPrice * od.Quantity) AS value, od.OrderID\
          FROM OrderDetails od\
          GROUP BY od.OrderID),\
        GeneralAvgAmtPerOrder AS (\
          SELECT ROUND(AVG(ps.value), 2) AS avg_round\
          FROM PerOrder_Sum ps)\
        SELECT c.CustomerID, ROUND(AVG(ps.value),2) AS avgAmt_perCustomer\
        FROM Customers c\
        JOIN Orders o ON o.CustomerID = c.CustomerID\
        JOIN PerOrder_Sum ps ON ps.OrderID = o.OrderID\
        GROUP BY c.CustomerID\
        HAVING AVG(ps.value) > (SELECT avg_round FROM GeneralAvgAmtPerOrder)\
        ORDER BY avgAmt_perCustomer DESC"
    db.execute(query)
    results = db.fetchall()
    return results

def top_ordered_product_per_customer(db):
    # return the list of the top ordered product by each customer
    # based on the total ordered amount in USD
    query = "WITH OrderedProducts AS (\
                SELECT CustomerID, ProductID, \
                SUM(OrderDetails.Quantity * OrderDetails.UnitPrice) \
                AS ProductValue\
                FROM OrderDetails\
                JOIN Orders ON OrderDetails.OrderID = Orders.OrderID\
                GROUP BY Orders.CustomerID, OrderDetails.ProductID\
                ORDER BY ProductValue DESC),\
            Ranks AS (\
            SELECT OrderedProducts.CustomerID, OrderedProducts.ProductID,\
                OrderedProducts.ProductValue,\
                RANK() OVER(\
                    PARTITION BY OrderedProducts.CustomerID \
                    ORDER BY OrderedProducts.ProductValue DESC\
                ) as order_rank\
            FROM OrderedProducts)\
        SELECT Ranks.CustomerID,Ranks.ProductID, Ranks.ProductValue\
        FROM Ranks\
        WHERE order_rank = 1\
        ORDER BY Ranks.ProductValue DESC"

    db.execute(query)
    results = db.fetchall()
    return results

def average_number_of_days_between_orders(db):
    # return the average number of days between two consecutive orders of the same customer
    query = "WITH CustomerOrders AS (\
                SELECT CustomerID, OrderID,OrderDate,\
                    LAG(OrderDate, 1, 0) OVER (\
                        PARTITION BY CustomerID\
                        ORDER By OrderDate\
                ) PreviousOrdersDate\
                FROM Orders)\
                SELECT ROUND(AVG(JULIANDAY(OrderDate) - \
                JULIANDAY(PreviousOrdersDate))) AS delta\
                FROM CustomerOrders\
                WHERE PreviousOrdersDate != 0"
    db.execute(query)
    results = int(db.fetchone()[0])
    return results
