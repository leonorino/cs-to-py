public class ImportException : Exception {
    public ImportException(string message, Exception inner) : base(message, inner) { }
}

public void Import(string path) {
    try {
        var lines = File.ReadAllLines(path);
        Parse(lines);
    }
    catch (IOException ex) when (ex.HResult == -2147024864) {
        Retry(path);                       // файл занят — пробуем ещё раз
    }
    catch (IOException ex) {
        throw new ImportException($"cannot read {path}", ex);
    }
}
