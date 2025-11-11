using Application;
using Application.Interfaces;
using Application.Services;
using Domain.Entities;
using Infrastructure.Repositories;
using Infrastructure.Data;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.CookiePolicy;
using Microsoft.EntityFrameworkCore;

namespace auth;

public class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);

        builder.Services.AddDbContext<DataContext>(options =>
            options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

        builder.Services.Configure<JwtOptions>(
            builder.Configuration.GetSection("JwtOptions"));

        builder.Services.AddAuthorization();
        builder.Services.AddEndpointsApiExplorer();
        builder.Services.AddSwaggerGen();
        builder.Services.AddHealthChecks();

        builder.Services.AddScoped<IAuthService, AuthService>();
        builder.Services.AddScoped<IAuthRepository, AuthRepository>();
        
        builder.Services.AddScoped<IJwtProvider, JwtProvider>();
        builder.Services.AddScoped<IPasswordHasher, PasswordHasher>();
        builder.Services.AddScoped<JwtOptions>();

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
        app.MapGet("/auth", () => "Hello, world!");
        app.MapGet("/auth/hello", () => "Hello from /hello!");
        app.MapHealthChecks("/auth/health");

        app.Run($"http://0.0.0.0:{port}");
    }
}
