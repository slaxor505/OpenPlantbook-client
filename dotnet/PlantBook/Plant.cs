namespace PlantBook;

public record Plant(
    string Pid,
    string? DisplayPid,
    string? Alias,
    string? Category,
    int? MaxLightMmol,
    int? MinLightMmol,
    int? MaxLightLux,
    int? MinLightLux,
    int? MaxTemp,
    int? MinTemp,
    int? MaxEnvHumid,
    int? MinEnvHumid,
    int? MaxSoilMoist,
    int? MinSoilMoist,
    int? MaxSoilEc,
    int? MinSoilEc,
    string? ImageUrl,
    bool? UserPlant
);
