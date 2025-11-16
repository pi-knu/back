using Application;
using Application.Interfaces;
using Application.Services;
using Domain.Entities;
using Infrastructure.Repositories;
using Infrastructure.Data;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.CookiePolicy;
using Microsoft.EntityFrameworkCore;
using DotNetEnv;

namespace auth;

public class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);
        
        Env.Load();

        var dbHost = Environment.GetEnvironmentVariable("POSTGRES_HOST") ?? "postgres";
        var dbPort = Environment.GetEnvironmentVariable("POSTGRES_PORT") ?? "5432";
        var dbName = Environment.GetEnvironmentVariable("POSTGRES_DB") ?? "main";
        var dbUser = Environment.GetEnvironmentVariable("POSTGRES_USER") ?? "postgres";
        var dbPassword = Environment.GetEnvironmentVariable("POSTGRES_PASSWORD") ?? "postgres";

        var connectionString = $"Host={dbHost};Port={dbPort};Database={dbName};Username={dbUser};Password={dbPassword}";
        
        builder.Services.Configure<JwtOptions>(options =>
        {
            options.SecretKey = Environment.GetEnvironmentVariable("JWT_SECRET_KEY") ?? "";
            options.ExpiresHours = int.Parse(Environment.GetEnvironmentVariable("JWT_EXPIRES_HOURS") ?? "12");
            options.Issuer = Environment.GetEnvironmentVariable("JWT_ISSUER") ?? "http://localhost/docs/auth/";
        });

        builder.Configuration.AddEnvironmentVariables();

        builder.Services.AddDbContext<DataContext>(options =>
            options.UseNpgsql(connectionString));

        builder.Services.AddAuthorization();
        builder.Services.AddEndpointsApiExplorer();
        builder.Services.AddSwaggerGen();
        builder.Services.AddHealthChecks();

        builder.Services.AddScoped<IAuthService, AuthService>();
        builder.Services.AddScoped<IAuthRepository, AuthRepository>();
        
        builder.Services.AddScoped<IJwtProvider, JwtProvider>();
        builder.Services.AddScoped<IPasswordHasher, PasswordHasher>();

        builder.Services.AddControllers();
        
        var port = Environment.GetEnvironmentVariable("PORT");

        var app = builder.Build();

        if (app.Environment.IsDevelopment())
        {
            app.UseSwagger();
            app.UseSwaggerUI();
        }
        
        app.UseRouting(); 
        app.UseCookiePolicy(new CookiePolicyOptions
        {
            MinimumSameSitePolicy = SameSiteMode.Strict,
            HttpOnly = HttpOnlyPolicy.Always,
            Secure = CookieSecurePolicy.Always
        });

        app.UseAuthorization();
        app.MapControllers();

        // Тести / маршрути
        app.MapHealthChecks("/auth/health");

        app.Run($"http://0.0.0.0:{port}");
    }
}
