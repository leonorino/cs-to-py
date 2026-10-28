# Перевод C# → Python

Шесть заданий. В каждом: исходник на C#, задание, что сдавать и на что смотрим.

**Общее правило для всех шести.** Перевод идёт через замысел, а не построчно.
Сначала выписать четыре пункта — граница, контракт, инвариант, ошибка — и только
потом писать код. Оценка в первую очередь за эти четыре пункта, а не за
синтаксис.

---

## П-01. Счёт с инвариантом

**Тема:** U1, U3 · **Уровень:** 4 · **Время:** 15 мин

**Дано.**

```csharp
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
```

**Задание.**

1. Выписать замысел: граница класса, его контракт, инвариант, что считается
   ошибкой.
2. Перевести на Python.
3. Сделать так, чтобы снаружи нельзя было получить отрицательный баланс
   случайно: `acc._balance = -100` не должно быть первым, что приходит в голову
   читателю.
4. В записке (3–5 строк) назвать: что теперь держит инвариант и чем это
   отличается от исходника.

**Сдать:** `p01.py`, `p01.md`.

**Смотрим:** инвариант проверяется в одном месте; ошибки — те же по смыслу;
в записке честно сказано, что защита теперь договорная, а не принудительная.

---

## П-02. Репозиторий и фабрика

**Тема:** U2, U6 · **Уровень:** 4 · **Время:** 20 мин

**Дано.**

```csharp
public interface IRoleRepository {
    bool IsAssigned(Role role, User user);
    void Assign(Role role, User user);
    void Unassign(Role role, User user);
}

public sealed class InMemoryRoleRepository : IRoleRepository {
    private readonly List<(Guid RoleId, Guid UserId)> _links = new();
    public bool IsAssigned(Role role, User user) =>
        _links.Contains((role.Id, user.Id));
    public void Assign(Role role, User user) => _links.Add((role.Id, user.Id));
    public void Unassign(Role role, User user) =>
        _links.Remove((role.Id, user.Id));
}

public sealed class SqlRoleRepository : IRoleRepository {
    private readonly string _connectionString;
    public SqlRoleRepository(string connectionString) => _connectionString = connectionString;
    public bool IsAssigned(Role role, User user) => /* запрос к БД */ false;
    public void Assign(Role role, User user) { /* INSERT */ }
    public void Unassign(Role role, User user) { /* DELETE */ }
}

public static class RoleRepositoryFactory {
    public static IRoleRepository Create(string kind, string connectionString) => kind switch {
        "memory" => new InMemoryRoleRepository(),
        "sql"    => new SqlRoleRepository(connectionString),
        _ => throw new ArgumentException($"unknown repository: {kind}")
    };
}
```

**Задание.**

1. Перевести на Python: интерфейс, две реализации, фабрику.
2. Добавить третью реализацию — например, `FileRoleRepository`, которая хранит
   связи в JSON-файле. Убедиться, что вызывающий код править не пришлось.
3. В записке ответить: что в Python играет роль интерфейса и что играет роль
   фабрики. Если роль играет одна и та же конструкция — сказать какая.

**Сдать:** `p02/` с модулями и `p02.md`.

**Смотрим:** реализации действительно взаимозаменяемы; фабрика не требует
правки при добавлении третьей; в записке назван механизм, а не «ну, тут всё
динамическое».

---

## П-03. Ресурс, который надо закрыть

**Тема:** U11 · **Уровень:** 4 · **Время:** 15 мин

**Дано.**

```csharp
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
```

**Задание.**

1. Перевести на Python так, чтобы объект можно было использовать в `with`.
2. Сделать вариант, где ошибка внутри блока не мешает записи закрыть файл, но
   сама ошибка не проглатывается.
3. В записке: что произойдёт, если у объекта не будет нужных методов, и когда
   это выяснится.

**Сдать:** `p03.py`, `p03.md`.

**Смотрим:** `__enter__`/`__exit__` на месте; возвращаемое значение `__exit__`
осмысленно; ошибка не теряется.

---

## П-04. Ошибка с причиной

**Тема:** U10 · **Уровень:** 4 · **Время:** 15 мин

**Дано.**

```csharp
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
```

**Задание.**

1. Перевести на Python: своё исключение, различение двух видов `IOException`,
   сохранение причины.
2. Добиться, чтобы при повторном броске в трассировке была видна исходная
   ошибка, а не только новая.
3. В записке: чем «поймать и бросить новое» отличается от «поймать и бросить то
   же» и когда нужно каждое.

**Сдать:** `p04.py`, `p04.md`.

**Смотрим:** `raise ... from ...`; фильтр по причине реализован осмысленно;
исходная ошибка не теряется.

---

## П-05. Money

**Тема:** U7, U8 · **Уровень:** 5 · **Время:** 20 мин

**Дано.**

```csharp
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
```

**Задание.**

1. Перевести на Python.
2. Проверить тремя экспериментами: сложение одинаковых валют, сложение разных,
   использование как ключа словаря.
3. Ответить: что будет, если определить `__eq__` и забыть `__hash__`? Проверить
   на практике, а не по памяти.
4. В записке: какие методы образуют один контракт и почему их нельзя
   определять по отдельности.

**Сдать:** `p05.py`, `p05.md` с выводом экспериментов.

**Смотрим:** `__eq__` и `__hash__` согласованы; `__repr__` есть; словарь
работает; объяснение про контракт, а не про «так принято».

---

## П-06. Шаблонный метод

**Тема:** U5 · **Уровень:** 5 · **Время:** 20 мин

**Дано.**

```csharp
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
```

**Задание.**

1. Перевести на Python двумя способами: через базовый класс и через передачу
   частей как аргументов (функции или объекты).
2. Для каждого способа назвать, что будет, если завтра понадобится третий
   вариант отчёта с другим порядком блоков.
3. В записке — вывод: какой способ вы бы выбрали и почему.

**Сдать:** `p06_a.py`, `p06_b.py`, `p06.md`.

**Смотрим:** оба варианта работают; сравнение по цене изменения, а не по вкусу;
наследование применено там, где оно оправдано.
