public sealed class ReportWriter : IDisposable {
    private readonly StreamWriter _writer;

    public ReportWriter(string path) {
        _writer = new StreamWriter(path);
    }

    public void Write(string line) => _writer.WriteLine(line);

    public void Dispose() => _writer.Dispose();
}

// использование
using (var w = new ReportWriter("report.txt")) {
    w.Write("header");
    w.Write("body");
}