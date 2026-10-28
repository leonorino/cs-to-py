public abstract class Report {
    public string Build() {
        var sb = new StringBuilder();
        sb.Append(Header());
        foreach (var row in Rows()) sb.Append(row);
        sb.Append(Footer());
        return sb.ToString();
    }

    protected abstract string Header();
    protected abstract IEnumerable<string> Rows();
    protected virtual string Footer() => "";
}

public sealed class SalesReport : Report {
    protected override string Header() => "sales\n";
    protected override IEnumerable<string> Rows() =>
        _rows.Select(r => $"{r.Date}: {r.Amount}\n");
}
