public sealed class Account {
    private decimal _balance;

    public Account(decimal initial) {
        if (initial < 0) throw new ArgumentOutOfRangeException(nameof(initial));
        _balance = initial;
    }

    public decimal Balance => _balance;

    public void Deposit(decimal amount) {
        if (amount <= 0) throw new ArgumentException("amount must be positive");
        _balance += amount;
    }

    public void Withdraw(decimal amount) {
        if (amount <= 0) throw new ArgumentException("amount must be positive");
        if (amount > _balance) throw new InvalidOperationException("insufficient funds");
        _balance -= amount;
    }
}