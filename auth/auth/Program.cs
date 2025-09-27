namespace auth;

public class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);

        builder.Services.AddAuthorization();
        builder.Services.AddEndpointsApiExplorer();
        builder.Services.AddSwaggerGen();
        
        var port = Environment.GetEnvironmentVariable("PORT") ?? "5010";

        var app = builder.Build();

        if (app.Environment.IsDevelopment())
        {
            app.UseSwagger();
            app.UseSwaggerUI();
        }

        app.UseAuthorization();

        // Тести / маршрути
        app.MapGet("/", () => "Hello, world!");
        app.MapGet("/hello", () => "Hello from /hello!");
        

        app.Run($"http://0.0.0.0:{port}");
    }
}