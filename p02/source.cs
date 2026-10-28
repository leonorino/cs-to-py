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