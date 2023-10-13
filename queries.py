# pylint:disable=C0111,C0103

def get_average_purchase(db):
    # return the average amount spent per order for each customer ordered by customer ID
    query = "WITH Order_Amounts AS (\
          SELECT SUM(od.UnitPrice * od.Quantity) AS amount, od.OrderID\
          FROM OrderDetails od\
          GROUP BY od.OrderID)\
        SELECT c.CustomerID,\
        ROUND(AVG(ov.amount), 2) AS average\
        FROM Customers c\
        JOIN Orders o ON c.CustomerID = o.CustomerID\
        JOIN Order_Amounts ov ON ov.OrderID = o.OrderID\
        GROUP BY c.CustomerID\
        ORDER BY c.CustomerID"

    db.execute(query)
    results = db.fetchall()
    return results

def get_general_avg_order(db):
    # return the average amount spent per order
    pass  # YOUR CODE HERE

def best_customers(db):
    # return the customers who have an average purchase greater than the general average purchase
    pass  # YOUR CODE HERE

def top_ordered_product_per_customer(db):
    # return the list of the top ordered product by each customer
    # based on the total ordered amount in USD
    pass  # YOUR CODE HERE

def average_number_of_days_between_orders(db):
    # return the average number of days between two consecutive orders of the same customer
    pass  # YOUR CODE HERE
