using Flurl;
using Flurl.Http;
using Flurl.Http.Configuration;
using Newtonsoft.Json.Serialization;

namespace PlantBook;

/// <inheritdoc />
public class PlantBook : IPlantBook
{
    private const string url = "https://open.plantbook.io/api/v1";

    private readonly OAuth2ClientCredentials credentials;
    private Token? token;

    static PlantBook()
    {
        FlurlHttp.Configure(settings =>
        {
            settings.JsonSerializer = new NewtonsoftJsonSerializer(new()
            {
                ContractResolver = new DefaultContractResolver { NamingStrategy = new SnakeCaseNamingStrategy() },
                NullValueHandling = Newtonsoft.Json.NullValueHandling.Ignore,
                ObjectCreationHandling = Newtonsoft.Json.ObjectCreationHandling.Replace,
            });
        });
    }

    public PlantBook(OAuth2ClientCredentials credentials)
    {
        this.credentials = credentials;
    }

    private async Task<Token> RefreshTokenIfNeededAsync()
    {
        if (token is null || token.IsExpired)
        {
            token = await GetTokenAsync();
        }
        return token;
    }

    private async Task<Token> GetTokenAsync()
    {
        return await url
            .AppendPathSegment("token/")
            .PostUrlEncodedAsync(new
            {
                grant_type = "client_credentials",
                client_id = credentials.ClientId,
                client_secret = credentials.Secret,
            })
            .ReceiveJson<Token>();
    }

    /// <inheritdoc />
    public async Task<SearchResult> SearchAsync(string alias, int? offset = null, int? limit = null, bool? userplant = null)
    {
        return await url
            .AppendPathSegments("plant", "search")
            .SetQueryParams(new { limit, offset, alias, userplant })
            .WithOAuthBearerToken((await RefreshTokenIfNeededAsync()).AccessToken)
            .GetAsync()
            .ReceiveJson<SearchResult>();
    }

    /// <inheritdoc />
    public async Task<Plant> GetDetailsAsync(string pid)
    {
        return await url
            .AppendPathSegments("plant", "detail", pid, "/")
            .WithOAuthBearerToken((await RefreshTokenIfNeededAsync()).AccessToken)
            .GetAsync()
            .ReceiveJson<Plant>();
    }

    /// <inheritdoc />
    public async Task<Plant> CreateAsync(Plant plant)
    {
        return await url
            .AppendPathSegments("plant", "create")
            .WithOAuthBearerToken((await RefreshTokenIfNeededAsync()).AccessToken)
            .PostJsonAsync(plant)
            .ReceiveJson<Plant>();
    }

    /// <inheritdoc />
    public async Task DeleteAsync(string pid)
    {
        await url
            .AppendPathSegments("plant", "delete")
            .WithOAuthBearerToken((await RefreshTokenIfNeededAsync()).AccessToken)
            .SendJsonAsync(HttpMethod.Delete, new { pid });
    }

    /// <inheritdoc />
    public async Task<Plant> UpdateAsync(Plant plant)
    {
        return await url
            .AppendPathSegments("plant", "update")
            .WithOAuthBearerToken((await RefreshTokenIfNeededAsync()).AccessToken)
            .PatchJsonAsync(plant)
            .ReceiveJson<Plant>();
    }
}
