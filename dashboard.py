from database.queries.transactions import get_transactions_for_user
from database.queries.categories import get_categories
from database.queries.users import get_user_by_id


def get_dashboard_data(user_id):
    user = get_user_by_id(user_id)
    transactions = get_transactions_for_user(user_id)
    categories = get_categories()

    total_income = 0.0
    total_expense = 0.0

    for transaction in transactions:
        amount = float(transaction["amount"])
        if transaction.get("type") == "income":
            total_income += amount
        else:
            total_expense += amount

    total_balance = total_income - total_expense

    return {
        "user": user,
        "transactions": transactions,
        "categories": categories,
        "total_balance": total_balance,
        "monthly_spending": total_expense,
        "income": total_income,
        "net": total_balance,
    }