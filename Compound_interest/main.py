import matplotlib.pyplot as plt
import numpy as np

def calculate_portfolio(annual_return, monthly_contribution, years, annual_expenses, inflation=0.03, months_with_contributions=None):
    """
    Simulates the growth of an investment portfolio with compound interest, regular contributions, and inflation adjustment.
    """
    total_months = years * 12
    monthly_return = (1 + annual_return) ** (1 / 12) - 1
    monthly_inflation = (1 + inflation) ** (1 / 12) - 1

    portfolio_value = [0]
    own_contribution = [0]
    balance = 0
    annual_profit = []
    annual_profit_percent = []
    fire_month = None

    fire_target_value = 25 * annual_expenses
    fire_target_value_real = fire_target_value

    for month in range(1, total_months + 1):
        # Add monthly contribution if within the contribution period
        if months_with_contributions is None or month <= months_with_contributions:
            balance += monthly_contribution
        # Apply monthly return
        balance *= (1 + monthly_return)
        portfolio_value.append(balance)
        own_contribution.append(monthly_contribution * month if months_with_contributions is None or month <= months_with_contributions else own_contribution[-1])

        # Adjust FIRE target for inflation
        fire_target_value_real *= (1 + monthly_inflation)

        # Check if FIRE is achieved
        if balance >= fire_target_value_real and fire_month is None:
            fire_month = month

        # Calculate annual profit and percent return
        if month % 12 == 0:
            year_profit = balance - own_contribution[month]
            year_profit_percent = (year_profit / own_contribution[month]) * 100
            annual_profit.append(year_profit)
            annual_profit_percent.append(year_profit_percent)

    return portfolio_value, own_contribution, annual_profit, annual_profit_percent, fire_month

def format_number(number):
    """Format number with spaces as thousands separator and comma as decimal separator."""
    return f"{number:,.2f}".replace(",", " ").replace(".", ",")

def display_results(annual_profit, annual_profit_percent, own_contribution, portfolio_value, fire_month):
    """Prints a summary table and final results of the simulation."""
    final_portfolio_value = portfolio_value[-1]
    final_own_contribution = own_contribution[-1]
    final_profit = final_portfolio_value - final_own_contribution

    print(f"{'Year':<5}{'Own contribution (PLN)':<25}{'Annual profit (PLN)':<20}{'Return (%)':<15}")
    for i in range(1, len(annual_profit) + 1):
        print(f"{i:<5}{format_number(own_contribution[i * 12]):<25}{format_number(annual_profit[i - 1]):<20}{annual_profit_percent[i - 1]:<15.2f}")

    print(f"\nFinal portfolio value: {format_number(final_portfolio_value)} PLN")
    print(f"Total own contribution: {format_number(final_own_contribution)} PLN")
    print(f"Total investment profit: {format_number(final_profit)} PLN")

    if fire_month:
        fire_year = fire_month // 12
        fire_month_num = fire_month % 12
        if fire_month_num == 0:
            fire_month_num = 12
            fire_year -= 1
        print(f"You can reach FIRE in month {fire_month_num} of year {fire_year} from now.")
    else:
        print("FIRE was not achieved in the given period.")

def create_charts(portfolio_value, own_contribution, annual_profit, final_portfolio_value, final_own_contribution, final_profit, fire_month):
    """Creates and displays charts for portfolio value and annual profits, with a summary below."""
    plt.figure(figsize=(8, 4))

    # Chart 1: Portfolio value and own contribution over time
    plt.subplot(1, 2, 1)
    plt.plot(portfolio_value, label='Portfolio value', color='blue')
    plt.plot(own_contribution, label='Own contribution', color='green', linestyle='--')
    plt.xlabel('Months')
    plt.ylabel('Value in PLN')
    plt.title('Portfolio value over time')
    plt.legend()
    plt.grid(True)

    # Chart 2: Annual profits
    plt.subplot(1, 2, 2)
    plt.bar(range(1, len(annual_profit) + 1), annual_profit, color='purple', alpha=0.7)
    plt.xlabel('Year')
    plt.ylabel('Annual profit (PLN)')
    plt.title('Annual portfolio profits')

    plt.tight_layout(rect=(0, 0.1, 1, 1))

    # Add summary below the charts
    summary = f"Final portfolio value: {format_number(final_portfolio_value)} PLN\n" \
              f"Total own contribution: {format_number(final_own_contribution)} PLN\n" \
              f"Total investment profit: {format_number(final_profit)} PLN\n"
    if fire_month:
        fire_year = fire_month // 12
        fire_month_num = fire_month % 12
        if fire_month_num == 0:
            fire_month_num = 12
            fire_year -= 1
        summary += f"You can reach FIRE in month {fire_month_num} of year {fire_year} from now."
    else:
        summary += "FIRE was not achieved in the given period."

    plt.gcf().text(0.5, 0.02, summary, ha='center', va='bottom', fontsize=11, bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray'))
    plt.show()
    plt.close('all')

def main():
    # Simulation parameters
    annual_return = 0.10
    monthly_contribution = 1000
    years = 42
    annual_expenses = 72000
    inflation = 0.03
    months_with_contributions = 120  # For example, stop contributing after 10 years (120 months)
    portfolio_value, own_contribution, annual_profit, annual_profit_percent, fire_month = calculate_portfolio(
        annual_return, monthly_contribution, years, annual_expenses, inflation, months_with_contributions
    )

    display_results(annual_profit, annual_profit_percent, own_contribution, portfolio_value, fire_month)
    final_portfolio_value = portfolio_value[-1]
    final_own_contribution = own_contribution[-1]
    final_profit = final_portfolio_value - final_own_contribution
    create_charts(portfolio_value, own_contribution, annual_profit, final_portfolio_value, final_own_contribution, final_profit, fire_month)

if __name__ == "__main__":
    main() 