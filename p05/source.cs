public readonly struct Money : IEquatable<Money> {
    public decimal Amount { get; }
    public string Currency { get; }

    public Money(decimal amount, string currency) {
        Amount = amount;
        Currency = currency ?? throw new ArgumentNullException(nameof(currency));
    }

    public static Money operator +(Money a, Money b) {
        if (a.Currency != b.Currency)
            throw new InvalidOperationException("currency mismatch");
        return new Money(a.Amount + b.Amount, a.Currency);
    }

    public bool Equals(Money other) =>
        Amount == other.Amount && Currency == other.Currency;
    public override bool Equals(object? o) => o is Money m && Equals(m);
    public override int GetHashCode() => HashCode.Combine(Amount, Currency);
}
