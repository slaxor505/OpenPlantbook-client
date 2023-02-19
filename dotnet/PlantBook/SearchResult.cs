using System.Web;

namespace PlantBook;

public record SearchResult(int Count, string? Next, string? Previous, List<Plant> Results)
{
    public int? Offset
    {
        get
        {
            var offset = Next is null ? null : HttpUtility.ParseQueryString(new Uri(Next).Query).Get("offset");
            return offset is not null ? int.Parse(offset) : null;
        }
    }
}
