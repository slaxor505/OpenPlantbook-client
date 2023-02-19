namespace PlantBook.Tests;

public class PlantBookTests
{
    [Test]
    public void GetDetailsAsync_ShouldGetToken_GetsPlant()
    {
        // Arrange
        using var httpTest = new HttpTest();
        httpTest
            .ForCallsTo("https://open.plantbook.io/api/v1/token/")
            .WithRequestBody("grant_type=client_credentials&client_id=id&client_secret=secret")
            .RespondWithJson(new { access_token = "abc", expires = DateTime.Now.AddMinutes(5).ToString("s") });

        httpTest
            .ForCallsTo("*testPlant/")
            .WithHeader("authorization", "Bearer abc")
            .RespondWithJson(new { alias = "testPlantAlias" });

        var sut = new PlantBook(new("id", "secret"));

        // Act
        var result = sut.GetDetailsAsync("testPlant").Result;

        // Asert            
        Assert.That(result.Alias, Is.EqualTo("testPlantAlias"));
    }

    [Test]
    public void GetDetailsAsync_ShouldGetToken_ButFails()
    {
        // Arrange
        using var httpTest = new HttpTest();
        httpTest
            .ForCallsTo("https://open.plantbook.io/api/v1/token/")
            .RespondWith("error!", 500);

        httpTest
            .ForCallsTo("*testPlant/")
            .RespondWithJson(new { alias = "testPlantAlias" });

        var sut = new PlantBook(new("", ""));

        // Act
        var result = sut.GetDetailsAsync("testPlant").Exception;

        // Asert            
        Assert.That(result!.InnerExceptions[0], Is.AssignableFrom(typeof(Flurl.Http.FlurlHttpException)));
    }

    [Test]
    public void GetDetailsAsync_ShouldReturnPlant()
    {
        // Arrange
        using var httpTest = new HttpTest();
        httpTest
            .ForCallsTo("*token/")
            .RespondWithJson(new { });

        httpTest
            .ForCallsTo("https://open.plantbook.io/api/v1/plant/detail/testPlant/")
            .RespondWithJson(new { alias = "testPlantAlias" });

        var sut = new PlantBook(new("", ""));

        // Act
        var result = sut.GetDetailsAsync("testPlant").Result;

        // Asert            
        Assert.That(result.Alias, Is.EqualTo("testPlantAlias"));
    }
}