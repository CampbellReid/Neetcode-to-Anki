using System.Net;
using System.Net.Http.Headers;
using Microsoft.Playwright;
using System.Text.Json;

var allProblemsJson = await File.ReadAllTextAsync("all_problems.json");
using var doc = JsonDocument.Parse(allProblemsJson);
var root = doc.RootElement;

var problems = new List<Problem>();

var i = 0;

foreach (var element in root.EnumerateArray())
{
    var neetCode150Exists = element.TryGetProperty("neetcode150", out var neetCode150);
    if(!neetCode150Exists)
    {
        continue;
    }

    var problem = element.GetProperty("problem").GetString();
    var link = element.GetProperty("link").GetString();
    // ReSharper disable once StringLiteralTypo
    var ncLink = element.GetProperty("ncLink").GetString();
    var id = ncLink?.TrimEnd('/');
    var difficulty = element.GetProperty("difficulty").GetString();
    var video = element.GetProperty("video").GetString();
    var pattern = element.GetProperty("pattern").GetString();

    var clientHandler = new HttpClientHandler
    {
        AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate,
    };
    var client = new HttpClient(clientHandler);
    var request = new HttpRequestMessage
    {
        Method = HttpMethod.Post,
        RequestUri = new Uri("https://us-central1-neetcode-dd170.cloudfunctions.net/getProblemMetadataFunction"),
        Headers =
        {
            { "host", "us-central1-neetcode-dd170.cloudfunctions.net" },
            { "connection", "keep-alive" },
            { "sec-ch-ua", "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"" },
            { "sec-ch-ua-mobile", "?0" },
            { "user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0" },
            { "sec-ch-ua-platform", "\"Windows\"" },
            { "accept", "*/*" },
            { "origin", "https://neetcode.io" },
            { "sec-fetch-site", "cross-site" },
            { "sec-fetch-mode", "cors" },
            { "sec-fetch-dest", "empty" },
            { "referer", "https://neetcode.io/" },
            { "accept-language", "en-US,en;q=0.9" },
        },
        Content = new StringContent("{\"data\":{\"problemId\":\"" + id + "\"}}")
        {
            Headers =
            {
                ContentType = new MediaTypeHeaderValue("application/json")
            }
        }
    };
    using (var response = await client.SendAsync(request))
    {
        response.EnsureSuccessStatusCode();
        var body = await response.Content.ReadAsStringAsync();
        using var metadataDoc = JsonDocument.Parse(body);
        var metadataRoot = metadataDoc.RootElement;
        var resultElement = metadataRoot.GetProperty("result");
        var description = resultElement.GetProperty("description").GetString();
        var pythonSolution = resultElement.GetProperty("solutions").GetProperty("python").GetString();

        problems.Add(new Problem(problem, ncLink, pattern, description, difficulty, video, pythonSolution));
    }

    Console.WriteLine(++i + " " + problem);

    // Pause for a second to avoid rate limiting
    await Task.Delay(1000);
}

var problemsJson = JsonSerializer.Serialize(problems, new JsonSerializerOptions { WriteIndented = true });
await File.WriteAllTextAsync("problems.json", problemsJson);

// ReSharper disable once StringLiteralTypo
//Console.WriteLine("Getting the NeetCode 150 Problems");
//var problemsAlreadyRetrieved = new HashSet<string>();

//using var playwright = await Playwright.CreateAsync();
//await using var browser = await playwright.Chromium.LaunchAsync(new BrowserTypeLaunchOptions
//{
//    Headless = false,
//});
//var page = await browser.NewPageAsync();
//await page.GotoAsync("https://neetcode.io/problems/duplicate-integer");

Console.ReadLine();

internal class Problem(
    string name,
    string ncLink,
    string pattern,
    string description,
    string difficulty,
    string video,
    string pythonSolution)
{
    public string Name { get; init; } = name;

    public string NcLink { get; init; } = ncLink;

    public string Pattern { get; init; } = pattern;

    public string Description { get; init; } = description;

    public string Difficulty { get; init; } = difficulty;

    public string Video { get; init; } = video;

    public string PythonSolution { get; init; } = pythonSolution;
}