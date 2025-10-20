namespace auth;

public class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);

        builder.Services.AddAuthorization();
        builder.Services.AddEndpointsApiExplorer();
        builder.Services.AddSwaggerGen();
        builder.Services.AddHealthChecks();
        
        var port = Environment.GetEnvironmentVariable("PORT");

        var app = builder.Build();

        if (app.Environment.IsDevelopment())
        {
            app.UseSwagger();
            app.UseSwaggerUI();
        }

        app.UseAuthorization();

        // Тести / маршрути
        app.MapGet("/auth", () => "Hello, world!");
        app.MapGet("/auth/hello", () => "Hello from /hello!");
        app.MapHealthChecks("/auth/health");

        app.Run($"http://0.0.0.0:{port}");
    }
}
