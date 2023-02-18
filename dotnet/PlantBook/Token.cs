namespace PlantBook;

public record Token(string AccessToken, string TokenType, DateTime Expires)
{
    public bool IsExpired => Expires - DateTime.UtcNow <= TimeSpan.FromMinutes(1);
}
